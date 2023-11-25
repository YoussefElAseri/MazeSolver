import random
from tkinter import Tk, BOTH, Canvas
from time import sleep
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1: Point, point_2: Point):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=fill_color, width=2
        )
        canvas.pack()


class Window:
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze")
        self.canvas = Canvas()
        self.canvas.pack()
        self.running = False
        self.__root.configure(bg="white")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, x1, x2, y1, y2, window: Window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = window
        self.visited = False

    def draw(self):
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        p3 = Point(self._x1, self._y2)
        p4 = Point(self._x2, self._y2)

        self._draw_wall(Line(p1, p2), self.has_top_wall)
        self._draw_wall(Line(p2, p4), self.has_right_wall)
        self._draw_wall(Line(p3, p4), self.has_bottom_wall)
        self._draw_wall(Line(p1, p3), self.has_left_wall)

    def _draw_wall(self, line, visible):
        if visible:
            fill_color = "black"
        else:
            fill_color = "white"
        self._win.draw_line(line, fill_color)

    def get_center_x(self):
        return (self._x1 + self._x2) / 2

    def get_center_y(self):
        return (self._y1 + self._y2) / 2

    def draw_move(self, to_cell, undo=False):
        p1 = Point(self.get_center_x(), self.get_center_y())
        p2 = Point(to_cell.get_center_x(), to_cell.get_center_y())
        line = Line(p1, p2)
        fill_color = "red"
        if undo:
            fill_color = "grey"
        self._win.draw_line(line, fill_color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._win = win
        self._cell_size_y = cell_size_y
        self._cell_size_x = cell_size_x
        self._num_cols = num_cols
        self._num_rows = num_rows
        self._y1 = y1
        self._x1 = x1
        self._cells: list[list[Cell]] = []
        self._create_cells()
        if seed:
            random.seed(seed)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        x1 = self._x1
        y1 = self._y1
        cell_width = self._cell_size_x
        cell_height = self._cell_size_y
        for row_nr in range(self._num_rows):
            row = []
            for col_nr in range(self._num_cols):
                new_cell = Cell(x1, x1 + cell_width, y1, y1 + cell_height, self._win)
                row.append(new_cell)
                x1 += cell_width
            self._cells.append(row)
            x1 = self._x1
            y1 += cell_height

        for row_nr in range(self._num_rows):
            for col_nr in range(self._num_cols):
                self._cells[row_nr][col_nr].draw()

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_rows-1][self._num_cols-1].has_bottom_wall = False
        self._draw_cell(self._num_rows-1, self._num_cols-1)

    def _cells_to_visit(self, i, j, wall_check=False):
        to_visit = []
        current_cell = self._cells[i][j]

        if j - 1 >= 0 and not self._cells[i][j-1].visited:
            if not wall_check or not current_cell.has_left_wall:
                to_visit.append([i, j-1])
        if j + 1 < self._num_cols and not self._cells[i][j+1].visited:
            if not wall_check or not current_cell.has_right_wall:
                to_visit.append([i, j+1])
        if i - 1 >= 0 and not self._cells[i-1][j].visited:
            if not wall_check or not current_cell.has_top_wall:
                to_visit.append([i-1, j])
        if i + 1 < self._num_rows and not self._cells[i+1][j].visited:
            if not wall_check or not current_cell.has_bottom_wall:
                to_visit.append([i+1, j])

        return to_visit

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = self._cells_to_visit(i, j)
            if len(to_visit) == 0 or i == self._num_rows:
                self._cells[i][j].draw()
                return

            direction = random.choice(to_visit)
            if direction[1] < j:
                self._cells[i][j].has_left_wall = False
                self._cells[i][j-1].has_right_wall = False
            elif direction[1] > j:
                self._cells[i][j].has_right_wall = False
                self._cells[i][j+1].has_left_wall = False
            elif direction[0] < i:
                self._cells[i][j].has_top_wall = False
                self._cells[i-1][j].has_bottom_wall = False
            elif direction[0] > i:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i+1][j].has_top_wall = False

            self._draw_cell(i, j)
            self._break_walls_r(direction[0], direction[1])

    def _reset_cells_visited(self):
        for row_nr in range(self._num_rows):
            for col_nr in range(self._num_cols):
                self._cells[row_nr][col_nr].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cel = self._cells[i][j]
        current_cel.visited = True
        if i == self._num_rows-1 and j == self._num_cols-1:
            return True

        to_visit = self._cells_to_visit(i, j, True)

        for direction in to_visit:
            current_cel.draw_move(self._cells[direction[0]][direction[1]])
            if self._solve_r(direction[0], direction[1]):
                return True
            current_cel.draw_move(self._cells[direction[0]][direction[1]], True)

        return False
