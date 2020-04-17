def right(position):
    x, y = position
    return x + 1, y


class Hero:
    def __init__(self):
        self.position = (0, 0)

    def move(self, direction):
        self.position = direction(self.position)
