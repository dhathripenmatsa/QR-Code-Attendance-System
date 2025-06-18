import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os

# Create folder to store QR codes
if not os.path.exists("qrcodes"):
    os.makedirs("qrcodes")

def generate_qr():
    student_id = entry_id.get()
    name = entry_name.get()

    if student_id == "" or name == "":
        messagebox.showwarning("Input Error", "Please enter both Student ID and Name.")
        return

    data = f"ID: {student_id}\nName: {name}"
    qr = qrcode.make(data)
    filename = f"qrcodes/{student_id}.png"
    qr.save(filename)

    img = Image.open(filename)
    img = img.resize((200, 200))
    qr_img = ImageTk.PhotoImage(img)
    label_qr.config(image=qr_img)
    label_qr.image = qr_img

    messagebox.showinfo("Success", f"QR Code generated for {name}")

root = tk.Tk()
root.title("QR Code Generator - Attendance")
root.geometry("400x500")
root.config(bg="#e6f2ff")

tk.Label(root, text="Student ID:", font=("Arial", 12), bg="#e6f2ff").pack(pady=5)
entry_id = tk.Entry(root, font=("Arial", 12))
entry_id.pack(pady=5)

tk.Label(root, text="Student Name:", font=("Arial", 12), bg="#e6f2ff").pack(pady=5)
entry_name = tk.Entry(root, font=("Arial", 12))
entry_name.pack(pady=5)

tk.Button(root, text="Generate QR Code", font=("Arial", 12), command=generate_qr, bg="#007acc", fg="white").pack(pady=20)

label_qr = tk.Label(root, bg="#e6f2ff")
label_qr.pack(pady=10)

root.mainloop()
