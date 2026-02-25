import os
import io
from flask import Flask, render_template, request, send_file
from datetime import datetime
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/meme_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

students = []
counter = 1

def generate_enroll():
    global counter
    eid = f"26HME{counter:03d}"
    counter += 1
    return eid

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register():
    enroll = generate_enroll()
    now = datetime.now()

    meme_uploaded = False
    meme_filename = None

    file = request.files.get("meme_file")
    if file and file.filename and allowed_file(file.filename):
        meme_filename = secure_filename(f"{enroll}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], meme_filename))
        meme_uploaded = True

    student = {
        "enroll": enroll,
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "regno": request.form["register_number"],
        "dept": request.form["department"],
        "year": request.form["year"],
        "college": request.form["college"],
        "registered_on": now.strftime("%d %b %Y"),
        "time": now.strftime("%H:%M:%S"),
        "meme_uploaded": meme_uploaded,
        "meme_filename": meme_filename
    }
    students.append(student)
    return render_template("success.html", name=student["name"], enroll=enroll, meme_done=meme_uploaded)

@app.route('/upload-meme/<enroll>', methods=["GET", "POST"])
def upload_meme(enroll):
    student = next((s for s in students if s["enroll"] == enroll), None)
    if not student:
        return f"<h2 style='font-family:sans-serif;padding:2rem;'>Student ID <strong>{enroll}</strong> not found. <a href='/'>Go Back</a></h2>", 404
    if request.method == "POST":
        file = request.files.get("meme_file")
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{enroll}_{file.filename}")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            student["meme_uploaded"] = True
            student["meme_filename"] = filename
            return render_template("success.html", name=student["name"], enroll=enroll, meme_done=True)
        else:
            error = "Invalid file. Please upload an image (PNG, JPG, GIF) or video (MP4, MOV, AVI, WEBM)."
            return render_template("upload_meme.html", student=student, error=error)
    return render_template("upload_meme.html", student=student, error=None)

@app.route('/registered-students')
def registered():
    return render_template("registered_students.html", students=students)

@app.route('/download')
def download():
    if not students:
        return "No students registered yet.", 400
    export_data = []
    for s in students:
        export_data.append({
            "Enrollment ID": s["enroll"],
            "Name": s["name"],
            "Email": s["email"],
            "Phone": s["phone"],
            "Register Number": s["regno"],
            "Department": s["dept"],
            "Year": s["year"],
            "College": s["college"],
            "Registered On": s["registered_on"],
            "Time": s["time"],
            "Meme Uploaded": "Yes" if s["meme_uploaded"] else "No",
            "Meme File": s["meme_filename"] if s["meme_filename"] else "-"
        })
    df = pd.DataFrame(export_data)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, download_name="registered_students.xlsx", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)