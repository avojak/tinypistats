import adafruit_ssd1306
import atexit
import board
import busio
import datetime
import psutil
import socket
import sys
import time

from gpiozero import CPUTemperature
from PIL import Image, ImageDraw, ImageFont

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64 
I2C_ADDR = 0x3C

IMAGE_MODE = "1" # 1-bit color

MARGIN = 2

def main():
    clear_display()
    main_loop(get_display())

def main_loop(oled):
    while True:
        image = Image.new(IMAGE_MODE, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        draw = ImageDraw.Draw(image)
        
        #draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline=255, fill=255)
        #draw.rectangle((5, 5, DISPLAY_WIDTH - 6, DISPLAY_HEIGHT - 6), outline=0, fill=0)




        font = ImageFont.load_default()
        text = time.strftime('%H:%M:%S', time.localtime())
        (font_width, font_height) = font.getsize(text)
        #draw.text((DISPLAY_WIDTH/2 - font_width/2, DISPLAY_HEIGHT/2 - font_height/2), text, font=font, fill=255)

        draw.text((0, 0), get_ip_address_line(), font=font, fill=255)
        draw.text((0, font_height + MARGIN), get_cpu_line(), font=font, fill=255)
        draw.text((0, font_height*2 + MARGIN*2), get_memory_line(), font=font, fill=255)
        draw.text((0, font_height*3 + MARGIN*3), get_disk_line(), font=font, fill=255)
        draw.text((0, font_height*4 + MARGIN*4), get_uptime_line(), font=font, fill=255)

        oled.image(image)
        oled.show()
        
        time.sleep(1)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def get_ip_address_line():
    return 'IP: {}'.format(get_ip_address())

def get_cpu_line():
    usage = '{}%'.format(psutil.cpu_percent())
    temp = '{:.1f}\xb0F'.format(CPUTemperature().temperature * (9/5) + 32)
    return 'CPU: {0:<6} {1}'.format(usage, temp)

def get_memory_line():
    total_memory = psutil.virtual_memory().total  / 1024 / 1024 / 1024
    used_memory = psutil.virtual_memory().used / 1024 / 1024 / 1024
    return 'Memory: {:.1f}/{:.1f}GB'.format(used_memory, total_memory)

def get_disk_line():
    hdd = psutil.disk_usage('/')
    used = hdd.used / (2**30)
    total = hdd.total / (2**30)
    return 'Disk: {:.1f}/{:.1f}GB'.format(used, total)

def get_uptime_line():
    uptime = time.time() - psutil.boot_time() # Uptime in seconds
    days = uptime / (3600*24)
    rem = uptime % (3600*24)
    hours = rem / 3600
    rem = rem % 3600
    mins = rem / 60
    sec = rem % 60
    return 'Uptime: %03d:%02d:%02d:%02d' % (days, hours, mins, sec)

def get_display():
    return adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, board.I2C(), addr=I2C_ADDR)

def clear_display():
    oled = get_display()
    oled.fill(0)
    oled.show()

@atexit.register
def cleanup():
    clear_display()

if __name__ == "__main__":
    main()
