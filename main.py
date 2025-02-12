import random, pygame, os, datetime


# Класс карты
class map_level:
    def __init__(self, level_number):
        global size_map
        self.size = size_map
        self.have_portal = False
        self.hw = ['T', 'H']
        self.rm = ['E', 'G', 'R']
        self.all_room = ['E', 'G', 'R', 'S', 'F']
        self.ln = level_number
        self.board = [['#'] * self.size for _ in range(self.size)]
        self.board[(self.size // 2)][(self.size // 2)] = 'S'
        self.coord = [(self.size // 2), (self.size // 2)]
        self.count_rm_G = 0
        self.orint = ['N', 'E', 'S', 'W']
        check = True

        # Генератор карты
        while self.count_rm_G != self.ln + 1:
            for i in range(self.size):
                for o in range(self.size):
                    if self.board[o][i] in self.all_room:
                        self.coord = [o, i]
                        self.start_room = self.board[self.coord[0]][self.coord[1]]
                        self.all_coord = [list(self.coord)]
                        self.rooms = [self.start_room, 'H', random.choice(self.rm)]
                        if self.start_room != 'E' and self.rooms[2] == 'G':
                            self.rooms[1] = 'T'

                        orn = random.choice(self.orint)  # Направление коридора

                        # Создание коридора
                        if orn == 'N' and self.coord[0] != 0:
                            if self.board[self.coord[0] - 1][self.coord[1]] == '#':
                                self.coord[0] -= 1
                            else:
                                orn = random.choice(['E', 'S', 'W'])


                        elif orn == 'E' and self.coord[1] != self.size - 1:
                            if self.board[self.coord[0]][self.coord[1] + 1] == '#':
                                self.coord[1] += 1
                            else:
                                orn = random.choice(['S', 'W'])

                        elif orn == 'S' and self.coord[0] != self.size - 1:
                            if self.board[self.coord[0] + 1][self.coord[1]] == '#':
                                self.coord[0] += 1
                            else:
                                orn = 'W'
                        elif orn == 'W' and self.coord[1] != 0:
                            if self.board[self.coord[0]][self.coord[1] - 1] == '#':
                                self.coord[1] -= 1
                        else:

                            continue
                        self.all_coord.append(list(self.coord))

                        # Создание комнаты
                        orn = random.choice(self.orint)
                        if orn == 'N' and self.coord[0] != 0 and self.board[self.coord[0] - 1][self.coord[1]] == '#':
                            self.coord[0] -= 1
                        elif orn == 'E' and self.coord[1] != self.size - 1 and self.board[self.coord[0]][
                            self.coord[1] + 1] == '#':
                            self.coord[1] += 1
                        elif orn == 'S' and self.coord[0] != self.size - 1 and self.board[self.coord[0] + 1][
                            self.coord[1]] == '#':
                            self.coord[0] += 1
                        elif orn == 'W' and self.coord[1] != 0 and self.board[self.coord[0] - 1][self.coord[1]] == '#':
                            self.coord[1] -= 1
                        self.all_coord.append(list(self.coord))

                        for a in range(self.all_coord[2][0] - 1, self.all_coord[2][0] + 2):
                            for b in range(self.all_coord[2][1] - 1, self.all_coord[2][1] + 2):
                                if self.board[a][b] in self.all_room:
                                    check = False

                        if check:

                            self.board[self.all_coord[1][0]][self.all_coord[1][1]] = self.rooms[1]
                            self.board[self.all_coord[2][0]][self.all_coord[2][1]] = self.rooms[2]

                            if self.rooms[2] == 'G':
                                self.count_rm_G += 1
                        check = True

                        if self.count_rm_G == self.ln + 1:
                            break
                check = True
                if self.count_rm_G == self.ln + 1:
                    break


# Класс для отрисовки карты
class map_draw:
    def __init__(self, size, map):
        self.size = size
        self.map_board = map.board
        self.crd = [size // 2, size // 2]

        self.left = 925
        self.top = 25
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.board = []
        for o in self.map_board[self.crd[0] - 2:self.crd[0] + 3]:
            self.board.append(o[self.crd[1] - 2:self.crd[1] + 3])
        self.screen = screen
        b = self.top
        for i in range(6):
            a = self.left
            for o in range(6):

                pygame.draw.rect(self.screen, (255, 255, 255),
                                 [a, b, self.cell_size, self.cell_size])
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 [a + 1, b + 1, self.cell_size - 2,
                                  self.cell_size - 2])

                if self.board[i - 1][o - 1] == 'R':
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                     [a + 3, b + 3, self.cell_size - 6,
                                      self.cell_size - 6])
                elif self.board[i - 1][o - 1] == 'H':
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                     [a + 6, b + 6, self.cell_size - 12,
                                      self.cell_size - 12])
                elif self.board[i - 1][o - 1] == 'S':
                    pygame.draw.rect(self.screen, (0, 125, 255),
                                     [a + 3, b + 3, self.cell_size - 6,
                                      self.cell_size - 6])
                elif self.board[i - 1][o - 1] == 'G':
                    pygame.draw.rect(self.screen, (255, 215, 0),
                                     [a + 3, b + 3, self.cell_size - 6,
                                      self.cell_size - 6])
                elif self.board[i - 1][o - 1] == 'E':
                    pygame.draw.rect(self.screen, (176, 0, 0),
                                     [a + 3, b + 3, self.cell_size - 6,
                                      self.cell_size - 6])
                elif self.board[i - 1][o - 1] == 'T':
                    pygame.draw.rect(self.screen, (176, 0, 0),
                                     [a + 6, b + 6, self.cell_size - 12,
                                      self.cell_size - 12])
                elif self.board[i - 1][o - 1] == 'F':
                    pygame.draw.rect(self.screen, (0, 176, 0),
                                     [a + 3, b + 3, self.cell_size - 6,
                                      self.cell_size - 6])
                if o == 3 and i == 3:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     [a + 9, b + 9, self.cell_size - 17,
                                      self.cell_size - 17])
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     [a + 10, b + 10, self.cell_size - 19,
                                      self.cell_size - 19])

                a = self.cell_size * o + self.left
            b = self.cell_size * i + self.top


