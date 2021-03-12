import sys

# def test_case1():
#     app = Qt.QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     connections = Connections()
#     mid_x = 400
#     mid_y = 400
#     r = 200
#     import math
#
#     n = 15
#     for i in range(n):
#         x, y = math.cos(2 * i / n * math.pi) * r + mid_x, math.sin(2 * i / n * math.pi) * r + mid_y
#         connections.add_rectangle(x, y, 50, 50)
#
#     for i in range(n):
#         for j in range(i):
#             connections.add_connection(i, j)
#
#     lines = connections.build_lines()
#
#     for _line_ in lines:
#         main_window.draw_line(_line_)
#
#     for _rect_ in connections.graph:
#         main_window.draw_rectangle(_rect_)
#     app.exec()
# def test_case2():
#     app = Qt.QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     connections = Connections()
#
#     tree_generator = TreeGenerator()
#
#     n = 10
#     edges = tree_generator.generate(n)
#     for i in range(n):
#         y_coord = i * 55 + 50
#         connections.add_rectangle(y_coord, i * i * 5 + 50, 50, 50)
#
#     for i, j in edges:
#         connections.add_connection(i, j)
#
#     lines = connections.build_lines()
#
#     for _line_ in lines:
#         main_window.draw_line(_line_)
#
#     for _rect_ in connections.graph:
#         main_window.draw_rectangle(_rect_)
#     app.exec()

if __name__ == '__main__':
    import human_and_time_database

    human_and_time_database.init_database()
    human_and_time_database.build_main_window(sys.argv)

