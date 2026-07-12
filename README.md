# 🚀 AssetFlow

> Enterprise Asset & Resource Management System

AssetFlow is a full-stack Enterprise Resource Planning (ERP) application that helps organizations efficiently manage physical assets, shared resources, maintenance workflows, and asset lifecycle operations.

The platform digitizes manual asset tracking by providing a centralized system for asset registration, allocation, maintenance, booking, auditing, and reporting.

---

## 📌 Project Status

| Module | Status |
|---------|--------|
| ✅ Backend | Completed |
| 🚧 Frontend | Under Development |
| 🔐 Authentication | Completed |
| 🗄️ Database Design | Completed |
| 🔌 REST APIs | Completed |
| 🎨 UI/UX | In Progress |

---

# 📖 Problem Statement

Organizations often rely on spreadsheets and paper logs to manage assets, leading to:

- Asset duplication
- Missing assets
- No ownership tracking
- Booking conflicts
- Difficult maintenance management
- Poor audit visibility

AssetFlow solves these problems through a centralized ERP platform supporting complete asset lifecycle management.

---

# ✨ Features

## 🔐 Authentication

- User Signup
- Secure Login
- JWT Authentication
- Password Encryption
- Role Based Access Control

---

## 👨‍💼 Organization Management

- Department Management
- Employee Directory
- Role Assignment
- Asset Categories

Roles include:

- Admin
- Asset Manager
- Department Head
- Employee

---

## 📦 Asset Management

- Register Assets
- Auto Generated Asset Tags
- Upload Asset Images
- Serial Number Tracking
- Asset Categories
- Asset Locations
- Asset Conditions

Lifecycle States

- Available
- Allocated
- Reserved
- Under Maintenance
- Lost
- Retired
- Disposed

---

## 🔄 Asset Allocation

- Allocate Assets
- Return Assets
- Transfer Requests
- Conflict Prevention
- Expected Return Date
- Allocation History

---

## 📅 Resource Booking

Book shared resources such as:

- Meeting Rooms
- Vehicles
- Equipment

Includes

- Calendar View
- Time Slot Booking
- Overlap Validation
- Reschedule
- Cancellation
- Booking History

---

## 🛠 Maintenance Workflow

Maintenance lifecycle

Pending

↓

Approved / Rejected

↓

Technician Assigned

↓

In Progress

↓

Resolved

Features

- Raise Requests
- Priority Levels
- Attach Images
- Approval Workflow
- Maintenance History

---

## 📋 Asset Audits

- Audit Cycles
- Auditor Assignment
- Asset Verification
- Missing Assets
- Damaged Assets
- Auto Discrepancy Reports

---

## 📊 Dashboard

Dashboard includes

- Assets Available
- Assets Allocated
- Active Bookings
- Maintenance Today
- Upcoming Returns
- Overdue Returns
- Pending Transfers

---

## 📈 Reports & Analytics

- Asset Utilization
- Maintenance Trends
- Department Reports
- Booking Statistics
- Export Reports

---

## 🔔 Notifications

- Asset Assigned
- Return Reminder
- Booking Reminder
- Maintenance Updates
- Audit Notifications
- Transfer Approval

---

# 🏗 Tech Stack

## Backend

- Java
- Spring Boot
- Spring Security
- Spring Data JPA
- Hibernate
- MySQL
- Maven
- JWT Authentication

## Frontend (Current Development)

- React.js
- Vite
- Tailwind CSS
- Axios
- React Router

## Database

- MySQL

## Tools

- Git
- GitHub
- Postman
- IntelliJ IDEA
- VS Code

---

# 📂 Project Structure

```
asset-flow/
│
├── backend/
│   ├── src/
│   ├── controller/
│   ├── service/
│   ├── repository/
│   ├── model/
│   ├── security/
│   ├── dto/
│   └── config/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── layouts/
│   └── assets/
│
├── README.md
└── .gitignore
```

---

# 🔄 System Workflow

```
User Login
      │
      ▼
Dashboard
      │
      ├──────────────┐
      ▼              ▼
Assets         Organization
      │
      ▼
Allocation
      │
      ▼
Maintenance
      │
      ▼
Audit
      │
      ▼
Reports
```

---

# 🔑 User Roles

## 👑 Admin

- Manage Departments
- Manage Categories
- Manage Employees
- Assign Roles
- View Analytics

---

## 📦 Asset Manager

- Register Assets
- Allocate Assets
- Approve Transfers
- Approve Maintenance
- Manage Returns

---

## 🏢 Department Head

- View Department Assets
- Approve Requests
- Book Shared Resources

---

## 👤 Employee

- View Assigned Assets
- Book Resources
- Raise Maintenance Requests
- Request Returns
- Request Transfers

---

# 🔐 Backend APIs

Authentication

```
POST /api/auth/signup
POST /api/auth/login
```

Departments

```
GET /api/departments
POST /api/departments
PUT /api/departments/{id}
DELETE /api/departments/{id}
```

Assets

```
GET /api/assets
POST /api/assets
PUT /api/assets/{id}
DELETE /api/assets/{id}
```

Employees

```
GET /api/employees
POST /api/employees
```

Maintenance

```
POST /api/maintenance
PUT /api/maintenance/{id}
GET /api/maintenance
```

Bookings

```
POST /api/bookings
GET /api/bookings
```

---

# ⚙ Backend Setup

Clone repository

```bash
git clone https://github.com/Ramana-Giri/asset-flow.git
```

Go to backend

```bash
cd backend
```

Install dependencies

```bash
mvn clean install
```

Configure

```
application.properties
```

Run

```bash
mvn spring-boot:run
```

Server

```
http://localhost:8080
```

---

# 🎨 Frontend Setup

Go to frontend

```bash
cd frontend
```

Install packages

```bash
npm install
```

Run

```bash
npm run dev
```

Frontend

```
http://localhost:5173
```

---

# 🗃 Database

Create a MySQL database

```
assetflow
```

Update

```
application.properties
```

with

```
Database URL
Username
Password
```

Run the application and Hibernate will generate the tables.

---

# 🚧 Upcoming Frontend Modules

- Login UI
- Dashboard
- Asset Registration
- Asset Directory
- Asset Allocation
- Resource Booking
- Maintenance Management
- Audit Module
- Reports & Analytics
- Notifications
- Profile Settings
- Responsive Design

---

# 🤝 Contributors

- Ramana Giri
- Team AssetFlow

---

# 🎯 Future Improvements

- QR Code Asset Tracking
- Barcode Scanner
- Email Notifications
- Mobile Responsive UI
- File Uploads
- Dark Mode
- Charts & Analytics
- Docker Deployment
- CI/CD Pipeline

---

# 📄 License

This project was developed as part of an ERP/Hackathon project for learning and demonstration purposes.

---

## ⭐ If you like this project, don't forget to give it a Star!
