
class FieldPart(object):
    main = 'map'
    radar = 'radar'
    weight = 'weight'


# здесь просто задаем цвета. Они не соответствуют своим названиям, но главное всё сгруппировано в одном месте
# при желании цвета можно легко поменять не колупаясь во всей логике приложения
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


# класс "клетка". Здесь мы задаем и визуальное отображение клеток и их цвет.
# по визуальному отображению мы проверяем какого типа клетка. Уж такая реализация.
# По этой причине нельзя обозначать одним символом два разных типа. Иначе в логике возникнет путаница.

class Cell(object):
    empty_cell = set_color(' ', Color.yellow2)
    ship_cell = set_color('■', Color.blue)
    destroyed_ship = set_color('X', Color.yellow)
    damaged_ship = set_color('□', Color.red)
    miss_cell = set_color('•', Color.miss)