import sys
import os
import curses

from todolist import TodoItem, TodoList

stdscr = curses.initscr()

curses.start_color() # Allow colors
curses.noecho()      # Don't print lines when typed.
stdscr.keypad(True)  # Recognize keypresses
curses.cbreak()      # Allow ^C to exit
curses.curs_set(0)   # Hide cursor

HEADER = " CHECKLIST - My Todos".ljust(curses.COLS, ' ')
FOOTER = " - ".join([
    "(n) to add new item",
    "(r) to rename",
    "(space) to toggle check",
    "(d) to delete",
    "(q) to quit"
])

# Color pairs
# 1 = Header highlight
# 2 = Selection blue
curses.init_pair(1, 0, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_BLUE, 0)

# Header and footers
stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
stdscr.addstr(curses.LINES - 1, 0, FOOTER)

# Main window
height = curses.LINES - 2
width = curses.COLS
start_y = 1
start_x = 0
win = curses.newwin(height, width, start_y, start_x)
win.border()

def global_refresh():
    stdscr.refresh()
    win.refresh()
    win.border()

todos = TodoList(
    [
        TodoItem("Walk dog", False),
        TodoItem("Do dishes", False),
        TodoItem("Write exam", False),
        TodoItem("Work out", False)
    ]
)

def main(stdscr):
    selection = 0

    # EVENT LOOP
    while True:
        todos.print_items(win)
        global_refresh()

        c = stdscr.getch()

        # TODO:
        # gg = Top
        # n = New item
        # r = Rename

        if c == ord('q'):
            stdscr.clear()
            os.system("clear")
            break
        elif c == ord('j'):
            todos.set_selection('down')
        elif c == ord('k'):
            todos.set_selection('up')
        elif c == ord('G'):
            todos.set_selection('bot')
        elif c == ord(' '):
            todos.toggle()
        elif c == ord('l'):
            todos.toggle('check')
        elif c == ord('h'):
            todos.toggle('uncheck')
        elif c == ord('d'):
            todos.pop()
        elif c == ord('K'):
            todos.swap('up')
        elif c == ord('J'):
            todos.swap('down')

        win.clear()
        win.border()
    # END EVENT LOOP

if __name__ == "__main__":
    curses.wrapper(main)
