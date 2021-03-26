import adafruit_ssd1306
import atexit
import board
import busio
import sys
import time

from PIL import Image, ImageDraw, ImageFont

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64 
I2C_ADDR = 0x3C

IMAGE_MODE = "1" # 1-bit color

def main():
    clear_display()
    main_loop(get_display())

def main_loop(oled):
    while True:
        image = Image.new(IMAGE_MODE, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        draw = ImageDraw.Draw(image)
        
        draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), outline=255, fill=255)
        draw.rectangle((5, 5, DISPLAY_WIDTH - 6, DISPLAY_HEIGHT - 6), outline=0, fill=0)

        font = ImageFont.load_default()
        text = time.strftime('%H:%M:%S', time.localtime())
        (font_width, font_height) = font.getsize(text)
        draw.text((DISPLAY_WIDTH/2 - font_width/2, DISPLAY_HEIGHT/2 - font_height/2), text, font=font, fill=255)

        oled.image(image)
        oled.show()

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
