#!/usr/bin/python3

"""
    Program: RGB Sandbox (rgb-sandbox.py)
    Author:  M. Heidenreich, (c) 2024

    Description: This code is provided in support of the following YouTube tutorial:
                    https://www.youtube.com/watch?v=Sf2ow0Ugwcw

    This program is a tool to experiment with RGB LED using Raspberry Pi.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from rgb_primer import OptimizedRGBLED, ColourBox, Display
from signal import signal, SIGTERM, SIGHUP
import curses
from gpiozero import RGBLED


def safe_exit(signum, frame):
    exit(1)


def main(stdscr):
    my_led = RGBLED(13, 19, 26)  # Common cathode
    # my_led = RGBLED(13, 19, 26, active_high=False)  # Common anode

    screen = Display()
    my_led.source = screen

    try:
        screen.run()

    # Suppress Traceback on exit
    except KeyboardInterrupt:
        pass

    # Deactivate LED and return GPIO ports to default
    finally:
        my_led.source = None
        my_led.close()


if __name__ == "__main__":
    # Handle common signals for safe program shutdown
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    # Use main program with curses safely
    curses.wrapper(main)
