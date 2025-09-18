# 🌲 Forest Fire – Tobii Eye-Tracking Game

A Unity-based game where you **move a rain cloud using only your eyes** to save trees from a raging forest fire.  
Powered by the [Tobii Eye Tracker](https://developer.tobii.com/).

---

## 🎯 Game Goal
Guide the rain cloud across a burning forest using **eye gaze control** and extinguish as many fires as possible.  
Your **score** equals the **number of trees saved**.

---

## 🕹️ How to Play
1. **Set Up the Eye Tracker**
   - Connect your Tobii Eye Tracker to the PC.
   - Run the Tobii calibration tool to adjust for your eyes and lighting.

2. **Start the Gaze Tracking Script**
   - Download the `tobii_eye_tracking.py` (main file) from this repository.
   - Run it locally:
     ```bash
     python tobii_eye_tracking.py
     ```
   - This script streams your gaze data to the game.

3. **Launch the Game**
   - Run the provided **EXE build** (`ForestFire.exe`).

4. **Control the Cloud**
   - Simply look where you want the **rain cloud** to move.
   - The cloud follows your gaze in real time and rains to put out fires.

5. **Scoring**
   - Each tree saved earns you **1 point**.
   - Save as many trees as possible before the timer runs out!

---

## 🛠️ Requirements
- **Hardware:** Tobii Eye Tracker 4C / Tobii Eye Tracker 5 (or compatible)
- **Software:**
  - Python 3.8+ (for `tobii_eye_tracking.py`)
  - Tobii Eye Tracker drivers & calibration software
  - Windows 10/11

---

## 🔧 Developer Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/forest-fire-tobii.git
