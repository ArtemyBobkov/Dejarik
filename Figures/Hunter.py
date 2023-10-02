from typing import List

from Figures.Figure import Figure
from Utils import Point, NUM_SECTORS


class Hunter(Figure):

    def find_targets(self) -> List[Point]:
        if self.position.radius == 0:
            return []
        return [Point(3 - self.position.radius, (self.position.sector + NUM_SECTORS - 2) % NUM_SECTORS),
                Point(3 - self.position.sector, (self.position.sector + 2) % NUM_SECTORS)]

    def __str__(self):
        return "H" + str(self.player) + str(self.position.radius) + "{:02d}".format(self.position.sector)