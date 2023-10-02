from typing import Tuple, List, Union, Callable

import numpy as np

NUM_SECTORS = 11


class Point:
    """
    Точка на доске. Предполагается, что radius от 0 до 2, где
    0 - дежарик, центр поля
    1 - средняя орбита
    2 - внешняя орбита
    Круг разбит на сектора, номера sector - от 0 до NUM_SECTORS - 1.
    Фигура первого игрока расставляется на
    """
    def __init__(self, radius: Union[int, Tuple[int, int]], sector: int = None):
        """
        Конструктор по двум точкам
        :param radius: int либо Tuple из двух интов - радиус и сектор
        :param sector: сектор
        """
        if isinstance(radius, Tuple):
            self.radius = radius[0]
            self.sector = radius[1]
        else:
            self.radius = radius
            self.sector = sector

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.radius == other.radius and self.sector == other.sector
        return False

    def __ne__(self, other):
        if isinstance(other, Point):
            return not self == other
        return False


def find_possible_moves(cell: Point) -> List[Point]:
    """
    Поиск возможных ячеек для окончания движения
    :param cell: начало движения
    :return: список доступных ходов
    """
    if cell.radius == 0:
        return [*map(Point, *np.array(np.arange(0, NUM_SECTORS), np.zeros(NUM_SECTORS)).T),
                *map(Point, *np.array(np.arange(0, NUM_SECTORS), np.ones(NUM_SECTORS)).T)]

    possible_moves = [
        Point(0, 0),
        Point(3 - cell.radius, (cell.sector + NUM_SECTORS - 1) % NUM_SECTORS),
        Point(3 - cell.radius, (cell.sector + NUM_SECTORS + 1) % NUM_SECTORS)
    ]
    if cell.radius == 2:
        possible_moves.extend([(cell.radius, (cell.sector + NUM_SECTORS - 2) % NUM_SECTORS),
                               (cell.radius, (cell.sector + 2) % NUM_SECTORS)])
    else:
        # пройти можно с 1 на 1 в любую точку через центр
        possible_moves.extend(np.delete(np.arange(0, NUM_SECTORS), cell.sector))
    return possible_moves


def cells_between(cell1: Point, cell2: Point) -> List[Point]:
    """
    Промежуточные клетки, между которыми должна пройти фигура
    :param cell1: начало движения
    :param cell2: конец движения
    :return: все варианты промежуточных клеток
    """

    assert_correct(cell1, cells_between)
    assert_correct(cell2, cells_between)

    # проход только по орбите
    if cell1.radius == cell2.radius:
        if cell1.radius == 0:
            raise AttributeError("Невалидно переходить из дежарика в дежарик!")
        # если пройти можно только через центр поля
        if abs(cell1.sector - cell2.sector) == 1:
            return [Point(2, 0)]
        # если проход через нулевой сектор
        if abs(cell1.sector - cell2.sector) > 1:
            return [Point(cell1.radius, 0 if cell1.sector == 1 or cell2.sector == 1 else NUM_SECTORS - 1)]
        return [Point(cell1.radius, (cell1.sector + cell2.sector) // 2)]

    if cell1.radius > cell2.radius:
        cell1, cell2 = cell2, cell1

    # проход только по радиусу
    if cell2.radius - cell1.radius == 2:
        return [Point(1, cell2.sector)]
    # случай с центром и средней орбитой
    if cell1.radius == 0:
        return [
            Point(1, (cell2.sector + 1) % NUM_SECTORS),
            Point(1, (cell2.sector + NUM_SECTORS - 1) % NUM_SECTORS)
        ]
    # случай с обычным движением между орбитами
    return [
        Point(1, cell2.sector),
        Point(2, cell1.sector)
    ]


def assert_correct(cell: Point, fun: Callable):
    if cell.radius < 0 or cell.radius > 2:
        raise AssertionError(f"Invalid radius: {cell.radius} in function {fun}")
    if cell.radius == 0 and cell.sector != 0:
        raise AssertionError(f"Invalid sector {cell.sector} for radius 0 in function {fun}")
    if cell.sector < 0 or cell.sector >= NUM_SECTORS:
        raise AssertionError(f"Invalid sector {cell.sector} in function {fun}")


def near(cell1: Point, cell2: Point) -> bool:
    if cell1 == cell2:
        raise ValueError("Две ячейки в сравнении не должны быть одинаковыми!")
    if cell1.radius > cell2.radius:
        cell1, cell2 = cell2, cell1
    if cell1.radius == 0:
        return cell2.radius == 1
    return (abs(cell1.sector - cell2.sector) <= 1 or
            max(cell1.sector, cell2.sector) == NUM_SECTORS - 1 and
            min(cell1.sector, cell2.sector) == 0)

