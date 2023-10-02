from typing import List

from Figures.Figure import Figure
from Utils import Point, NUM_SECTORS


class Guard(Figure):
    """
    Страж. Не умеет бить, защищает фигуры по бокам от себя и по радиусу
    """

    def defence_aura(self) -> List[Point]:
        if not self.abilities_work:
            return []

        return [
            Point(self.position.radius, (self.position.sector + 1) % NUM_SECTORS),
            Point(self.position.radius, (self.position.sector - 1 + NUM_SECTORS) % NUM_SECTORS),
            Point(3 - self.position.radius, self.position.sector)
        ]

    def find_targets(self) -> List[Point]:
        return []

    def __str__(self):
        return "G" + str(self.player) + str(self.position.radius) + "{:02d}".format(self.position.sector)
