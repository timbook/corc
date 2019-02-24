import os
import sys
import json
import curses

from todolist import TodoItem, TodoList
import argutils

args = argutils.get_args()

if args.list:
    # TODO: List
    sys.exit(0)

if args.new:
    # Determine list name. Defaults to filename given.
    name = args.name if args.name else args.new.replace('.json', '')
    todos = TodoList([], name)

    # Decides where file will be saved, locally or globally.
    if args.is_global:
        home_dir = os.environ['HOME']
        prefix = home_dir + "/.corc/"
        if not os.path.isdir(home_dir + "/.corc"):
            os.mkdir(home_dir + "/.corc")
    else:
        prefix = "./"

    FILE = prefix + args.new.replace('.json', '') + ".json"

elif args.using:
    # TODO
    pass
else:
    # TODO: Use default
    pass

# todos = TodoList([
    # TodoItem("Walk dog", False),
    # TodoItem("Do dishes", False),
    # TodoItem("Write exam", False),
    # TodoItem("Work out", False)
# ], name="TESTER TODO")

stdscr = curses.initscr()

curses.start_color() # Allow colors
curses.noecho()      # Don't print lines when typed.
stdscr.keypad(True)  # Recognize keypresses
curses.cbreak()      # Allow ^C to exit
curses.curs_set(0)   # Hide cursor

HEADER = " CHECKLIST - My Todos".ljust(curses.COLS, ' ')
FOOTER = " - ".join([
    "(n) to add new item",
    "(space) to toggle check",
    "(D) to delete",
    "(q) to quit"
])

# Color pairs
curses.init_pair(1, 0, curses.COLOR_BLUE) # Corc header
curses.init_pair(2, curses.COLOR_BLUE, 0) # Selection blue

# Header and footers
stdscr.addstr(0, 0, HEADER, curses.color_pair(1))
stdscr.addstr(curses.LINES - 1, 0, FOOTER)

# List window
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

def main(stdscr):
    selection = 0

    # EVENT LOOP
    while True:
        todos.print_items(win)
        global_refresh()

        c = stdscr.getch()

        if c == ord('q'):
            stdscr.clear()
            os.system("clear")
            break
        elif c == ord('s') or c == ord('S'):
            todos.to_json(FILE)
        elif c == ord('j') or c == curses.KEY_DOWN:
            todos.set_selection('down')
        elif c == ord('k') or c == curses.KEY_UP:
            todos.set_selection('up')
        elif c == ord('g'):
            todos.set_selection('top')
        elif c == ord('G'):
            todos.set_selection('bot')
        elif c == ord(' '):
            todos.toggle()
        elif c == ord('l') or c == curses.KEY_RIGHT:
            todos.toggle('check')
        elif c == ord('h') or c == curses.KEY_LEFT:
            todos.toggle('uncheck')
        elif c == ord('D'):
            todos.pop()
        elif c == ord('u'):
            todos.undo()
        elif c == ord('K'):
            todos.swap('up')
        elif c == ord('J'):
            todos.swap('down')
        elif c == ord('o') or c == ord('n'):
            todos.add_new(win)

        win.clear()
        global_refresh()
    # END EVENT LOOP

if __name__ == "__main__":
    curses.wrapper(main)
