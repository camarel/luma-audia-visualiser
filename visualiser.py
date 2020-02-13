#!/usr/bin/env python3
#
# Copyright (c) 2020 Claudio Marelli
# See LICENSE.txt for details

import sys

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas


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
                    draw.line((i, 0, i, num), fill="red")

    def handle_stdin(self):
        while True:
            try:
                # read line without last two chars
                line = sys.stdin.readline()[:-2]
                nums = map(int, line.split(';'))
                self.draw(nums)

            except Exception as e:
                print(e)

    def close(self):
        self.device.hide()
        print('closing device')


if __name__ == "__main__":
    visualizer = Visualizer()

    try:
        visualizer.handle_stdin()

    except KeyboardInterrupt:
        pass
        visualizer.close()
