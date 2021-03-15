from PyQt5.QtGui import QPainterPath


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
        return self.history == other.history and self.name == other.name \
               and self.year_of_born == other.year_of_born and self.year_of_death == other.year_of_death

    def __hash__(self):
        return hash(self.name) ^ hash(self.history) ^ hash(self.year_of_born) ^ hash(self.year_of_death)


class Connections:
    class Rectangle:
        x1, y1, x2, y2 = 0, 0, 0, 0
        connections = []
        current_index = 0
        name = ''''''
        description = ''''''
        year = 0
        widget = None

        def __init__(self, x1, y1, w, h, index=0, name='42', years='yrs', description='''12345'''):
            self.x1 = x1
            self.y1 = y1
            self.x2 = w + self.x1
            self.y2 = h + self.y1
            self.connections = []
            self.current_index = index
            self.name = name
            self.years = years
            self.description = description

        def add_connection(self, parent_a, parent_b=-1):
            if parent_b == -1:
                self.connections.append((parent_a,))
            else:
                self.connections.append((parent_a, parent_b))

    events = []
    graph = []
    lines = []  # QPainterPath

    def __init__(self):
        self.graph = []
        self.lines = []
        self.events = []

    def clear(self):
        self.graph = []
        self.lines = []
        self.events = []

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

    def add_connection(self, child, a, b=-1):
        self.graph[child].add_connection(a, b)

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
                if len(to) == 1 or to[1] is None:
                    to = to[0]
                    mid_x1 = (rectangle.x1 + rectangle.x2) / 2
                    mid_y1 = (rectangle.y1 + rectangle.y2) / 2
                    mid_x2 = (self.graph[to].x1 + self.graph[to].x2) / 2
                    mid_y2 = (self.graph[to].y1 + self.graph[to].y2) / 2
                    path = QPainterPath()

                    path.moveTo(mid_x1, mid_y1)
                    path.cubicTo(mid_x1, mid_y1, (mid_x1 + mid_x2) / 2, (mid_y1 + mid_y2) / 2, mid_x2, mid_y2)

                    self.lines.append(path)
                else:
                    a, b = to

                    mid_x1 = (rectangle.x1 + rectangle.x2) / 2
                    mid_y1 = rectangle.y1
                    mid_xa = (self.graph[a].x1 + self.graph[a].x2) / 2
                    mid_ya = (self.graph[a].y1 + self.graph[a].y2) / 2
                    mid_xb = (self.graph[b].x1 + self.graph[b].x2) / 2
                    mid_yb = (self.graph[b].y1 + self.graph[b].y2) / 2
                    path = QPainterPath()

                    mid_x2 = (mid_xa + mid_xb) / 2
                    mid_y2 = (mid_ya + mid_yb) / 2

                    mid_x1, mid_y1, mid_x2, mid_y2 = mid_x2, mid_y2, mid_x1, mid_y1

                    path.moveTo(mid_x1, mid_y1)

                    if mid_y1 != mid_y2:
                        mid_y1 += 100
                        path.lineTo(mid_x1, mid_y1)
                        mid_y2 -= 100
                        path.lineTo(mid_x2, mid_y2)
                        path.lineTo(mid_x2, mid_y2 + 100)
                    else:
                        path.lineTo(mid_x2, mid_y2)

                    self.lines.append(path)

        return self.lines

    def generate_connections_with_humans_structure(self, humans_list):
        data = list(humans_list)
        data_size = len(data)

        depth = [0 for _ in range(data_size)]
        index_of_human = dict((element, index) for index, element in enumerate(data))

        changed = True
        iterations = 0
        while changed:
            iterations += 1
            changed = False
            for index, element in enumerate(data):
                if element.pair is not None:
                    pair_depth = depth[index_of_human[element.pair]]
                    if pair_depth > depth[index]:
                        changed = True
                        depth[index] = pair_depth
                for child in element.children:
                    if depth[index] + 1 > depth[index_of_human[child]]:
                        changed = True
                        depth[index_of_human[child]] = max(depth[index_of_human[child]], depth[index] + 1)
        print('Iterations =', iterations)
        depths_elements = [[] for _ in range(max(depth) + 1)]

        for index, element in enumerate(data):
            if element in depths_elements[depth[index]]:
                current_x = 450 * depths_elements[depth[index]].index(element) + 50
            else:
                current_x = 450 * len(depths_elements[depth[index]]) + 50
                depths_elements[depth[index]].append(element)
                if element.pair is not None:
                    depths_elements[depth[index]].append(element.pair)

            current_y = depth[index] * 450 + 50
            self.add_rectangle(current_x, current_y, 400, 150, element.name,
                               '{} - {} yrs'.format(element.year_of_born, element.year_of_death), element.history)

        for index, element in enumerate(data):
            pair_index = -1
            if data[index].pair is not None:
                pair_index = index_of_human[data[index].pair]
                if pair_index > index:
                    self.add_connection(index, pair_index)
            for child in data[index].children:
                child_index = index_of_human[child]
                self.add_connection(child_index, index, pair_index)
        return self.build_lines()

    def generate_events_rectangles(self, min_x, max_x, min_y, max_y, linearly_distributed=True):
        selected_events = self.events
        max_year = max(int(event.date) for event in selected_events)
        min_year = min(int(event.date) for event in selected_events)

        result = []
        iteration = 0
        length = len(selected_events)

        for event in selected_events:
            if linearly_distributed:
                iteration += 1
                current_y = iteration / length * (max_y - min_y) - 100
            else:
                current_y = (int(event.date) - min_year) / (max_year - min_year) * (max_y - min_y)
            result.append(
                Connections.Rectangle(min_x, current_y, max_x - min_x, 50, description=event.description,
                                      years=event.date, name=event.title))

        return result


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
