# luma-audia-visualiser

Audio spectrum visualizer for a 32 x 8 LED matrix (MAX7219). In my
case it is used on a Raspberry Pi with mpc as an internet radio player.

The music is played via mpc Music Player Daemon, that also outputs the
music to cava. Cava then calculates the audio spectrum and exports it
via standard input to the python script.

## Installation

Install the display driver for MAX7219, instructions see:
https://luma-led-matrix.readthedocs.io/en/latest/install.html

Thanks to:
* [cava](https://github.com/karlstav/cava)
* [Luma.LED_Matrix](https://github.com/rm-hull/luma.led_matrix)
* [Soundlights](https://github.com/nvbn/soundlights)
