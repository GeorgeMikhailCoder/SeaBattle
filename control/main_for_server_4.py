import os
from random import randrange
from random import choice
from optimal_placement import main as ship_placement_jenny
from ship_extraction import ship_placement_oleg
from client import ServerConnection
from PaintPrimitives import Cell, FieldPart
from Ship import Ship

class Field(object):
    '''
        Поле игры состоит из трех частей: карта где расставлены корабли игрока,
        радар на котором игрок отмечает свои ходы и результаты,
        поле с весом клеток, которое используется для ходов ИИ
    '''

    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.radar = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]
        self.weight = [[1 for _ in range(size)] for _ in range(size)]

    def get_field_part(self, element):
        if element == FieldPart.main:
            return self.map
        if element == FieldPart.radar:
            return self.radar
        if element == FieldPart.weight:
            return self.weight

    def draw_field(self, element):
        '''
            Метод для отрисовки различных полей
        '''

        field = self.get_field_part(element)
        weights = self.get_max_weight_cells()

        if element == FieldPart.weight:
            for x in range(self.size):
                for y in range(self.size):
                    if (x, y) in weights:
                        print('\033[1;32m', end='')
                    if field[x][y] < self.size:
                        print(" ", end='')
                    if field[x][y] == 0:
                        print(str("" + ". " + ""), end='')
                    else:
                        print(str("" + str(field[x][y]) + " "), end='')
                    print('\033[0;0m', end='')
                print()

        else:
            # Всё что было выше - рисование веса для отладки, его можно не использовать в конечной игре.
            # Само поле рисуется всего лишь вот так:
            for x in range(-1, self.size):
                for y in range(-1, self.size):
                    if x == -1 and y == -1:
                        print("  ", end="")
                        continue
                    if x == -1 and y >= 0:
                        print(y + 1, end=" ")
                        continue
                    if x >= 0 and y == -1:
                        print(Game.letters[x], end='')
                        continue
                    print(" " + str(field[x][y]), end='')
                print("")
        print("")


    def check_ship_fits(self, ship, element):
        '''
            Функция проверяет помещается ли корабль на конкретную позицию конкретного поля.
            будем использовать при расстановке кораблей, а так же при вычислении веса клеток
            возвращает False если не помещается и True если корабль помещается
        '''

        field = self.get_field_part(element)

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or \
                ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False

        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Cell.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):

                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False

        return True

    def mark_destroyed_ship(self, ship, element):
        '''
            Когда корабль уничтожен необходимо пометить все клетки вокруг него с промахами (Cell.miss_cell),
            а все клетки корабля - уничтожеными (Cell.destroyed_ship)
        '''

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                field[p_x][p_y] = Cell.miss_cell

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = Cell.destroyed_ship

    def add_ship_to_field(self, ship, element):
        '''
            добавление корабля: пробегаемся от позиции х у корабля по его высоте и ширине и помечаем на поле эти клетки
            element - определяем, к какой части поля мы обращаемся: основная, радар или вес
        '''

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                # заметьте в клетку мы записываем ссылку на корабль.
                # таким образом обращаясь к клетке мы всегда можем получить текущее HP корабля
                field[p_x][p_y] = ship

    def get_max_weight_cells(self):
        '''
            метод возвращает координаты с самым большим коэффициентом шанса попадания
        '''
        weights = {}
        max_weight = 0
        # добавляем наиболее "тяжелые" клетки
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))

        return weights[max_weight]

    # пересчет веса клеток
    def recalculate_weight_map(self, available_ships):
        # Расчет весов для совершения выстрела ИИ-игроком
        self.weight = [[1 for _ in range(self.size)] for _ in range(self.size)]
        # Если находим раненый корабль - ставим крестом клетки с увеличенными весами
        # А диагоналям от раненой клетки вписываем нули
        for x in range(self.size):
            for y in range(self.size):
                if self.radar[x][y] == Cell.damaged_ship:

                    self.weight[x][y] = 0

                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x - 1][y + 1] = 0

                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= 50
                    if y + 1 < self.size:
                        self.weight[x][y + 1] *= 50

                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x + 1][y + 1] = 0

        # Перебираем все корабли оставшиеся у противника.
        for i in range(0, len(available_ships)):
            ship_size = available_ships[i]
            ship = Ship(ship_size, 1, 1, 0)

            for x in range(self.size):
                for y in range(self.size):
                    if self.radar[x][y] in (Cell.destroyed_ship, Cell.damaged_ship, Cell.miss_cell) \
                            or self.weight[x][y] == 0:
                        self.weight[x][y] = 0
                        continue
                    # вращаем корабль и проверяем помещается ли он
                    for rotation in range(0, 4):
                        ship.set_position(x, y, rotation)
                        if self.check_ship_fits(ship, FieldPart.radar):
                            self.weight[x][y] += 1

