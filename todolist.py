from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Checkbox, Button
from textual.containers import VerticalScroll, Horizontal
from textual import on
import sqlite3

class TodoItem(Horizontal):
    def __init__(self, task_id: int, tasks_label: str, is_completed: bool = False) -> None:
        super().__init__()
        self.tasks_label = tasks_label
        self.tasks_id = task_id
        self.is_completed = is_completed


    def compose(self) -> ComposeResult:
        yield Checkbox(self.tasks_label, classes="tasks", value=self.is_completed)
        yield Button("🗑️", variant="error", id="btn_delete")

    @on(Button.Pressed, "#btn_delete")
    def on_btn_delete(self) -> None:
        self.app.db.delete_task(self.tasks_id)
        self.remove()

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
        if event.checkbox.value:
            event.checkbox.add_class("checked")
        else:
            event.checkbox.remove_class("checked")
        self.app.db.update_task_status(self.tasks_id, event.checkbox.value)






class TodoList(App):
    CSS_PATH = 'style.tcss'
    BINDINGS = [('q', "bind_quit", "Quit"),]

    def __init__(self):
        super().__init__()
        self.db = TodoDatabase()
    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="scrollbar"):
            pass
        yield Input(placeholder="Write task...")
        yield Footer()

    def on_mount(self) -> None:

        self.db.get_all_tasks()
        for task in self.db.get_all_tasks():
            self.query_one("#scrollbar").mount(TodoItem(task[0], task[1], bool(task[2])))

    # Add tasks action
    @on(Input.Submitted)
    def add_task(self, event:Input.Submitted) -> None:
        new_task = event.value
        new_id = self.db.add_task(new_task)
        self.query_one("#scrollbar").mount(TodoItem(task_id=new_id, tasks_label=new_task))

        if event.value == "":
            return

        event.input.value = ""

    # Check tasks action



    def action_bind_quit(self) -> None:
        self.exit()

'''
BACKEND [SQLITE]
'''

class TodoDatabase:
    def __init__(self, db_name="todolist.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_label TEXT NOT NULL,
            is_complete INTEGER DEFAULT 0
            )''')
    def add_task(self, task_label:str) -> int:
        self.cursor.execute('''INSERT INTO tasks (task_label) VALUES (?)''', (task_label,))
        self.conn.commit()

        new_id = self.cursor.lastrowid
        return new_id if new_id is not None else 0

    def get_all_tasks(self) -> list:
        self.cursor.execute("SELECT ID, task_label, is_complete FROM tasks")
        return self.cursor.fetchall()

    def update_task_status(self, task_id:int, is_complete:bool) -> None:
        status = 1 if is_complete else 0
        self.cursor.execute("UPDATE tasks SET is_complete=? WHERE id=?", (status, task_id))
        self.conn.commit()

    def delete_task(self, task_id:int) -> None:
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()


if __name__ == '__main__':
    app = TodoList()
    app.run()
