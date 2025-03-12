import network
import socket
import time
import neopixel
import machine
from machine import Pin, I2C
from dht import DHT11
from ssd1306 import SSD1306_I2C

# WiFi Configuration
SSID = "Shaam"
PASSWORD = "hehe4Times"
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)

# Wait for WiFi to connect
while not sta.isconnected():
    time.sleep(1)
    print("Connecting...")

print("Connected! IP Address:", sta.ifconfig()[0])

# NeoPixel LED Setup
np = neopixel.NeoPixel(Pin(48), 1)  # Change Pin if necessary

def set_neopixel(r, g, b):
    """ Set NeoPixel color with RGB values """
    np[0] = (r, g, b)
    np.write()

# OLED Display Setup
i2c = I2C(1, scl=Pin(9), sda=Pin(8))  # Change if necessary
oled = SSD1306_I2C(128, 64, i2c)

def display_text(text):
    """ Display text on the OLED screen """
    oled.fill(0)  # Clear screen
    oled.text(text, 0, 10)
    oled.show()

# Web Page HTML
def web_page():
    """ Generate HTML web page for ESP32 control """
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Control</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; margin: 0; padding: 20px; }
            h2 { color: #333; }
            .container { max-width: 400px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); margin: auto; }
            input, button { margin: 5px; padding: 10px; width: 100%; border: 1px solid #ccc; border-radius: 5px; }
            button { background-color: #28a745; color: white; cursor: pointer; }
            button:hover { background-color: #218838; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>ESP32 Web Control</h2>
            <h3>Set NeoPixel Color</h3>
            <form action="/" method="GET">
                <input type="number" name="r" min="0" max="255" placeholder="Red (0-255)"> 
                <input type="number" name="g" min="0" max="255" placeholder="Green (0-255)"> 
                <input type="number" name="b" min="0" max="255" placeholder="Blue (0-255)">
                <button type="submit">Set Color</button>
            </form>
            <h3>Display Text on OLED</h3>
            <form action="/" method="GET">
                <input type="text" name="msg" placeholder="Enter text">
                <button type="submit">Display</button>
            </form>
        </div>
    </body>
    </html>
    """
    return html

# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Fix EADDRINUSE error
s.bind(('', 80))
s.listen(5)
print("Web server started!")

# Main Server Loop
while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        print("Request:", request)

        # Parse URL Parameters Manually
        if "GET /?" in request:
            params = request.split(" ")[1].split("?")[1].split("&")
            param_dict = {}
            for p in params:
                key_val = p.split("=")
                if len(key_val) == 2:
                    param_dict[key_val[0]] = key_val[1]

            # Handle RGB Input
            if "r" in param_dict and "g" in param_dict and "b" in param_dict:
                try:
                    r = int(param_dict.get("r", 0))
                    g = int(param_dict.get("g", 0))
                    b = int(param_dict.get("b", 0))

                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        set_neopixel(r, g, b)
                except ValueError:
                    print("Invalid RGB values received")

            # Handle OLED Text Input
            if "msg" in param_dict:
                msg = param_dict["msg"]
                print("Displaying on OLED:", msg)  # Debugging
                display_text(msg)

        response = web_page()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + response)
        conn.close()

    except Exception as e:
        print("Server error:", e)
        conn.close()