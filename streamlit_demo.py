import streamlit as st
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import pandas as pd
import os

st.title("📸 QR Code Attendance System")

name = st.text_input("Enter your Name")
user_id = st.text_input("Enter your ID")

if st.button("Start QR Scanner"):
    cap = cv2.VideoCapture(0)

    st.write("Press 'q' in the camera window to stop scanning.")

    while True:
        success, frame = cap.read()
        for barcode in decode(frame):
            data = barcode.data.decode("utf-8")
            st.success(f"✅ QR Code Scanned: {data}")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            df = pd.DataFrame([[user_id, name, data, timestamp]],
                              columns=["ID", "Name", "QR", "Time"])
            if not os.path.exists("attendance.csv"):
                df.to_csv("attendance.csv", index=False)
            else:
                df.to_csv("attendance.csv", mode='a', header=False, index=False)

            cap.release()
            break

        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
