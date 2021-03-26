import adafruit_ssd1306
import board
import busio
import sys
from PIL import Image, ImageDraw, ImageFont

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# sys.exit()

image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
draw.rectangle((5, 5, oled.width - 6, oled.height - 6), outline=0, fill=0)

font = ImageFont.load_default()
text = "Hello Andrew!"
(font_width, font_height) = font.getsize(text)
draw.text((oled.width/2 - font_width/2, oled.height/2 - font_height/2), text, font=font, fill=255)

oled.image(image)
oled.show()
