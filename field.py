from matrix import Matrix
import copy

from settings import FIELD_HEIGHT, FIELD_WIDTH
from tetromino import Tetromino


class TouchesEdge(Exception):
    pass


class Field(Matrix):
    """A field on """

    def render(self, tetr: Tetromino) -> list:
        """
        Returns a temporary frame with tetromino placed on a field at given
        coordinates
        """
        result_list = copy.deepcopy(self.list)

        for y in range(tetr.y, tetr.y + tetr.size_y):
            if y >= 0:  # no need to render elements that are out of top border
                for x in range(tetr.x, tetr.x + tetr.size_x):
                    result_list[y][x] = (tetr[y - tetr.y][x - tetr.x]
                                         or self[y][x])

        return result_list

    @staticmethod
    def place_at_top_center_x(tetr: Tetromino) -> None:
        x_center_field = FIELD_WIDTH // 2 + FIELD_WIDTH % 2
        x_center_element = tetr.size_x // 2
        x_center_element_on_field = x_center_field - x_center_element
        tetr.x = x_center_element_on_field
        tetr.y = -tetr.size_y

    def rotate(self, tetr):
        if self._is_able_to_rotate(tetr):
            tetr.rotate()

    def move_right(self, tetr: Tetromino) -> None:
        if self._is_able_to_move_right(tetr):
            tetr.x += 1

    def move_left(self, tetr: Tetromino) -> None:
        if self._is_able_to_move_left(tetr):
            tetr.x -= 1

    @staticmethod
    def move_down(tetr: Tetromino) -> None:
        tetr.y += 1

    def has_landed(self, tetr: Tetromino) -> bool:
        """
        Checks if tetromino has landed (either it is in contact with other one,
        or it has reached the bottom line)
        """
        reached_bottom = tetr.y == FIELD_HEIGHT - tetr.size_y - 1
        touched_edge = self._touched_edge(tetr)
        if reached_bottom or touched_edge:
            print(f'{reached_bottom=}, {touched_edge=}')
            return True

        return False

    def fixate(self, tetr):
        """
        Fixates tetromino on a field
        """
        for y in range(tetr.y, tetr.y + tetr.size_y):
            for x in range(tetr.x, tetr.x + tetr.size_x):
                self.list[y][x] = self[y][x] or tetr[y - tetr.y][x - tetr.x]

    def handle_filled_rows(self):
        """
        Returns number of block that were deleted
        """
        result = self._get_filled_rows()

        with open('/dev/pts/0', 'w') as term:
            term.write(str(result))

        if isinstance(result, tuple):
            first_index, last_index = result
            return self._remove_filled_rows(first_index, last_index)
        elif isinstance(result, int):
            index = result
            return self._remove_filled_rows(index)

        return 0

    @staticmethod
    def out_of_top_border(tetr):
        return tetr.y - tetr.size_y + 1 < 0

    def _get_filled_rows(self):
        """
        Returns None, if not filled, if only one row is filled, returns
        it's index, if more than one is filled, returns first and last indexes
        """
        first_found, last_found = False, False
        first_index, last_index = None, None

        for i in range(self.size_y):
            if not first_found:
                if all(self[i]):
                    first_found = True
                    first_index = i
            else:
                if not all(self[i]):
                    break
                else:
                    last_found = True
                    last_index = i

        if first_found:
            return first_index if not last_found else first_index, last_index
        else:
            return None

    def _remove_filled_rows(self, start, end=None):
        if not end:
            del self.list[start]
            self.list.insert(0, [0] * FIELD_WIDTH)
            return 1
        else:
            for i in range(start, end + 1):
                del self.list[i]
                self.list.insert(0, [0] * FIELD_WIDTH)
            return end - start + 1

    def _is_able_to_move_right(self, tetr: Tetromino) -> bool:
        if self.size_x - (tetr.x + tetr.size_x - 1) - 1 < 1:
            return False

        first_right_block_index = None

        for y in range(tetr.size_y):
            for x in range(tetr.size_x - 1, -1, -1):
                if tetr[y][x] == 1 or tetr[y][x] == 2:
                    first_right_block_index = x
                    break

            if self[tetr.y + y][tetr.x + first_right_block_index + 1] == 1:
                return False

        return True

    def _is_able_to_move_left(self, tetr: Tetromino) -> bool:
        if tetr.x == 0:
            return False

        first_left_block_index = None
        for y in range(tetr.size_y):
            for x in range(tetr.size_x):
                if tetr[y][x] == 1 or tetr[y][x] == 2:
                    first_left_block_index = x
                    break

            if self[tetr.y + y][tetr.x + first_left_block_index - 1] == 1:
                return False

        return True

    def _touched_edge(self, tetr):
        """
        Checks if tetromino is in contact with other tetromino on field
        """
        for y in range(tetr.size_y):
            for x in range(tetr.size_x):
                is_edge_brick = (
                        tetr[y][x] and tetr.safe_get(y+1, x) in (0, None))
                is_edge_brick = is_edge_brick and tetr.y + y >= 0
                is_in_contact = (
                        self.safe_get(tetr.y + y + 1, tetr.x + x) in (1, 2))
                if is_edge_brick and is_in_contact:
                    return True
        return False

    def _is_overlapping_brick(self, tetr):
        for y in range(tetr.size_y):
            for x in range(tetr.size_x):
                if self[tetr.y + y][tetr.x + x] == 1:
                    return True

        return False

    def _out_of_borders(self, tetr):
        out_of_left_corner = tetr.x < 0 or tetr.y < 0
        out_of_right_corner = (tetr.x + tetr.size_x > self.size_x
                               or tetr.y + tetr.size_y > self.size_y)

        return out_of_right_corner or out_of_left_corner

    def _is_able_to_rotate(self, tetr):
        tetr_copy = copy.deepcopy(tetr)
        tetr_copy.rotate()
        # need to check if tetromino conflicts with field's state
        is_able = (not self._out_of_borders(tetr_copy)
                   and not self._is_overlapping_brick(tetr_copy))

        return is_able

