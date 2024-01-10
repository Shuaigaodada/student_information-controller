from frame import Screen, Window, Pair

Screen.init()

Screen.main.clear()
WIDTH, HEIGHT = Screen.size()
stdscr = Screen.main

# main menu
toolLine: Window = Screen.new_window(WIDTH, 5, 0, 0)
toolLine.create_box("|", "|", "-", "-", "+", "+", "+", "+")

toolLine.update()

stdscr.getch()
