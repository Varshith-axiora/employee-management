from flask import Flask, render_template, request, redirect, jsonify
import os

from database import (
    init_db,
    add_employee,
    get_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
    search_employees
)

# ----------------------------
# Read values from environment
# ----------------------------
APP_NAME = os.getenv("APP_NAME", "🚀 Employee Management System")
COMPANY = os.getenv("COMPANY", "Axiora")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

app = Flask(__name__)

# Initialize the database
init_db()


@app.route("/")
def home():

    keyword = request.args.get("search")

    if keyword:
        employees = search_employees(keyword)
    else:
        employees = get_employees()

    return render_template(
        "index.html",
        employees=employees,
        app_name=APP_NAME,
        company=COMPANY,
        environment=ENVIRONMENT
    )


@app.route("/add", methods=["POST"])
def add_employee_route():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    salary = request.form["salary"]

    add_employee(name, email, department, salary)

    return redirect("/")


@app.route("/edit/<int:employee_id>")
def edit_employee(employee_id):

    employee = get_employee_by_id(employee_id)

    return render_template(
        "edit.html",
        employee=employee
    )


@app.route("/update/<int:employee_id>", methods=["POST"])
def update_employee_route(employee_id):

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    salary = request.form["salary"]

    update_employee(
        employee_id,
        name,
        email,
        department,
        salary
    )

    return redirect("/")


@app.route("/delete/<int:employee_id>")
def delete_employee_route(employee_id):

    delete_employee(employee_id)

    return redirect("/")


@app.route("/api/employees", methods=["GET"])
def api_get_employees():

    employees = get_employees()

    employee_list = []

    for emp in employees:
        employee_list.append({
            "id": emp[0],
            "name": emp[1],
            "email": emp[2],
            "department": emp[3],
            "salary": emp[4]
        })

    return jsonify(employee_list)

@app.route("/api/employees/<int:employee_id>", methods=["GET"])
def api_get_employee(employee_id):

    employee = get_employee_by_id(employee_id)

    if not employee:
        return jsonify({"message": "Employee not found"}), 404

    return jsonify({
        "id": employee[0],
        "name": employee[1],
        "email": employee[2],
        "department": employee[3],
        "salary": employee[4]
    })

@app.route("/api/employees", methods=["POST"])
def api_add_employee():

    data = request.get_json()

    add_employee(
        data["name"],
        data["email"],
        data["department"],
        data["salary"]
    )

    return jsonify({
        "message": "Employee added successfully"
    }), 201

@app.route("/api/employees/<int:employee_id>", methods=["PUT"])
def api_update_employee(employee_id):

    data = request.get_json()

    update_employee(
        employee_id,
        data["name"],
        data["email"],
        data["department"],
        data["salary"]
    )

    return jsonify({
        "message": "Employee updated successfully"
    })

@app.route("/api/employees/<int:employee_id>", methods=["DELETE"])
def api_delete_employee(employee_id):

    delete_employee(employee_id)

    return jsonify({
        "message": "Employee deleted successfully"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)