# Отрисовка интерфейса
class draw_interface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 925
        self.top = 275
        self.cell_size = 65
        self.indent = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        self.screen = screen
        b = self.top
        for i in range(self.height):
            a = self.left
            for o in range(self.width):
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 [a, b, self.cell_size, self.cell_size])
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 [a + 1, b + 1, self.cell_size - 2,
                                  self.cell_size - 2])
                a += self.cell_size + self.indent
            b += self.cell_size + self.indent

    def coord(self, pos):
        self.pos = list(pos)
        self.x = None
        self.y = None
        if self.left <= self.pos[0] <= self.left + self.cell_size * self.width + self.indent and self.top <= self.pos[
            1] <= self.top + self.cell_size * self.height + self.indent * 2:
            if 0 <= self.pos[0] - self.left <= 65:
                self.x = 0
            elif 85 <= self.pos[0] - self.left <= 150:
                self.x = 1

            if 0 <= self.pos[1] - self.top <= 65:
                self.y = 0
            elif 85 <= self.pos[1] - self.top <= 150:
                self.y = 1
            elif 170 <= self.pos[1] - self.top <= 235:
                self.y = 2
            elif 255 <= self.pos[1] - self.top <= 320:
                self.y = 3

        return (self.x, self.y)


class image(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        pygame.sprite.Sprite.__init__(self)
        self.fullname = os.path.join('data/image', self.name)
        self.image = pygame.image.load(self.fullname).convert_alpha()


if __name__ == '__main__':
    win = 2
    number_potion = 0
    list_text = []
    max_size_list_text = 16
    g_room_list = []
    e_room_list = []
    looted_room_list = []
    t_room_list = []
    orientation_for_attack = None
    hp_player = 100
    enemy_alive = False
    all_gold = 0
    player_step = True
    trap_exist = False
    mode = 'walk'
    size_map = 41
    fps = 60
    number_level = 1
    pygame.init()
    pygame.display.set_caption('Координаты клетки')
    size = width, height = 1100, 900
    screen = pygame.display.set_mode(size)
    map = map_level(number_level)
    num_g_room = map.count_rm_G
    interface = draw_interface(2, 4)
    board = map_draw(size_map, map)
    running = True
    fight_icon = image('fight.png')
    walk_icon = image('walk.png')
    pick_up_icon = image('pick up.png')
    inventory_icon = image('inventory.png')
    defense_icon = image('defense.png')
    heal_potion_icon = image('heal_potion.png')
    watch_icon = image('watch.png')
    watch_icon = pygame.transform.scale(watch_icon.image, (60, 60))
    dead_end_image = image('dead_end.png')
    wall_image = image('wall.png')
    trap_image = image('trap.png')
    gold_image = image('gold.png')
    treasure_image = image('treasure.png')
    dark_arrow_image = image('dark.png')
    lite_arrow_image = image('lite.png')
    rat_image = image('rat.png')
    rat_image = pygame.transform.scale(rat_image.image, (600, 600))
    trap_image = pygame.transform.scale(trap_image.image, (200, 200))
    screen.fill((0, 0, 0))

    while running:
        # Начальный экран
        if win == 2:
            file_statistics = open('data/statistics/statistics_gold.txt', 'r', encoding='utf-8')
            max_gold = file_statistics.readline()[:-1]
            last_gold = file_statistics.readline()[:-1]
            file_statistics.close()
            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 30)
            text = font.render(f'Лучший счет: {max_gold}', True,
                               (255, 255, 255))
            screen.blit(text, [10, 10])
            font = pygame.font.Font(None, 30)
            text = font.render(f'Прошлый счет: {last_gold}', True,
                               (255, 255, 255))
            screen.blit(text, [10, 40])
            font = pygame.font.Font(None, 60)
            text = font.render(f'Проект по PyGame', True,
                                   (255, 255, 255))
            screen.blit(text, [370, 300])
            font = pygame.font.Font(None, 20)
            text = font.render('Что бы начать новую игру нажмите любую кнопку',
                               True,
                               (255, 255, 255))
            screen.blit(text, [380, 700])
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    win = 0
        elif win == 0:
            count_halls = 0
            dam_player = random.randint(10, 50)

            for event in pygame.event.get():
                while len(list_text) > max_size_list_text:
                    list_text.pop(0)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if interface.coord(event.dict['pos']) != None:
                        cord_mode = list(interface.coord(event.dict['pos']))

                        if cord_mode == [0, 0]:
                            mode = 'watch'
                        elif cord_mode == [1, 0]:
                            mode = 'fight'
                        elif cord_mode == [0, 1]:
                            mode = 'walk'
                        elif cord_mode == [1, 1]:
                            mode = 'inventory'
                        elif cord_mode == [0, 2]:
                            mode = 'defence'
                        elif cord_mode == [1, 2]:
                            mode = 'pick up'
                        elif cord_mode == [0, 3]:
                            if number_potion >= 1:
                                number_potion -= 1
                                hp_player += 25
                                if hp_player > 100:
                                    hp_player = 100
                                list_text.append(f'Вы использовали зелье лечения.')
                                list_text.append(f'Ваше здоровье сейчас {hp_player}')

                if event.type == pygame.KEYDOWN:
                    screen.fill((0, 0, 0))

                    if mode == 'walk' and trap_exist:
                        hp_player -= random.randint(1, 100)
                        list_text.append('Вы попали в ловушку.')
                        list_text.append(f'Ваше здоровье сейчас {hp_player}')
                        trap_exist = False
                        t_room_list.append(list(board.crd))

                    # Перемещение
                    elif mode == 'walk' and not enemy_alive:
                        if event.dict['key'] == 97 and map.board[board.crd[0]][board.crd[1] - 1] != '#':
                            board.crd[1] -= 1
                        elif event.dict['key'] == 100 and map.board[board.crd[0]][board.crd[1] + 1] != '#':
                            board.crd[1] += 1
                        elif event.dict['key'] == 119 and map.board[board.crd[0] - 1][board.crd[1]] != '#':
                            board.crd[0] -= 1
                        elif event.dict['key'] == 115 and map.board[board.crd[0] + 1][board.crd[1]] != '#':
                            board.crd[0] += 1

                        # Переход на следующий уровень
                        elif event.dict['key'] == 13 and map.board[board.crd[0]][board.crd[1]] == 'F':
                            number_level += 1
                            if number_level <= 10:
                                map = map_level(number_level)
                                num_g_room = map.count_rm_G
                                g_room_list = []
                                e_room_list = []
                                t_room_list = []
                                board = map_draw(size_map, map)
                            else:
                                win = 1

                    if mode == 'fight' and enemy_alive and orientation_for_attack != None:
                        if player_step:
                            if event.dict['key'] == 97 and orientation_for_attack == 'W':
                                hp_enemy -= dam_player
                            elif event.dict['key'] == 100 and orientation_for_attack == 'E':
                                hp_enemy -= dam_player
                            elif event.dict['key'] == 119 and orientation_for_attack == 'N':
                                hp_enemy -= dam_player
                            elif event.dict['key'] == 115 and orientation_for_attack == 'S':
                                hp_enemy -= dam_player
                            list_text.append(f'Вы нанесли врагу {dam_player} урона')
                            if hp_enemy <= 0:
                                enemy_alive = False
                                e_room_list.append(list(board.crd))
                                list_text.append(f'Вы убили врага')
                            else:
                                list_text.append(f'У врага осталось {hp_enemy} здоровья')
                                list_text.append('Ход врага. Защищайтесь')
                                time_start = datetime.datetime.now()

                            orientation_for_attack = None
                            player_step = False

                    elif mode == 'defence' and map.board[board.crd[0]][
                        board.crd[1]] == 'E' and board.crd not in e_room_list and orientation_for_attack != None:
                        if not player_step:
                            dam_enemy = random.randint(25, 90)
                            if event.dict['key'] == 97 and orientation_for_attack != 'W':
                                hp_player -= dam_enemy
                                list_text.append(f'Враг нанес {dam_enemy} урона')
                                list_text.append(f'У вас осталось {hp_player} здоровья')
                            elif event.dict['key'] == 100 and orientation_for_attack != 'E':
                                hp_player -= dam_enemy
                                list_text.append(f'Враг нанес {dam_enemy} урона')
                                list_text.append(f'У вас осталось {hp_player} здоровья')
                            elif event.dict['key'] == 119 and orientation_for_attack != 'N':
                                hp_player -= dam_enemy
                                list_text.append(f'Враг нанес {dam_enemy} урона')
                                list_text.append(f'У вас осталось {hp_player} здоровья')
                            elif event.dict['key'] == 115 and orientation_for_attack != 'S':
                                hp_player -= dam_enemy
                                list_text.append(f'Враг нанес {dam_enemy} урона')
                                list_text.append(f'У вас осталось {hp_player} здоровья')
                            else:
                                list_text.append('Вы полностью отразили удар')
                            orientation_for_attack = None
                            player_step = True
                            list_text.append('Ваш ход. Атакуйте')
                            time_start = datetime.datetime.now()
                            if hp_player <= 0:
                                win = -1
                            break

                    elif mode == 'watch' and trap_exist:
                        if event.dict['key'] == 97 and orientation_for_attack == 'W':
                            list_text.append('Вы обезвредили ловушку')
                            trap_exist = False
                            t_room_list.append(list(board.crd))
                            orientation_for_attack = None
                        elif event.dict['key'] == 100 and orientation_for_attack == 'E':
                            list_text.append('Вы обезвредили ловушку')
                            trap_exist = False
                            t_room_list.append(list(board.crd))
                            orientation_for_attack = None
                        elif event.dict['key'] == 119 and orientation_for_attack == 'N':
                            list_text.append('Вы обезвредили ловушку')
                            trap_exist = False
                            t_room_list.append(list(board.crd))
                            orientation_for_attack = None
                        elif event.dict['key'] == 115 and orientation_for_attack == 'S':
                            list_text.append('Вы обезвредили ловушку')
                            trap_exist = False
                            t_room_list.append(list(board.crd))
                            orientation_for_attack = None

                    # Проверка что бы собрать золото в сокровищнице
                    elif event.dict['key'] == 13 and map.board[board.crd[0]][
                        board.crd[1]] == 'G' and board.crd not in g_room_list and mode == 'pick up':
                        all_gold += random.randint(1, 11) * number_level
                        num_g_room -= 1
                        g_room_list.append(list(board.crd))

                    # Проверка что бы собрать золото с монстра
                    elif event.dict['key'] == 13 and map.board[board.crd[0]][
                        board.crd[
                            1]] == 'E' and board.crd in e_room_list and board.crd not in looted_room_list and mode == 'pick up':
                        number_potion += random.randint(0, 2)
                        if number_potion > 10:
                            number_potion = 10
                        all_gold += random.randint(1, 5) * number_level
                        looted_room_list.append(list(board.crd))
                    if num_g_room == 0:
                        map.board[size_map // 2][size_map // 2] = ('F')

            # Проверка на тупик
            for i in range(-1, 2):
                for o in range(-1, 2):
                    if map.board[board.crd[0] - i][board.crd[1] - o] in ['T', 'H']:
                        count_halls += 1
            if count_halls == 1 and map.board[board.crd[0]][board.crd[1]] not in ['T', 'H']:
                screen.blit(dead_end_image.image, [0, 0])
            else:
                screen.blit(wall_image.image, [0, 0])

            # Создание врага
            if map.board[board.crd[0]][board.crd[1]] == 'E' and board.crd not in e_room_list and not enemy_alive:
                enemy_alive = True
                hp_enemy = 100
                time_start = datetime.datetime.now()
            # Ход игрока
            if orientation_for_attack == None:
                orientation_for_attack = random.choice(['N', 'E', 'S', 'W'])
            # Отрисовка боя
            if enemy_alive:
                screen.blit(rat_image, [150, 300])
                screen.blit(pygame.transform.rotate(dark_arrow_image.image, 270), [10, 400])
                screen.blit(pygame.transform.rotate(dark_arrow_image.image, 90), [780, 400])
                screen.blit(dark_arrow_image.image, [400, 780])
                screen.blit(pygame.transform.rotate(dark_arrow_image.image, 180), [400, 10])
                if orientation_for_attack == 'N':
                    screen.blit(pygame.transform.rotate(lite_arrow_image.image, 180), [400, 10])
                elif orientation_for_attack == 'E':
                    screen.blit(pygame.transform.rotate(lite_arrow_image.image, 90), [780, 400])
                elif orientation_for_attack == 'S':
                    screen.blit(lite_arrow_image.image, [400, 780])
                elif orientation_for_attack == 'W':
                    screen.blit(pygame.transform.rotate(lite_arrow_image.image, 270), [10, 400])

            # Таймер в бою
            if map.board[board.crd[0]][
                board.crd[1]] == 'E' and board.crd not in e_room_list and orientation_for_attack != None:
                time_check = datetime.datetime.now()
                if player_step:
                    if (time_check - time_start).seconds > 2:
                        orientation_for_attack = None
                        player_step = False
                        list_text.append('Вы не успели нанести удар')
                        list_text.append('Ход врага. Защищайтесь')
                        time_start = datetime.datetime.now()
                else:
                    if (time_check - time_start).seconds > 2:
                        dam_enemy = random.randint(25, 90)
                        hp_player -= dam_enemy
                        list_text.append('Вы пропустили удар врага')
                        list_text.append(f'Враг нанес {dam_enemy} урона')
                        list_text.append(f'У вас осталось {hp_player} здоровья')
                        list_text.append('Ваш ход. Атакуйте')
                        orientation_for_attack = None
                        player_step = True
                        list_text.append('Ваш ход. Атакуйте')
                        time_start = datetime.datetime.now()
                        if hp_player <= 0:
                            win = -1

            # Создание ловушки
            if map.board[board.crd[0]][board.crd[1]] == 'T' and board.crd not in t_room_list and not trap_exist:
                trap_exist = True
                time_start = datetime.datetime.now()
            # Отрисовка ловушки
            if trap_exist:
                if orientation_for_attack == 'N':
                    trap_reverse_image = pygame.transform.rotate(trap_image, 180)
                    screen.blit(trap_reverse_image, [350, 10])
                elif orientation_for_attack == 'E':
                    trap_reverse_image = pygame.transform.rotate(trap_image, 90)
                    screen.blit(trap_reverse_image, [650, 400])
                elif orientation_for_attack == 'S':
                    screen.blit(trap_image, [330, 680])
                elif orientation_for_attack == 'W':
                    trap_reverse_image = pygame.transform.rotate(trap_image, 270)
                    screen.blit(trap_reverse_image, [60, 400])
            # Таймер ловушки
            if trap_exist:
                time_check = datetime.datetime.now()
                if (time_check - time_start).seconds > 2:
                    orientation_for_attack = None
                    trap_damage = random.randint(1, 100)
                    hp_player -= trap_damage
                    list_text.append('Вы попали в ловушку.')
                    list_text.append(f'Ловушка нанесла {trap_damage} урона')
                    list_text.append(f'Ваше здоровье сейчас {hp_player}')
                    trap_exist = False
                    t_room_list.append(list(board.crd))

            # Отрисовка сундука для сокровищницы
            if map.board[board.crd[0]][board.crd[1]] == 'G' and board.crd not in g_room_list:
                screen.blit(treasure_image.image, [330, 550])

            # Отрисовка лута с монстра
            elif map.board[board.crd[0]][
                board.crd[1]] == 'E' and board.crd in e_room_list and board.crd not in looted_room_list:
                screen.blit(gold_image.image, [330, 680])
            if hp_player <= 0:
                win = -1

            # Отрисовка кол-во золота
            font = pygame.font.Font(None, 30)
            text = font.render(f'Золото {all_gold}', True, (255, 255, 255))
            screen.blit(text, [925, 190])

            # Отрисовка хп
            font = pygame.font.Font(None, 30)
            text = font.render('Здоровье', True, (255, 255, 255))
            screen.blit(text, [925, 215])
            pygame.draw.rect(screen, (255, 255, 255),
                             [925, 240, 150, 20])
            pygame.draw.rect(screen, (0, 0, 0),
                             [927, 242, 146, 16])
            pygame.draw.rect(screen, (200, 20, 20),
                             [927, 242, round(hp_player * 1.46), 16])

            # Отрисовка текста
            pygame.draw.rect(screen, (255, 255, 255),
                             [905, 620, 190, 275])
            pygame.draw.rect(screen, (0, 0, 0),
                             [907, 622, 186, 271])
            for i in range(len(list_text)):
                font = pygame.font.Font(None, 15)
                text = font.render(list_text[i], True, (255, 255, 255))
                screen.blit(text, [910, 625 + 17 * i])

            # Отрисовка иконок интерфейса
            interface.render(screen)
            board.render(screen)
            screen.blit(fight_icon.image, [1010, 275])
            screen.blit(walk_icon.image, [925, 360])
            screen.blit(pick_up_icon.image, [1008, 440])
            screen.blit(inventory_icon.image, [1010, 360])
            screen.blit(defense_icon.image, [924, 444])
            screen.blit(heal_potion_icon.image, [929, 530])
            screen.blit(watch_icon, [926, 275])
            font = pygame.font.Font(None, 30)
            text = font.render(str(number_potion), True, (255, 255, 255))
            screen.blit(text, [965, 575])
            pygame.display.flip()

        # Финишный экран
        elif win != 0:
            file_statistics = open('data/statistics/statistics_gold.txt', 'r', encoding='utf-8')
            max_gold = file_statistics.readline()[:-1]
            last_gold = file_statistics.readline()[:-1]
            file_statistics.close()

            # Обновление рекорда
            if int(max_gold) < all_gold:
                font = pygame.font.Font(None, 30)
                max_gold = all_gold
                file_statistics = open('data/statistics/statistics_gold.txt', 'w', encoding='utf-8')
                file_statistics.writelines([f'{max_gold}\n', f'{last_gold}\n'])
                file_statistics.close()

            # Отрисовка финишного экрана
            screen.fill((0, 0, 0))

            font = pygame.font.Font(None, 30)
            text = font.render(f'Лучший счет: {max_gold}', True,
                               (255, 255, 255))
            screen.blit(text, [10, 10])
            if int(max_gold) == all_gold:
                font = pygame.font.Font(None, 30)
                text = font.render('Новый рекорд', True,
                                   (255, 255, 255))
                screen.blit(text, [190, 10])

            font = pygame.font.Font(None, 30)
            text = font.render(f'Прошлый счет: {last_gold}', True,
                               (255, 255, 255))
            screen.blit(text, [10, 40])
            font = pygame.font.Font(None, 40)
            # Текст в случае победы
            if win == 1:
                text = font.render(f'Вы прошли подземелье и прихватили с собой {all_gold} золотых монет', True,
                                   (255, 255, 255))
                screen.blit(text, [120, 300])
            # Текст в случае поражения
            else:
                text = font.render(f'Вы погибли в подземелье, но нашли {all_gold} золотых монет', True,
                                   (255, 255, 255))
                screen.blit(text, [200, 300])
            font = pygame.font.Font(None, 20)
            text = font.render(f'Вы можете нажать Esc что бы закрыть игру или нажать Enter что бы начать новую игру ',
                               True,
                               (255, 255, 255))
            screen.blit(text, [250, 700])
            pygame.display.flip()
            for event in pygame.event.get():
                while len(list_text) > max_size_list_text:
                    list_text.pop(0)
                # Закрытие игры
                if event.type == pygame.QUIT:
                    last_gold = all_gold
                    file_statistics = open('data/statistics/statistics_gold.txt', 'w', encoding='utf-8')
                    file_statistics.writelines([f'{max_gold}\n', f'{last_gold}\n'])
                    file_statistics.close()
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.dict['key'] == 27:
                        last_gold = all_gold
                        file_statistics = open('data/statistics/statistics_gold.txt', 'w', encoding='utf-8')
                        file_statistics.writelines([f'{max_gold}\n', f'{last_gold}\n'])
                        file_statistics.close()
                        running = False
                    # Запуск игры заново
                    else:
                        last_gold = all_gold
                        file_statistics = open('data/statistics/statistics_gold.txt', 'w', encoding='utf-8')
                        file_statistics.writelines([f'{max_gold}\n', f'{last_gold}\n'])
                        file_statistics.close()
                        win = 0
                        number_potion = 0
                        list_text = []
                        g_room_list = []
                        e_room_list = []
                        looted_room_list = []
                        t_room_list = []
                        orientation_for_attack = None
                        hp_player = 100
                        enemy_alive = False
                        all_gold = 0
                        player_step = True
                        trap_exist = False
                        mode = 'walk'
                        number_level = 1
                        map = map_level(number_level)
                        num_g_room = map.count_rm_G
                        interface = draw_interface(2, 4)
                        board = map_draw(size_map, map)
                        screen.fill((0, 0, 0))
                        screen.blit(wall_image.image, [0, 0])
