# !/usr/bin/python3
import sys

from random import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsRectItem, QLabel, QWidget, QLayout, QVBoxLayout, QHBoxLayout, QBoxLayout, QFrame, \
    QGraphicsSceneMouseEvent, QTableView, QPushButton, QTableWidget, QMenu
from PyQt5.QtGui import QPainterPath, QMouseEvent, QPainter, QKeyEvent
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QPen, QFont, QCursor
from PyQt5 import Qt


class MainWindow(QMainWindow):
    class MainScene(QGraphicsScene):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent

        def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
            if event.button() == 2:
                current_x, current_y = event.scenePos().x(), event.scenePos().y()

                for rect, object_rect in self.parent.rectangles:
                    if rect.x1 <= current_x <= rect.x2 and \
                            rect.y1 <= current_y <= rect.y2:
                        try:
                            context_menu = QMenu()

                            history = context_menu.addAction('history')
                            action = context_menu.exec(QCursor().pos())

                            if action == history:
                                rect.widget = QWidget()
                                layout = QHBoxLayout()
                                label = QLabel()
                                label.setText(rect.description)
                                layout.addWidget(label)
                                rect.widget.setLayout(layout)
                                rect.widget.setGeometry(QCursor().pos().x(), QCursor().pos().y(), 300, 100)
                                rect.widget.show()

                        except Exception as exception:
                            print(exception)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Genealogy tree')
        self.setGeometry(200, 100, 1000, 900)
        self.view = QTableView()

        layout = QHBoxLayout()

        w = QWidget()
        w.setLayout(layout)

        self.scene = self.MainScene(self)

        self.graphics_view = QGraphicsView(self.scene)
        self.graphics_view.setFixedSize(900, 900)
        self.setMouseTracking(True)

        layout.addWidget(self.graphics_view)

        database_layout = QVBoxLayout()
        layout.addLayout(database_layout)
        for i in range(5):
            database_layout.addWidget(QPushButton('kek'))

        self.setCentralWidget(w)

        self.lines = []
        self.rectangles = []
        self.scale = 1

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == 43:  # plus -> zoom in
            self.graphics_view.scale(6 / 5, 6 / 5)
            self.scale *= 6 / 5
        elif a0.key() == 45:  # minus -> zoom out
            self.graphics_view.scale(5 / 6, 5 / 6)
            self.scale *= 5 / 6
        elif a0.key() == 61:  # equal -> reset zoom
            print(self.scale)
            self.graphics_view.scale(1 / self.scale, 1 / self.scale)
            self.scale = 1

    def draw_rectangle(self, rect, pen=QPen(Qt.Qt.black), brush=QBrush(Qt.Qt.yellow)):
        object_rect = self.scene.addRect(rect.x1, rect.y1, rect.x2 - rect.x1, rect.y2 - rect.y1, pen, brush)

        self.rectangles.append((rect, object_rect))

        path = QPainterPath()
        font = QFont()
        font.setPixelSize(35)

        path.addText(rect.x1 + 5, rect.y1 + 35, font, rect.name)
        path.addText(rect.x1 + 5, rect.y1 + 80, font, rect.years)
        self.scene.addPath(path)

    def draw_line(self, line):
        color = Qt.Qt.black
        pen = QPen(color)
        pen.setWidth(3)
        self.lines.append(line)
        self.scene.addPath(line, pen)


class Human:
    pair = None
    children = None
    name = ''''''
    history = ''''''
    year_of_born = 0
    year_of_death = 0

    def __init__(self, name='''''', history='''''', year_of_born=0, year_of_death=0, pair=None, children=None):
        if children is None:
            children = []
        self.pair = pair
        self.children = list(children)
        self.name = name
        self.history = history
        self.year_of_born = year_of_born
        self.year_of_death = year_of_death

    def __eq__(self, other):
        return self.history == other.history and self.name == other.name

    def __hash__(self):
        return hash(self.name) ^ hash(self.history) ^ hash(self.year_of_born)


