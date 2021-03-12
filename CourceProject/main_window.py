from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QCursor
from PyQt5.QtGui import QPainterPath, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QGraphicsSceneMouseEvent, QTableView, QPushButton, QMenu, QApplication, QTextEdit, QErrorMessage, QRadioButton

import human_and_time_database


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
                                rect.widget.setWindowTitle('Biography of {}'.format(rect.name))
                                layout = QHBoxLayout()
                                label = QLabel()
                                label.setText(rect.description)
                                layout.addWidget(label)
                                rect.widget.setLayout(layout)
                                rect.widget.setGeometry(QCursor().pos().x(), QCursor().pos().y(), 500, 200)
                                rect.widget.show()

                        except Exception as exception:
                            print(exception)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        import sys
        sys.exit(0)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Genealogy tree')
        self.setGeometry(500, 50, 1000, 900)
        self.view = QTableView()

        layout = QHBoxLayout()

        w = QWidget(self)
        w.setLayout(layout)

        self.scene = self.MainScene(self)

        self.graphics_view = QGraphicsView(self.scene)
        self.graphics_view.setFixedSize(900, 900)
        self.setMouseTracking(True)

        layout.addWidget(self.graphics_view)

        database_layout = QVBoxLayout()
        layout.addLayout(database_layout)

        font = QFont('Times')
        font.setPixelSize(20)
        change_tree_structure_button = QPushButton('change structure of the tree')
        change_tree_structure_button.setFixedSize(300, 150)
        change_tree_structure_button.setFont(font)
        rebuild_tree_button = QPushButton('rebuild tree')
        rebuild_tree_button.setFixedSize(300, 150)
        rebuild_tree_button.setFont(font)
        database_layout.addWidget(change_tree_structure_button)
        database_layout.addWidget(rebuild_tree_button)

        change_tree_structure_button.clicked.connect(self.change_tree_structure)
        rebuild_tree_button.clicked.connect(self.rebuild_tree)

        self.setCentralWidget(w)

        self.lines = []
        self.rectangles = []
        self.scale = 1
        self.db_widget = None
        self.add_element_widget = None
        self.remove_element_widget = None
        self.add_connection_widget = None
        self.remove_connection_widget = None

    def change_tree_structure(self):
        self.db_widget = QWidget()
        self.db_widget.setGeometry(1000, 200, 400, 100)
        self.db_widget.setWindowTitle('Change structure of the tree')

        layout = QVBoxLayout()

        add_element_in_data_base = QPushButton('add note')
        remove_element_from_data_base = QPushButton('del note')
        add_connection_in_data_base = QPushButton('add connection')
        remove_connection_in_data_base = QPushButton('del connection')

        layout.addWidget(add_element_in_data_base)
        layout.addWidget(remove_element_from_data_base)
        layout.addWidget(add_connection_in_data_base)
        layout.addWidget(remove_connection_in_data_base)

        add_element_in_data_base.clicked.connect(self.add_element_in_data_base)
        remove_element_from_data_base.clicked.connect(self.remove_element_from_data_base)
        add_connection_in_data_base.clicked.connect(self.add_connection_in_data_base)
        remove_connection_in_data_base.clicked.connect(self.remove_connection_in_data_base)

        self.db_widget.setLayout(layout)
        self.db_widget.show()

    def add_element_in_data_base(self):
        add_element_widget = QWidget()
        add_element_widget.setGeometry(1100, 250, 700, 200)
        add_element_widget.setWindowTitle('Add element')
        layout = QVBoxLayout()
        first_layout = QHBoxLayout()
        second_layout = QHBoxLayout()
        layout.addLayout(first_layout)
        layout.addLayout(second_layout)
        apply_button = QPushButton('apply')

        apply_button.clicked.connect(self.apply_button_operation_add_element)
        layout.addWidget(apply_button)
        for title in ['name', 'biography', 'year of born', 'year of death']:
            first_layout.addWidget(QLabel(title))
            second_layout.addWidget(QTextEdit())
        add_element_widget.setLayout(layout)
        add_element_widget.show()
        self.add_element_widget = add_element_widget

    def apply_button_operation_add_element(self):
        name = self.add_element_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
        biography = self.add_element_widget.layout().itemAt(1).layout().itemAt(1).widget().toPlainText()
        year_of_born = self.add_element_widget.layout().itemAt(1).layout().itemAt(2).widget().toPlainText()
        year_of_death = self.add_element_widget.layout().itemAt(1).layout().itemAt(3).widget().toPlainText()

        if name and biography and year_of_death and year_of_death:
            human_and_time_database.HumanModel.create(name=name, biography=biography,
                                                      year_of_born=year_of_born,
                                                      year_of_death=year_of_death)
            self.add_element_widget.close()
        else:
            message = QErrorMessage(self)
            message.setWindowTitle('Input data error')
            message.showMessage('All fields must be filled')

    def remove_element_from_data_base(self):
        try:
            remove_element_widget = QWidget()
            remove_element_widget.setGeometry(1100, 250, 700, 200)
            remove_element_widget.setWindowTitle('Del element')
            layout = QVBoxLayout()
            first_layout = QHBoxLayout()
            second_layout = QHBoxLayout()
            layout.addLayout(first_layout)
            layout.addLayout(second_layout)
            apply_button = QPushButton('apply')

            apply_button.clicked.connect(self.apply_button_operation_del_element)
            layout.addWidget(apply_button)
            for title in ['name']:
                first_layout.addWidget(QLabel(title))
                second_layout.addWidget(QTextEdit())
            remove_element_widget.setLayout(layout)
            remove_element_widget.show()
            self.remove_element_widget = remove_element_widget

        except Exception as e:
            print(e)

    def apply_button_operation_del_element(self):
        try:
            name = self.remove_element_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
            if name:
                query = human_and_time_database.HumanModel.select().where(
                    human_and_time_database.HumanModel.name == name).limit(1)
                if len(list(query)) == 1:
                    human = query[0]

                    new_rows = []
                    for row in human_and_time_database.RelationTable.select():
                        if human.id in [row.spouse, row.parent1, row.parent2]:
                            current_human = row.human
                            current_spouse = None if row.spouse == human.id else row.spouse
                            current_parent1 = None if row.parent1 == human.id else row.parent1
                            current_parent2 = None if row.parent2 == human.id else row.parent2
                            new_rows.append((current_human, current_spouse, current_parent1, current_parent2))

                    human_and_time_database.RelationTable.delete().where(
                        (human_and_time_database.RelationTable.human == human.id) |
                        (human_and_time_database.RelationTable.spouse == human.id) |
                        (human_and_time_database.RelationTable.parent1 == human.id) |
                        (human_and_time_database.RelationTable.parent2 == human.id)
                    ).execute()

                    for h, s, p1, p2 in new_rows:
                        human_and_time_database.RelationTable.create(human=h, spouse=s,
                                                                     parent1=p1,
                                                                     parent2=p2)

                    human_and_time_database.HumanModel.delete().where(
                        human_and_time_database.HumanModel.name == name
                    ).execute()

                    self.remove_element_widget.close()
                else:
                    message = QErrorMessage(self)
                    message.setWindowTitle('Input data error')
                    message.showMessage('No such node in the tree')
            else:
                message = QErrorMessage(self)
                message.setWindowTitle('Input data error')
                message.showMessage('All fields must be filled')
        except Exception as e:
            print('apply_button_operation_del_element: ', e)

    def add_connection_in_data_base(self):
        add_connection_widget = QWidget()
        add_connection_widget.setGeometry(1100, 250, 700, 200)
        add_connection_widget.setWindowTitle('Add connection')
        layout = QVBoxLayout()
        first_layout = QHBoxLayout()
        second_layout = QHBoxLayout()
        layout.addLayout(first_layout)
        layout.addLayout(second_layout)
        apply_button = QPushButton('apply')

        apply_button.clicked.connect(self.apply_button_operation_add_connection)
        layout.addWidget(apply_button)
        for title in ['name 1', 'name 2']:
            first_layout.addWidget(QLabel(title))
            second_layout.addWidget(QTextEdit())

        third_layout = QVBoxLayout()
        second_layout.addLayout(third_layout)
        first_layout.addWidget(QLabel(''))
        first_layout.addWidget(QLabel('Type of connection'))

        first_button = QRadioButton('spouse - spouse connection')
        first_button.setChecked(True)
        second_button = QRadioButton('parent - child connection')

        third_layout.addWidget(first_button)
        third_layout.addWidget(second_button)

        add_connection_widget.setLayout(layout)
        add_connection_widget.show()
        self.add_connection_widget = add_connection_widget

    def apply_button_operation_add_connection(self):
        name1 = self.add_connection_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
        name2 = self.add_connection_widget.layout().itemAt(1).layout().itemAt(1).widget().toPlainText()
        spouse_connection = self.add_connection_widget.layout().itemAt(1).layout().itemAt(2).layout().itemAt(
            0).widget().isChecked()
        try:
            if name1 and name2:
                human_1 = human_and_time_database.HumanModel.select().where(
                    human_and_time_database.HumanModel.name == name1)
                human_2 = human_and_time_database.HumanModel.select().where(
                    human_and_time_database.HumanModel.name == name2)

                if len(human_1) != 1 or len(human_2) != 1:
                    message = QErrorMessage(self)
                    message.setWindowTitle('Input data error')
                    message.showMessage('No human with set name in the tree')
                    return
                human_1 = human_1[0]
                human_2 = human_2[0]

                human_id1 = human_1.id
                human_id2 = human_2.id
                if human_id1 == human_id2:
                    message = QErrorMessage(self)
                    message.setWindowTitle('Input data error')
                    message.showMessage('Cant create a connection between human and himself')
                    return
                print('okay')
                if spouse_connection:
                    all_connections = human_and_time_database.RelationTable.select()

                    graph = dict()
                    for connection in all_connections:
                        human = connection.human
                        spouse = connection.spouse
                        parent1 = connection.parent1
                        parent2 = connection.parent2
                        graph[human] = (spouse, parent1, parent2)

                    if human_id1 not in graph:
                        graph[human_id1] = (None, None, None)

                    if human_id2 not in graph:
                        graph[human_id2] = (None, None, None)

                    if graph[human_id1][0] == human_id2:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('Connection already exists')
                        return

                    if graph[human_id1][0] is not None or graph[human_id2][0] is not None:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('Another connection already exists with at least one of humans')
                        return

                    queue = [human_id1]
                    i = 0
                    used = set()
                    while i < len(queue):
                        v = queue[i]
                        if v is None or v in used:
                            i += 1
                            continue
                        used.add(v)
                        if v == human_id2:
                            message = QErrorMessage(self)
                            message.setWindowTitle('Input data error')
                            message.showMessage('Cyclic dependence! The connection cannot be built')
                            return

                        queue.append(graph[v][0])
                        queue.append(graph[v][1])
                        queue.append(graph[v][2])

                    queue = [human_id2]
                    i = 0
                    used = set()
                    while i < len(queue):
                        v = queue[i]
                        if v is None or v in used:
                            i += 1
                            continue
                        used.add(v)
                        if v == human_id1:
                            message = QErrorMessage(self)
                            message.setWindowTitle('Input data error')
                            message.showMessage('Cyclic dependence! The connection cannot be built')
                            return

                        queue.append(graph[v][0])
                        queue.append(graph[v][1])
                        queue.append(graph[v][2])

                    human_1 = human_id1
                    human_1_spouse = human_id2
                    human_1_parent1 = graph[human_id1][1]
                    human_1_parent2 = graph[human_id1][2]

                    human_2 = human_id2
                    human_2_spouse = human_id1
                    human_2_parent1 = graph[human_id2][1]
                    human_2_parent2 = graph[human_id2][2]

                    human_and_time_database.RelationTable.delete().where(
                        (human_and_time_database.RelationTable.human == human_1) |
                        (human_and_time_database.RelationTable.human == human_2)
                    ).execute()

                    human_and_time_database.RelationTable.create(human=human_1, spouse=human_1_spouse,
                                                                 parent1=human_1_parent1, parent2=human_1_parent2)

                    human_and_time_database.RelationTable.create(human=human_2, spouse=human_2_spouse,
                                                                 parent1=human_2_parent1, parent2=human_2_parent2)

                    self.add_connection_widget.close()
                else:
                    all_connections = human_and_time_database.RelationTable.select()

                    graph = dict()
                    for connection in all_connections:
                        human = connection.human
                        spouse = connection.spouse
                        parent1 = connection.parent1
                        parent2 = connection.parent2
                        graph[human] = (spouse, parent1, parent2)

                    if human_id1 not in graph:
                        graph[human_id1] = (None, None, None)

                    if human_id2 not in graph:
                        graph[human_id2] = (None, None, None)

                    if graph[human_id2][1] == human_id1 or graph[human_id2][2] == human_id1:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('Connection already exists')
                        return

                    print(graph[human_id2])
                    if graph[human_id2][1] is not None and graph[human_id2][2] is not None:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('The child already has two parents')
                        return

                    queue = [human_id1]
                    i = 0
                    used = set()
                    while i < len(queue):
                        v = queue[i]
                        if v is None or v in used:
                            i += 1
                            continue
                        used.add(v)
                        if v == human_id2:
                            message = QErrorMessage(self)
                            message.setWindowTitle('Input data error')
                            message.showMessage('Cyclic dependence! The connection cannot be built')
                            return

                        queue.append(graph[v][0])
                        queue.append(graph[v][1])
                        queue.append(graph[v][2])

                    queue = [human_id2]
                    i = 0
                    used = set()
                    while i < len(queue):
                        v = queue[i]
                        if v is None or v in used:
                            i += 1
                            continue
                        used.add(v)
                        if v == human_id1:
                            message = QErrorMessage(self)
                            message.setWindowTitle('Input data error')
                            message.showMessage('Cyclic dependence! The connection cannot be built')
                            return

                        queue.append(graph[v][0])
                        queue.append(graph[v][1])
                        queue.append(graph[v][2])

                    human_1 = human_id1
                    human_1_spouse = graph[human_id1][0]
                    human_1_parent1 = graph[human_id1][1]
                    human_1_parent2 = graph[human_id1][2]

                    human_2 = human_id2
                    human_2_spouse = graph[human_id2][0]
                    human_2_parent1 = graph[human_id2][1]
                    human_2_parent2 = graph[human_id2][2]
                    if human_2_parent1 is None:
                        human_2_parent1 = human_1
                    else:
                        human_2_parent2 = human_1

                    human_and_time_database.RelationTable.delete().where(
                        (human_and_time_database.RelationTable.human == human_1) |
                        (human_and_time_database.RelationTable.human == human_2)
                    ).execute()

                    human_and_time_database.RelationTable.create(human=human_1, spouse=human_1_spouse,
                                                                 parent1=human_1_parent1, parent2=human_1_parent2)

                    human_and_time_database.RelationTable.create(human=human_2, spouse=human_2_spouse,
                                                                 parent1=human_2_parent1, parent2=human_2_parent2)

                    self.add_connection_widget.close()


            else:
                message = QErrorMessage(self)
                message.setWindowTitle('Input data error')
                message.showMessage('All fields must be filled')

        except Exception as e:
            print(e)

    def remove_connection_in_data_base(self):
        remove_connection_widget = QWidget()
        remove_connection_widget.setGeometry(1100, 250, 700, 200)
        remove_connection_widget.setWindowTitle('Add connection')
        layout = QVBoxLayout()
        first_layout = QHBoxLayout()
        second_layout = QHBoxLayout()
        layout.addLayout(first_layout)
        layout.addLayout(second_layout)
        apply_button = QPushButton('apply')

        apply_button.clicked.connect(self.apply_button_operation_remove_connection)
        layout.addWidget(apply_button)
        for title in ['name 1', 'name 2']:
            first_layout.addWidget(QLabel(title))
            second_layout.addWidget(QTextEdit())

        third_layout = QVBoxLayout()
        second_layout.addLayout(third_layout)
        first_layout.addWidget(QLabel(''))
        first_layout.addWidget(QLabel('Type of connection'))

        first_button = QRadioButton('spouse - spouse connection')
        first_button.setChecked(True)

        second_button = QRadioButton('parent - child connection')

        third_layout.addWidget(first_button)
        third_layout.addWidget(second_button)

        remove_connection_widget.setLayout(layout)
        remove_connection_widget.show()
        print('okay')
        self.remove_connection_widget = remove_connection_widget

    def apply_button_operation_remove_connection(self):
        name1 = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
        name2 = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(1).widget().toPlainText()
        spouse_connection = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(2).layout().itemAt(
            0).widget().isChecked()
        print(name1, name2)
        try:
            if name1 and name2:
                human_1 = human_and_time_database.HumanModel.select().where(
                    human_and_time_database.HumanModel.name == name1)
                human_2 = human_and_time_database.HumanModel.select().where(
                    human_and_time_database.HumanModel.name == name2)

                if len(human_1) != 1 or len(human_2) != 1:
                    message = QErrorMessage(self)
                    message.setWindowTitle('Input data error')
                    message.showMessage('No human with set name in the tree')
                    return
                human_1 = human_1[0]
                human_2 = human_2[0]

                human_id1 = human_1.id
                human_id2 = human_2.id
                if human_id1 == human_id2:
                    message = QErrorMessage(self)
                    message.setWindowTitle('Input data error')
                    message.showMessage('No connection between human and himself')
                    return
                if spouse_connection:
                    all_connections = human_and_time_database.RelationTable.select()

                    graph = dict()
                    for connection in all_connections:
                        human = connection.human
                        spouse = connection.spouse
                        parent1 = connection.parent1
                        parent2 = connection.parent2
                        graph[human] = (spouse, parent1, parent2)

                    if human_id1 not in graph:
                        graph[human_id1] = (None, None, None)

                    if human_id2 not in graph:
                        graph[human_id2] = (None, None, None)

                    if graph[human_id1][0] != human_id2:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('No connection')
                        return

                    human_1 = human_id1
                    human_1_spouse = None
                    human_1_parent1 = graph[human_id1][1]
                    human_1_parent2 = graph[human_id1][2]

                    human_2 = human_id2
                    human_2_spouse = None
                    human_2_parent1 = graph[human_id2][1]
                    human_2_parent2 = graph[human_id2][2]

                    human_and_time_database.RelationTable.delete().where(
                        (human_and_time_database.RelationTable.human == human_1) |
                        (human_and_time_database.RelationTable.human == human_2)
                    ).execute()

                    human_and_time_database.RelationTable.create(human=human_1, spouse=human_1_spouse,
                                                                 parent1=human_1_parent1, parent2=human_1_parent2)

                    human_and_time_database.RelationTable.create(human=human_2, spouse=human_2_spouse,
                                                                 parent1=human_2_parent1, parent2=human_2_parent2)

                    self.remove_connection_widget.close()
                else:
                    all_connections = human_and_time_database.RelationTable.select()

                    graph = dict()
                    for connection in all_connections:
                        human = connection.human
                        spouse = connection.spouse
                        parent1 = connection.parent1
                        parent2 = connection.parent2
                        graph[human] = (spouse, parent1, parent2)

                    if human_id1 not in graph:
                        graph[human_id1] = (None, None, None)

                    if human_id2 not in graph:
                        graph[human_id2] = (None, None, None)

                    if graph[human_id2][1] != human_id1 and graph[human_id2][2] != human_id1:
                        message = QErrorMessage(self)
                        message.setWindowTitle('Input data error')
                        message.showMessage('No connection')
                        return

                    human_1 = human_id1
                    human_1_spouse = graph[human_id1][0]
                    human_1_parent1 = graph[human_id1][1]
                    human_1_parent2 = graph[human_id1][2]

                    human_2 = human_id2
                    human_2_spouse = graph[human_id2][0]
                    human_2_parent1 = graph[human_id2][1]
                    human_2_parent2 = graph[human_id2][2]

                    if human_2_parent1 == human_1:
                        human_2_parent1 = None
                    else:
                        human_2_parent2 = None

                    human_and_time_database.RelationTable.delete().where(
                        (human_and_time_database.RelationTable.human == human_1) |
                        (human_and_time_database.RelationTable.human == human_2)
                    ).execute()

                    human_and_time_database.RelationTable.create(human=human_1, spouse=human_1_spouse,
                                                                 parent1=human_1_parent1, parent2=human_1_parent2)

                    human_and_time_database.RelationTable.create(human=human_2, spouse=human_2_spouse,
                                                                 parent1=human_2_parent1, parent2=human_2_parent2)

                    self.remove_connection_widget.close()

            else:
                message = QErrorMessage(self)
                message.setWindowTitle('Input data error')
                message.showMessage('All fields must be filled')

        except Exception as e:
            print(e)

    def rebuild_tree(self):
        try:
            human_and_time_database.build_tree_from_database(self)
        except Exception as e:
            print(e)
        print('CHANGE')

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

    def draw_rectangle(self, rect, pen=QPen(Qt.black, 8, Qt.SolidLine), brush=QBrush(QColor.fromRgb(220, 214, 240))):
        object_rect = self.scene.addRect(rect.x1, rect.y1, rect.x2 - rect.x1, rect.y2 - rect.y1, pen, brush)

        self.rectangles.append((rect, object_rect))

        path = QPainterPath()
        font = QFont()
        font.setPixelSize(35)

        path.addText(rect.x1 + 5, rect.y1 + 35, font, rect.name)
        path.addText(rect.x1 + 5, rect.y1 + 80, font, rect.years)
        self.scene.addPath(path)

    def relax(self):
        kx = self.graphics_view.size().width() / max(1, self.graphics_view.sceneRect().width())
        ky = self.graphics_view.height() / max(1, self.graphics_view.sceneRect().height())
        k = min(kx, ky) * 0.95
        self.graphics_view.scale(k, k)

    def draw_line(self, line):
        color = Qt.black
        pen = QPen(color, 8, Qt.SolidLine)
        self.lines.append(line)
        self.scene.addPath(line, pen)
