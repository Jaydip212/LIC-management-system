-- ============================================================
-- LIC Management System - MySQL Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS lic_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lic_management;

-- ------------------------------------------------------------
-- Table: admins
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(100) NOT NULL UNIQUE,
    email       VARCHAR(150) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,  -- bcrypt hashed
    full_name   VARCHAR(200) NOT NULL,
    role        ENUM('super_admin','admin') DEFAULT 'admin',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login  DATETIME NULL
);

-- ------------------------------------------------------------
-- Table: agents
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agents (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    agent_code      VARCHAR(50) NOT NULL UNIQUE,
    full_name       VARCHAR(200) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    mobile          VARCHAR(20) NOT NULL,
    address         TEXT,
    city            VARCHAR(100),
    state           VARCHAR(100),
    license_number  VARCHAR(100),
    commission_rate DECIMAL(5,2) DEFAULT 5.00,
    status          ENUM('active','inactive') DEFAULT 'active',
    joined_date     DATE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: policies
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS policies (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    policy_code     VARCHAR(50) NOT NULL UNIQUE,
    policy_name     VARCHAR(200) NOT NULL,
    policy_type     ENUM('life','health','term','endowment','ulip','pension','child','vehicle') NOT NULL,
    coverage_amount DECIMAL(15,2) NOT NULL,
    premium_amount  DECIMAL(10,2) NOT NULL,
    duration_years  INT NOT NULL,
    benefits        TEXT,
    description     TEXT,
    status          ENUM('active','inactive') DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table: customers
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    customer_code   VARCHAR(50) NOT NULL UNIQUE,
    full_name       VARCHAR(200) NOT NULL,
    email           VARCHAR(150),
    mobile          VARCHAR(20) NOT NULL,
    address         TEXT,
    city            VARCHAR(100),
    state           VARCHAR(100),
    pincode         VARCHAR(10),
    date_of_birth   DATE,
    gender          ENUM('male','female','other'),
    nominee_name    VARCHAR(200),
    nominee_relation VARCHAR(100),
    policy_id       INT,
    agent_id        INT,
    policy_start_date DATE,
    policy_end_date   DATE,
    sum_assured     DECIMAL(15,2),
    status          ENUM('active','inactive','lapsed') DEFAULT 'active',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE SET NULL,
    FOREIGN KEY (agent_id)  REFERENCES agents(id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- Table: premium_payments
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS premium_payments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    payment_code    VARCHAR(50) NOT NULL UNIQUE,
    customer_id     INT NOT NULL,
    policy_id       INT NOT NULL,
    amount          DECIMAL(10,2) NOT NULL,
    due_date        DATE NOT NULL,
    payment_date    DATE,
    payment_mode    ENUM('cash','cheque','online','upi','neft') DEFAULT 'online',
    status          ENUM('paid','pending','overdue') DEFAULT 'pending',
    receipt_number  VARCHAR(100),
    remarks         TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (policy_id)   REFERENCES policies(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Table: claims
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS claims (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    claim_code      VARCHAR(50) NOT NULL UNIQUE,
    customer_id     INT NOT NULL,
    policy_id       INT NOT NULL,
    claim_type      ENUM('death','maturity','accident','health','vehicle') NOT NULL,
    claim_amount    DECIMAL(15,2) NOT NULL,
    claim_date      DATE NOT NULL,
    incident_date   DATE,
    incident_description TEXT,
    document_path   VARCHAR(500),
    status          ENUM('pending','approved','rejected','under_review') DEFAULT 'pending',
    remarks         TEXT,
    resolved_date   DATE,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (policy_id)   REFERENCES policies(id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- Table: contact_messages
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS contact_messages (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    phone       VARCHAR(20),
    email       VARCHAR(150) NOT NULL,
    subject     VARCHAR(300),
    message     TEXT NOT NULL,
    is_read     TINYINT(1) DEFAULT 0,
    replied     TINYINT(1) DEFAULT 0,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Sample Data
-- ============================================================

-- Admin (password: Admin@123)
INSERT INTO admins (username, email, password, full_name, role) VALUES
('admin', 'admin@licms.com', '$2b$12$LQv3c1yqBwEHFl5eBvhMdOQTG5VEnhMVz6vghxlJfVn.yZ5KXWBHC', 'System Administrator', 'super_admin');

-- Agents
INSERT INTO agents (agent_code, full_name, email, mobile, address, city, state, license_number, commission_rate, status, joined_date) VALUES
('AGT001', 'Jaydip Jadhav',    'jaydip.jadhav@licms.com',   '9876543210', '45, MG Road',     'Mumbai',    'Maharashtra', 'LIC/AG/2018/001', 6.50, 'active', '2018-04-01'),
('AGT002', 'Sanika Chavan',          'sanika.chavan@licms.com',   '9845678901', '12, Park Street',  'Pune', 'Maharashtra',   'LIC/AG/2019/002', 5.75, 'active', '2019-07-15'),
('AGT003', 'Rajveer Shinde',            'rajveer.shinde@licms.com',     '9812345678', '78, Civil Lines',  'Nashik',     'Maharashtra',       'LIC/AG/2020/003', 5.50, 'active', '2020-01-10'),
('AGT004', 'Mayur Tawade',          'mayur.tawade@licms.com',   '9900112233', '34, Ring Road',    'Nagpur', 'Maharashtra',     'LIC/AG/2021/004', 5.00, 'inactive','2021-03-22');

-- Policies
INSERT INTO policies (policy_code, policy_name, policy_type, coverage_amount, premium_amount, duration_years, benefits, description, status) VALUES
('POL001', 'LIC Jeevan Anand',        'endowment', 1000000.00, 3500.00, 20, 'Death benefit + Maturity benefit + Bonus', 'A participating endowment plan offering financial protection and savings.', 'active'),
('POL002', 'LIC Tech Term',           'term',      5000000.00,  850.00, 25, 'Pure risk cover, tax benefits u/s 80C', 'Online term plan offering high life cover at affordable premiums.', 'active'),
('POL003', 'LIC New Jeevan Amar',     'term',      2500000.00,  620.00, 30, 'Increasing cover option, accidental benefit', 'Comprehensive term protection plan with increasing sum assured.', 'active'),
('POL004', 'LIC Jeevan Labh',         'endowment', 2000000.00, 5200.00, 16, 'Maturity benefit, survival benefit, bonus', 'Limited premium paying endowment plan with loyalty additions.', 'active'),
('POL005', 'LIC New Money Back Plan', 'endowment',  800000.00, 4100.00, 20, 'Survival benefit every 5 years, death cover', 'Money back plan with periodic survival benefits.', 'active'),
('POL006', 'LIC Pension Plan',        'pension',   1500000.00, 6000.00, 15, 'Guaranteed pension, death benefit, surrender value', 'Retirement solution offering guaranteed monthly pension.', 'active'),
('POL007', 'LIC Child Career Plan',   'child',      600000.00, 2800.00, 18, 'Education + marriage corpus, waiver of premium', 'Secure your child\'s future education and career milestones.', 'active'),
('POL008', 'LIC Health Protection',   'health',     300000.00, 1200.00, 10, 'Hospitalization cover, critical illness', 'Complete health coverage for self and family.', 'active');

-- Customers
INSERT INTO customers (customer_code, full_name, email, mobile, address, city, state, pincode, date_of_birth, gender, nominee_name, nominee_relation, policy_id, agent_id, policy_start_date, policy_end_date, sum_assured, status) VALUES
('CUS001', 'Aakash Wani',        'aakash.wani@email.com',   '9711223344', '102, Sector 15',     'Aurangabad',     'Maharashtra',          '431001', '1985-06-15', 'male',   'Snehlata Wani',    'Wife',   1, 1, '2022-01-01', '2042-01-01', 1000000.00, 'active'),
('CUS002', 'Pradnya Patil',       'pradnya.patil@email.com',  '9922334455', '45, Deccan',  'Pune', 'Maharashtra',   '411004', '1990-03-22', 'female', 'Ramesh Patil',     'Husband',2, 2, '2021-06-15', '2046-06-15', 5000000.00, 'active'),
('CUS003', 'Rohan Kadam',       'rohan.kadam@email.com',  '9833445566', '78, Satellite Area', 'Kolhapur', 'Maharashtra',     '416002', '1978-11-08', 'male',   'Anita Kadam',    'Wife',   4, 4, '2023-03-01', '2039-03-01', 2000000.00, 'active'),
('CUS004', 'Snehal Deshmukh',         'snehal.deshmukh@email.com',    '9744556677', '23, Indiranagar',    'Thane', 'Maharashtra',   '400601', '1995-07-30', 'female', 'Ashabai Deshmukh',      'Mother', 5, 2, '2022-09-01', '2042-09-01',  800000.00, 'active'),
('CUS005', 'Vishal Kale',        'vishal.kale@email.com',   '9655667788', '56, Lajpat Nagar',   'Solapur',     'Maharashtra',       '413003', '1982-02-18', 'male',   'Manjula Kale',  'Wife',   2, 3, '2020-11-01', '2045-11-01', 2500000.00, 'active'),
('CUS006', 'Neha Pawar',        'neha.pawar@email.com',   '9866778899', '89, VIP Road',      'Nanded',   'Maharashtra', '431602', '1988-09-12', 'female', 'Subir Pawar',     'Father', 6, 1, '2021-08-01', '2036-08-01', 1500000.00, 'active'),
('CUS007', 'Omkar Joshi',    'omkar.joshi@email.com',      '9977889900', '34, Jubilee Hills',  'Amravati', 'Maharashtra',   '444601', '1975-04-25', 'male',   'Sonia Joshi', 'Wife',   7, 2, '2023-01-15', '2041-01-15',  600000.00, 'active'),
('CUS008', 'Rutuja Kulkarni',       'rutuja.kulkarni@email.com',  '9788990011', '12, Fort Area',      'Sangli',   'Maharashtra',  '416416', '1993-12-05', 'female', 'Rajan Kulkarni',   'Brother',3, 3, '2022-06-01', '2052-06-01', 2500000.00, 'active');

-- Premium Payments
INSERT INTO premium_payments (payment_code, customer_id, policy_id, amount, due_date, payment_date, payment_mode, status, receipt_number, remarks) VALUES
('PAY001', 1, 1, 3500.00, '2026-01-01', '2025-12-28', 'online', 'paid',    'RCP/2025/001', 'Quarterly premium paid'),
('PAY002', 2, 2,  850.00, '2026-01-15', '2026-01-10', 'upi',    'paid',    'RCP/2026/002', 'Annual premium paid'),
('PAY003', 3, 4, 5200.00, '2026-02-01', NULL,          'cash',   'pending', NULL,           'Due for February'),
('PAY004', 4, 5, 4100.00, '2026-01-01', '2025-12-30', 'online', 'paid',    'RCP/2025/004', 'Quarterly premium paid'),
('PAY005', 5, 2,  620.00, '2026-03-01', NULL,          'neft',   'pending', NULL,           'Due for March'),
('PAY006', 6, 6, 6000.00, '2026-01-20', '2026-01-18', 'cheque', 'paid',    'RCP/2026/006', 'Annual pension premium'),
('PAY007', 7, 7, 2800.00, '2026-02-15', NULL,          'online', 'overdue', NULL,           'Overdue - reminder sent'),
('PAY008', 8, 3,  620.00, '2026-03-15', NULL,          'online', 'pending', NULL,           'Due mid-March');

-- Claims
INSERT INTO claims (claim_code, customer_id, policy_id, claim_type, claim_amount, claim_date, incident_date, incident_description, status, remarks) VALUES
('CLM001', 5, 2, 'accident',  500000.00, '2026-01-10', '2026-01-05', 'Motor accident resulting in hospitalization', 'under_review', 'Documents submitted, verification in progress'),
('CLM002', 6, 6, 'maturity',  1500000.00,'2026-02-01', '2036-08-01', 'Policy maturity claim', 'pending', 'Claim initiated for maturity payout'),
('CLM003', 2, 2, 'health',     80000.00, '2025-12-15', '2025-12-10', 'Hospitalization for surgery', 'approved', 'Approved - payment processed'),
('CLM004', 3, 4, 'death',    2000000.00, '2026-03-01', '2026-02-25', 'Nominee claim filed after policyholder demise', 'pending', 'Awaiting death certificate');

-- Contact Messages
INSERT INTO contact_messages (name, phone, email, subject, message, is_read) VALUES
('Aniket More',   '9887766554', 'aniket.more@gmail.com',    'Policy Enquiry',     'I would like to know more about your term insurance plans for 30-year coverage.', 1),
('Swati Rane','9776655443', 'swati.rane@yahoo.com',        'Claim Assistance',   'My claim has been pending for 2 weeks. Can someone help me with the status?', 0),
('Kiran Desai',    '9665544332', 'kiran.desai@outlook.com',   'Premium Due Dates',  'I need information about my upcoming premium payment schedule.', 0),
('Pallavi Gaikwad',  '9554433221', 'pallavi.gaikwad@gmail.com',      'New Policy Purchase','I want to purchase a child plan for my 5-year-old daughter.', 1),
('Sandeep Bhosale',  '9443322110', 'sandeep.bhosale@email.com',   'Agent Contact',      'Please connect me with an agent in Pune for policy consultation.', 0);
