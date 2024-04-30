import fabric
import gi
import urllib.request

from loguru import logger
from my_utils import *

from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.wayland import Window
from fabric.widgets.label import Label
from fabric.utils.fabricator import Fabricator
from fabric.widgets.overlay import Overlay
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.utils import exec_shell_command_async


from fabric.utils import set_stylesheet_from_file, get_relative_path

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class BarMedia(Box):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        # defining shit.

        self.mainbox = Box(
            name="main-box",
            v_align='center'
        )

        self.sub_box = Box(
            name="sub-box",
            h_align='center',
            orientation='vertical',
        )

        self.song_info = Label(
            label="nothing playing...",
            name='bar-media-label',
        )

        self.song_prog = Gtk.ProgressBar(
            fraction=True,
            halign=True
        )
        
        self.icon_button = Button(label="", name="status-icon", v_align="center", h_align='center')
        self.icon_button.connect('button-press-event', lambda *args: exec_shell_command_async("playerctl play-pause", None))

        self.song_cover = Box(
            name="cover-box",
            children=[
                Overlay(
                    children=Box(name="media-cover", style=f"background-image: url('file://cover.png')"),
                    overlays=[
                        self.icon_button,
                    ],
                ),
            ],
        )

        info = Fabricator(stream=True, poll_from=r'''playerctl --follow metadata --format {{title}},,{{artist}},,{{position}},,{{mpris:length}},,{{status}}''')
        info.connect("changed", self.set_info)

        self.sub_box.add_children([self.song_info,self.song_prog])

        self.mainbox.add_children([self.song_cover, self.sub_box])
        self.add_children(self.mainbox)

        GLib.Thread.new(None, self.update_cover,)

    def update_cover(self):
        def get_cover(_, data):
            try: 
                urllib.request.urlretrieve(data, "cover.png")
                self.song_cover.set_style("background-image: url('cover.png');")
            
            except Exception as e:
                logger.info(e)
                

        cover = Fabricator(stream=True, poll_from=r'''playerctl --follow metadata --format {{mpris:artUrl}}''')
        cover.connect("changed", get_cover)
    
    def set_info(self,_, data:str):
        title, artist, pos, length, status = data.split(',,')
        self.song_info.set_label(format_song_name(f'{title} • {artist}', 30))
        self.song_prog.set_fraction(float(pos)/float(length)) if float(length) != 0 else self.song_prog.set_fraction(0)

        sd = {
            "Playing" : "",
            "Paused" : "",
            "Stopped": ""
        }

        self.icon_button.set_label(sd[status])

