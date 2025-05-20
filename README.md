# 🏥 Hospital Management System

A simple GUI-based Hospital Management System built using **Python (Tkinter)** and **MySQL**. This application allows for the management of doctor and patient records in a hospital environment.

## 🚀 Features

### 👨‍⚕️ Doctor Management
- Add new doctors
- View list of all doctors
- Store doctor's name, specialization, contact, and availability

### 🧑‍🦽 Patient Management
- Add new patients
- View list of all patients with assigned doctor
- Store patient details including name, age, gender, ailment, doctor, and admission/discharge dates

## 🛠 Tech Stack

- **Python 3.x**
- **Tkinter** (for GUI)
- **MySQL** (as the backend database)
- `mysql-connector-python` (for connecting Python with MySQL)

---



## 🗃️ Database Schema

### Table: `doctors`

| Column         | Type         |
|----------------|--------------|
| doctor_id      | INT (PK)     |
| name           | VARCHAR(100) |
| specialization | VARCHAR(50)  |
| contact        | VARCHAR(15)  |
| availability   | VARCHAR(50)  |

### Table: `patients`

| Column           | Type         |
|------------------|--------------|
| patient_id       | INT (PK)     |
| name             | VARCHAR(100) |
| age              | INT          |
| gender           | ENUM         |
| ailment          | VARCHAR(100) |
| assigned_doctor  | INT (FK)     |
| admission_date   | DATE         |
| discharge_date   | DATE         |

---

## ⚙️ How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system
