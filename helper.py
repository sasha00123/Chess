WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    return WHITE if color == BLACK else BLACK


def correct_coords(row, col):
    """
    Функция проверяет, что координаты (row, col) лежат
    внутри доски
    """
    return 0 <= row < 8 and 0 <= col < 8
