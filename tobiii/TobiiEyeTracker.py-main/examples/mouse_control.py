import socket
import pyautogui
import screeninfo
import time

# Disable pyautogui's fail-safe and increase speed
pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0

# Initialize socket connection
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 1235))

# Get primary monitor resolution
monitor = screeninfo.get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height
print(f"Screen resolution: {screen_width}x{screen_height}")

# Initialize tracking
last_x = screen_width / 2
last_y = screen_height / 2
smoothing_factor = 0.3  # Increased for stability

def move_cursor(x, y):
    """Move cursor with normalized coordinates (0-1)"""
    try:
        # Convert to screen coordinates
        screen_x = int(x * screen_width)
        screen_y = int(y * screen_height)
        
        # Apply smoothing
        global last_x, last_y
        smooth_x = int((screen_x * smoothing_factor) + (last_x * (1 - smoothing_factor)))
        smooth_y = int((screen_y * smoothing_factor) + (last_y * (1 - smoothing_factor)))
        
        # Ensure within bounds
        smooth_x = max(0, min(smooth_x, screen_width - 1))
        smooth_y = max(0, min(smooth_y, screen_height - 1))
        
        # Move mouse
        pyautogui.moveTo(smooth_x, smooth_y, _pause=False)
        
        # Update last position
        last_x, last_y = smooth_x, smooth_y
        
        # Print status
        print(f"Eye: ({x:.3f}, {y:.3f}) → Screen: ({smooth_x}, {smooth_y})", end='\r')
        
    except Exception as e:
        print(f"\nError moving cursor: {e}")

print("Starting eye tracking... (Press Ctrl+C to exit)")
while True:
    try:
        # Get data from eye tracker
        message, _ = sock.recvfrom(1024)
        data = message.decode('utf-8').split(',')
        
        if len(data) == 3:  # timestamp, x, y
            try:
                x = float(data[1])
                y = float(data[2])
                
                if x >= 0 and y >= 0:  # Valid coordinates
                    move_cursor(x, y)
                    
            except ValueError:
                continue
                
    except KeyboardInterrupt:
        print("\nStopping eye tracking...")
        break
    except Exception as e:
        print(f"\nConnection error: {e}")
        time.sleep(0.1)

sock.close() 