from flask import Flask, render_template, request, send_file
from datetime import datetime
import pandas as pd
import io

app = Flask(__name__)

students = []
counter = 1


def generate_enroll():
    global counter
    eid = f"26HME{counter:03d}"
    counter += 1
    return eid


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    enroll = generate_enroll()
    now = datetime.now()

    student = {
        "enroll": enroll,
        "name": request.form["name"],
        "phone": request.form["phone"],
        "regno": request.form["register_number"],
        "dept": request.form["department"],
        "year": request.form["year"],
        "college": request.form["college"],
        "date": request.form["event_date"],
        "time": now.strftime("%H:%M:%S")
    }

    students.append(student)

    return render_template("success.html",
                           name=student["name"],
                           enroll=enroll)


@app.route('/registered-students')
def registered():
    return render_template("registered_students.html", students=students)


@app.route('/download')
def download():
    df = pd.DataFrame(students)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output,
                     download_name="registered_students.xlsx",
                     as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)