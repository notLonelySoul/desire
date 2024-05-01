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

        self.progress = CircularProgressBar(
            name="bar-todo-progress",
            size=(30, 30), 
            percentage=10,
        )

        self.add(self.progress)