#!/usr/bin/python3

"""
    Program: RGB Pulse Demo (rgb-pulse.py)
    Author:  M. Heidenreich, (c) 2024

    Description: This code is provided in support of the following YouTube tutorial:
                    https://www.youtube.com/watch?v=Sf2ow0Ugwcw

    This program demonstrates how to gradually fade in and out a range of colours
    using a RGB LED with Raspberry Pi and Python.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from gpiozero import RGBLED
from time import sleep
from signal import pause, signal, SIGTERM, SIGHUP
from random import choice

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
        active = True
        while (active):
            name, value = choice(list(bright_colours.items()))
            print(name)

            my_led.pulse(fade_in_time=5, fade_out_time=0,
                         off_color=(0, 0, 0), on_color=value,  n=1, background=False)

            my_led.pulse(fade_in_time=0, fade_out_time=5,
                         off_color=(0, 0, 0), on_color=value,  n=1, background=False)

    # Suppress Traceback on exit
    except KeyboardInterrupt:
        pass

    # Deactivate LED and return GPIO ports to default
    finally:
        active = False
        my_led.close()


if __name__ == "__main__":
    # Handle common signals for safe program shutdown
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    main()
