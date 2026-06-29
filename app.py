from flask import Flask, render_template, request, redirect
from database import (
    init_db,
    add_employee,
    get_employees,
    get_employee_by_id,
    update_employee,
    delete_employee,
    search_employees
)

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
        employees=employees
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)