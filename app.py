from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

registered_students = []
enroll_counter = 1


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    global enroll_counter

    name = request.form.get("name")
    phone = request.form.get("phone")
    register_number = request.form.get("register_number")
    department = request.form.get("department")
    year = request.form.get("year")
    college = request.form.get("college")
    reg_date = request.form.get("reg_date")   # ✅ selected from calendar

    # ✅ duplicate check
    for s in registered_students:
        if s["register_number"] == register_number:
            return "Student already registered!"

    # ✅ year code from selected date
    year_code = reg_date[2:4]   # YYYY-MM-DD → YY

    # ✅ enroll number format
    enroll_number = f"{year_code}HME{enroll_counter:03}"

    # ✅ auto system time
    auto_time = datetime.now().strftime("%H:%M:%S")

    student = {
        "enroll_number": enroll_number,
        "name": name,
        "register_number": register_number,
        "department": department,
        "year": year,
        "college": college,
        "phone": phone,
        "date": reg_date,     # from calendar
        "time": auto_time     # automatic
    }

    registered_students.append(student)
    enroll_counter += 1

    return render_template("success.html", student=student)


@app.route('/registered-students')
def view_students():
    return render_template(
        "registered_students.html",
        students=registered_students,
        total=len(registered_students)
    )


if __name__ == "__main__":
    app.run(debug=True)