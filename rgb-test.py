#!/usr/bin/python3

"""
    Program: RGB Test (rgb-test.py)
    Author:  M. Heidenreich, (c) 2024

    Description: This code is provided in support of the following YouTube tutorial:
                    https://www.youtube.com/watch?v=Sf2ow0Ugwcw

    This program will test whether a RGB LED is connected correctly to Raspberry Pi GPIO.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from gpiozero import RGBLED
from time import sleep

my_led = RGBLED(13, 19, 26)  # Common cathode
# my_led = RGBLED(13, 19, 26, active_high=False) # Common anode

my_led.color = (1, 0, 0)
print("Red...")
sleep(2)

my_led.color = (0, 1, 0)
print("Green...")
sleep(2)

my_led.color = (0, 0, 1)
print("Blue...")
sleep(2)

my_led.color = (1, 1, 1)
print("White...")
sleep(2)
