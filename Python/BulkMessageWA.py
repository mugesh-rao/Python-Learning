import time
import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

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
    print(formatted_mobile)
    api_url = f"https://api.textmebot.com/send.php?recipient=+91{formatted_mobile}&apikey=xqVoHxJtM417&text={requests.utils.quote(message)}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print(f"Message sent to {name} ({mobile})")
        else:
            print(f"Failed to send message to {name}: {response.text}")
    except Exception as e:
        print(f"Error sending message to {name}: {e}")

# Function to read hospitals from Excel
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path, usecols=[0, 1], names=["name", "mobile"], skiprows=1)
        df = df.dropna(subset=["name", "mobile"])  # Remove rows without name or mobile
        return df.to_dict(orient="records")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read Excel file: {e}")
        return []

# Function to select file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Function to send messages
def send_messages():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Warning", "Please select an Excel file first.")
        return
    
    hospitals = read_excel_file(file_path)
    if not hospitals:
        messagebox.showwarning("Warning", "No valid data found in the file.")
        return
    
    for hospital in hospitals:
        send_whatsapp_message(hospital["name"], hospital["mobile"])
        time.sleep(8)  # Wait 8 seconds before sending the next message
    
    messagebox.showinfo("Success", "Messages sent successfully!")

# Create UI
root = tk.Tk()
root.title("Bulk WhatsApp Sender")
root.geometry("500x250")

tk.Label(root, text="Select Excel File:").pack(pady=5)

file_entry = tk.Entry(root, width=50)
file_entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=select_file)
browse_button.pack(pady=5)

send_button = tk.Button(root, text="Send Messages", command=send_messages, bg="green", fg="white")
send_button.pack(pady=20)

root.mainloop()
