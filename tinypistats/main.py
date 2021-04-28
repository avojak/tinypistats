import adafruit_ssd1306
import argparse
import atexit
import board
import busio
import datetime
import logging
import os
import psutil
import signal
import socket
import sys
import time

from gpiozero import CPUTemperature
from PIL import Image, ImageDraw, ImageFont

PIDFILE = '/tmp/.tinypistats.pid'

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64 
I2C_ADDR = 0x3C

IMAGE_MODE = "1" # 1-bit color

MARGIN = 2

class TinyPiStatsService():

    log = logging.getLogger('tinypistats')
    log.setLevel(os.environ.get('LOGLEVEL', 'INFO'))

    def start(self):
        self._write_pidfile()
        self._clear_display()
        oled = self._get_display()
        while True:
            image = Image.new(IMAGE_MODE, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            draw = ImageDraw.Draw(image)

            font = ImageFont.load_default()
            text = time.strftime('%H:%M:%S', time.localtime())
            (font_width, font_height) = font.getsize(text)

            draw.text((0, 0), self._get_ip_address_line(), font=font, fill=255)
            draw.text((0, font_height + MARGIN), self._get_cpu_line(), font=font, fill=255)
            draw.text((0, font_height*2 + MARGIN*2), self._get_memory_line(), font=font, fill=255)
            draw.text((0, font_height*3 + MARGIN*3), self._get_disk_line(), font=font, fill=255)
            draw.text((0, font_height*4 + MARGIN*4), self._get_uptime_line(), font=font, fill=255)

            oled.image(image)
            oled.show()
        
            time.sleep(1)

    def stop(self):
        pid = int(self._read_pidfile())
        self.log.info('Killing PID = {}'.format(pid))
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            self.log.error('No process found for PID = {}'.format(pid))
            sys.exit(1)
        self._delete_pidfile()
        self._clear_display()

    def _write_pidfile(self):
        pid = str(os.getpid())
        self.log.info('New PID = {}'.format(pid))
        with open(PIDFILE, 'w') as pidfile:
            pidfile.write(pid)

    def _read_pidfile(self):
        with open(PIDFILE, 'r') as pidfile:
            return pidfile.read().replace('\n', '')

    def _delete_pidfile(self):
        try:
            os.unlink(PIDFILE)
        except FileNotFoundError:
            self.log.error('{} not found'.format(PIDFILE))
            sys.exit(1)

    def _get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def _get_ip_address_line(self):
        return 'IP: {}'.format(self._get_ip_address())

    def _get_cpu_line(self):
        usage = '{}%'.format(psutil.cpu_percent())
        temp = '{:.1f}\xb0F'.format(CPUTemperature().temperature * (9/5) + 32)
        return 'CPU: {0:<6} {1}'.format(usage, temp)

    def _get_memory_line(self):
        total_memory = psutil.virtual_memory().total  / 1024 / 1024 / 1024
        used_memory = psutil.virtual_memory().used / 1024 / 1024 / 1024
        return 'Memory: {:.1f}/{:.1f}GB'.format(used_memory, total_memory)

    def _get_disk_line(self):
        hdd = psutil.disk_usage('/')
        used = hdd.used / (2**30)
        total = hdd.total / (2**30)
        return 'Disk: {:.1f}/{:.1f}GB'.format(used, total)

    def _get_uptime_line(self):
        uptime = time.time() - psutil.boot_time() # Uptime in seconds
        days = uptime / (3600*24)
        rem = uptime % (3600*24)
        hours = rem / 3600
        rem = rem % 3600
        mins = rem / 60
        sec = rem % 60
        return 'Uptime: %03d:%02d:%02d:%02d' % (days, hours, mins, sec)

    def _get_display(self):
        return adafruit_ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, board.I2C(), addr=I2C_ADDR)

    def _clear_display(self):
        oled = self._get_display()
        oled.fill(0)
        oled.show()


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('command', choices=['start', 'stop'])
    args = parser.parse_args()

    service = TinyPiStatsService()

    if args.command == 'start':
        service.start()
    elif args.command == 'stop':
        service.stop()
    else:
        sys.exit('Unknown command: {}'.format(args.command))

#@atexit.register
#def cleanup():
#    clear_display()
#    delete_pidfile()

if __name__ == "__main__":
    main()
