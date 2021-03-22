from peewee import Model, CharField, SqliteDatabase, DateField, Field
from settings import *
from connections import *
from main_window import *

import os

os.remove(DATABASE_LOCATION)
main_database = SqliteDatabase(DATABASE_LOCATION)
id_to_rectangle = dict()


class BaseModel(Model):
    class Meta:
        database = main_database


class HumanModel(BaseModel):
    name = CharField(null=False)
    biography = CharField(null=False)
    year_of_born = DateField()
    year_of_death = DateField()

    class Meta:
        db_table = 'Human'


class RelationTable(BaseModel):
    human = Field(HumanModel, unique=True)
    spouse = Field(HumanModel)
    parent1 = Field(HumanModel)
    parent2 = Field(HumanModel)

    class Meta:
        db_table = 'RelativeTable'


class TimeEvent(BaseModel):
    title = CharField(unique=True)
    description = CharField()
    date = DateField()

    class Meta:
        db_table = 'TimeEvent'


def find_human_model_by_human(human):
    return HumanModel.select().where(HumanModel.name == human.name).limit(1)[0]


def get_human_by_id(index):
    if index is None:
        return None
    return HumanModel.get(index)


def init_database():
    try:
        global main_database
        main_database.create_tables([HumanModel, RelationTable, TimeEvent])

        # reading the default data:
        data = open('input.txt', encoding='utf-8').read().split('\n')
        human_list = [None for _ in range(len(data))]
        id_human_to_index = dict()
        id_human_to_index['None'] = None
        for index, line in enumerate(data):
            while "  " in line:
                line = line.replace('  ', ' ')
                line = line.replace('   ', ' ')
            line = line.split(',')
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
            if human.children == ['None']:
                human.children = []
            for index, child in enumerate(human.children):
                human.children[index] = human_list[id_human_to_index[child]]

        for human in human_list:
            row = HumanModel.create(name=human.name, biography=human.history, year_of_born=human.year_of_born,
                                    year_of_death=human.year_of_death)
            row.save()

        parents = dict((human, []) for human in human_list)

        for human in human_list:
            for child in human.children:
                parents[child].append(human)

        for human in human_list:
            current_human = HumanModel.select().where(HumanModel.name == human.name).limit(1)[0]
            spouse = None if human.pair is None else find_human_model_by_human(human.pair)
            parent1 = None if len(parents[human]) <= 0 else find_human_model_by_human(parents[human][0])
            parent2 = None if len(parents[human]) <= 1 else find_human_model_by_human(parents[human][1])

            if human.pair is not None:
                spouse = HumanModel.select().where(HumanModel.name == human.pair.name).limit(1)[0]

            RelationTable.create(human=current_human, spouse=spouse, parent1=parent1, parent2=parent2)

        with open('input_events.txt', encoding='utf-8') as inp:
            input_events = inp.read().split('\n')
            for event in input_events:
                event = event.split(',')
                TimeEvent.create(title=event[1], description=event[2], date=event[0])

    except Exception as e:
        print('error in init_database:', e)


def build_tree_from_database(main_window):
    try:
        if main_window.scene.prev_active_rect is not None:
            main_window.scene.prev_active_rect.setBrush(QBrush(QColor.fromRgb(250, 240, 240)))
            main_window.scene.prev_active_rect = None
        for element in main_window.scene.active_elements:
            element.setBrush(QBrush(QColor.fromRgb(240, 240, 250)))
            main_window.scene.active_elements = []
    except Exception as e:
        print(e)

    main_window.scene.clear()
    main_window.rectangles = []
    main_window.events = []
    main_window.lines = []
    main_window.scene.prev_active_rect = None

    connections = Connections()
    human_list = []
    index_of_human = dict()

    for human in HumanModel.select():
        human_list.append(Human(human.name, human.biography, human.year_of_born, human.year_of_death))
        index_of_human[human] = len(human_list) - 1

    for relation in RelationTable.select():
        human = get_human_by_id(relation.human)
        spouse = get_human_by_id(relation.spouse)
        parent1 = get_human_by_id(relation.parent1)
        parent2 = get_human_by_id(relation.parent2)

        if spouse is not None:
            human_list[index_of_human[human]].pair = human_list[index_of_human[spouse]]

        for parent in [parent1, parent2]:
            if parent is not None:
                human_list[index_of_human[parent]].children.append(human_list[index_of_human[human]])

    lines = connections.generate_connections_with_humans_structure(human_list)

    for _line_ in lines:
        main_window.draw_line(_line_)

    for _rect_ in connections.graph:
        main_window.draw_rectangle(_rect_)

    min_y = 0
    max_y = 100

    if len(connections.graph):
        min_y = connections.graph[0].y1
        max_y = connections.graph[0].y2

    for _rect_ in connections.graph:
        min_y = min(min_y, _rect_.y1)
        max_y = max(max_y, _rect_.y2)

    min_x = -200
    max_x = 0

    main_window.scene.addRect(min_x, min_y - 50, max_x - min_x, max_y + 100 - min_y,
                              QPen(Qt.black, 2, Qt.SolidLine),
                              QBrush(QColor.fromRgb(240, 250, 240)))

    events = TimeEvent.select()

    length = len(events)

    if length == 0:
        return

    events = sorted(events, key=lambda x: int(x.date))
    for event in events:
        connections.events.append(event)

    draw_events = connections.generate_events_rectangles(min_x, max_x, min_y, max_y, LINEARLY_DISTRIBUTED)
    for _event_ in draw_events:
        main_window.draw_event(_event_, min_x, max_x, min_y, max_y)


def build_main_window(argv):
    try:
        app = QApplication(argv)
        main_window = MainWindow()
        main_window.show()

        build_tree_from_database(main_window)
        main_window.relax()
        app.exec()
    except Exception as e:
        print('Error in build_main_window:', e)
