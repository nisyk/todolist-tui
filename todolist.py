from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.widgets import Header, Footer, Input, Checkbox
from textual.containers import VerticalScroll
from textual import on



class TodoList(App):
    CSS_PATH = 'style.tcss'
    BINDINGS = [('r', "bind_remove", "Remove"),
                ('q', "bind_quit", "Quit"),]

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="scrollbar"):
            pass
        yield Input(placeholder="Write task...")
        yield Footer()


    @on(Input.Submitted)
    def add_task(self, event:Input.Submitted) -> None:
        new_task = event.value
        if event.value == "":
            return
        else:
            self.query_one("#scrollbar").mount(Checkbox(new_task, classes="tasks"))
            event.input.value = ""

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event:Checkbox.Changed) -> None:
        if event.checkbox.value:
            event.checkbox.add_class("checked")
        else:
            event.checkbox.remove_class("checked")



    def action_bind_remove(self) -> None:
        try:
            remove_task = self.query(".tasks").last()
            remove_task.remove()

        except NoMatches:
            pass

    def action_bind_quit(self) -> None:
        self.exit()

if __name__ == '__main__':
    app = TodoList()
    app.run()