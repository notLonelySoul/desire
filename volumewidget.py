from fabric.widgets.circular_progress_bar import CircularProgressBar
from fabric.widgets.eventbox import EventBox
from fabric.widgets.overlay import Overlay
from fabric.widgets.label import Label
from fabric.widgets.box import Box
from fabric.audio.service import Audio
from fabric.utils.helpers import exec_shell_command_async

class VolumeWidget(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio = Audio()

        self.circular_progress_bar = CircularProgressBar(
            name="volume-circular-progress-bar",
            background_color=False,  # false = disabled
            radius_color=False,
            pie=True,
        )

        self.event_box = EventBox(
            events="scroll",
            children=Overlay(
                children=self.circular_progress_bar,
                overlays=Label(
                    label="",
                    style="margin: 0px 6px 0px 0px; font-size: 12px;",  # because glyph icon is not centered
                ),
            ),
        )

        self.event_box.connect("scroll-event", self.on_scroll)
        self.audio.connect("speaker-changed", self.update)
        self.add(self.event_box)

    def on_scroll(self, widget, event):
        if event.direction == 0:
            self.audio.speaker.volume += 2
        elif event.direction == 1:
            self.audio.speaker.volume -= 2

    def update(self, *args):
        if self.audio.speaker is None:
            return
        self.circular_progress_bar.percentage = self.audio.speaker.volume
        return

        print(float(data.replace('%', '')))
        