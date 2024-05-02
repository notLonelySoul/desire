from fabric.hyprland.service import HyprlandEvent
import gi 
from loguru import logger

gi.require_version("Gtk", "3.0")
from gi.repository import GLib

def on_activewindow(self, obj, event: HyprlandEvent):
        
        if '.' in event.data[0]: 
            event.data[0] = event.data[0].split('.')[-1]

        GLib.idle_add(
            self.set_label,
            self.formatter.get_formatted(
                win_class=event.data[0],
                win_title=event.data[1],
            ),
        )
        return logger.info(
            f"[ActiveWindow] Activated window {event.data[0]}, {event.data[1]}"
        )