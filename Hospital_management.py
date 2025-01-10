import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pradeep@1234", 
    database="hospital_management"
)
cursor = db.cursor()

# Create tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(50),
    contact VARCHAR(15),
    availability VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    ailment VARCHAR(100),
    assigned_doctor INT,
    admission_date DATE,
    discharge_date DATE,
    FOREIGN KEY (assigned_doctor) REFERENCES doctors(doctor_id)
);
""")

db.commit()

# Add Doctor Function
def add_doctor():
    name = doctor_name.get()
    specialization = doctor_specialization.get()
    contact = doctor_contact.get()
    availability = doctor_availability.get()

    if name and specialization and contact and availability:
        query = "INSERT INTO doctors (name, specialization, contact, availability) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, specialization, contact, availability))
        db.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")
        clear_doctor_fields()
        view_doctors()
    else:
        messagebox.showerror("Error", "All fields are required!")

def clear_doctor_fields():
    doctor_name.delete(0, tk.END)
    doctor_specialization.delete(0, tk.END)
    doctor_contact.delete(0, tk.END)
    doctor_availability.delete(0, tk.END)

def view_doctors():
    cursor.execute("SELECT * FROM doctors")
    rows = cursor.fetchall()
    for row in doctor_table.get_children():
        doctor_table.delete(row)
    for row in rows:
        doctor_table.insert("", tk.END, values=row)

# Add Patient Function
def add_patient():
    name = patient_name.get()
    age = patient_age.get()
    gender = patient_gender.get()
    ailment = patient_ailment.get()
    assigned_doctor = patient_assigned_doctor.get()
    admission_date = patient_admission_date.get()

    if name and age and gender and ailment and assigned_doctor and admission_date:
        query = """
        INSERT INTO patients (name, age, gender, ailment, assigned_doctor, admission_date) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, age, gender, ailment, assigned_doctor, admission_date))
        db.commit()
        messagebox.showinfo("Success", "Patient added successfully!")
        clear_patient_fields()
        view_patients()
    else:
        messagebox.showerror("Error", "All fields are required!")

def clear_patient_fields():
    patient_name.delete(0, tk.END)
    patient_age.delete(0, tk.END)
    patient_gender.set("")
    patient_ailment.delete(0, tk.END)
    patient_assigned_doctor.delete(0, tk.END)
    patient_admission_date.delete(0, tk.END)

def view_patients():
    cursor.execute("""
    SELECT p.patient_id, p.name, p.age, p.gender, p.ailment, d.name AS doctor_name, p.admission_date, p.discharge_date 
    FROM patients p 
    LEFT JOIN doctors d ON p.assigned_doctor = d.doctor_id
    """)
    rows = cursor.fetchall()
    for row in patient_table.get_children():
        patient_table.delete(row)
    for row in rows:
        patient_table.insert("", tk.END, values=row)

# Main Tkinter Window
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("800x600")

# Tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Doctor Tab
doctor_tab = tk.Frame(notebook)
notebook.add(doctor_tab, text="Doctors")

# Doctor Form
tk.Label(doctor_tab, text="Name").grid(row=0, column=0, padx=5, pady=5)
doctor_name = tk.Entry(doctor_tab)
doctor_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(doctor_tab, text="Specialization").grid(row=1, column=0, padx=5, pady=5)
doctor_specialization = tk.Entry(doctor_tab)
doctor_specialization.grid(row=1, column=1, padx=5, pady=5)

tk.Label(doctor_tab, text="Contact").grid(row=2, column=0, padx=5, pady=5)
doctor_contact = tk.Entry(doctor_tab)
doctor_contact.grid(row=2, column=1, padx=5, pady=5)

tk.Label(doctor_tab, text="Availability").grid(row=3, column=0, padx=5, pady=5)
doctor_availability = tk.Entry(doctor_tab)
doctor_availability.grid(row=3, column=1, padx=5, pady=5)

tk.Button(doctor_tab, text="Add Doctor", command=add_doctor).grid(row=4, column=0, columnspan=2, pady=10)

# Doctor Table
doctor_table = ttk.Treeview(doctor_tab, columns=("ID", "Name", "Specialization", "Contact", "Availability"), show="headings")
doctor_table.grid(row=5, column=0, columnspan=2, pady=10)

for col in ("ID", "Name", "Specialization", "Contact", "Availability"):
    doctor_table.heading(col, text=col)

tk.Button(doctor_tab, text="View Doctors", command=view_doctors).grid(row=6, column=0, columnspan=2, pady=10)

# Patient Tab
patient_tab = tk.Frame(notebook)
notebook.add(patient_tab, text="Patients")

tk.Label(patient_tab, text="Name").grid(row=0, column=0, padx=5, pady=5)
patient_name = tk.Entry(patient_tab)
patient_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Age").grid(row=1, column=0, padx=5, pady=5)
patient_age = tk.Entry(patient_tab)
patient_age.grid(row=1, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Gender").grid(row=2, column=0, padx=5, pady=5)
patient_gender = ttk.Combobox(patient_tab, values=["Male", "Female", "Other"])
patient_gender.grid(row=2, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Ailment").grid(row=3, column=0, padx=5, pady=5)
patient_ailment = tk.Entry(patient_tab)
patient_ailment.grid(row=3, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Assigned Doctor (ID)").grid(row=4, column=0, padx=5, pady=5)
patient_assigned_doctor = tk.Entry(patient_tab)
patient_assigned_doctor.grid(row=4, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Admission Date (YYYY-MM-DD)").grid(row=5, column=0, padx=5, pady=5)
patient_admission_date = tk.Entry(patient_tab)
patient_admission_date.grid(row=5, column=1, padx=5, pady=5)

tk.Button(patient_tab, text="Add Patient", command=add_patient).grid(row=6, column=0, columnspan=2, pady=10)

# Patient Table
patient_table = ttk.Treeview(patient_tab, columns=("ID", "Name", "Age", "Gender", "Ailment", "Doctor", "Admission", "Discharge"), show="headings")
patient_table.grid(row=7, column=0, columnspan=2, pady=10)

for col in ("ID", "Name", "Age", "Gender", "Ailment", "Doctor", "Admission", "Discharge"):
    patient_table.heading(col, text=col)

tk.Button(patient_tab, text="View Patients", command=view_patients).grid(row=8, column=0, columnspan=2, pady=10)

# Run Application
root.mainloop()
