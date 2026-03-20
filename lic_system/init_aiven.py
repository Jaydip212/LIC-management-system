import pymysql
import os
import ssl

# Database configuration - Setup these environment variables locally before running
# or replace with your Aiven details
host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
db_name = os.environ.get('MYSQL_DB', 'defaultdb') # Aiven's default is usually defaultdb
port = int(os.environ.get('MYSQL_PORT', 3306))
ca_path = 'ca.pem' # Ensure ca.pem is in the same folder

print(f"Connecting to Aiven MySQL at {host}...")

try:
    if not os.path.exists(ca_path):
        print(f"Error: {ca_path} not found! Please make sure you saved the CA certificate to this file.")
        exit(1)

    # Connect with SSL
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db_name,
        port=port,
        ssl={'ca': ca_path}
    )
    cur = conn.cursor()
    
    # Read schema.sql
    schema_path = 'schema.sql'
    if not os.path.exists(schema_path):
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    with open(schema_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Remove 'CREATE DATABASE' and 'USE' lines for Aiven
    # Aiven usually doesn't allow creating databases via script
    lines = sql.split('\n')
    filtered_lines: list[str] = []
    for line in lines:
        if line.strip().upper().startswith('CREATE DATABASE') or line.strip().upper().startswith('USE '):
            continue
        filtered_lines.append(line)
    
    sql = '\n'.join(filtered_lines)
    
    # Split by statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    print(f"Executing {len(statements)} statements on database '{db_name}'...")
    for statement in statements:
        if statement:
            try:
                cur.execute(statement)
            except Exception as e:
                print(f"Warning/Error: {e}")
                
    conn.commit()
    print("\nDatabase tables created and sample data inserted successfully on Aiven!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
