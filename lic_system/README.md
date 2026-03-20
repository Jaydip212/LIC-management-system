# 🛡️ LIC Management System

A **premium, production-ready** Life Insurance Corporation management platform built with **Flask (Python)**, **MySQL**, and **Vanilla HTML/CSS/JS**.

---

## 🚀 Features

### Public Website

- Beautiful landing page with hero section, floating cards & animations
- Insurance plans / services catalog with filtering
- About Us, Testimonials, FAQ, Contact form
- Fully responsive (mobile, tablet, desktop)

### Admin Panel

- Secure login with bcrypt password hashing
- **Dashboard** — KPIs, charts (Chart.js), recent activity
- **Customer Management** — Add / Edit / View / Delete with pagination & search
- **Policy Management** — CRUD for all insurance plan types
- **Payment Management** — Track paid / pending / overdue premiums
- **Agent Management** — Agent profiles, commission tracking
- **Claim Management** — Full claims lifecycle with status tracking
- **Messages** — View and manage contact form submissions
- **Reports & Analytics** — Monthly collection chart, policy distribution, top agents

---

## 📁 Project Structure

```
lic_system/
├── app.py                  # Main Flask application
├── config.py               # Configuration (DB, secret keys)
├── requirements.txt        # Python dependencies
├── schema.sql              # MySQL database schema + sample data
├── .env.example            # Environment variables template
├── routes/
│   ├── auth.py             # Login / logout
│   ├── dashboard.py        # Admin dashboard
│   ├── customers.py        # Customer CRUD
│   ├── policies.py         # Policy CRUD
│   ├── payments.py         # Payment CRUD
│   ├── agents.py           # Agent CRUD
│   ├── claims.py           # Claims CRUD
│   ├── messages.py         # Contact messages
│   ├── reports.py          # Analytics
│   └── public.py           # Public website routes
├── templates/
│   ├── public/             # Public website HTML templates
│   └── admin/              # Admin panel HTML templates
└── static/
    ├── css/
    │   ├── main.css         # Public website styles
    │   └── admin.css        # Admin dashboard styles
    └── js/
        ├── main.js          # Public website JS
        └── admin.js         # Admin panel JS
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.10+
- MySQL Server 8.0+
- pip

### 2. Clone / Navigate to the project

```powershell
cd "f:\project 2026\LIC management system\lic_system"
```

### 3. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

> **Windows note:** If `mysqlclient` fails to install, try:
>
> ```powershell
> pip install mysqlclient --global-option=build_ext --global-option="-IC:\path\to\mysql\include"
> ```
>
> Or use `PyMySQL` instead — see alternate config below.

### 5. Set up the database

Open MySQL and run:

```sql
source schema.sql;
```

Or from the command line:

```powershell
mysql -u root -p < schema.sql
```

### 6. Configure environment

Copy `.env.example` to `.env` and fill in your credentials:

```powershell
copy .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-very-secret-key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=lic_management
```

### 7. Run the application

```powershell
python app.py
```

Open your browser at **<http://localhost:5000>**

---

## 🔑 Default Admin Credentials

| Field    | Value              |
|----------|--------------------|
| Username | `admin`            |
| Password | `admin@123`        |
| URL      | `/admin/login`     |

> **Change this immediately in production!**  
> Go to `schema.sql` and update the bcrypt hash to your own password.

---

## 📊 Database Tables

| Table              | Description                        |
|--------------------|------------------------------------|
| `admins`           | Admin accounts with hashed passwords |
| `policies`         | Insurance plan catalog             |
| `agents`           | Agent profiles                     |
| `customers`        | Customer records linked to policies & agents |
| `premium_payments` | Payment tracking (paid/pending/overdue) |
| `claims`           | Insurance claim records            |
| `contact_messages` | Website contact form submissions   |

> **Marathi Guide Available:** For step-by-step instructions in Marathi on how to view and edit these tables using MySQL Workbench, please see [DATABASE_GUIDE_MARATHI.md](DATABASE_GUIDE_MARATHI.md).

---

## 🛠️ Tech Stack

| Layer       | Technology                              |
|-------------|------------------------------------------|
| Backend     | Python 3, Flask 3.0                     |
| Database    | MySQL 8.0 via Flask-MySQLdb             |
| Auth        | bcrypt + Flask sessions                 |
| Frontend    | HTML5, CSS3 (custom design system), Vanilla JS |
| Charts      | Chart.js 4.4                            |
| Icons       | Font Awesome 6.5                        |
| Fonts       | Google Fonts (Inter)                    |

---

## 🔒 Security Notes

- Passwords hashed with **bcrypt**
- Session-based authentication with configurable lifetime
- Admin routes protected by `@login_required` decorator
- File uploads restricted by type and stored safely
- Flash messages for user feedback

---

## 📜 License

This project is for educational / demonstration purposes.
