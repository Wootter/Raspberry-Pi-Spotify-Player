import time
import board
import busio
import gpiozero
import os

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

# Use gpiozero to control the reset pin
oled_reset_pin = gpiozero.OutputDevice(4, active_high=False)  # GPIO 4 for reset, active low

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use I2C for communication
i2c = board.I2C()

# Manually reset the display (high -> low -> high for reset pulse)
oled_reset_pin.on()
time.sleep(0.1)  # Delay for a brief moment
oled_reset_pin.off()  # Toggle reset pin low
time.sleep(0.1)  # Wait for reset
oled_reset_pin.on()  # Turn reset pin back high

# Create the OLED display object
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Set display rotation
rotation = int(os.environ.get("OLED_ROTATION", "1"))
if rotation == 2:
    try:
        oled.rotate(2)  # 180 degrees
    except AttributeError:
        oled.rotation = 2

# Clear the display
oled.fill(0)
oled.show()

# Create a blank image for drawing
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PixelOperator.ttf")
try:
    font = ImageFont.truetype(font_path, 16)
except OSError:
    font = ImageFont.load_default()

# Static MP3 player UI example
draw.rectangle((0, 0, oled.width - 1, oled.height - 1), outline=0, fill=255)

# Album artwork placeholder
draw.rectangle((4, 6, 43, 45), outline=0, fill=0)
draw.rectangle((10, 12, 37, 39), outline=255, width=1)
draw.ellipse((17, 19, 30, 32), outline=255, width=2)
draw.line((12, 37, 36, 14), fill=255, width=2)

# Track information
draw.text((48, 7), "NOW PLAYING", font=font, fill=0)
draw.text((48, 24), "Midnight", font=font, fill=0)
draw.text((48, 39), "The Night Owls", font=font, fill=0)

# Progress bar and playback controls
draw.text((4, 48), "1:24", font=font, fill=0)
draw.line((31, 55, 96, 55), fill=0, width=2)
draw.ellipse((61, 52, 67, 58), outline=0, fill=0)
draw.text((103, 48), "3:42", font=font, fill=0)
draw.polygon((43, 63, 43, 56, 38, 59), fill=0)
draw.polygon((78, 56, 78, 63, 84, 59), fill=0)

# Display the image
oled.image(image)
oled.show()

# Wait for the next loop
time.sleep(LOOPTIME)