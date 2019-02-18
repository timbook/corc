import curses

class TodoItem:
    def __init__(self, name, compl):
        self.name = name
        self.compl = compl

class TodoList:
    def __init__(self, todos):
        self.todos = todos
        self.selection = 0

    def print_items(self, win, y=1, x=1):
        for i, item in enumerate(self.todos):
            cp = 2 if i == self.selection else 0
            marker = 'X' if item.compl else ' '
            win.addstr(1 + i, 1, f"[{marker}] {item.name}", curses.color_pair(cp))

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
        if len(self.todos) == 0:
            return None

        if self.selection == len(self.todos) - 1:
            self.set_selection('up')

        self.todos.pop(self.selection)

    def swap(self, pos):
        if pos == 'up' and self.selection != 0:
            self.todos[self.selection - 1], self.todos[self.selection] = \
                self.todos[self.selection], self.todos[self.selection - 1]
            self.set_selection('up')
        elif pos == 'down' and self.selection != len(self.todos) - 1:
            self.todos[self.selection + 1], self.todos[self.selection] = \
                self.todos[self.selection], self.todos[self.selection + 1]
            self.set_selection('down')
