import psycopg
import os


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "postgres-service"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        department VARCHAR(100) NOT NULL,
        salary INTEGER NOT NULL
    )
    """)

    conn.commit()

    cursor.close()

    conn.close()


def add_employee(name, email, department, salary):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees(name,email,department,salary)
        VALUES(%s,%s,%s,%s)
    """, (name, email, department, salary))

    conn.commit()

    cursor.close()

    conn.close()


def get_employees():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    cursor.close()

    conn.close()

    return employees


def get_employee_by_id(employee_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (employee_id,)
    )

    employee = cursor.fetchone()

    cursor.close()

    conn.close()

    return employee


def update_employee(employee_id, name, email, department, salary):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE employees
        SET
            name=%s,
            email=%s,
            department=%s,
            salary=%s
        WHERE id=%s
    """, (
        name,
        email,
        department,
        salary,
        employee_id
    ))

    conn.commit()

    cursor.close()

    conn.close()


def delete_employee(employee_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (employee_id,)
    )

    conn.commit()

    cursor.close()

    conn.close()


def search_employees(keyword):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM employees
        WHERE name LIKE %s
        """,
        ('%' + keyword + '%',)
    )

    employees = cursor.fetchall()

    cursor.close()

    conn.close()

    return employees