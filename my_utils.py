import gi 

gi.require_version("Gtk", "3.0")
from gi.repository import GLib

def format_song_name(info: str, max_limit: int):
    if len(info) > max_limit: rs = info[:max_limit] + '...';
    else: rs = info
    return rs

def format_date_command(info: str):
    info = info.split()
    sd = {
        "Monday": "Mon",
        "Tuesday": "Tue",
        "Wednesday": "Wed",
        "Thursday": "Thu",
        "Friday": "Fri",
        "Saturday": "Sat",
        "Sunday": "Sun"
    }
    
    info[0] = sd[info[0]]
    
    time = info[4].split(':')[:2]

    final = time[0] + ':' + time[1]


def invoke_repeater_threaded(timeout: int, callback: callable, *args):
    def invoke_threaded_repeater():
        ctx = GLib.MainContext.new()
        loop = GLib.MainLoop.new(ctx, False)

        source = GLib.timeout_source_new(timeout)
        source.set_priority(GLib.PRIORITY_LOW)
        source.set_callback(callback, *args)
        source.attach(ctx)

        loop.run()

    GLib.Thread.new(None, invoke_threaded_repeater)

