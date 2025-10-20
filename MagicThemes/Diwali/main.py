# MicroPython Base Code for Pico WH Magic Robots
# Released under the GNU GPL v3.0 October 2025

# Aditya Rao, IIT Madras
# 23f3000019@es.study.iitm.ac.in

# MagicThemes for the robot's mobile control panel
# Launched on Diwali, Laxmi Pooja, 2025
# This is the base code using web sockets released on 20th October 2025.
# This HTML serving section is modified to use Gzip compression (index.html.gz).

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
    strafe_right()
    time.sleep(0.8)
    move_stop()
    move_backward()
    time.sleep(0.8)
    move_stop()
    strafe_left()
    time.sleep(0.8)
    move_stop()
    
    move_forward()
    time.sleep(0.8)
    move_stop()
    strafe_right()
    time.sleep(0.8)
    move_stop()
    move_backward()
    time.sleep(0.8)
    move_stop()
    strafe_left()
    time.sleep(0.8)
    move_stop()


# Ensure motors are stopped at boot
move_stop()

# --- WEB SERVER AND FILE LOADING LOGIC ---

def load_webpage_content():
    try:
        
        with open('magic.ar', 'rb') as f:
            print("Serving magic: magic.ar")
            
            return f.read(), True 
    except OSError:
        try:
            
            with open('alt.ar', 'r') as f:
                print("Serving other: alt.ar")
                # Return content encoded as bytes, and flag as uncompressed
                return f.read().encode('utf-8'), False
        except OSError:
            # 3. If both fail, send an error (critical failure)
            print("CRITICAL ERROR: magic.ar or alt.ar not found!")
            return b"<h1>CRITICAL ERROR: magic.ar or alt.ar not found!</h1>", False

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
    raise RuntimeError('\n\nCould not connect to the **Magic Robot** Wi-Fi\n(Connection details are "magic" / "iitmadras")\n')
else:
    ip_address = wlan.ifconfig()[0]
    print(f'\n\nConnected to the **Magic Robot** WiFi\n\nUse this IP address: {ip_address} in your mobile browser\n')

# Setup web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(addr)
s.listen(1)
print('Listening on', addr)

state = "OFF"
random_value = 0

# Read the HTML content (compressed or uncompressed) once at startup
HTML_CONTENT, IS_GZIPPED = load_webpage_content()


# --- MAIN SERVER LOOP ---
while True:
    try:
        # Wait for a client connection
        conn, addr = s.accept()
        # conn.settimeout(3.0) # Optional: Set a timeout for recv
        print('Got a connection from mobile/laptop: ', addr)

        # Receive and process the HTTP request
        request = conn.recv(1024)
        request_str = str(request)

        try:
            # Extract the path (e.g., '/forward', '/stop')
            path = request_str.split(' ')[1]
        except IndexError:
            path = '/'

        # Simplistic check if the client supports Gzip compression
        client_accepts_gzip = b'Accept-Encoding: gzip' in request

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
            random_value = random.randint(10, 20)
            state = f'Random Value: {random_value}'
        
        # Determine the HTTP Header based on compression availability and client support
        if IS_GZIPPED and client_accepts_gzip:
            # Send compressed file with the Content-Encoding header
            header = 'HTTP/1.0 200 OK\r\nContent-Encoding: gzip\r\nContent-type: text/html\r\n\r\n'
            response_content = HTML_CONTENT
        else:
            # Send uncompressed content (or fallback/error content)
            header = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
            response_content = HTML_CONTENT
        
        # Send header and content
        conn.send(header.encode('utf-8'))
        conn.send(response_content) 
        conn.close()

    except OSError as e:
        # Catch common connection errors (e.g., client disconnecting)
        print(f"Error: {e}. Closing connection.")
        try:
            conn.close()
        except NameError:
            pass
        time.sleep(0.1)