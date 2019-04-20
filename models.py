import copy
from typing import List, Optional
from helper import *


class Piece:
    """
    Общий интерфейс для фигур
    """
    ch = '*'

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_char(self):
        return self.ch

    def can_move(self, board, row, col, row1, col1):
        raise NotImplementedError

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


# TODO: Проверка на шах, мат, пат, оппозицию

class Board:
    color = WHITE
    field: List[List[Optional[Piece]]] = [[None] * 8 for i in range(8)]

    def check_field(self):
        """
        Возвращает -1 если шаха нет, иначе число, соотвествующее цвету стороны, которой шах
        """
        bkx, bky = -1, -1
        wkx, wky = -1, -1

        for i in range(8):
            for j in range(8):
                if isinstance(self.field[i][j], King):
                    if self.field[i][j].color == WHITE:
                        wkx, wky = i, j
                    else:
                        bkx, bky = i, j

        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None:
                    if self.field[i][j].color == WHITE and self.field[i][j].can_attack(self, i, j, bkx, bky):
                        return BLACK
                    if self.field[i][j].color == BLACK and self.field[i][j].can_attack(self, i, j, wkx, wky):
                        return WHITE
        return -1

    def __init__(self):
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def print(self):  # Распечатать доску в текстовом виде (см. скриншот)
        print('     +----+----+----+----+----+----+----+----+')
        for row in range(7, -1, -1):
            print(' ', row, end='  ')
            for col in range(8):
                print('|', self.cell(row, col), end=' ')
            print('|')
            print('     +----+----+----+----+----+----+----+----+')
        print(end='        ')
        for col in range(8):
            print(col, end='    ')
        print()

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """
        Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.
        """
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.get_char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """
        Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False
        """

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False

        # TODO: рокировка
        # Стоит сделать здесь, потому что метод can_move не должен менять фигуру.
        # Возможно, стоит сделать общий метод move у класса Piece и переопределить его у короля

        # TODO: шах
        # Нужно создать копию доски. проверить. что нет шаха, и только если все хорошо - передвигать и возвращать True

        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False

        new_field = copy.deepcopy(self)
        new_field.field[row][col] = None  # Снять фигуру.
        new_field.field[row1][col1] = piece  # Поставить на новое место.
        if new_field.check_field() == self.color:
            return False

        self.field = copy.deepcopy(new_field.field)
        self.color = opponent(self.color)

        return True


class Rook(Piece):
    ch = 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True


class Pawn(Piece):
    ch = 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Knight(Piece):
    """
    Класс коня. Пока что заглушка, которая может ходить в любую клетку.
    """
    ch = 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        dx = abs(row1 - row)
        dy = abs(col1 - col)
        return dx <= 2 and dy <= 2 and dx + dy == 3


class King(Piece):
    ch = 'K'

    def can_move(self, board, row, col, row1, col1):
        return abs(row - row1) <= 1 and abs(col - col1) <= 1


class Bishop(Piece):
    ch = 'B'

    def can_move(self, board, row, col, row1, col1):
        # Небольшой математический трюк
        if row + col != row1 + col1 and row - col != row1 - col1:
            return False

        sx = 1 if row < row1 else -1
        sy = 1 if col < col1 else -1

        while row + sx != row1:
            row += sx
            col += sy
            if board.get_piece(row, col) is not None:
                return False
        return True


class Queen(Piece):
    ch = 'Q'

    def can_move(self, board, row, col, row1, col1):
        return Rook(self.color).can_move(board, row, col, row1, col1) or \
               Bishop(self.color).can_move(board, row, col, row1, col1)
