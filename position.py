class Position:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def convert_units(self):
        # returns position of the cell in the cell list
        return self.line * 15 + self.column
