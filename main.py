from Environment.Field import Field
from Figures.Figure import Figure
from Figures.Guard import Guard
from Figures.Hunter import Hunter

if __name__ == '__main__':
    a = Hunter(1, (2, 1))
    b = Guard(2, (2, 0))
    print("".join(map(str, [a, b])))