class Connections:
    class Rectangle:
        x1, y1, x2, y2 = 0, 0, 0, 0
        connections = []
        current_index = 0
        name = ''''''
        description = ''''''
        widget = None

        def __init__(self, x1, y1, w, h, index, name='42', years='yrs', description='''12345'''):
            self.x1 = x1
            self.y1 = y1
            self.x2 = w + self.x1
            self.y2 = h + self.y1
            self.connections = []
            self.current_index = index
            self.name = name
            self.years = years
            self.description = description

        def add_connection(self, index):
            self.connections.append(index)

    graph = []
    lines = []  # QPainterPath

    def __init__(self):
        self.graph = []
        self.lines = []

    def clear(self):
        self.graph = []
        self.lines = []

    def add_rectangle(self, x1, y1, x2, y2, name='''''', year='''''', history=''''''):
        self.graph.append(self.Rectangle(x1, y1, x2, y2, len(self.graph), name, year, history))

    def add_random_rectangle(self):
        max_x = 500
        min_x = 100
        max_y = 500
        min_y = 100
        from random import randint

        x1 = randint(min_x, max_x)
        x2 = 50

        y1 = randint(min_y, max_y)
        y2 = 50

        self.add_rectangle(x1, y1, x2, y2)

    def add_connection(self, f, t):
        self.graph[f].add_connection(t)

    def add_random_connection(self):
        n = len(self.graph)
        from random import randint
        f = randint(0, n - 1)
        t = randint(0, n - 1)
        while f == t or t in self.graph[f].connections:
            f = randint(0, n - 1)

        self.add_connection(f, t)

    def build_lines(self):
        self.lines = []

        for rectangle in self.graph:
            for to in rectangle.connections:
                mid_x1 = (rectangle.x1 + rectangle.x2) / 2
                mid_y1 = (rectangle.y1 + rectangle.y2) / 2
                mid_x2 = (self.graph[to].x1 + self.graph[to].x2) / 2
                mid_y2 = (self.graph[to].y1 + self.graph[to].y2) / 2
                path = QPainterPath()

                path.moveTo(mid_x1, mid_y1)
                path.cubicTo(mid_x1, mid_y1, (mid_x1 + mid_x2) / 2, (mid_y1 + mid_y2) / 2, mid_x2, mid_y2)

                self.lines.append(path)

        return self.lines

    def generate_connections_with_humans_structure(self, humans_list):
        data = list(humans_list)
        data_size = len(data)

        depth = [0 for _ in range(data_size)]
        index_of_human = dict((element, index) for index, element in enumerate(data))

        for index, element in enumerate(data):

            if element.pair is not None:
                depth[index_of_human[element.pair]] = depth[index] = \
                    max(depth[index], depth[index_of_human[element.pair]])

            for child in element.children:
                depth[index_of_human[child]] = max(depth[index_of_human[child]], depth[index] + 1)

        depths_elements = [[] for _ in range(max(depth) + 1)]

        for index, element in enumerate(data):
            if element in depths_elements[depth[index]]:
                current_x = depths_elements[depth[index]].index(element)
                current_x = 450 * current_x + 50
            else:
                if element.pair is None:
                    current_x = len(depths_elements[depth[index]])
                    current_x = 450 * current_x + 50
                    depths_elements[depth[index]].append(element)
                else:
                    current_x = len(depths_elements[depth[index]])
                    current_x = 450 * current_x + 50
                    depths_elements[depth[index]].append(element)
                    depths_elements[depth[index]].append(element.pair)

            current_y = depth[index] * 300 + 50
            self.add_rectangle(current_x, current_y, 300, 150, element.name,
                               '{} - {} yrs'.format(element.year_of_born, element.year_of_death), element.history)

        for index, element in enumerate(data):
            if data[index].pair is not None:
                pair_index = index_of_human[data[index].pair]
                if pair_index > index:
                    self.add_connection(index, pair_index)
            for child in data[index].children:
                child_index = index_of_human[child]
                self.add_connection(index, child_index)
        return self.build_lines()


class TreeGenerator:
    g = []

    def __init__(self):
        self.g = []

    def generate(self, size_of_graph):
        self.g = [-1 for _ in range(size_of_graph)]
        from random import randrange
        for _v_ in range(1, size_of_graph):
            self.g[_v_] = randrange(0, _v_)

        edges = []
        for _v_ in range(1, size_of_graph):
            edges.append((self.g[_v_], _v_))

        return edges


def test_case1():
    app = Qt.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    connections = Connections()
    mid_x = 400
    mid_y = 400
    r = 200
    import math

    n = 15
    for i in range(n):
        x, y = math.cos(2 * i / n * math.pi) * r + mid_x, math.sin(2 * i / n * math.pi) * r + mid_y
        connections.add_rectangle(x, y, 50, 50)

    for i in range(n):
        for j in range(i):
            connections.add_connection(i, j)

    lines = connections.build_lines()

    for _line_ in lines:
        main_window.draw_line(_line_)

    for _rect_ in connections.graph:
        main_window.draw_rectangle(_rect_)
    app.exec()


def test_case2():
    app = Qt.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    connections = Connections()

    tree_generator = TreeGenerator()

    n = 10
    edges = tree_generator.generate(n)
    for i in range(n):
        y_coord = i * 55 + 50
        connections.add_rectangle(y_coord, i * i * 5 + 50, 50, 50)

    for i, j in edges:
        connections.add_connection(i, j)

    lines = connections.build_lines()

    for _line_ in lines:
        main_window.draw_line(_line_)

    for _rect_ in connections.graph:
        main_window.draw_rectangle(_rect_)
    app.exec()


def test_case3():
    app = Qt.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    connections = Connections()

    data = open('input.txt').read().split('\n')
    human_list = [None for _ in range(len(data))]
    id_human_to_index = dict()
    id_human_to_index['None'] = None
    for index, line in enumerate(data):
        while "  " in line:
            line = line.replace('  ', ' ')
            line = line.replace('   ', ' ')
        line = line.split()
        current_len = len(line)
        name = line[1]
        description = line[2]
        year_of_born = int(line[3])
        year_of_death = int(line[4])
        pair = line[5]
        children = []
        for child_index in range(6, current_len):
            child = line[child_index]
            children.append(child)
        id_human_to_index[line[0]] = index
        human_list[index] = Human(name, description, year_of_born, year_of_death, pair, children)

    for human in human_list:
        pair_index = id_human_to_index[human.pair]
        if pair_index is None:
            human.pair = None
        else:
            human.pair = human_list[pair_index]

        for index, child in enumerate(human.children):
            human.children[index] = human_list[id_human_to_index[child]]

    lines = connections.generate_connections_with_humans_structure(human_list)

    for _line_ in lines:
        main_window.draw_line(_line_)

    for _rect_ in connections.graph:
        main_window.draw_rectangle(_rect_)
    app.exec()


if __name__ == '__main__':
    test_case3()

#    app = QApplication(sys.argv)
#    w = mainwindow.MainWindow("test.bd")
#    w.show()
#    sys.exit(app.exec_())


# #!/usr/bin/python3
# import mainwindow
# import sys
#
# from PyQt5.QtWidgets import *
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = mainwindow.MainWindow("test.bd")
#     w.show()
#     sys.exit(app.exec_())
