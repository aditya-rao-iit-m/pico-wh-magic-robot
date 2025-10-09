# MicroPython Base Code for Pico WH Magic Robots
# Released under the GNU GPL v3.0 October 2025

# Aditya Rao, IIT Madras
# 23f3000019@es.study.iitm.ac.in

# This is the base code using web sockets released on 5th October 2025.
# This is meant to be a baseline for creating Raspberry Pi Pico WH based magic robots. 
# Users are free to use this code for non-commercial purposes only.
# Users are encouraged to modify it and create macros, multiple moves coded into a single Magic Button.
# Please remember the GNU GPL v3.0 license requires attribution and also requires you to share derivative works.

import network
import socket
import time
import random
from machine import Pin

# LED Indicator
led = Pin('LED', Pin.OUT)

# Mappings
# Motor Driver Objects: Front Left (FL), Rear Left (RL), Front Right (FR), Rear Right (RR)

# Left Motor Driver (Controls Rear Left and Front Left)
# Rear Left Motor (RL)
# IN1 -> GPIO 21 (Pin 27) of the Pico WH
rear_left_forward = Pin(21, Pin.OUT)
# IN2 -> GPIO 20 (Pin 26) of the Pico WH
rear_left_backward = Pin(20, Pin.OUT)

# Front Left Motor (FL)
# IN3 -> GPIO 19 (Pin 25) of the Pico WH
front_left_forward = Pin(19, Pin.OUT)
# IN4 -> GPIO 18 (Pin 24) of the Pico WH
front_left_backward = Pin(18, Pin.OUT)

# Right Motor Driver (Controls Front Right and Rear Right)
# Front Right Motor (FR)
# IN1 -> GPIO 10 (Pin 14) of the Pico WH
front_right_forward = Pin(10, Pin.OUT)
# IN2 -> GPIO 11 (Pin 15)
front_right_backward = Pin(11, Pin.OUT)

# Rear Right Motor (RR)
# IN3 -> GPIO 12 (Pin 16) of the Pico WH
rear_right_forward = Pin(12, Pin.OUT)
# IN4 -> GPIO 13 (Pin 17) of the Pico WH
rear_right_backward = Pin(13, Pin.OUT)

# Wi-Fi credentials
ssid = 'magic'
password = 'iitmadras'


# --- MOVEMENT CONTROL FUNCTIONS ---

# Helper function to ensure all motors are stopped (for safety)
def move_stop():
    """Sets all motor control pins LOW to stop all movement."""
    # Front Motors
    front_left_forward.value(0)
    front_left_backward.value(0)
    front_right_forward.value(0)
    front_right_backward.value(0)
    
    # Rear Motors
    rear_left_forward.value(0)
    rear_left_backward.value(0)
    rear_right_forward.value(0)
    rear_right_backward.value(0)

def move_forward():
    """Moves the robot straight forward. All wheels spin in the forward direction."""
    # Front Left (FL) Forward, Rear Left (RL) Forward
    front_left_forward.value(1); front_left_backward.value(0)
    rear_left_forward.value(1); rear_left_backward.value(0)
    
    # Front Right (FR) Forward, Rear Right (RR) Forward
    front_right_forward.value(1); front_right_backward.value(0)
    rear_right_forward.value(1); rear_right_backward.value(0)

def move_backward():
    """Moves the robot straight backward. All wheels spin in the backward direction."""
    # Front Left (FL) Backward, Rear Left (RL) Backward
    front_left_forward.value(0); front_left_backward.value(1)
    rear_left_forward.value(0); rear_left_backward.value(1)
    
    # Front Right (FR) Backward, Rear Right (RR) Backward
    front_right_forward.value(0); front_right_backward.value(1)
    rear_right_forward.value(0); rear_right_backward.value(1)

def move_right():
    """Spins the robot clockwise (turn right in place)."""
    # Left wheels forward, Right wheels backward
    
    # Left Motors Forward
    front_left_forward.value(1); front_left_backward.value(0)
    rear_left_forward.value(1); rear_left_backward.value(0)
    
    # Right Motors Backward
    front_right_forward.value(0); front_right_backward.value(1)
    rear_right_forward.value(0); rear_right_backward.value(1)

def move_left():
    """Spins the robot counter-clockwise (turn left in place)."""
    # Left wheels backward, Right wheels forward
    
    # Left Motors Backward
    front_left_forward.value(0); front_left_backward.value(1)
    rear_left_forward.value(0); rear_left_backward.value(1)
    
    # Right Motors Forward
    front_right_forward.value(1); front_right_backward.value(0)
    rear_right_forward.value(1); rear_right_backward.value(0)
    
