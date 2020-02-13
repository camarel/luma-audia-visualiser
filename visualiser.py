#!/usr/bin/env python3
#
# Copyright (c) 2020 Claudio Marelli
# See LICENSE.txt for details

import sys
import subprocess
from time import sleep
from threading import Thread

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import show_message
from luma.core.legacy.font import CP437_FONT, SINCLAIR_FONT, LCD_FONT


class Visualizer():
    def __init__(self):
        # create matrix device
        serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(serial, cascaded=4, block_orientation=-90)
        self.device.contrast(2)

        print('initialized device')

    def draw(self, nums):
        with canvas(self.device) as draw:
            for i, num in enumerate(nums):
                num -= 1
                if num >= 0:
                    draw.line((i, 8, i, 8 - num), fill="red")

    def show_song_title(self):
        proc = subprocess.Popen(['mpc', 'current'], stdout=subprocess.PIPE)

        msg = proc.stdout.readline()[:-1].decode('utf-8')
        print(msg)
        if len(msg) == 0:
            msg = 'nothing playing ...'

        print(msg)
        # CP437_FONT, SINCLAIR_FONT, LCD_FONT
        show_message(self.device, msg, fill="white", font=SINCLAIR_FONT)

    def delayed_titles(self, timeout=2):
        while True:
            self.lcd_free = True
            sleep(timeout)
            self.lcd_free = False
            self.show_song_title()

    def handle_stdin(self):
        while True:
            try:
                # read line without last two chars
                line = sys.stdin.readline()[:-2]
                nums = map(int, line.split(';'))

                if self.lcd_free:
                    self.draw(nums)

            except Exception as e:
                print(e)

    def close(self):
        self.device.hide()
        print('closing device')


if __name__ == "__main__":
    visualizer = Visualizer()

    try:
        thread = Thread(target=visualizer.delayed_titles)
        thread.start()

        visualizer.handle_stdin()

    except KeyboardInterrupt:
        pass
        visualizer.close()
