import http.client
import logging
import math
import os
import spidev as SPI
import sys
import time
from PIL import Image, ImageDraw, ImageFont

from lib import LCD_1inch28

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level=logging.DEBUG)

class Connector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = http.client.HTTPConnection(host, port, timeout=1);

    def getBoost(self):
        try:
            self.connection.request("GET", "/")
            response = self.connection.getresponse()

            return float(response.read())
        except:
            self.reconnect()

            return 0.0

    def reconnect(self):
        self.connection = http.client.HTTPConnection(self.host, self.port, timeout=1)

connection = Connector('192.168.8.161', 4000)

try:
    # Initialize display
    disp = LCD_1inch28.LCD_1inch28()
    disp.Init()
    disp.clear()

    ValueFont = ImageFont.truetype("./font/vt323.ttf", 92)
    UnitFont = ImageFont.truetype("./font/vt323.ttf", 24)
    InfoFont = ImageFont.truetype("./font/vt323.ttf", 12)

    # Display image
    logging.info("show image")

    min_boost = 0
    max_boost = 2.0
    warn_boost = 1.8

    history = [];

    i = 0
    while True:
        boost = connection.getBoost()

        history = [boost] + history
        if len(history) > 70:
            history = history[:-1]

        logging.info("{:.2f}".format(boost));

        image = Image.new("RGB", (disp.width, disp.height), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        textColor = (255,255,255)
        if boost > warn_boost:
            textColor = (255, 0, 0)

        draw.text((120, 120), "{:.2f}".format(boost), anchor="mm", fill=textColor, font=ValueFont)
        draw.text((120, 158), "BAR", anchor="mm", fill=(150, 150, 150), font=UnitFont)

        start = 135
        end = start + 270 * ((boost - min_boost) / (max_boost - min_boost));
        draw.arc(((0, 0), (239, 239)), start, end, fill=(255, 255, 255), width=20)

        last = None;
        for index, value in  enumerate(history):
            cord = (85 + (len(history) - index), int(210 - 30 * (value / max_boost)));
            if last == None:
                draw.point(cord, fill=(int(255 * (value / max_boost)), 0, 255))
            else:
                draw.line([last, cord], fill=(int(255 * (value / max_boost)), 0, 255))
            last = cord

        draw.line([(85, 180), (85, 210), (155, 210)])

        draw.text((120, 210), "M: {:.2f}".format(max(history)), anchor="ma", fill=(255, 255, 255), font=UnitFont)

        disp.ShowImage(image.rotate(180))

        i += 1

    # Shut down display
    disp.module_exit()
except IOError as e:
    logging.info(e)
    exit()
except KeyboardInterrupt:
    disp.module_exit()
    exit()
