# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk  # noqa


class MemoWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(
            self,
            title="Memo",
            icon_name="tomboy",
        )
        self.resize(600, 600)

        self.setup_header_bar()
        self.setup_text_area()
        self.load_tomboy_text()

    def load_tomboy_text(self):
        import os
        import xml.etree.ElementTree as ET
        NS = {
            'tomboy': 'http://beatniksoftware.com/tomboy',
        }
        path = os.path.expanduser('~/.local/share/tomboy/02969b4f-59f7-401a-95d1-c4ad99fcc7ca.note')

        root = ET.parse(path)
        self.header.set_title(root.find('tomboy:title', NS).text)

        self.textbuffer = self.text_view.get_buffer()
        self.textbuffer.set_text(root.find('.//tomboy:note-content', NS).text)

    def setup_header_bar(self):
        self.header = Gtk.HeaderBar(margin=0)
        self.header.set_show_close_button(True)
        self.header.set_title(self.get_title())

        notebooks = [
            "Dev",
            "Groceries",
            "Lyst",
            "Open Source",
        ]

        self.notebook_combobox = Gtk.ComboBoxText()
        for nb in notebooks:
            self.notebook_combobox.append_text(nb)
        self.notebook_combobox.set_active(0)

        self.header.pack_end(self.notebook_combobox)

        self.set_titlebar(self.header)

    def setup_text_area(self):
        self.text_view = Gtk.TextView(margin=8)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.add(self.text_view)


if __name__ == '__main__':
    win = MemoWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
