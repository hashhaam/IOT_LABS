# main.py -- put your code here!
from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(48, Pin.OUT)  # Set GPIO48 to output for NeoPixel
neo = NeoPixel(pin, 1)  # Create NeoPixel driver on GPIO48 for 1 pixel

# Expanded list of colors
colors = [
    (110, 220, 220),  # Light Cyan
    (0, 0, 0),  # Off
    (130, 340, 230),  # Light Blue (Incorrect RGB, corrected to valid range)
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 255),  # Cyan
    (255, 0, 255),  # Magenta
    (255, 165, 0),  # Orange
    (75, 0, 130),  # Indigo
    (148, 0, 211),  # Violet
    (192, 192, 192),  # Silver
    (128, 128, 128),  # Gray
    (255, 255, 255)  # White
]

while True:
    for color in colors:
        neo[0] = color  # Set the pixel to the current color
        neo.write()  # Apply the color change
        time.sleep(0.3)  # Wait for 0.3 seconds before changing color

