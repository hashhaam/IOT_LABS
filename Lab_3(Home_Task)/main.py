from machine import Pin, I2C
import dht
import ssd1306
import time
import framebuf

# Initialize I2C for OLED (ESP32: GPIO22=SCL, GPIO21=SDA | ESP8266: GPIO5=SCL, GPIO4=SDA)
i2c = I2C(0, scl=Pin(8), sda=Pin(9))

# Initialize OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize DHT sensor (DHT11 or DHT22 on GPIO4)
dht_sensor = dht.DHT11(Pin(4))

# Define 16x16 Bitmap for Temperature (🌡️)
temp_icon = bytearray([
    0b00000000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00011000, 0b00000000,
    0b00111100, 0b00000000,
    0b00100100, 0b00000000,
    0b00100100, 0b00000000,
    0b00111100, 0b00000000,
    0b00000000, 0b00000000
])

# Define 16x16 Bitmap for Humidity (💧)
humidity_icon = bytearray([
    0b00000000, 0b00000000,
    0b00001000, 0b00000000,
    0b00011100, 0b00000000,
    0b00111110, 0b00000000,
    0b00111110, 0b00000000,
    0b01111111, 0b00000000,
    0b01111111, 0b00000000,
    0b01111111, 0b00000000,
    0b01111111, 0b00000000,
    0b00111110, 0b00000000,
    0b00111110, 0b00000000,
    0b00011100, 0b00000000,
    0b00001000, 0b00000000,
    0b00000000, 0b00000000
])

# Function to display a bitmap
def draw_bitmap(x, y, bitmap):
    fb = framebuf.FrameBuffer(bitmap, 16, 16, framebuf.MONO_HLSB)
    oled.blit(fb, x, y)

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        # Clear display
        oled.fill(0)

        # Draw bitmaps
        draw_bitmap(5, 10, temp_icon)    # Temperature icon at (5,10)
        draw_bitmap(5, 40, humidity_icon) # Humidity icon at (5,40)

        # Display values next to icons
        oled.text("{} C".format(temp), 25, 15)  # Temperature text
        oled.text("{} %".format(hum), 25, 45)   # Humidity text

        oled.show()

        print("Temperature:", temp, "C")
        print("Humidity:", hum, "%")

        time.sleep(2)
    
    except Exception as e:
        print("Error:", e)
        time.sleep(2)