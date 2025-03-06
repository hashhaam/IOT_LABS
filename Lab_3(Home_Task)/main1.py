from machine import Pin, I2C
import dht
import ssd1306
import time
import framebuf

# Initialize I2C for OLED
i2c = I2C(0, scl=Pin(8), sda=Pin(9))

# Initialize OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize DHT sensor (DHT11 on GPIO4)
dht_sensor = dht.DHT11(Pin(4))

# Define a flag for updating the display
update_display = True

# Initialize button (GPIO12) for interrupt
button = Pin(0, Pin.IN, Pin.PULL_UP)

# Define 16x16 Bitmaps
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

# Interrupt handler for button press
def button_pressed(pin):
    global update_display
    update_display = True  # Set flag to update the display

# Attach interrupt to button (trigger on falling edge)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Main loop
while True:
    if update_display:
        try:
            dht_sensor.measure()
            temp = dht_sensor.temperature()
            hum = dht_sensor.humidity()

            # Clear display
            oled.fill(0)

            # Draw bitmaps
            draw_bitmap(5, 10, temp_icon)    # Temperature icon
            draw_bitmap(5, 40, humidity_icon) # Humidity icon

            # Display values next to icons
            oled.text("{} C".format(temp), 25, 15)  # Temperature text
            oled.text("{} %".format(hum), 25, 45)   # Humidity text

            oled.show()

            print("Temperature:", temp, "C")
            print("Humidity:", hum, "%")

            # Reset update flag after updating the display
            update_display = False

        except Exception as e:
            print("Error:", e)

    time.sleep(0.1)  # Small delay to avoid CPU overuse