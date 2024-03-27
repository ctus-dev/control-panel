"""Interface for retreiving stats and displaying on an OLED"""

import socket
import time
from pathlib import Path

import adafruit_ssd1306
import board
import psutil as ps
from PIL import Image, ImageDraw, ImageFont

KB = 1024
MB = KB * 1024
GB = MB * 1024

WIDTH = 128
HEIGHT = 64
FONTSIZE = 16

LOOPTIME = 1.0


def get_ipv4_from_interface(interfacename):
    """Returns the IP from a specific interface"""

    try:
        iface = ps.net_if_addrs()[interfacename]
        for addr in iface:
            if addr.family is socket.AddressFamily.AF_INET:
                return f"IP: {addr.address}"
    except Exception:
        return "IP: ???:???:???:???"


# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

padding = -2
top = padding
bottom = oled.height - padding
x = 0

# font = ImageFont.load_default()
font = ImageFont.truetype(
    f"{Path(__file__).parent / 'lib' / 'PixelOperator.ttf'}", FONTSIZE
)

count = 0
while True:
    count += 1
    if 1 <= count <= 5:
        ip = get_ipv4_from_interface("eth0")
    elif 6 <= count <= 9:
        ip = socket.gethostname()
    else:
        count = 0

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    cpu = f"CPU: {ps.cpu_percent():.1f} %"

    temps = ps.sensors_temperatures()
    temp = f"{temps['cpu_thermal'][0].current:.1f} °C"

    mem = ps.virtual_memory()
    mem_usage = f"Mem: {(mem.used+GB-1)/GB:.1f}/ {round((mem.total+GB-1)/GB):.1f} GB"

    root = ps.disk_usage("/")
    disk = f"Disk: {(root.used+GB-1)/GB:.1f}/ {(root.total+GB-1)/GB:.1f} GB"

    draw.text((x, top), ip, font=font, fill=255)
    draw.text((x, top + FONTSIZE), cpu, font=font, fill=255)
    draw.text((x + 80, top + FONTSIZE), temp, font=font, fill=255)
    draw.text((x, top + 2 * FONTSIZE), mem_usage, font=font, fill=255)
    draw.text((x, top + 3 * FONTSIZE), disk, font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)