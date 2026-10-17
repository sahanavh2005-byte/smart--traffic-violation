from flask import Flask, render_template, Response, jsonify
import cv2
import os
import datetime

app = Flask(__name__)

# Config
STOP_LINE_Y = 400
violation_count = 0
fgbg = cv2.createBackgroundSubtractorMOG2()
os.makedirs("violations", exist_ok=True)

def detect_violation():
    global violation_count
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ROI & Background Subtraction
        fgmask = fgbg.apply(frame)
        _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1500: # Vehicle filter
                x,y,w,h = cv2.boundingRect(cnt)
                if y+h > STOP_LINE_Y: # Crossed stop line
                    # Draw
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
                    # Save proof
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    cv2.imwrite(f"violations/violation_{timestamp}.jpg", frame)
                    violation_count += 1
        
        # Draw stop line
        cv2.line(frame, (0, STOP_LINE_Y), (frame.shape[1], STOP_LINE_Y), (0,255,0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_violation(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/count')
def count():
    return jsonify({"violations": violation_count})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
