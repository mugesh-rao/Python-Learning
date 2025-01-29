import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Email server settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'growwto@gmail.com'
SENDER_PASSWORD = 'Mugesh23ego$'

# Function to send emails
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, to_email, text)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error: {e}")

# Route to show the upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        # Save the uploaded file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Read the Excel file
        df = pd.read_excel(file_path)

        # Loop through rows and send emails
        for index, row in df.iterrows():
            recipient_email = row['email']  # Assuming you have an 'email' column in Excel
            subject = "Your Excel Data"
            body = f"Hello, \n\nHere is your data:\n{row.to_dict()}"

            send_email(recipient_email, subject, body)

        return "Emails have been sent!"

    return "Invalid file format!"

if __name__ == '__main__':
    app.run(debug=True)
