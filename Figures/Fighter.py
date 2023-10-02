from typing import List

import numpy as np

from Figures.Figure import Figure
from Utils import Point, NUM_SECTORS


class Fighter(Figure):

    def find_targets(self) -> List[Point]:
        if self.position.radius == 0:
            return list(map(Point, *np.array(np.arange(0, NUM_SECTORS), np.ones(NUM_SECTORS)).T))
        r = self.position.radius
        s = self.position.sector
        return [Point(r, (s + 1) % NUM_SECTORS),
                Point(r, (s - 1 + NUM_SECTORS) % NUM_SECTORS),
                Point(3 - r, s),
                Point(3 - r, (s + 1) % NUM_SECTORS),
                Point(3 - r, (s - 1 + NUM_SECTORS) % NUM_SECTORS)
                ]

    def __str__(self):
        return "F" + str(self.player) + str(self.position.radius) + "{:02d}".format(self.position.sector)
