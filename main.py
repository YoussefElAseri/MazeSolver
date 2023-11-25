from Logic import *


if __name__ == "__main__":
    win = Window(800, 600)
    num_cols = 12
    num_rows = 10
    m1 = Maze(5, 5, num_rows, num_cols, 20, 20, win, 0)
    m1.solve()
    win.wait_for_close()
