import unicurses as _curses
import typing
import atexit
import locale

STATE = int
OK = 0
ERR = 1

class Window:
    def __init__(self: typing.Self, _win) -> None:
        self.id = _win
    
    def draw(self: typing.Self, content: str, x: int = 0, y: int = 0) -> STATE:
        _curses.mvwaddstr(self.id, y, x, content)
        return OK

    def update(self: typing.Self) -> STATE:
        _curses.wrefresh(self.id)
        return OK
    
    def resize(self: typing.Self, height: int, width: int) -> STATE:
        _curses.wresize(self.id, height, width)
        return OK
    
    def clear(self: typing.Self) -> STATE:
        _curses.wclear(self.id)
        return OK
    
    def attron(self: typing.Self, pair: int) -> STATE:
        _curses.wattron(pair)
        return OK
    
    def attroff(self: typing.Self, pair: int) -> STATE:
        _curses.wattroff(pair)
        return OK

    def getch(self: typing.Self) -> int:
        return _curses.wgetch(self.id)

    def move(self: typing.Self, x: int, y: int) -> STATE:
        _curses.wmove(self.id, y, x)
        return OK

    @property
    def size(self: typing.Self) -> typing.Tuple[int, int]:
        height, width = _curses.getmaxyx(self.id)
        return width, height
    
    def create_box(
        self: typing.Self,
        left: str, 
        right: str, 
        top: str, 
        bottom: str, 
        left_top: str, 
        right_top: str, 
        left_bottom: str, 
        right_bottom: str
        ) -> STATE:
        if all(len(char) == 1 for char in [left, right, top, bottom, left_top, right_top, left_bottom, right_bottom]):
            _curses.border(
                ord(left), 
                ord(right), 
                ord(top), 
                ord(bottom), 
                ord(left_top), 
                ord(right_top), 
                ord(left_bottom), 
                ord(right_bottom)
            )
            return OK
        else:
            return ERR



class Screen:
    main: Window
    @staticmethod
    def init() -> STATE:
        locale.setlocale(locale.LC_ALL, "")
        Screen.main = Window(_curses.initscr())
        _curses.cbreak()
        _curses.noecho()
        _curses.start_color()
        _curses.keypad(Screen.main.id, True)
        return OK

    @atexit.register
    @staticmethod
    def reset() -> STATE:
        _curses.echo()
        _curses.nocbreak()
        _curses.endwin()
        _curses.keypad(Screen.main.id, False)
        return OK
    
    def size() -> typing.Tuple[int, int]:
        return Screen.main.size
    
    def new_window(width: int = 0, height: int = 0, begin_x: int = 0, begin_y: int = 0) -> Window:
        return Window(_curses.newwin(height, width, begin_x, begin_y))

        

class Pair:
    _PAIR_ID = 1
    @staticmethod
    def create(fg_id: int, bg_id: int) -> int:
        _curses.init_pair(Pair._PAIR_ID, fg_id, bg_id)
        Pair._PAIR_ID += 1
        return Pair._PAIR_ID - 1

    def create_color(_id: int, hex_code: str) -> int:
        R, G, B = int(hex_code[1:3], 16), int(hex_code[3:5], 16), int(hex_code[5:7], 16)
        _curses.init_color(_id, R, G, B)
        return _id





