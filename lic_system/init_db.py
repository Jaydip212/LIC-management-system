import pymysql
import os

# Database configuration
host = os.environ.get('MYSQL_HOST', 'localhost')
user = os.environ.get('MYSQL_USER', 'root')
password = os.environ.get('MYSQL_PASSWORD', 'Jaydip@123')

print(f"Connecting to MySQL at {host} as {user}...")
try:
    # Connect without database first
    conn = pymysql.connect(host=host, user=user, password=password)
    cur = conn.cursor()
    
    # Read schema.sql
    with open('schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Split by statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    print("Executing schema.sql statements...")
    for statement in statements:
        if statement:
            try:
                cur.execute(statement)
            except Exception as e:
                print(f"Warning on execution: {e}")
                
    conn.commit()
    print("Database initialized successfully!")
    
except Exception as e:
    print(f"Error connecting or executing: {e}")
finally:
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
