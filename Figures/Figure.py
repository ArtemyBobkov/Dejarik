from typing import List, Union, Tuple

from Utils import Point


class Figure:

    def defence_aura(self) -> List[Point]:
        """
        Определяет, может ли фигура защищать других
        :return: список точек под защитой фигуры
        """
        return []

    def __init__(self, player: int, position: Union[Point, Tuple[int, int]]):
        self.player = player
        if isinstance(position, Point):
            self.position = position
        else:
            self.position = Point(position)
        self.made_move = False
        self.made_attack = False
        self.made_push = False
        self.used_special_ability = False
        self.abilities_work = True

    def move(self, position: Point):
        self.position = position
        self.made_move = True

    def make_attack(self, position: Point):
        self.position = position
        self.made_attack = True

    def push(self, enemy, new_position: Point):
        enemy.position = new_position
        self.made_push = True

    def find_targets(self) -> List[Point]:
        """
        Найти возможные точки для атаки
        :return:
        """
        raise NotImplementedError

