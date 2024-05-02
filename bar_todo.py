import fabric
import gi

from loguru import logger

from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label
from fabric.widgets.circular_progress_bar import CircularProgressBar

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class BarToDo(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.task_progress = 0

        self.mainbox = Box(name="bar-todo-box")

        self.progress = CircularProgressBar(
            name="bar-todo-progress",
            radius_color=False,
            pie=True,
            size=(30, 30),
            percentage=10,
            tooltip_text=f"progress: {self.task_progress}"
        )

        self.task = Button(
            name="bar-task-label-button",
            label="no tasks yet...",
        )
        
        self.task_done_button = Button(
            name="bar-task-done-button",
            label="",
            v_expand=False,
        )
        
        self.mainbox.add_children([self.progress, self.task, self.task_done_button])

        self.add_children([self.mainbox,])