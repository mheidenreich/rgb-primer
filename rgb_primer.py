"""
    Program: RGB Primer (rgb_primer.py)
    Author:  M. Heidenreich, (c) 2024

    Description: This code is provided in support of the following YouTube tutorial:
                    https://www.youtube.com/watch?v=Sf2ow0Ugwcw

    This file is low-level support code for the rgb-sandbox.py program.

    THIS SOFTWARE AND LINKED VIDEO TOTORIAL ARE PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS
    ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
    IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
    OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from gpiozero import RGBLED
import curses


class OptimizedRGBLED(RGBLED):
    def __init__(self, *args, **kwargs):
        super(OptimizedRGBLED, self).__init__(*args, **kwargs)

    @property
    def value(self):
        return super(OptimizedRGBLED, self).value

    @value.setter
    def value(self, value):
        super(OptimizedRGBLED, self.__class__).value.fset(self, value)


class ColourBox:
    def __init__(self, label, colour, display):
        # Constructor for ColourBox
        self.label = label      # Human-readable name such as 'RED'
        self.colour = colour    # curses colour code (integer)
        self.display = display  # reference to a curses display window
        self.value = 0          # 8-bit colour value, 0 to 255
        self.pwm = 0            # PWM duty cycle, 0 to 1
        self.next = self        # Used to link ColourBox objects in sequence
        self.previous = self    # Used to link ColourBox objects in sequence

    def draw_plain_box(self):
        # Draw a plain box
        self.display.bkgd(curses.color_pair(self.colour))
        self.display.border()
        self.display.addstr(0, 1, self.label)
        self.display.refresh()

    def draw_bold_box(self):
        # Draw a bold box - indicates focus
        height, width = self.display.getmaxyx()

        self.display.bkgd(curses.A_BOLD | curses.color_pair(self.colour))

        for column in range(1, width-1):
            self.display.addch(0, column, "\u2550")
            self.display.addch(height-1, column, "\u2550")

        for row in range(1, height-1):
            self.display.addch(row, 0, "\u2551")
            self.display.addch(row, width-1, "\u2551")

        self.display.addch(0, 0, "\u2554")
        self.display.addch(0, width-1, "\u2557")
        self.display.addch(height-1, 0, "\u255A")

        try:
            # Attempt to add a character in the bottom-right corner
            # Always results in an exception thrown
            self.display.addch(height-1, width-1, "\u255D")
        except curses.error:
            pass

        self.display.addstr(0, 1, self.label)
        self.display.refresh()

    def update(self):
        # Update the box with current values
        self.display.addstr(1, 12, f"{self.value: 4d}")
        self.display.addstr(2, 13, f"{self.pwm: >7.5f}")
        self.display.addstr(3, 14, f"{self.pwm*100: >5.1f}")
        self.display.refresh()


class Display:
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    BLUE = curses.COLOR_BLUE

    def __init__(self):
        # Constructor for Display
        self.initialize_curses()

        self.red = ColourBox("RED", self.RED, curses.newwin(5, 22, 1, 1))
        self.green = ColourBox("GREEN", self.GREEN, curses.newwin(5, 22, 1, 23))
        self.blue = ColourBox("BLUE", self.BLUE, curses.newwin(5, 22, 1, 46))

        for box in (self.red, self.green, self.blue):
            box.display.addstr(1, 2, "Value:       0/255")
            box.display.addstr(2, 2, "PWM Duty:  0.00000")
            box.display.addstr(3, 2, "Intensity:    0.0%")
            box.draw_plain_box()

        self.red.draw_bold_box()
        self.active_box = self.red  # RED box is active when program starts

        self.legend = curses.newwin(10, 80, 7, 1)
        self.legend.keypad(True)

        self.legend.addstr(0, 1, "Instructions:", curses.A_BOLD)
        self.legend.addstr(1, 3, "Press 'UP'/'DOWN' arrow keys to change values up and down.")
        self.legend.addstr(2, 3, "Use 'Shift' key to make changes faster.")
        self.legend.addstr(3, 3, "Press 'PgUp'/'PgDn' keys to toggle between 0 and 255.")
        self.legend.addstr(4, 3, "Press 'LEFT'/'RIGHT' arrows to change active colour.")
        self.legend.addstr(5, 3, "Use 'Ctrl' key to make changes to all three colours at once.")
        self.legend.addstr(7, 1, "Press 'Ctrl + c' to exit program...")
        self.legend.refresh()

        # Link all threee display boxes in a closed loop, bi-directional
        self.red.next = self.green
        self.green.next = self.blue
        self.blue.next = self.red

        self.red.previous = self.blue
        self.green.previous = self.red
        self.blue.previous = self.green

    def __iter__(self):
        # Returns a generator providing RGB colour as tuples
        return self.values

    def initialize_curses(self):
        # Initialize curses
        curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.start_color()
        curses.use_default_colors()

        for colour in (self.RED, self.GREEN, self.BLUE):
            curses.init_pair(colour, colour, -1)

    def run(self):
        # Keyboard polling loop
        while True:
            self.handle_key(self.legend.getch())

    def update(self, box, value):
        # Update a box with a new value
        if value == 5 or value == -5:
            value = self.nearest_five(box, value)
        else:
            value += box.value

        self.set_value(box, value)

    def update_all(self, value):
        # Update all boxes with a new value
        for box in (self.red, self.green, self.blue):
            if value == 5 or value == -5:
                self.set_value(box, self.nearest_five(box, value))
            else:
                self.update(box, value)

    def set_all(self, value):
        # Update all boxes with a new value within allowed range
        for box in (self.red, self.green, self.blue):
            self.set_value(box, value)

    def set_value(self, box, value):
        if 0 <= value <= 255:
            box.value = value
            box.pwm = (value / 255)**2
            box.update()

    def nearest_five(self, box, value):
        # Returns nearest multiple of 5 in the direction given
        if value > 0:
            return ((box.value + 5) // 5) * 5
        else:
            return ((box.value - 1) // 5) * 5

    def handle_key(self, key):
        # Callbacks associated with specific keyboard keys
        key_actions = {
            260: lambda: self.change_focus(self.active_box.previous),                               # left
            261: lambda: self.change_focus(self.active_box.next),                                   # right

            259: lambda: self.update(self.active_box, 1),                                           # Up
            258: lambda: self.update(self.active_box, -1),                                          # Down
            337: lambda: self.set_value(self.active_box, self.nearest_five(self.active_box, 5)),       # Shift + Up
            336: lambda: self.set_value(self.active_box, self.nearest_five(self.active_box, -5)),   # Shift + Down
            571: lambda: self.update_all(1),                                                         # Ctrl + Up
            530: lambda: self.update_all(-1),                                                        # Ctrl + Down

            339: lambda: self.set_value(self.active_box, 255),                                      # PgUp
            338: lambda: self.set_value(self.active_box, 0),                                        # PgDn
            560: lambda: self.set_all(255),                                                         # Ctrl + PgUp
            555: lambda: self.set_all(0),                                                           # Ctrl + PgDn

            572: lambda: self.update_all(5),                                                        # Ctrl + Shift + Up
            531: lambda: self.update_all(-5)                                                        # Ctrl + Shift + Down
        }

        # Execute associated function if key is mapped
        action = key_actions.get(key)

        if action:
            action()

    def change_focus(self, new_active_box):
        # Visual box focus change
        self.active_box.draw_plain_box()
        self.active_box = new_active_box
        self.active_box.draw_bold_box()

    @property
    def value(self):
        return (self.red.value, self.green.value, self.blue.value)

    @property
    def values(self):
        # Returns a tuple compatible with gpiozero source
        while True:
            yield (self.red.pwm, self.green.pwm, self.blue.pwm)
