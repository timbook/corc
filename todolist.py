import curses

class TodoItem:
    def __init__(self, name, compl):
        self.name = name
        self.compl = compl

class TodoList:
    def __init__(self, todos):
        self.todos = todos
        self.selection = 0
        self.buffer = []

    def print_items(self, win, y=1, x=1):
        for i, item in enumerate(self.todos):
            cp = 2 if i == self.selection else 0
            marker = 'X' if item.compl else ' '
            win.addstr(1 + i, 1, f"[{marker}] {i + 1} - {item.name}", curses.color_pair(cp))

    def set_selection(self, pos):
        if pos == 'down':
            self.selection = min(len(self.todos) - 1, self.selection + 1)
        elif pos == 'up':
            self.selection = max(0, self.selection - 1)
        elif pos == 'top':
            self.selection = 0
        elif pos == 'bot':
            self.selection = len(self.todos) - 1

    def toggle(self, task=None):
        if task is None:
            self.todos[self.selection].compl = not self.todos[self.selection].compl
        elif task == 'check':
            self.todos[self.selection].compl = True
        elif task == 'uncheck':
            self.todos[self.selection].compl = False

    def pop(self):
        if self.todos:
            deleted_todo = self.todos.pop(self.selection)
            deleted_selection = self.selection

            if self.selection == len(self.todos) - 1:
                self.set_selection('up')

            self.buffer.append((deleted_selection, deleted_todo))

    def undo(self):
        if self.buffer:
            index, todo = self.buffer.pop()
            self.todos.insert(index, todo)

    def swap(self, pos):
        if pos == 'up' and self.selection != 0:
            self.todos[self.selection - 1], self.todos[self.selection] = \
                self.todos[self.selection], self.todos[self.selection - 1]
            self.set_selection('up')
        elif pos == 'down' and self.selection != len(self.todos) - 1:
            self.todos[self.selection + 1], self.todos[self.selection] = \
                self.todos[self.selection], self.todos[self.selection + 1]
            self.set_selection('down')

    def add_new(self, win):
        self.todos.insert(self.selection + 1, TodoItem("", False))
        self.selection += 1
        win.clear()
        win.border()
        self.print_items(win)

        curses.echo()
        curses.curs_set(1)
        new_item = win.getstr(self.selection + 1, 9).decode('utf-8')
        curses.noecho()
        curses.curs_set(0)

        self.todos[self.selection].name = new_item
