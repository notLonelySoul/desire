import gi 
import os

gi.require_version("Gtk", "3.0")
from gi.repository import GLib

CONF_CACHE_DIR = GLib.get_user_cache_dir() + '/fabric' 

if not os.path.exists(CONF_CACHE_DIR): os.mkdir(CONF_CACHE_DIR)

USER_NAME = GLib.get_user_name()


DATA_DIR = f"/home/{USER_NAME}/.data/"
