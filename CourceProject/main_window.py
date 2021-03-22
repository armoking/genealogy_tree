from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QPen, QFont, QCursor, QColor
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QLabel, QWidget, QVBoxLayout, QHBoxLayout, \
    QGraphicsSceneMouseEvent, QTableView, QPushButton, QMenu, QApplication, QTextEdit, QErrorMessage, QRadioButton, \
    QGraphicsTextItem

import human_and_time_database


class MainWindow(QMainWindow):
    class MainScene(QGraphicsScene):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.prev_active_rect = None
            self.active_elements = []

        def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
            try:
                good = False
                for _event, event_object in self.parent.events:
                    if _event.x1 <= event.scenePos().x() <= _event.x2 \
                            and _event.y1 <= event.scenePos().y() <= _event.y2:
                        if self.prev_active_rect is not None:
                            self.prev_active_rect.setBrush(QBrush(QColor.fromRgb(250, 240, 240)))
                            self.prev_active_rect = None
                        event_object.setBrush(QBrush(Qt.green))
                        self.prev_active_rect = event_object
                        good = True
                if not good and self.prev_active_rect is not None:
                    self.prev_active_rect.setBrush(QBrush(QColor.fromRgb(250, 240, 240)))
                    self.prev_active_rect = None
            except Exception as e:
                print(e)

        def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
            try:
                for element in self.active_elements:
                    element.setBrush(QBrush(QColor.fromRgb(240, 240, 250)))
            except Exception as exception:
                print('error with a brush in mousePressEvent in MainScene:', exception)
            try:
                if event.button() == 2:
                    current_x, current_y = event.scenePos().x(), event.scenePos().y()

                    for rect, object_rect in self.parent.rectangles:
                        try:
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

                        except Exception as exception:
                            print(exception)
                elif event.button() == 1:
                    current_x, current_y = event.scenePos().x(), event.scenePos().y()
                    for _event, event_object in self.parent.events:
                        if _event.x1 <= current_x <= _event.x2 and _event.y1 <= current_y <= _event.y2:
                            for _rect, object_rect in self.parent.rectangles:
                                year_from = int(_rect.years.split()[0])
                                year_to = int(_rect.years.split()[2])
                                if year_from <= int(_event.years) <= year_to:
                                    object_rect.setBrush(QBrush(QColor.fromRgb(200, 200, 240)))
                                    self.active_elements.append(object_rect)
                    pass

            except Exception as e:
                print(e)
            print('finished')

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
        self.graphics_view.setMouseTracking(True)
        self.graphics_view.setFixedSize(900, 900)
        self.setMouseTracking(True)
        self.events = []

        layout.addWidget(self.graphics_view)

        database_layout = QVBoxLayout()
        layout.addLayout(database_layout)

        font = QFont('Times')
        font.setPixelSize(20)

        change_tree_structure_button = QPushButton('change structure of the tree')
        change_tree_structure_button.setFixedSize(300, 150)
        change_tree_structure_button.setFont(font)

        change_events_structure_button = QPushButton('change structure of events')
        change_events_structure_button.setFixedSize(300, 150)
        change_events_structure_button.setFont(font)

        rebuild_tree_button = QPushButton('rebuild tree')
        rebuild_tree_button.setFixedSize(300, 150)
        rebuild_tree_button.setFont(font)

        database_layout.addWidget(change_tree_structure_button)
        database_layout.addWidget(change_events_structure_button)
        database_layout.addWidget(rebuild_tree_button)

        change_events_structure_button.clicked.connect(self.change_events_structure)
        change_tree_structure_button.clicked.connect(self.change_tree_structure)
        rebuild_tree_button.clicked.connect(self.rebuild_tree)

        self.setCentralWidget(w)

        self.scale = 1
        self.db_widget = None
        self.add_element_widget = None
        self.remove_element_widget = None
        self.add_connection_widget = None
        self.remove_connection_widget = None
        self.db_widget_events = None
        self.add_event_widget = None
        self.remove_event_widget = None

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

    def change_events_structure(self):
        self.db_widget_events = QWidget()
        self.db_widget_events.setGeometry(1000, 200, 400, 100)
        self.db_widget_events.setWindowTitle('Change structure of events')

        layout = QVBoxLayout()

        add_element_in_data_base = QPushButton('add note')
        remove_element_from_data_base = QPushButton('del note')

        layout.addWidget(add_element_in_data_base)
        layout.addWidget(remove_element_from_data_base)

        add_element_in_data_base.clicked.connect(self.add_event_in_data_base)
        remove_element_from_data_base.clicked.connect(self.remove_event_from_data_base)

        self.db_widget_events.setLayout(layout)
        self.db_widget_events.show()

    def add_event_in_data_base(self):
        add_event_widget = QWidget()
        add_event_widget.setGeometry(1100, 250, 700, 200)
        add_event_widget.setWindowTitle('Add new event')
        layout = QVBoxLayout()
        first_layout = QHBoxLayout()
        second_layout = QHBoxLayout()
        layout.addLayout(first_layout)
        layout.addLayout(second_layout)
        apply_button = QPushButton('apply')

        apply_button.clicked.connect(self.apply_button_operation_add_event)
        layout.addWidget(apply_button)
        for title in ['title', 'description', 'year']:
            first_layout.addWidget(QLabel(title))
            second_layout.addWidget(QTextEdit())
        add_event_widget.setLayout(layout)
        add_event_widget.show()
        self.add_event_widget = add_event_widget

    def apply_button_operation_add_event(self):
        title = self.add_event_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
        description = self.add_event_widget.layout().itemAt(1).layout().itemAt(1).widget().toPlainText()
        year = self.add_event_widget.layout().itemAt(1).layout().itemAt(2).widget().toPlainText()

        if title and description and year:
            human_and_time_database.TimeEvent.create(title=title, description=description, date=year)
            self.add_event_widget.close()
        else:
            message = QErrorMessage(self)
            message.setWindowTitle('Input data error')
            message.showMessage('All fields must be filled')

    def remove_event_from_data_base(self):
        try:
            remove_event_widget = QWidget()
            remove_event_widget.setGeometry(1100, 250, 700, 200)
            remove_event_widget.setWindowTitle('Del event')
            layout = QVBoxLayout()
            first_layout = QHBoxLayout()
            second_layout = QHBoxLayout()
            layout.addLayout(first_layout)
            layout.addLayout(second_layout)
            apply_button = QPushButton('apply')
            print('here')
            apply_button.clicked.connect(self.apply_button_operation_del_event)
            print('here')
            layout.addWidget(apply_button)
            print('here')
            for title in ['title']:
                first_layout.addWidget(QLabel(title))
                second_layout.addWidget(QTextEdit())
            print('here')
            remove_event_widget.setLayout(layout)
            remove_event_widget.show()
            print('here')
            self.remove_event_widget = remove_event_widget
            print('here')
        except Exception as e:
            print('here', e)

    def apply_button_operation_del_event(self):
        try:
            title = self.remove_event_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
            if title:
                query = human_and_time_database.TimeEvent.select().where(
                    human_and_time_database.TimeEvent.title == title).limit(1)
                if len(list(query)) == 1:
                    human_and_time_database.TimeEvent.delete().where(
                        (human_and_time_database.TimeEvent.title == query[0].title)
                    ).execute()
                    self.remove_event_widget.close()
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

        self.remove_connection_widget = remove_connection_widget

    def apply_button_operation_remove_connection(self):
        name1 = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(0).widget().toPlainText()
        name2 = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(1).widget().toPlainText()
        spouse_connection = self.remove_connection_widget.layout().itemAt(1).layout().itemAt(2).layout().itemAt(
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

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == 43:  # plus -> zoom in
            self.graphics_view.scale(6 / 5, 6 / 5)
            self.scale *= 6 / 5
        elif a0.key() == 45:  # minus -> zoom out
            self.graphics_view.scale(5 / 6, 5 / 6)
            self.scale *= 5 / 6
        elif a0.key() == 61:  # equal -> reset zoom
            self.graphics_view.scale(1 / self.scale, 1 / self.scale)
            self.scale = 1

    def draw_rectangle(self, rect, pen=QPen(Qt.black, 8, Qt.SolidLine), brush=QBrush(QColor.fromRgb(240, 240, 255))):
        object_rect = self.scene.addRect(rect.x1, rect.y1, rect.x2 - rect.x1, rect.y2 - rect.y1, pen, brush)

        self.rectangles.append((rect, object_rect))

        text_name = QGraphicsTextItem(rect.name)
        text_years = QGraphicsTextItem(rect.years)
        text_name.setPos(rect.x1 + 15, rect.y1 + 15)
        text_years.setPos(rect.x1 + 15, rect.y1 + 70)
        font = QFont()
        font.setBold(False)
        font.setPixelSize(35)
        text_name.setFont(font)
        text_years.setFont(font)

        self.scene.addItem(text_name)
        self.scene.addItem(text_years)

    def relax(self):
        kx = self.graphics_view.size().width() / max(1, self.graphics_view.sceneRect().width())
        ky = self.graphics_view.height() / max(1, self.graphics_view.sceneRect().height())
        k = min(kx, ky) * 2
        self.graphics_view.scale(k, k)

    def draw_line(self, line):
        color = Qt.black
        pen = QPen(color, 8, Qt.SolidLine)
        self.lines.append(line)
        self.scene.addPath(line, pen)

    def draw_event(self, event, min_x, max_x, min_y, max_y, pen=QPen(Qt.black, 3, Qt.SolidLine),
                   brush=QBrush(QColor.fromRgb(250, 240, 240))):

        object_event = self.scene.addRect(event.x1, event.y1, event.x2 - event.x1, event.y2 - event.y1, pen, brush)

        text = event.description.split()
        pre = 0
        result_text = event.name + '\n\n'
        for word in text:
            if pre + len(word) > 50:
                pre = 0
                result_text += '\n'
            pre += len(word) + 1
            result_text += word + ' '

        object_event.setToolTip(result_text)
        self.events.append((event, object_event))

        text_event = QGraphicsTextItem(str(event.years))
        text_event.setPos(event.x1 + 5, event.y1 + 5)
        font = QFont()
        font.setBold(False)
        font.setPixelSize(25)
        text_event.setFont(font)
        text_event.setFont(font)
        self.scene.addItem(text_event)
