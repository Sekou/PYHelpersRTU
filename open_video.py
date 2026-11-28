import cv2

video_path = "2018_youbot_top_view.avi"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Calculate delay in milliseconds to match the video's original FPS
fps = cap.get(cv2.CAP_PROP_FPS)
delay = int(1000 / fps) if fps > 0 else 30

while True:
    ret, frame = cap.read()

    # If the video reaches the end, reset to the first frame
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    cv2.imshow("Looped AVI Video", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(delay) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

#2026 S. Diane
# Запрос ИИ: how to program py cv2 loop avi video
# pip install opencv-python --break-system-packages
