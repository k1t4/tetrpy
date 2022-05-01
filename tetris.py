import curses.ascii
from datetime import datetime, timedelta

from field import Field
from window import Window
from settings import TICK_TIME, INPUT_GAP
from tetromino import Tetromino


class Tetris:
    def __init__(self):
        self.window = Window()
        self.field = Field()
        self.score = 0

    def drop_tetr(self, tetr):
        self.field.place_at_top_center_x(tetr)
        start_time = datetime.now()
        last_input_time = datetime.now()

        while True:
            if self.field.has_landed(tetr):
                print('i was here')
                self.field.fixate(tetr)
                if self.field.out_of_top_border(tetr):
                    print(f'out of top border')
                    return True
                num_handled_rows = self.field.handle_filled_rows()
                self.score += num_handled_rows
                return False

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

                if key == curses.ascii.ESC:
                    self.start_pause()

            frame = self.field.render(tetr)
            self.window.print_std(frame)

    def start_game(self):
        tetr, next_one = Tetromino(), Tetromino()
        while True:
            self.window.print_next(next_one.list)
            self.window.print_score(self.score)
            is_game_end = self.drop_tetr(tetr)
            if is_game_end:
                self.window.deactivate()
                return
            tetr, next_one = next_one, Tetromino()

    def start_pause(self):
        while True:
            key = self.window.get_input()
            if key != curses.ERR:
                return

    @staticmethod
    def _time_to_tick(start_time):
        return datetime.now() - start_time >= timedelta(seconds=TICK_TIME)

    @staticmethod
    def _time_for_input(last_input_time):
        return last_input_time + timedelta(seconds=INPUT_GAP) <= datetime.now()

    def end_game(self):
        pass
