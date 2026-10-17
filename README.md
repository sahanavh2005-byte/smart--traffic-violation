# 🚦 Smart Traffic Violation System - AI Traffic Cop
### Bangalore Hackathon 2026 | Team: Circuit Breakers

> AI-based automatic signal jump detection using Computer Vision. Saves proof automatically and counts e-challans. Built for Bangalore Smart City.

### 🎯 Problem
Bangalore has 1.2+ Crore vehicles but violations caught manually.
- 50,000+ signal jumps daily, no proof
- Traffic police risk life
- Commercial systems cost Rs. 2 Lakhs per signal

### ✅ Our Solution
Low-cost (< Rs.5000) AI system:
1. Detects vehicles crossing STOP LINE during RED signal
2. Auto saves photographic evidence with timestamp
3. Maintains violation count for e-challan
4. Runs at 30 FPS real-time

### 🏗️ How It Works
Webcam -> ROI -> MOG2 Background Subtraction -> Contour Detection -> Area Filter -> Check y2 > STOP_LINE -> RED/GREEN Logic -> Save Proof

### 💻 Tech Stack
- Python 3.11
- OpenCV 5.0 (MOG2)
- Flask Backend
- HTML/CSS/JS Frontend (Police Control Room Dashboard)

### 🚀 How to Run
```bash
pip install opencv-python Flask
python app.py
# Open http://localhost:5000
python final.py # standalone version
