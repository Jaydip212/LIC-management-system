import os
import glob

routes_dir = r"f:\project 2026\LIC management system\lic_system\routes"
for file_path in glob.glob(os.path.join(routes_dir, "*.py")):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = content.replace("from app import mysql, login_required", "from extensions import mysql, login_required")
    new_content = new_content.replace("from app import mysql", "from extensions import mysql")
    
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")
print("Done.")
