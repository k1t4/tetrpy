import curses

from settings import FIELD_HEIGHT, FIELD_WIDTH, NEXTFIELD_HEIGHT, \
    NEXTFIELD_WIDTH


class Window:
    def __init__(self, height=FIELD_HEIGHT, width=FIELD_WIDTH):
        self.height = height
        self.width = width
        self.std_scr, self.next_scr, self.score_scr = self._create_windows()

    def print_std(self, frame):
        frame_str = self.to_ascii_string(frame)
        self.std_scr.addstr(0, 0, frame_str)
        self.std_scr.refresh()

    def print_next(self, frame):
        scoreboard_list = [[0 for _ in range(NEXTFIELD_WIDTH)]
                           for __ in range(NEXTFIELD_HEIGHT)]
        for y in range(len(frame)):
            for x in range(len(frame[0])):
                scoreboard_list[y][x] = frame[y][x]

        frame_str = self.to_ascii_string(scoreboard_list)

        self.next_scr.erase()
        self.next_scr.addstr(0, 0, 'next one')
        self.next_scr.addstr(2, 0, frame_str)
        self.next_scr.refresh()

    def print_score(self, score):
        self.score_scr.erase()
        self.score_scr.addstr(0, 0, 'score:')
        self.score_scr.addstr(2, 0, str(score))
        self.score_scr.refresh()

    def render_string(self, string):
        self.std_scr.addstr(string)

    def render_matrix(self, matrix):
        string = '\n'.join(''.join(line) for line in matrix)
        self.render_string(string)
        self.deactivate()

    def deactivate(self):
        curses.nocbreak()
        self.std_scr.keypad(False)
        curses.echo()
        curses.endwin()

    def get_input(self):
        return self.std_scr.getch()

    @staticmethod
    def _create_windows():
        curses.initscr()
        stdscr = curses.newwin(FIELD_HEIGHT+1, FIELD_WIDTH * 2 + 1)
        nextscreen = curses.newwin(NEXTFIELD_HEIGHT + 3,
                                   NEXTFIELD_WIDTH * 2 + 1,
                                   0,
                                   FIELD_WIDTH * 2 + 3)
        scorescreen = curses.newwin(10, 10,
                                    NEXTFIELD_HEIGHT + 4, FIELD_WIDTH * 2 + 3)
        curses.noecho()
        stdscr.nodelay(True)
        curses.cbreak()
        stdscr.keypad(True)

        return stdscr, nextscreen, scorescreen

    @staticmethod
    def to_ascii_string(frame):
        string = ''
        for row in frame:
            for el in row:
                if el:
                    string += '██'
                else:
                    string += '  '
            string += '\n'
        else:
            for el in row:
                if el:
                    string += '██'
                else:
                    string += '  '

        return string
