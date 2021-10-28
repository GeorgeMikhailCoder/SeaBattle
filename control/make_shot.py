'''class Color:
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
    '''

from .main import Player

p = Player()

p.make_shot()

def make_shot(self, target_player):
    sx, sy = self.get_input('shot')

    if sx + sy == 500 or self.field.radar[sx][sy] != Cell.empty_cell:
        return 'retry'
    # результат выстрела это то что целевой игрок ответит на наш ход
    # промазал, попал или убил (в случае убил возвращается корабль)
    shot_res = target_player.receive_shot((sx, sy))

    if shot_res == 'miss':
        self.field.radar[sx][sy] = Cell.miss_cell

    if shot_res == 'get':
        self.field.radar[sx][sy] = Cell.damaged_ship

    if type(shot_res) == Ship:
        destroyed_ship = shot_res
        self.field.mark_destroyed_ship(destroyed_ship, FieldPart.radar)
        self.enemy_ships.remove(destroyed_ship.size)
        shot_res = 'kill'

    # после совершения выстрела пересчитаем карту весов
    self.field.recalculate_weight_map(self.enemy_ships)

    return shot_res