class Game(object):
    letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
    ships_rules = {'1': 4,'2': 3,'3': 3, '4': 2, '5': 2, '6': 2, '7': 1, '8': 1, '9': 1, '10': 1}
    field_size = len(letters)

    def __init__(self):
        self.message = []
        self.current_player = None

    def add_player(self, player):
        # при добавлении игрока создаем для него поле
        player.field = Field(Game.field_size)
        player.enemy_ships = list(Game.ships_rules.values())
        self.ships_setup(player)
        # высчитываем вес для клеток поля (это нужно только для ИИ, но в целом при расширении возможностей
        # игры можно будет например на основе этого давать подсказки игроку).
        player.field.recalculate_weight_map(player.enemy_ships)
        # добавлено для одного игрока в одной программе
        self.current_player = player

    def ships_setup(self, player):

        # делаем расстановку кораблей в количестве, указанном в правилах класса Game
        for i in Game.ships_rules:
            retry_count = 50
            ship_size = Game.ships_rules[i]

            while True:

                Game.clear_screen()
                if player.auto_ship_setup is False:
                    player.field.draw_field(FieldPart.main)
                    player.message.append(f'Введите левую верхнюю координату и ориентацию (H - горизонтально или V - вертикально) для корабля №{i} длиной {ship_size} ')
                    for _ in player.message:
                        print(_)

                player.message.clear()

                if player.auto_ship_setup is False:
                    # создаем предварительно экземпляр класса Ship
                    ship = Ship(ship_size, 0, 0, 0)
                    x, y, r = player.get_input('ship_setup')
                else:
                    stage_calc = ship_placement_jenny()
                    all_ship_list = ship_placement_oleg(stage_calc)
                    ii = int(i) - 1
                    x, y, r, ssi = all_ship_list[ii]
                    ship = Ship(ssi, 0, 0, 0)
                # если пользователь ввёл неправильные координаты функция возвратит нули
                if x + y + r < 0:
                    continue

                ship.set_position(x, y, r)

                # если корабль помещается на заданной позиции, то добавляем игроку на поле корабль
                # также добавляем корабль в список кораблей игрока и переходим к следующему кораблю для расстановки
                if player.field.check_ship_fits(ship, FieldPart.main):
                    player.field.add_ship_to_field(ship, FieldPart.main)
                    player.ships.append(ship)
                    break

                # сюда мы добираемся только если корабль не поместился. пишем юзеру что позиция неправильная
                # и отнимаем попытку на расстановку
                player.message.append('Неправильная позиция!')
                retry_count -= 1
                if retry_count < 0:
                    # после заданного количества неудачных попыток - обнуляем карту игрока
                    player.field.map = [[Cell.empty_cell for _ in range(Game.field_size)] for _ in
                                        range(Game.field_size)]
                    player.ships = []
                    self.ships_setup(player)
                    return True

    def draw(self):
        if True:
            self.current_player.field.draw_field(FieldPart.main)
            self.current_player.field.draw_field(FieldPart.radar)

            # для отображения весовой матрицы ИИ-противника раскомментировать
            #self.current_player.field.draw_field(FieldPart.weight)
        for line in self.current_player.message:
            print(line)


    @staticmethod
    #очистка терминала
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')


class Player(object):

    def __init__(self, name, is_ai, skill, auto_ship):
        self.name = name
        self.is_ai = is_ai
        self.auto_ship_setup = auto_ship
        self.skill = skill
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.field = None

    # Или расстановка кораблей или совершение выстрела
    def get_input(self, input_type):

        if input_type == "ship_setup":

            if self.is_ai or self.auto_ship_setup:
                user_input = str(choice(Game.letters)) + str(randrange(0, self.field.size)) + choice(["H", "V"])
            else:
                user_input = input().upper().replace(" ", "")

            if len(user_input) < 3:
                return 0, 0, 0

            x, y, r = user_input[0], user_input[1:-1], user_input[-1]

            if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1) or \
                    r not in ("H", "V"):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return 0, 0, 0

            return Game.letters.index(x), int(y) - 1, 0 if r == 'H' else 1

        if input_type == "shot":

            if self.is_ai:
                if self.skill == 1:
                    x, y = choice(self.field.get_max_weight_cells())
                if self.skill == 0:
                    x, y = randrange(0, self.field.size), randrange(0, self.field.size)
            else:
                user_input = input().upper().replace(" ", "")
                x, y = user_input[0].upper(), user_input[1:]
                if x not in Game.letters or not y.isdigit() or int(y) not in range(1, Game.field_size + 1):
                    self.message.append('Приказ непонятен, ошибка формата данных')
                    return 500, 0
                x = Game.letters.index(x)
                y = int(y) - 1
            return x, y

    # при совершении выстрела мы будем запрашивать ввод данных с типом shot
    def make_shot(self):
        mistake_counter = 0
        n = 50
        sx, sy = self.get_input('shot')
        while sx == 500 and sy == 0:
            mistake_counter += 1
            print(f'Ошибка ввода, осталось {n-mistake_counter} попыток')
            sx, sy = self.get_input('shot')
        return sx, sy

    def receive_remote(self, shot_res, rec_ship, sx, sy):
        '''
            мы убиваем удаленный корабль
        '''
        if shot_res == 'miss':
            self.field.radar[sx][sy] = Cell.miss_cell

        if shot_res == 'get':
            self.field.radar[sx][sy] = Cell.damaged_ship

        if shot_res == 'kill':
            destroyed_ship = rec_ship
            self.field.mark_destroyed_ship(destroyed_ship, FieldPart.radar)
            self.enemy_ships.remove(destroyed_ship.size)

        # после совершения выстрела пересчитаем карту весов
        self.field.recalculate_weight_map(self.enemy_ships)

        return shot_res

    # сервер убивает наш корабль
    def receive_local(self, shot):

        sx, sy = shot

        if type(self.field.map[sx][sy]) == Ship:
            ship = self.field.map[sx][sy]
            ship.hp -= 1

            if ship.hp <= 0:
                self.field.mark_destroyed_ship(ship, FieldPart.main)
                self.ships.remove(ship)
                return 'kill', ship

            self.field.map[sx][sy] = Cell.damaged_ship
            return 'get', ship

        else:
            self.field.map[sx][sy] = Cell.miss_cell
            return 'miss', None

