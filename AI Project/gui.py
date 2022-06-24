import sys
from math import sqrt
from typing import List, Tuple, Dict
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QBrush, QPen, QPolygonF
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsEllipseItem
from window_ui import Ui_MainWindow


Cell = Tuple[int, int]


class Puzzle:
    def __init__(self,
                 maximum: int,
                 dimensions: Tuple[int, int],
                 rows: List[List[int]],
                 dots: List[Tuple[Cell, Cell]]):
        self.rows = rows
        self.dots = dots
        self.maximum = maximum
        self.row_count, self.column_count = dimensions

    @classmethod
    def parse(cls, input: str):
        lines = input.splitlines()
        x, y, m = map(int, lines[0].split())
        rows = []
        for line in lines[1: x + 1]:
            rows.append(list(map(int, line.split())))
        dots = []
        for line in lines[x + 2:]:
            y1, x1, y2, x2 = map(int, line.split())
            dots.append(((x1, y1), (x2, y2)))
        return cls(m, (x, y), rows, dots)


class HexCell(QGraphicsPolygonItem):
    def __init__(self, x, y, radius, value: str, brush: QBrush):
        super().__init__()
        polygon = QPolygonF()
        center = complex(x, y)
        last_point = complex(0, -radius)
        polygon.append(self.translate(center, last_point))
        rotation = complex(0.5, sqrt(3)/2)
        for i in range(6):
            last_point = last_point * rotation
            polygon.append(self.translate(center, last_point))
        self.setPolygon(polygon)
        self.setBrush(brush)
        self.text = QGraphicsTextItem(value, self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    @staticmethod
    def translate(c1: complex, c2: complex):
        p = c1 + c2
        return QPointF(p.real, p.imag)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, solved_puzzle: str = None, solved_cells: List[List] = None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.scene: QGraphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.cells: Dict[Cell, HexCell] = {}
        if solved_puzzle:
            self.plainTextEdit.setPlainText(solved_puzzle)
            self.do_draw_puzzle()
            if solved_cells:
                self.highlight_solved_cells(solved_cells)

    def highlight_solved_cells(self, solved_cells: List[List]):
        for solved_cell in solved_cells:
            self.cells[(solved_cell[0], solved_cell[1])].setBrush(QBrush(Qt.white))

    def pushButton_clicked(self):
        self.do_draw_puzzle()

    def do_draw_puzzle(self):
        puzzle = Puzzle.parse(self.plainTextEdit.toPlainText())
        self.scene.clear()
        self.cells.clear()
        r = self.spinBox.value()
        y = 0
        indent = sqrt(3) * r / 2
        for i, row in enumerate(puzzle.rows):
            x = 0 if len(row) == puzzle.column_count else indent
            for j, cell in enumerate(row):
                if cell == -2:
                    hex = HexCell(x, y, r, "", QBrush(Qt.black))
                elif cell == -1:
                    hex = HexCell(x, y, r, "", QBrush(Qt.gray))
                elif cell == 0:
                    hex = HexCell(x, y, r, "", QBrush(Qt.white))
                else:
                    hex = HexCell(x, y, r, str(cell), QBrush(Qt.cyan))
                self.cells[(i, j)] = hex
                self.scene.addItem(hex)
                x += 2 * indent
            y += 3 * r / 2
        for dot in puzzle.dots:
            (x1, y1), (x2, y2) = dot
            a = 2 * x1 * indent
            if len(puzzle.rows[y1]) != puzzle.column_count:
                a += indent
            b = 2 * x2 * indent
            if len(puzzle.rows[y2]) != puzzle.column_count:
                b += indent
            y1 = 3 * y1 * r / 2
            y2 = 3 * y2 * r / 2
            x = (a + b) / 2
            y = (y1 + y2) / 2
            # line = QGraphicsLineItem(a, y1, b, y2)
            # line.setPen(QPen(Qt.red))
            # self.scene.addItem(line)
            rect = QGraphicsEllipseItem(x - 4, y - 4, 8, 8)
            self.scene.addItem(rect)
            rect.setBrush(QBrush(Qt.black))


class App(QApplication):
    def __init__(self, solved_puzzle: str = None, solved_cells: List[List] = None):
        super().__init__()
        self.main_window = MainWindow(solved_puzzle, solved_cells)
        self.main_window.show()


def draw_puzzle(solved_puzzle: str, solved_cells: List[List] = None):
    App(solved_puzzle, solved_cells).exec_()


if __name__ == "__main__":
    app = App()
    app.exec_()
