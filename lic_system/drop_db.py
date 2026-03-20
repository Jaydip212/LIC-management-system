import pymysql
import os

host = os.environ.get('MYSQL_HOST', 'localhost')
user = os.environ.get('MYSQL_USER', 'root')
password = os.environ.get('MYSQL_PASSWORD', 'Jaydip@123')

conn = pymysql.connect(host=host, user=user, password=password)
cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS lic_management;")
conn.commit()
cur.close()
conn.close()
print("Dropped successfully.")
