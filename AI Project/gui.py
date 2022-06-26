import sys
from math import sqrt
from typing import List, Tuple, Dict
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QBrush, QPen, QPolygonF
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsPolygonItem, QGraphicsTextItem, QGraphicsEllipseItem
from canvas import MplCanvas
from window_ui import Ui_MainWindow
from puzzle import *


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
    def __init__(self, solved_puzzle: str = None, solved_cells: List[Cell] = None, objective_values: List[int] = None):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        self.draw_button.clicked.connect(self.draw_button_clicked)
        self.scene: QGraphicsScene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.cells: Dict[Cell, HexCell] = {}
        if solved_puzzle:
            self.puzzle_plain_text_edit.setPlainText(solved_puzzle)
            self.do_draw_puzzle()
            if solved_cells:
                self.highlight_solved_cells(solved_cells)
                self.solved_cells_plain_text_edit.setPlainText("\n".join(f"{i} {j}" for i, j in solved_cells))
        if objective_values:
            self.canvas.axes.plot(range(len(objective_values)), objective_values)
            self.canvas.axes.set_xlabel('Epoch')
            self.canvas.axes.set_ylabel('Fitness')
            self.canvas.axes.set_title('Convergence of Fitness per Epoch')

    def highlight_solved_cells(self, solved_cells: List[Cell]):
        for solved_cell in solved_cells:
            self.cells[(solved_cell[0], solved_cell[1])].setBrush(QBrush(Qt.white))

    def draw_button_clicked(self):
        self.do_draw_puzzle()
        cells = []
        for line in self.solved_cells_plain_text_edit.toPlainText().splitlines():
            x, y = map(int, line.split())
            cells.append((x, y))
        self.highlight_solved_cells(cells)

    def do_draw_puzzle(self):
        puzzle = Puzzle.parse(self.puzzle_plain_text_edit.toPlainText())
        self.scene.clear()
        self.cells.clear()
        r = self.spinBox.value()
        y = 0
        indent = sqrt(3) * r / 2
        for i, row in enumerate(puzzle.cells):
            x = 0 if len(row) == puzzle.column_count else indent
            for j, cell in enumerate(row):
                if cell == -2:
                    hex = HexCell(x, y, r, "", QBrush(Qt.black))
                elif cell == -1:
                    hex = HexCell(x, y, r, "", QBrush(Qt.gray))
                elif cell == 0:
                    hex = HexCell(x, y, r, "", QBrush(Qt.white))
                elif cell == 1:
                    hex = HexCell(x, y, r, str(cell), QBrush(Qt.yellow))
                elif cell == puzzle.max_num:
                    hex = HexCell(x, y, r, str(cell), QBrush(Qt.yellow))
                else:
                    hex = HexCell(x, y, r, str(cell), QBrush(Qt.cyan))
                self.cells[(i, j)] = hex
                self.scene.addItem(hex)
                x += 2 * indent
            y += 3 * r / 2
        for dot in puzzle.dots:
            (y1, x1), (y2, x2) = dot
            a = 2 * x1 * indent
            if len(puzzle.cells[y1]) != puzzle.column_count:
                a += indent
            b = 2 * x2 * indent
            if len(puzzle.cells[y2]) != puzzle.column_count:
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
    def __init__(self, solved_puzzle: str = None, solved_cells: List[Cell] = None, objective_values: List[int] = None):
        super().__init__()
        self.main_window = MainWindow(solved_puzzle, solved_cells, objective_values)
        self.main_window.show()


def draw_puzzle(solved_puzzle: str, solved_cells: List[Cell] = None, objective_values: List[int] = None):
    App(solved_puzzle, solved_cells, objective_values).exec_()


if __name__ == "__main__":
    app = App()
    app.exec_()