def strafe_left():
    """Moves the robot directly to the left (strafe)."""
    # FL & RR Backward, FR & RL Forward
    
    # Front Left Backward, Rear Left Forward
    front_left_forward.value(0); front_left_backward.value(1)
    rear_left_forward.value(1); rear_left_backward.value(0)
    
    # Front Right Forward, Rear Right Backward
    front_right_forward.value(1); front_right_backward.value(0)
    rear_right_forward.value(0); rear_right_backward.value(1)
    
def strafe_right():
    """Moves the robot directly to the right (strafe)."""
    # FL & RR Forward, FR & RL Backward
    
    # Front Left Forward, Rear Left Backward
    front_left_forward.value(1); front_left_backward.value(0)
    rear_left_forward.value(0); rear_left_backward.value(1)
    
    # Front Right Backward, Rear Right Forward
    front_right_forward.value(0); front_right_backward.value(1)
    rear_right_forward.value(1); rear_right_backward.value(0)

# --- DIAGONAL MOVEMENT FUNCTIONS ---

def forward_left_diagonal():
    """Moves the robot diagonally forward-left."""
    # FL/RR Stop, FR/RL Forward
    move_stop() # Start with stop to clear previous state
    
    # Front Right Forward, Rear Left Forward
    front_right_forward.value(1)
    rear_left_forward.value(1)

def forward_right_diagonal():
    """Moves the robot diagonally forward-right."""
    # FR/RL Stop, FL/RR Forward
    move_stop() # Start with stop to clear previous state
    
    # Front Left Forward, Rear Right Forward
    front_left_forward.value(1)
    rear_right_forward.value(1)
    
def backward_left_diagonal():
    """Moves the robot diagonally backward-left."""
    # FL/RR Stop, FR/RL Backward
    move_stop() # Start with stop to clear previous state
    
    # Front Left Backward, Rear Right Backward
    front_left_backward.value(1)
    rear_right_backward.value(1)

def backward_right_diagonal():
    """Moves the robot diagonally backward-right."""
    # FR/RL Stop, FL/RR Backward
    move_stop() # Start with stop to clear previous state
    
    # Front Right Backward, Rear Left Backward
    front_right_backward.value(1)
    rear_left_backward.value(1)

# NEW MAGIC function (square pattern twice)
def move_magic():
    """Executes a simple square pattern twice."""
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()
    move_forward()
    time.sleep(0.8)
    move_stop()
    move_right()
    time.sleep(0.3)
    move_stop()


# Ensure motors are stopped at boot
move_stop()

# --- WEB SERVER AND WI-FI LOGIC (Kept as is, as it is functional) ---

