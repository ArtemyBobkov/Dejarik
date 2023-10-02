from typing import List

from Figures import Figure
import numpy as np

from Figures.Fighter import Fighter
from Figures.Guard import Guard
from Figures.Hunter import Hunter
from Figures.Pet import Pet
from Utils import Point, cells_between, assert_correct, NUM_SECTORS, near


class Field:
    """
    Игровое поле, содержит фигуры и карту занятых клеток
    """

    FIGURE_NAME_MAPPING = {Hunter: "H", Guard: "G", Fighter: "F", Pet: "P"}

    def __init__(self, figures1: List, figures2: List):
        self.figures1 = figures1
        self.figures2 = figures2
        orbits = np.array(*np.array(np.arange(0, NUM_SECTORS), np.zeros(NUM_SECTORS), np.zeros(NUM_SECTORS)).T,
                          *np.array(np.arange(0, NUM_SECTORS), np.ones(NUM_SECTORS), np.zeros(NUM_SECTORS)).T).T
        self.map = dict(map(lambda key, value: (key, value),
                            list(map(Point, orbits[:2].T)), orbits[2]))
        self.map[Point(2, 0)] = 0
        self.guards = {}
        for figure1, figure2 in zip(figures1, figures2):
            if isinstance(figure1, Guard):
                self.guards[1] = figure1
            if isinstance(figure2, Guard):
                self.guards[2] = figure2
            self.map[figure1.position] = Field.FIGURE_NAME_MAPPING[figure1.__class__] + "1"
            self.map[figure2.position] = Field.FIGURE_NAME_MAPPING[figure2.__class__] + "2"

    def can_move(self, start: Point, finish: Point) -> bool:
        """
        Можно ли совершить движение между двумя заданными клетками. Проверка на наличие фигур в промежутке
        :param start: начальная клетка
        :param finish: конечная клетка
        :return: можно ли пройти от одной до другой
        """

        assert_correct(start, self.can_move)
        assert_correct(finish, self.can_move)

        if self.map[finish] != 0:
            return False
        middle_paths = cells_between(start, finish)
        for middle in middle_paths:
            assert_correct(middle, self.can_move)
            if self.map[middle] == 0:
                return True

    def can_attack(self, figure1: Figure, figure2: Figure, player: int) -> bool:
        """
        Проверка, может ли фигура атаковать другую
        """
        if 3 - player in self.guards and figure2.position in self.guards[3 - player].defence_aura():
            return False
        if figure2.position in figure1.find_targets():
            if isinstance(figure1, Hunter):
                r = figure1.position.radius
                s = figure1.position.sector
                if figure2.position.sector == (s + NUM_SECTORS - 2) % NUM_SECTORS:
                    return self.map[Point(3 - r, s)] == 0 and \
                        self.map[Point(3 - r, (s + NUM_SECTORS - 1) % NUM_SECTORS)] == 0
                else:
                    return self.map[Point(3 - r, s)] == 0 and \
                        self.map[Point(3 - r, (s + NUM_SECTORS + 1) % NUM_SECTORS)] == 0
            return True

    def can_push(self, figure1: Figure, figure2: Figure, new_pos: Point):
        return near(figure1.position, figure2.position) and self.map[new_pos] == 0

    def make_attack(self, figure1: Figure, figure2: Figure, player: int) -> str:
        self.map[figure2.position] = self.map[figure1.position]
        self.map[figure1.position] = 0
        if isinstance(figure2, Guard):
            self.guards.pop(player)
        if player == 1:
            self.figures2.remove(figure2)
        else:
            self.figures1.remove(figure2)
        figure1.make_attack(figure2.position)
        return str(figure1)

    def make_move(self, figure: Figure, new_pos: Point) -> str:
        self.map[new_pos] = self.map[figure.position]
        self.map[figure.position] = 0
        figure.make_move(new_pos)
        return str(figure)

    def make_push(self, figure2: Figure, new_pos: Point) -> str:
        self.map[new_pos] = self.map[figure2.position]
        self.map[figure2.position] = 0
        return str(figure2)

    def state(self) -> str:
        return "".join(map(str, [*self.figures1, *self.figures2]))
