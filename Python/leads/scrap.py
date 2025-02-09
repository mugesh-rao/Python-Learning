import os
import time
import requests
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Define upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to send WhatsApp message
def send_whatsapp_message(name, mobile):
    message = f"""
    Hi *{name}* 👋,
    
    I’m Mugesh Rao, a web developer from Chennai.
    
    I’ve been following your work at *{name}* and truly admire the impact you're making.
    
    I create affordable, high-converting websites tailored to businesses like yours.
    
    Check out my work here: https://mugesh-rao.web.app/
    
    If you’d like to explore how we can elevate *{name}’s* website, I’d be happy to discuss—starting at very affordable prices. 😊
    
    Looking forward to hearing from you!
    """
    
    formatted_mobile = str(mobile).replace(" ", "").lstrip("0")  # Format mobile number
    api_url = f"https://api.textmebot.com/send.php?recipient=+91{formatted_mobile}&apikey=xqVoHxJtM417&text={requests.utils.quote(message)}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print(f"Message sent to {name} ({mobile})")
        else:
            print(f"Failed to send message to {name}: {response.text}")
    except Exception as e:
        print(f"Error sending message to {name}: {e}")

# Function to read Excel file and return records
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path, usecols=[0, 1], names=["name", "mobile"], skiprows=1)
        df = df.dropna(subset=["name", "mobile"])  # Remove rows without name or mobile
        return df.to_dict(orient="records")
    except Exception as e:
        return str(e)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to upload the Excel file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Read Excel file and send messages
        hospitals = read_excel_file(filename)
        
        if isinstance(hospitals, list):
            for hospital in hospitals:
                send_whatsapp_message(hospital["name"], hospital["mobile"])
                time.sleep(8)  # Wait before sending next message
            flash('Messages sent successfully!')
        else:
            flash(f"Error reading file: {hospitals}")
        
        return redirect(url_for('index'))

    flash('Invalid file format. Please upload an Excel file.')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)
