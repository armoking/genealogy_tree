import sys

if __name__ == '__main__':
    try:
        import human_and_time_database

        human_and_time_database.init_database()
        human_and_time_database.build_main_window(sys.argv)
    except Exception as e:
        print(e)
