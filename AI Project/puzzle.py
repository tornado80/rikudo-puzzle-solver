from typing import List, Tuple, Union, Dict

Cell = Tuple[int, int]
Dot = Tuple[Cell, Cell]
Dots = List[Dot]


class Puzzle:
    def __init__(self,
                 max_num: int,
                 dimensions: Tuple[int, int],
                 cells: List[List[int]],
                 dots: Dots,
                 empty_cells: List[Cell],
                 fixed_nums: Dict[int, Cell]):
        self.cells: List[List[int]] = cells
        self.fixed_nums: dict[int: Cell] = fixed_nums
        self.empty_cells: List[Cell] = empty_cells
        self.dots: Dots = dots
        self.dot_count: int = len(dots)
        self.max_num: int = max_num
        self.row_count, self.column_count = dimensions

        self.pairwise_distances: dict[(Cell, Cell): int] = {}
        self.calculate_cells_pairwise_distances()

        self.coordinate_num: dict[int: Cell] = {}
        self.calculate_fixed_cells_coordinate_num()
        self.calculate_empty_cells_coordinate_num()

    def __str__(self):
        lines = [f"{self.row_count} {self.column_count} {self.max_num}"]
        for row in self.cells:
            lines.append(" ".join(map(str, row)))
        lines.append(f"{self.dot_count}")
        for cell1, cell2 in self.dots:
            lines.append(f"{cell1[0]} {cell1[1]} {cell2[0]} {cell2[1]}")
        return "\n".join(lines)

    def set_empty_cells(self, filled_cells: List[int]):
        # TODO: efficient lookup : we can make empty_cells hashmap (20 * 36)
        for i, filled_cell in enumerate(filled_cells):
            self.cells[self.empty_cells[i][0]][self.empty_cells[i][1]] = filled_cell

    @classmethod
    def parse(cls, input: str):
        lines = input.splitlines()
        x, y, m = map(int, lines[0].split())
        cells: List[List[int]] = []
        empty_cells: List[Cell] = []
        fixed_nums: dict[int: Cell] = {}
        for i, line in enumerate(lines[1: x + 1]):
            row = []
            for j, cell in enumerate(map(int, line.split())):
                row.append(cell)
                if cell > 0:
                    fixed_nums[cell] = (i, j)
                if cell == 0:
                    empty_cells.append((i, j))
            cells.append(row)
        dots = []
        for line in lines[x + 2:]:
            x1, y1, x2, y2 = map(int, line.split())
            dots.append(((x1, y1), (x2, y2)))
        return cls(m, (x, y), cells, dots, empty_cells, fixed_nums)

    def find_coordinates(self, k: int) -> Union[Cell, None]:
        '''if k in self.fixed_nums:
            return self.fixed_nums[k]
        for i, j in self.empty_cells:
            if self.cells[i][j] == k:
                return i, j
        return None'''
        # we assume that k is in coordinates and cells filled in the gene
        return self.coordinate_num[k]

    def is_successor(self, cell1: Cell, cell2: Cell) -> bool:
        return abs(self.cells[cell1[0]][cell1[1]] - self.cells[cell2[0]][cell2[1]]) == 1

    def is_neighbour(self, x1: Cell, x2: Cell) -> bool:
        if x1[0] == x2[0]:
            return abs(x1[1] - x2[1]) == 1
        elif x1[0] + 1 == x2[0] and len(self.cells[x1[0]]) > len(self.cells[x2[0]]):
            return x1[1] == x2[1] or x1[1] == x2[1] + 1
        elif x1[0] + 1 == x2[0] and len(self.cells[x1[0]]) < len(self.cells[x2[0]]):
            return x1[1] == x2[1] or x1[1] + 1 == x2[1]
        elif x1[0] == x2[0] + 1 and len(self.cells[x1[0]]) > len(self.cells[x2[0]]):
            return x1[1] == x2[1] or x1[1] + 1 == x2[1]
        elif x1[0] == x2[0] + 1 and len(self.cells[x1[0]]) < len(self.cells[x2[0]]):
            return x1[1] == x2[1] or x1[1] == x2[1] + 1
        else:
            return False

    def neighbours(self, cell: Cell) -> List[Cell]:
        i, j = cell
        res = []
        if len(self.cells[i]) == self.column_count:
            if i != 0 and j != 0:
                res.append((i - 1, j - 1))
            if i != 0 and j != self.column_count - 1:
                res.append((i - 1, j))
            if i != self.row_count - 1 and j != 0:
                res.append((i + 1, j - 1))
            if i != self.row_count - 1 and j != self.column_count - 1:
                res.append((i + 1, j))
        if len(self.cells[i]) == self.column_count - 1:
            if i != 0:
                res.append((i - 1, j))
                res.append((i - 1, j + 1))
            if i != self.row_count - 1:
                res.append((i + 1, j))
                res.append((i + 1, j + 1))
        if j != 0:
            res.append((i, j - 1))
        if j != len(self.cells[i]) - 1:
            res.append((i, j + 1))
        return res

    def bfs(self, src: Cell, dest: Cell) -> int:
        if src == dest:
            return 0
        explored = {src: 0}
        queue = [src]
        while len(queue) != 0:
            v = queue.pop(0)
            for u in self.neighbours(v):
                if self.cells[u[0]][u[1]] < 0 or u in explored:
                    continue
                explored[u] = explored[v] + 1
                queue.append(u)
                if u == dest:
                    return explored[u]
        return -1

    def calculate_cells_pairwise_distances(self):
        for i1 in range(self.row_count):
            for j1 in range(len(self.cells[i1])):
                for i2 in range(self.row_count):
                    for j2 in range(len(self.cells[i2])):
                        self.pairwise_distances[((i1, j1), (i2, j2))] = self.bfs((i1, j1), (i2, j2))

    def calculate_fixed_cells_coordinate_num(self):
        #for (k, v) in self.fixed_nums.items():
        #    self.coordinate_num[k] = v
        self.coordinate_num = self.fixed_nums.copy()

    def calculate_empty_cells_coordinate_num(self):
        for i, j in self.empty_cells:
            self.coordinate_num[self.cells[i][j]] = (i, j)

    def calculate_coordinates(self):
        calculate_fixed_cells_coordinate_num()
