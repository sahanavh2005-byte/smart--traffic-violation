import cv2
import os
import datetime

# --- SETTINGS ---
STOP_LINE_Y = 400
VEHICLE_MIN_AREA = 1500

# Setup
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
os.makedirs("violations", exist_ok=True)
cap = cv2.VideoCapture(0) # 0 for webcam, or put video path "traffic.mp4"

violation_count = 0
print("AI Traffic Cop Started - Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Background Subtraction
    fgmask = fgbg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # 2. Find Contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > VEHICLE_MIN_AREA:
            x,y,w,h = cv2.boundingRect(cnt)
            # Check if crossed stop line
            if y+h > STOP_LINE_Y:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
                cv2.putText(frame, "VIOLATION!", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                
                # Save proof
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                cv2.imwrite(f"violations/violation_{timestamp}.jpg", frame)
                violation_count += 1
                print(f"Violation #{violation_count} saved!")
    
    # Draw STOP line
    cv2.line(frame, (0, STOP_LINE_Y), (frame.shape[1], STOP_LINE_Y), (0,255,0), 3)
    cv2.putText(frame, f"Violations: {violation_count}", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
    
    cv2.imshow("AI Traffic Cop - Bangalore Smart City", frame)
    cv2.imshow("Mask", thresh)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
