from settings import FIELD_HEIGHT, FIELD_WIDTH


class Matrix:
    def __init__(self, list_=None, x_len=FIELD_WIDTH, y_len=FIELD_HEIGHT):
        if not list_:
            list_ = self._create_zero_list(x_len, y_len)
        self.list = list_

    def __getitem__(self, i):
        return self.list[i]

    def __len__(self):
        return len(self.list)

    @staticmethod
    def _create_zero_list(x_len, y_len):
        result_list = [[0 for _ in range(x_len)] for __ in range(y_len)]
        return result_list

    @property
    def size_x(self):
        return len(self[0])

    @property
    def size_y(self):
        return len(self)

    @property
    def size(self):
        return self.size_y, self.size_x

    def __str__(self):
        ret_string = ''
        for row in self.list:
            ret_string += str(row) + '\n'
        return ret_string

    def safe_get(self, y, x):
        try:
            return self[y][x]
        except IndexError:
            return None
