import fabric
import gi
import psutil
import subprocess

from loguru import logger

from fabric.widgets.wayland import Window
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.date_time import DateTime
from fabric.utils.string_formatter import FormattedString
from fabric.hyprland.widgets import ActiveWindow, Workspaces, WorkspaceButton
from fabric.hyprland.service import Hyprland, HyprlandEvent
from fabric.utils.fabricator import Fabricator
from fabric.utils import set_stylesheet_from_file, invoke_repeater

from bar_media import BarMedia
from my_utils import *

connection = Hyprland()

gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk, Gdk, GLib

class Bar(Window):
    def __init__(self,) -> None:
        super().__init__(
            layer='top',
            anchor='left top right',
            visible=False,
            exclusive=True,
            all_visible=False, 
        )


        self.datebox = Box(
            name="date-box",
            children=[
                DateTime(name="time"),
            ]
        )

        self.center = Box(
            name='center-box',
            children=[self.datebox],
        )

        # Left shit...
        self.active_window = ActiveWindow(
            formatter=FormattedString(
                "{test_title(win_class)}",
                test_title=lambda x, max_length=20: "Desktop"
                if len(x) == 0
                else x
                if len(x) <= max_length
                else x[: max_length - 3] + "...",
            ),
            name="hyprland-window",
        )

        self.window_box = Box(name="window-box", children=[self.active_window,], h_align='center')

        Workspaces.scroll_handler = self.scroll_handler
        self.workspaces = Workspaces(
            spacing=2,
            name="workspaces",
            buttons_list=[
                WorkspaceButton(label=FormattedString("1")),
                WorkspaceButton(label=FormattedString("2")),
                WorkspaceButton(label=FormattedString("3")),
                WorkspaceButton(label=FormattedString("4")),
                WorkspaceButton(label=FormattedString("5")),
                WorkspaceButton(label=FormattedString("6")),
                WorkspaceButton(label=FormattedString("7")),
            ],
        )

        self.left = Box(
            name='left-box',
            children=[self.window_box, self.workspaces]
        )

        # right stuff.
        self.cpu_bar = Gtk.ProgressBar(fraction=True)
        self.cpu_bar.set_name("sys-stats")
        self.cpu_pc = Box(
            name="sys-info",
            children=[
                Label(label=""),
                self.cpu_bar,
            ],
            v_align='center',
        )
        self.ram_bar = Gtk.ProgressBar(fraction=True)
        self.ram_bar.set_name("sys-stats")
        self.ram_pc = Box(
            name="sys-info",
            children=[
                Label(label="󰧑"),
                self.ram_bar,
            ],
            v_align="center",
        )

        self.sys_info = Box(
            orientation='v',
            children=[self.cpu_pc, self.ram_pc]
        )

        self.right = Box(
            name="right-box",
            children=[
                self.sys_info,
            ],
            v_align='center',
        )

        self.bar = CenterBox(
            start_children = [
                self.left,
            ],
            center_children = [
                self.center,
            ],
            end_children= [
                self.right,
            ]
        )
        
        self.add(self.bar)
        self.show_all()

        invoke_repeater_threaded(1000, lambda *args: self.update_sys_info())

    def apply_styles(*args):
        logger.info("[Bar] Applied Styles...")
        return set_stylesheet_from_file('bar.css')
    
    def scroll_handler(self, widget, event: Gdk.EventScroll):
        match event.direction:
            case Gdk.ScrollDirection.UP:
                connection.send_command(
                    "batch/dispatch workspace -1",
                )
                logger.info("[Workspaces] Moved to the next workspace")
            case Gdk.ScrollDirection.DOWN:
                connection.send_command(
                    "batch/dispatch workspace +1",
                )
                logger.info("[Workspaces] Moved to the previous workspace")
            case _:
                logger.info(
                    f"[Workspaces] Unknown scroll direction ({event.direction})"
                )
        return
    
    def update_sys_info(self):
        self.cpu_bar.set_fraction(psutil.cpu_percent(interval=1)/100)
        self.ram_bar.set_fraction(psutil.virtual_memory().percent/100)
        return True

if __name__ == "__main__":
    win = Bar()
    win.apply_styles()

    fabric.start()
