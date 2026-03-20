import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def add_sample_data():
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    db = os.getenv('MYSQL_DB')
    port = int(os.getenv('MYSQL_PORT', 16407))
    ca_path = os.path.abspath('ca.pem')

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port,
        ssl={'ca': ca_path},
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Check if policies already exist to avoid duplicates
            cursor.execute("SELECT COUNT(*) as count FROM policies")
            result = cursor.fetchone()
            if result['count'] > 0:
                print(f"Database already has {result['count']} policies. Skipping insertion.")
                return

            samples = [
                ("Jeevan Anand", "endowment", "A combination of protection and savings. Provides financial support for the family of the deceased policyholder.", 1000000, 35000, 20),
                ("Term Assurance Plan", "term", "Pure life cover at lowest cost. High financial protection for your family in case of unfortunate events.", 5000000, 12000, 30),
                ("Children's Career Plan", "child", "Secure your child's education and future expenses with guaranteed returns and bonuses.", 1500000, 45000, 15),
                ("Health Plus Plan", "health", "Comprehensive health coverage for the entire family including hospital cash and major surgical benefits.", 500000, 8500, 1),
                ("New Pension Plus", "pension", "Plan your retirement with regular income and market-linked returns. Secure your golden years.", 2000000, 100000, 25),
                ("Bima Jyoti", "ulip", "A non-linked, individual, saving life insurance plan which offers a combination of protection and savings.", 800000, 28000, 15)
            ]

            sql = """INSERT INTO policies (policy_name, policy_type, description, coverage_amount, premium_amount, duration_years, status)
                     VALUES (%s, %s, %s, %s, %s, %s, 'active')"""
            
            cursor.executemany(sql, samples)
            connection.commit()
            print(f"Successfully added {len(samples)} sample policies.")

    finally:
        connection.close()

if __name__ == "__main__":
    add_sample_data()
