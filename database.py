import sqlite3
import os

DB_PATH = os.path.join("database", "employee.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        department TEXT NOT NULL,
        salary INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_employee(name, email, department, salary):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees(name,email,department,salary)
        VALUES(?,?,?,?)
    """, (name, email, department, salary))

    conn.commit()
    conn.close()


def get_employees():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    conn.close()

    return employees


def get_employee_by_id(employee_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    )

    employee = cursor.fetchone()

    conn.close()

    return employee


def update_employee(employee_id, name, email, department, salary):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name = ?,
            email = ?,
            department = ?,
            salary = ?
        WHERE id = ?
    """, (name, email, department, salary, employee_id))

    conn.commit()

    conn.close()

def delete_employee(employee_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    conn.commit()

    conn.close()


def search_employees(keyword):

    print("Searching for:", keyword)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM employees
        WHERE name LIKE ?
        """,
        ('%' + keyword + '%',)
    )

    employees = cursor.fetchall()

    print("Results:", employees)

    conn.close()

    return employees