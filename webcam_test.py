import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Webcam not detected.")
else:
    print("✅ Webcam is working.")

cap.release()
