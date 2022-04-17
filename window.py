import curses
import time

from settings import FIELD_HEIGHT, FIELD_WIDTH


class Window:
    def __init__(self, height=FIELD_HEIGHT, width=FIELD_WIDTH):
        self.height = height
        self.width = width
        self.stdscr = self._create_window()

    def print(self, frame):
        frame_str = self.to_ascii_string(frame)
        self.stdscr.addstr(0, 0, frame_str)
        self.stdscr.refresh()

    def render_string(self, string):
        self.stdscr.addstr(string)

    def render_matrix(self, matrix):
        string = '\n'.join(''.join(line) for line in matrix)
        self.render_string(string)
        self.deactivate()

    def deactivate(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def get_input(self):
        return self.stdscr.getch()

    @staticmethod
    def _create_window():
        curses.initscr()
        stdscr = curses.newwin(FIELD_HEIGHT+1, FIELD_WIDTH+1)
        #stdscr.box('o', 'o')
        curses.noecho()
        stdscr.nodelay(True)
        #curses.cbreak()
        stdscr.keypad(True)

        return stdscr

    @staticmethod
    def to_ascii_list(frame):
        ascii_list = []
        for row in frame:
            ascii_list.append([])
            for el in row:
                if el == 2:
                    char = '*'
                elif el == 1:
                    char = '*'
                else:
                    char = ' '
                ascii_list[-1].append(char)

        return ascii_list

    def to_ascii_string(self, frame):
        ascii_matrix = self.to_ascii_list(frame)
        string = ''
        for row_list in ascii_matrix:
            row = ''.join(row_list)
            string += row + '\n'
        else:
            row = ''.join(row_list)
            string += row

        return string
