# 🏠 LIC Management System - Localhost वर Run करण्याचा Guide
### (College Handover - Easy Setup)

> **हा guide वाचा, एक-एक step follow करा, project run होईल!**

---

## 📦 आधी हे Install करावे लागेल

| Software | Download Link | Size |
|---|---|---|
| **Python 3.11** | [python.org/downloads](https://www.python.org/downloads/) | ~25 MB |
| **XAMPP** | [apachefriends.org](https://www.apachefriends.org/download.html) | ~150 MB |

> ⚠️ **Python install करताना** - "Add Python to PATH" ✅ टिक करायला विसरू नका!

---

## ✅ STEP 1: XAMPP Install आणि MySQL Start करा

1. **XAMPP install करा** (default settings ठेवा)
2. **XAMPP Control Panel उघडा**
3. **MySQL** च्या समोर **"Start"** बटण दाबा → Status **"Running"** दिसेल
4. **Apache** पण Start करा (optional, पण करा)

   ```
   XAMPP Control Panel:
   Apache  → [Start]  ✅
   MySQL   → [Start]  ✅
   ```

---

## ✅ STEP 2: Database बनवा

### 2a. phpMyAdmin उघडा
1. Browser मध्ये जा → `http://localhost/phpmyadmin`
2. Username: `root`, Password: रिकामे (blank) → **"Go"** दाबा

### 2b. नवीन Database बनवा
1. डाव्या बाजूला **"New"** दाबा
2. Database name: **`lic_management`** टाका
3. Collation: **`utf8mb4_unicode_ci`** निवडा
4. **"Create"** दाबा

### 2c. Schema Import करा
1. डाव्या बाजूला `lic_management` database वर click करा
2. वरच्या menu मधून **"Import"** tab वर जा
3. **"Choose File"** दाबा
4. हा file निवडा:
   ```
   LIC management system\lic_system\schema.sql
   ```
5. **"Go"** दाबा → "Import has been successfully finished" message येईल ✅

> 🎉 Database तयार! Tables + Sample Data सर्व import झाले.

---

## ✅ STEP 3: `.env` File Update करा

`lic_system` folder मध्ये `.env` file उघडा (Notepad ने) आणि **सर्व content delete करून** हे paste करा:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=lic_management
MYSQL_PORT=3306
SECRET_KEY=lic-ms-local-secret-key-2026
FLASK_DEBUG=True
```

> ⚠️ **MYSQL_PASSWORD** - जर तुम्ही XAMPP install केले असेल तर password रिकामे सोडा. जर tuमचा MySQL password set केला असेल तर तो टाका.

**File Save करा** (Ctrl+S)

---

## ✅ STEP 4: Python Virtual Environment बनवा

**Command Prompt (CMD) उघडा** - Start Menu → "cmd" search करा → Enter

```bash
cd "f:\project 2026\LIC management system\lic_system"
```

> 📌 **Note:** जर project दुसऱ्या drive/folder मध्ये असेल तर त्याप्रमाणे path change करा.
> उदा: `cd "C:\Users\Student\Desktop\LIC management system\lic_system"`

**Virtual Environment बनवा:**
```bash
python -m venv venv
```

**Virtual Environment Activate करा:**
```bash
venv\Scripts\activate
```

> ✅ CMD मध्ये `(venv)` दिसेल - म्हणजे activate झाला!

---

## ✅ STEP 5: Required Packages Install करा

```bash
pip install Flask==3.0.0 PyMySQL==1.1.0 bcrypt==4.1.2 python-dotenv==1.0.0 Werkzeug==3.0.1
```

> ⏳ 2-3 मिनिटे लागतील, packages download होतील...
> "Successfully installed" message आल्यावर पुढे जा.

---

## ✅ STEP 6: Application Run करा

```bash
python app.py
```

**असे दिसेल:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

> 🎉 **Project चालू झाला!**

---

## ✅ STEP 7: Browser मध्ये उघडा

Browser उघडा आणि हे URL टाका:

| Page | URL |
|---|---|
| **🏠 Main Website** | `http://localhost:5000` |
| **🔐 Admin Login** | `http://localhost:5000/admin/login` |

### Admin Login Details:
```
Username: admin
Password: Admin@123
```

---

## 🛑 Project बंद करण्यासाठी

CMD मध्ये **`Ctrl + C`** दाबा → Project बंद होईल.

---

## 🔄 पुढच्या वेळी Run करण्यासाठी (Short Steps)

दर वेळी हे करा:

1. **XAMPP → MySQL Start करा**
2. **CMD उघडा:**
   ```bash
   cd "f:\project 2026\LIC management system\lic_system"
   venv\Scripts\activate
   python app.py
   ```
3. Browser मध्ये `http://localhost:5000` उघडा ✅

---

## ❌ Common Errors आणि Solutions

### Error: `No module named 'flask'`
```bash
venv\Scripts\activate
pip install Flask==3.0.0
```

### Error: `Access denied for user 'root'@'localhost'`
→ `.env` file मधील `MYSQL_PASSWORD` check करा. XAMPP मध्ये default password रिकामे असते.

### Error: `Unknown database 'lic_management'`
→ phpMyAdmin मध्ये जा, `lic_management` database बनवला का ते बघा (Step 2 परत करा).

### Error: `ModuleNotFoundError: No module named 'pymysql'`
```bash
pip install PyMySQL==1.1.0
```

### Error: Port already in use
→ CMD मध्ये: `python app.py` ऐवजी `python app.py --port 5001` आणि browser मध्ये `http://localhost:5001`

### `venv\Scripts\activate` काम करत नाही?
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
(हे PowerShell मध्ये run करा, नंतर CMD मध्ये activate करा)

---

## 📁 Project Structure समजून घ्या

```
LIC management system/
└── lic_system/
    ├── app.py          ← Main application (हेच run करायचे)
    ├── config.py       ← Database settings
    ├── .env            ← Passwords/Secrets (आपण edit केला)
    ├── schema.sql      ← Database tables + sample data
    ├── requirements.txt← Required packages list
    ├── routes/         ← सर्व pages चे code
    ├── templates/      ← HTML pages
    └── static/         ← CSS, JS, Images
```

---

## 🔑 Sample Data (आधीच Import झाले आहे)

### Admin:
| Username | Password |
|---|---|
| `admin` | `Admin@123` |

### Customers: Aakash Wani, Pradnya Patil, Rohan Kadam (आणि इतर)
### Agents: Jaydip Jadhav, Sanika Chavan, Rajveer Shinde, Mayur Tawade
### Policies: 8 LIC policies (Jeevan Anand, Tech Term, etc.)
### Payments: 8 sample payments
### Claims: 4 sample claims

---

> 💡 **कुठलीही अडचण आली तर** error message screenshot घ्या आणि professor/मित्राला दाखवा!

> 🎓 **All the best! Project successfully run करा!** 🚀
