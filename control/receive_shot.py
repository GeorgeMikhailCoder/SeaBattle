class Color:
    yellow2 = '\033[1;35m'
    reset = '\033[0m'
    blue = '\033[0;34m'
    yellow = '\033[1;93m'
    red = '\033[1;93m'
    miss = '\033[0;35m'


# функция которая окрашивает текст в заданный цвет.
def set_color(text, color):
    return color + text + Color.reset

class Cell(object):
    empty_cell = set_color(' ', Color.yellow2)
    ship_cell = set_color('■', Color.blue)
    destroyed_ship = set_color('X', Color.yellow)
    damaged_ship = set_color('□', Color.red)
    miss_cell = set_color('•', Color.miss)
def receive_shot(self, shot):
    sx, sy = shot

    if type(self.field.map[sx][sy]) == Ship:
        ship = self.field.map[sx][sy]
        ship.hp -= 1

        if ship.hp <= 0:
            self.field.mark_destroyed_ship(ship, FieldPart.main)
            self.ships.remove(ship)
            return ship

        self.field.map[sx][sy] = Cell.damaged_ship
        return 'get'

    else:
        self.field.map[sx][sy] = Cell.miss_cell
        return 'miss'