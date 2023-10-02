from typing import List

from Figures.Figure import Figure
from Utils import Point


class Pet(Figure):

    def find_targets(self) -> List[Point]:
        if self.position.radius == 0:
            return []
        return [Point(3 - self.position.radius, self.position.sector)]

    def __str__(self):
        return "P" + str(self.player) + str(self.position.radius) + "{:02d}".format(self.position.sector)
