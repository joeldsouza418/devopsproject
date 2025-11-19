from flask import Flask, render_template_string, request
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import json
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Exam Reminder</title></head>
<body style="font-family:Arial; margin:40px;">
    <h2>Hello from DevOps Pipeline</h2>
    <h3>Set Exam Reminder</h3>

    <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Exam Date:</label><br>
        <input type="date" name="exam_date" required><br><br>

        <button type="submit">Set Reminder</button>
    </form>

    <p>{{ msg }}</p>
</body>
</html>
"""

REMINDER_FILE = "reminders.json"

def load_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_reminders(data):
    with open(REMINDER_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        exam_date = request.form["exam_date"]

        reminders = load_reminders()
        reminders.append({
            "name": name,
            "email": email,
            "exam_date": exam_date
        })
        save_reminders(reminders)

        msg = "Reminder saved successfully!"

    return render_template_string(HTML_PAGE, msg=msg)

def send_email(to_email, subject, body):
    sender = "yourgmail@gmail.com"
    password = "pkgs xbku mdgr ubnc"  # Gmail App Password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())

def check_exam_reminders():
    today = datetime.now().strftime("%Y-%m-%d")
    reminders = load_reminders()
    remaining = []

    for r in reminders:
        if r["exam_date"] == today:
            body = f"Hello {r['name']}, this is a reminder that your exam is today!"
            send_email(r["email"], "Exam Reminder", body)
        else:
            remaining.append(r)

    save_reminders(remaining)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_exam_reminders, "cron", hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
