import curses
from datetime import datetime, timedelta

from field import Field
from window import Window
from settings import TICK_TIME, INPUT_GAP
from tetromino import Tetromino


class Tetris:
    def __init__(self):
        self.window = Window()
        self.field = Field()

    def drop_tetr(self, tetr):
        self.field.place_at_top_center_x(tetr)
        start_time = datetime.now()
        last_input_time = datetime.now()

        while True:
            if self.field.has_landed(tetr):
                self.field.fixate(tetr)
                num_rows_removed = self.field.handle_filled_rows()
                with open('/dev/pts/0', 'w') as term:
                    term.write(str(num_rows_removed))
                return

            if self._time_to_tick(start_time):
                start_time = datetime.now()
                self.field.move_down(tetr)

            key = self.window.get_input()

            if self._time_for_input(last_input_time):
                if key in (curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_LEFT):
                    last_input_time = datetime.now()

                if key == curses.KEY_RIGHT:
                    self.field.move_right(tetr)

                if key == curses.KEY_LEFT:
                    self.field.move_left(tetr)

                if key == curses.KEY_UP:
                    self.field.rotate(tetr)

                if key == curses.KEY_DOWN:
                    self.field.move_down(tetr)

            frame = self.field.render(tetr)
            self.window.print(frame)

    def start_game(self):
        while True:
            tetr = Tetromino()
            self.drop_tetr(tetr)

    @staticmethod
    def _time_to_tick(start_time):
        return datetime.now() - start_time >= timedelta(seconds=TICK_TIME)

    @staticmethod
    def _time_for_input(last_input_time):
        return last_input_time + timedelta(seconds=INPUT_GAP) <= datetime.now()

    def end_game(self):
        pass
