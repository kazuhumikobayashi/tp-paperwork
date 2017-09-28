class Point:
    CODE_POINT_A = ord('A')

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.cell_name = '{0}{1}'.format(self.col_to_string(), row)

    def col_to_string(self):
        offsets = []
        x = self.col
        while x > 0:
            s = x % 26
            x = x // 26
            if s == 0:
                s = 26
                x = x - 1
            s = s - 1
            offsets.insert(0, s)

        s = ''
        for offset in offsets:
            code_point = self.CODE_POINT_A + offset
            chars = chr(code_point)
            s += chars
        return s

    def get_cell_name(self):
        return self.cell_name
