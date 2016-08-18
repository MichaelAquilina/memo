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
        self.load_text()

    def load_text(self):
        with open('memo.txt', 'r') as fp:
            text = fp.read()
        text_buffer = self.text_view.get_buffer()
        text_buffer.set_text(text)

    def save_text(self, event):
        text_buffer = self.text_view.get_buffer()
        note_text = text_buffer.get_text(
            text_buffer.get_start_iter(),
            text_buffer.get_end_iter(),
            False,
        )
        with open('memo.txt', 'w') as fp:
            fp.write(note_text)

    def setup_header_bar(self):
        self.header = Gtk.HeaderBar(margin=0)
        self.header.set_title(self.get_title())

        toolbar_items = (
            (Gtk.STOCK_CLOSE, "Close", Gtk.main_quit),
            (Gtk.STOCK_REFRESH, "Reload", None),
            (Gtk.STOCK_SAVE, "Save", self.save_text),
        )
        for stock_item, tooltip, callback_method in toolbar_items:
            button = Gtk.ToolButton(stock_item)
            button.set_tooltip_text(tooltip)
            if callback_method:
                button.connect('clicked', callback_method)

            button.set_is_important(True)
            self.header.pack_end(button)

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
