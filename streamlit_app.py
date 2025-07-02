# streamlit_app.py
import streamlit as st
import qrcode
import io
from PIL import Image
from pyzbar.pyzbar import decode
from datetime import datetime
import pandas as pd
import os

# File paths
ATTENDANCE_FILE = "attendance.csv"
TXT_LOG         = "attendance_log.txt"

# Expected CSV header
COLS = ["Student_ID", "Student_Name", "Date", "Time"]

# ---------------------------------------------------------------------
# Streamlit page setup
# ---------------------------------------------------------------------
st.set_page_config(page_title="QR Attendance System", layout="centered")
st.title("📸 QR Code‑Based Smart Attendance System")

# ---------------------------------------------------------------------
# QR code generator section
# ---------------------------------------------------------------------
st.header("📇 Generate QR Code")

with st.form("qr_form", clear_on_submit=True):
    student_name = st.text_input("Enter Student Name")
    student_id   = st.text_input("Enter Student ID")
    submitted    = st.form_submit_button("Generate QR Code")

if submitted:
    if student_name and student_id:
        data = f"{student_id},{student_name}"
        qr_img = qrcode.make(data)

        # Ensure 'qrcodes' folder exists
        os.makedirs("qrcodes", exist_ok=True)

        # Save QR image in the folder with student info
        filepath = os.path.join("qrcodes", f"{student_id}_{student_name}.png")
        qr_img.save(filepath)

        # Display QR in the app
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Scan this QR", width=200)

        st.success(f"✅ QR Code saved to: {filepath}")
    else:
        st.warning("Please enter both Student ID and Student Name")

# ---------------------------------------------------------------------
# Attendance scanner section
# ---------------------------------------------------------------------
st.header("🎥 Scan QR Code for Attendance")

img = st.camera_input("Show your QR Code to the webcam and click **Capture**")

if img:
    img = Image.open(img)
    results = decode(img)

    if results:
        qr_data = results[0].data.decode("utf-8")
        try:
            scanned_id, scanned_name = qr_data.split(",", 1)
        except ValueError:
            st.error("Invalid QR format. Expected 'StudentID,StudentName'.")
            st.stop()

        # Current date & time
        now       = datetime.now()
        date_str  = now.strftime("%Y-%m-%d")
        time_str  = now.strftime("%H:%M:%S")

        # Load or initialise CSV
        if os.path.exists(ATTENDANCE_FILE):
            df = pd.read_csv(ATTENDANCE_FILE)
            # If header mismatch, force‑fix but warn user
            if list(df.columns) != COLS:
                df.columns = COLS[: len(df.columns)]
        else:
            df = pd.DataFrame(columns=COLS)

        # Duplicate check (same student, same day)
        already = ((df["Student_ID"] == scanned_id) & (df["Date"] == date_str)).any()

        if already:
            st.warning(f"⚠️  {scanned_name} ({scanned_id}) already marked today.")
        else:
            # Build new row
            new_row = {
                "Student_ID":   scanned_id,
                "Student_Name": scanned_name,
                "Date":         date_str,
                "Time":         time_str,
            }

            # Append to CSV
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(ATTENDANCE_FILE, index=False)

            # Append to TXT log
            with open(TXT_LOG, "a", encoding="utf-8") as f:
                f.write(f"{date_str} {time_str}  |  {scanned_name} (ID: {scanned_id})\n")

            # Success feedback
            st.balloons()
            st.success(f"✅ Attendance marked for {scanned_name} at {time_str}")
    else:
        st.error("❌ Could not detect a QR code in the captured image.")