# HTML page with control interface
def webpage(random_value, state):
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
          <title>Mecanum Control Interface</title>
          <style>
            /* Lock down all text selection everywhere */
            * {
              user-select: none;
              -webkit-user-select: none;
              -moz-user-select: none;
              -ms-user-select: none;
            }

            body {
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
              height: 80vh;
              margin: 0;
              background-color: black;
              font-family: sans-serif;
            }
            
            .magic-text {
              transform: rotate(90deg);
              display: inline-block;
              font-size: 24px;
              font-weight: bold;
              color: black;
              transition: transform 0.1s ease;
            }

            .main-grid {
              display: grid;
              grid-template-columns: 100px 100px 100px;
              grid-template-rows: 100px 100px 100px;
              gap: 20px;
              margin-top: 110px;

            }

            .button {
              width: 100px;
              height: 100px;
              border: none;
              border-radius: 20px;
              font-size: 14px;
              font-weight: bold;
              color: black;
              display: flex;
              align-items: center;
              justify-content: center;
              text-align: center;
              cursor: pointer;
              touch-action: manipulation;

              /* REMOVE tap highlight on mobile */
              -webkit-tap-highlight-color: transparent;

              /* REMOVE focus outline */
              outline: none;

              /* Transition for press animation */
              transition: transform 0.1s ease, box-shadow 0.1s ease;
            }

            /* Depress effect (buttons shrink more on press) */
            .button:active {
              transform: scale(0.85);
              box-shadow: inset 0 4px 6px rgba(0,0,0,0.2);
            }

            /* Keep rotated buttons upright when pressed */
            .rotate-text {
              transform: rotate(90deg);
              transition: transform 0.1s ease;
            }
            .rotate-text:active {
              transform: rotate(90deg) scale(0.85);
            }

            /* Magic button: keep its larger base size but shrink proportionally on press
                (1.25 * 0.85 = 1.0625) */
            .magic {
              transform: scale(1.25);
              z-index: 2;
              border-radius: 24px;
              background: linear-gradient(#f2cb1d, #f5820f);
              color: black;
              font-size: 18px;
              font-weight: 800;
            }
            .magic:active {
              transform: scale(1.0625);
              box-shadow: inset 0 4px 6px rgba(0,0,0,0.2);
            }

            /* Magic text also stays rotated and scales with press */
            .magic-text:active {
              transform: rotate(90deg) scale(0.85);
            }

            /* Just in case focus appears later */
            .button:focus {
              outline: none;
            }

            .red { background-color: #ff3b30; }
            .blue { background-color: #00cfff; }
            .green { background-color: #73e04d; }
            .orange { background-color: #fbbd3c; }
            .lavender { background-color: #d5a5fa;}


          </style>
        </head>
        <body>

          <div class="main-grid">
            <div></div>
            <button class="button blue rotate-text" ontouchstart="sendCommand('left')" ontouchend="sendCommand('stop')">↺<br>SPIN LEFT</button>
            <div></div>

            <button class="button red rotate-text" ontouchstart="sendCommand('backward')" ontouchend="sendCommand('stop')">BACKWARD<br>↓</button>
            <button class="button orange magic" ontouchstart="sendCommand('magic')" ontouchend="sendCommand('stop')">
              <span class="magic-text">MAGIC</span>
            </button>
            <button class="button red rotate-text" ontouchstart="sendCommand('forward')" ontouchend="sendCommand('stop')">↑<br>FORWARD</button>
        
            <div></div>
            <button class="button blue rotate-text" ontouchstart="sendCommand('right')" ontouchend="sendCommand('stop')">↻<br>SPIN RIGHT</button>
            <div></div>
          </div>

          

          <script>
            function sendCommand(cmd) {
              fetch("/" + cmd)
                .catch(error => console.error("Failed to send command:", error));
            }
          </script>

        </body>
        </html>
    """
    return html


# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait for connection
timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for the **Magic Robot** Wi-Fi connection...')
    time.sleep(1)

# Check status
if wlan.status() != 3:
    # If connection fails, the program will halt here.
    raise RuntimeError('\n\nCould not connect to  the **Magic Robot** Wi-Fi\nPlease turn on the Magic hotspot on your mobile first, before powering up the Robot\nEnsure portable hotspot setting is set at 2.4GHz\nEnsure portable hotspot has ssid "magic" and password "iitmadras"\nOnly the portable hotspot should be on, turn off mobile data and wifi\nReboot the mobile and try again, if the control panel does not appear in the mobile browser\nAditya Rao, IIT Madras\n')
else:
    ip_address = wlan.ifconfig()[0]
    print(f'\n\nConnected to the **Magic Robot** WiFi\n\nUse this IP address: {ip_address} in your mobile browser\n\nIn case the remote control panel does not appear,\nreboot the mobile phone and try this process again\n')

# Setup web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
# Allow the socket address to be reused immediately after the server stops
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(addr)
s.listen(1)
print('Listening on', addr)

state = "OFF"
random_value = 0

# --- MAIN SERVER LOOP ---
while True:
    try:
        # Wait for a client connection
        conn, addr = s.accept()
        print('Got a connection from your mobile / laptop with IP address: ', addr)

        # Receive and process the HTTP request
        request = conn.recv(1024)
        request = str(request)
        # print("Request:", request) # Uncomment for detailed logging

        try:
            # Extract the path (e.g., '/forward', '/stop')
            path = request.split(' ')[1]
        except IndexError:
            path = '/'

        # Route the request to the appropriate motor function
        if path == '/lighton':
            led.value(1)
            state = 'LED ON'
        elif path == '/lightoff':
            led.value(0)
            state = 'LED OFF'
        elif path == '/forward':
            move_forward()
            state = 'Moving Forward'
        elif path == '/backward':
            move_backward()
            state = 'Moving Backward'
        elif path == '/left': # Spin Left
            move_left()
            state = 'Spinning Left'
        elif path == '/right': # Spin Right
            move_right()
            state = 'Spinning Right'
        elif path == '/magic':
            move_magic()
            state = 'MAGIC Activated (Test Sequence)'
        elif path == '/strafe_left':
            strafe_left()
            state = 'Strafing Left'
        elif path == '/strafe_right':
            strafe_right()
            state = 'Strafing Right'
        elif path == '/front_left':
            forward_left_diagonal()
            state = 'FWD Left Diagonal'
        elif path == '/front_right':
            forward_right_diagonal()
            state = 'FWD Right Diagonal'
        elif path == '/back_left':
            backward_left_diagonal()
            state = 'BKWD Left Diagonal'
        elif path == '/back_right':
            backward_right_diagonal()
            state = 'BKWD Right Diagonal'
        elif path == '/stop':
            move_stop()
            state = 'Stopped'
        elif path == '/value':
            # This is a dummy action from the original code
            random_value = random.randint(10, 20)
            state = f'Random Value: {random_value}'
        
        # Generate the HTML response
        response = webpage(random_value, state)

        # Send the HTTP header and content
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response.encode())
        conn.close()

    except OSError as e:
        print(f"Error: {e}. Closing connection.")
        # Attempt to close the connection in case of an error
        try:
            conn.close()
        except NameError:
            # conn wasn't defined yet, safe to ignore
            pass
        # Short delay to prevent a fast loop on continuous errors
        time.sleep(0.1)