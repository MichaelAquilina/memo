# -*- coding: utf-8 -*-

import os

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk  # noqa

from memo import note

if __name__ == '__main__':
    win = note.Note(
        os.path.expanduser('~/.local/share/memo'),
        'dev/hello_world.md',
    )
    win.show_all()
    Gtk.main()
