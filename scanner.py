import cv2
from pyzbar.pyzbar import decode
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os

# Set up popup root
root = tk.Tk()
root.withdraw()

# File to store attendance
attendance_file = "attendance.csv"

# Load today's existing entries (to avoid duplicates)
today_date = datetime.now().strftime('%Y-%m-%d')
marked_ids = set()

if os.path.exists(attendance_file):
    with open(attendance_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:
                id_, name, timestamp = row
                if timestamp.startswith(today_date):
                    marked_ids.add(id_)

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam")
    exit()

print("[INFO] Scanner running... Show QR codes one by one.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for qr in decode(frame):
        data = qr.data.decode('utf-8')

        try:
            lines = data.split('\n')
            student_id = lines[0].replace("ID: ", "").strip()
            name = lines[1].replace("Name: ", "").strip()

            if student_id in marked_ids:
                print(f"⚠️ Duplicate: {name} already marked today.")
                messagebox.showwarning("Duplicate", f"{name}'s attendance is already marked today.")
            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(attendance_file, "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([student_id, name, now])
                    marked_ids.add(student_id)

                print(f"✅ {name} marked at {now}")
                messagebox.showinfo("Marked", f"{name}'s attendance has been marked!")

        except Exception as e:
            print("❌ Error reading QR content:", e)

        # Delay to avoid reading the same QR repeatedly
        cv2.waitKey(1500)

    cv2.imshow("QR Attendance Scanner - Press 'q' to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Scanner stopped.")
        break

cap.release()
cv2.destroyAllWindows()