def init_input():

    print("Hello there! \n Please enter your name")
    user_name = input()
    print("Please type yes or no to play as AI")
    while True:
        pl_type = input().replace(" ", '')
        if pl_type == 'yes':
            pl_type = True
            break
        elif pl_type == 'no':
            pl_type = False
            break
        else:
            print("Wrong argument, try again")

    if pl_type is False:
        print("Please enter yes or no to play with automatic ship placement \n")
        while True:
            sh_pl = input().replace(" ", '')
            if sh_pl == 'yes':
                sh_pl = True
                break
            elif sh_pl == 'no':
                sh_pl = False
                break
            else:
                print("Invalid argument, try again")
    else:
        sh_pl = True

    if pl_type is True:
        print("Please enter skill level of AI, 0 or 1, 1 is stronger")
        while True:
            sk_l = input().replace(" ", '')
            try:
                sk_l = int(sk_l)
            except:
                print("Invalid argument, try again")
                continue
            if sk_l == 1 or sk_l == 0:
                break
            else:
                print("Invalid argument, try again")
    else:
        sk_l = 1

    return user_name, pl_type, sh_pl, sk_l




if __name__ == '__main__':

    user_name1, pl_type1, sh_pl1, sk_l1 = init_input()

    # последовательная инициализация всех объектов
    player1 = Player(name=user_name1, is_ai=pl_type1, auto_ship=sh_pl1, skill=sk_l1)
    game = Game()
    game.add_player(player1)
    server = ServerConnection()
    server.want()

    globStatus_active = server.begin()
    end_flag = False

    while True:
        Game.clear_screen()
        game.draw()
        game.current_player.message.clear()
        # очищаем список сообщений для игрока. В следующий ход он уже получит новый список сообщений
        # ждём результата выстрела на основе выстрела текущего игрока в следующего

        if globStatus_active:
            #game.current_player.message.append("Ожидание приказа: ")
            print("Ожидание приказа: ")
            x, y = game.current_player.make_shot()
            #game.current_player.message.append(f"Огонь по {game.letters[x]}{y+1} ")
            print(f"Огонь по {game.letters[x]}{y + 1} ")
            server.shot(x,y)
            ans_from_serv, assum_ship, end_flag = server.wait_ans()
            shot_result = game.current_player.receive_remote(ans_from_serv, assum_ship, x, y)

            if end_flag is True:
                print(f'Вы, {game.current_player.name}, выиграли матч!')
                break


        # в зависимости от результата накидываем сообщений и текущему игроку и следующему
        # ну и если промазал - передаем ход следующему игроку.
            if shot_result == 'miss':
                globStatus_active = False
                continue
            elif shot_result == 'retry':
                game.current_player.message.append('Попробуйте еще раз')
                continue
            elif shot_result == 'get':
                game.current_player.message.append('Попадание в корабль противника')
                continue
            elif shot_result == 'kill':
                game.current_player.message.append('Корабль противника уничтожен!')
                continue

        if not globStatus_active:
            # ждем на вход координаты удара противника, обрабатываем и отрисовываем их
            xx, yy = server.wait_shot()
            xx = int(xx)
            yy = int(yy)
            send_str, giv_ship = game.current_player.receive_local((xx,yy))
            server.make_ans(send_str, giv_ship, (len(game.current_player.ships) == 0))
            if send_str == 'miss':
                globStatus_active = True
                continue

        # проверяем игру на окончание по флагу и количеству кораблей противника и своих
        if (len(game.current_player.ships) == 0) or end_flag or (len(game.current_player.enemy_ships) == 0):
            Game.clear_screen()
            game.current_player.field.draw_field(FieldPart.main)
            if end_flag == 1 or len(game.current_player.enemy_ships) == 0:
                print(f'Вы, {user_name1} выиграли матч! Поздравления!')
            else:
                print(f'Сожалеем, {game.current_player.name}, но Вы проиграли!')
            break

    print('Спасибо за игру!')
    exit()
