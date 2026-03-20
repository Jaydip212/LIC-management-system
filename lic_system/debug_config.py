import os
import sys
from flask import Flask

# Add project dir to sys.path
sys.path.append(r"f:\project 2026\LIC management system\lic_system")

try:
    from config import config
    app = Flask(__name__)
    
    # Check both production and default configs
    print("--- DEFAULT CONFIG ---")
    app.config.from_object(config['default'])
    for key in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_DB', 'MYSQL_PORT']:
        print(f"{key}: {app.config.get(key)}")
        
    print("\n--- PRODUCTION CONFIG ---")
    app.config.from_object(config['production'])
    for key in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_DB', 'MYSQL_PORT']:
        print(f"{key}: {app.config.get(key)}")
        
    print("\n--- ENVIRONMENT VARIABLES (OS) ---")
    for key in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_DB', 'MYSQL_PORT']:
        print(f"{key}: {os.environ.get(key)}")

except Exception as e:
    print(f"Error: {e}")
