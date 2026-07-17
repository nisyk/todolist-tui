from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Checkbox, Button
from textual.containers import VerticalScroll, Horizontal
from textual import on

class TodoItem(Horizontal):
    def __init__(self, tasks_label:str) -> None:
        super().__init__()
        self.tasks_label = tasks_label


    def compose(self) -> ComposeResult:
        yield Checkbox(self.tasks_label, classes="tasks")
        yield Button("🗑️", variant="error", id="btn_delete")

    @on(Button.Pressed, "#btn_delete")
    def on_btn_delete(self) -> None:
        self.remove()






class TodoList(App):
    CSS_PATH = 'style.tcss'
    BINDINGS = [('q', "bind_quit", "Quit"),]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="scrollbar"):
            pass
        yield Input(placeholder="Write task...")
        yield Footer()

    # Add tasks action
    @on(Input.Submitted)
    def add_task(self, event:Input.Submitted) -> None:
        new_task = event.value
        if event.value == "":
            return

        self.query_one("#scrollbar").mount(TodoItem(new_task))
        event.input.value = ""

    # Check tasks action
    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
        if event.checkbox.value:
            event.checkbox.add_class("checked")
        else:
            event.checkbox.remove_class("checked")


    def action_bind_quit(self) -> None:
        self.exit()

if __name__ == '__main__':
    app = TodoList()
    app.run()
