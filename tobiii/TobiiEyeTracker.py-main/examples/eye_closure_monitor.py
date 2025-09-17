import socket
import winsound
import time
from datetime import datetime
import threading

# Constants
UDP_IP = "127.0.0.1"
UDP_PORT = 1235
TRACKING_TIMEOUT = 1.0  # seconds before considering tracking lost
BEEP_FREQUENCY = 1000  # Hz
BEEP_DURATION = 200    # milliseconds for tracking beep (shorter for less annoyance)
LOST_BEEP_DURATION = 500  # milliseconds for lost tracking alert
MIN_BEEP_INTERVAL = 1.0  # minimum seconds between tracking beeps

class EyeTrackingMonitor:
    def __init__(self):
        # Initialize socket connection
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))
        
        # Tracking state
        self.last_tracking_time = time.time()
        self.last_beep_time = 0
        self.is_tracking = True
        self.last_alert = 0
        
        # Start monitoring thread
        self.running = True
        self.monitor_thread = threading.Thread(target=self._check_tracking)
        self.monitor_thread.start()

    def _play_tracking_beep(self):
        current_time = time.time()
        if current_time - self.last_beep_time >= MIN_BEEP_INTERVAL:
            winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)
            self.last_beep_time = current_time

    def _play_lost_alert(self):
        current_time = time.time()
        if current_time - self.last_alert >= LOST_BEEP_DURATION/1000:
            winsound.Beep(BEEP_FREQUENCY, LOST_BEEP_DURATION)
            self.last_alert = current_time
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Alert: Eye tracking lost!")

    def _check_tracking(self):
        while self.running:
            current_time = time.time()
            time_since_last_track = current_time - self.last_tracking_time
            
            if time_since_last_track > TRACKING_TIMEOUT:
                if self.is_tracking:
                    self.is_tracking = False
                self._play_lost_alert()
            else:
                if not self.is_tracking:
                    print("\nTracking restored!")
                    self.is_tracking = True
            
            time.sleep(0.1)

    def run(self):
        print("Starting eye tracking monitoring... (Press Ctrl+C to exit)")
        print(f"Will alert if tracking is lost for more than {TRACKING_TIMEOUT} seconds")
        
        while True:
            try:
                # Get data from eye tracker
                message, _ = self.sock.recvfrom(1024)
                data = message.decode('utf-8').split(',')
                
                if len(data) == 3:  # timestamp, x, y
                    try:
                        x = float(data[1])
                        y = float(data[2])
                        
                        if x >= 0 and y >= 0:  # Valid coordinates
                            self.last_tracking_time = time.time()
                            print(f"Eye position: ({x:.3f}, {y:.3f}) Status: {'TRACKING' if self.is_tracking else 'LOST'}", end='\r')
                            # Play tracking beep when valid data is received
                            self._play_tracking_beep()
                            
                    except ValueError:
                        continue
                    
            except KeyboardInterrupt:
                print("\nStopping eye tracking...")
                break
            except Exception as e:
                print(f"\nConnection error: {e}")
                time.sleep(0.1)

        # Cleanup
        self.running = False
        self.monitor_thread.join()
        self.sock.close()

if __name__ == "__main__":
    monitor = EyeTrackingMonitor()
    monitor.run() 