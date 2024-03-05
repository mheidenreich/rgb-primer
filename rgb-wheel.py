#!/usr/bin/python3

"""
    Program: RGB Colour Wheel Demo (rgb-wheel.py)
    Author:  M. Heidenreich, (c) 2024

    Description: This code is provided in support of the following YouTube tutorial:
                    https://www.youtube.com/watch?v=Sf2ow0Ugwcw

    This program demonstrates how to produce a range of colours using a RGB LED with Raspberry Pi and Python.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from gpiozero import RGBLED
from time import sleep
from signal import pause, signal, SIGTERM, SIGHUP

# A selection of RGB colours
bright_colours = {
    "Red": (1.0, 0.0, 0.0),
    "Orange": (1.0, 0.5, 0.0),
    "Yellow": (1.0, 1.0, 0.0),
    "Lime": (0.5, 1.0, 0.0),
    "Green": (0.0, 1.0, 0.0),
    "Teal": (0.0, 1.0, 0.5),
    "Cyan": (0.0, 1.0, 1.0),
    "Azure": (0.0, 0.5, 1.0),
    "Blue": (0.0, 0.0, 1.0),
    "Purple": (0.5, 0.0, 1.0),
    "Magenta": (1.0, 0.0, 1.0),
    "Pink": (1.0, 0.0, 0.5)
}


# Program shutdown handler
def safe_exit(signum, frame):
    exit(0)


def main():
    my_led = RGBLED(13, 19, 26)  # Common cathode
    # my_led = RGBLED(13, 19, 26, active_high=False)  # Common anode

    try:
        for key, colour in bright_colours.items():
            my_led.color = colour
            print(key)
            sleep(2)

    # Suppress Traceback on exit
    except KeyboardInterrupt:
        pass

    # Deactivate LED and return GPIO ports to default
    finally:
        my_led.close()


if __name__ == "__main__":
    # Handle common signals for safe program shutdown
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    main()
