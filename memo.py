# -*- coding: utf-8 -*-

import glob
import os

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk  # noqa


def slugify(text):
    tokens = text.split(' ')
    return '_'.join([t.lower() for t in tokens])


class MemoWindow(Gtk.Window):
    MEMO_STORAGE = '~/.local/share/memo/'

    def __init__(self):
        self.setup_notebook_directory()

        Gtk.Window.__init__(
            self,
            title="Memo",
            icon_name="tomboy",
        )
        self.resize(600, 600)
        self.connect('delete-event', self.close_and_save)

        self.setup_header_bar()
        self.setup_text_area()
        self.load_text()
        self.update_title()

    def setup_notebook_directory(self):
        self.notes_directory = os.path.expanduser(self.MEMO_STORAGE)
        if not os.path.exists(self.notes_directory):
            os.mkdir(self.notes_directory)

    def get_current_path(self):
        return os.path.join(
            self.notes_directory,
            self.get_current_folder(),
            '{}.md'.format(slugify(self.get_current_title())),
        )

    def load_text(self):
        if not os.path.exists(self.get_current_path()):
            return

        with open(self.get_current_path(), 'r') as fp:
            text = fp.read()
        text_buffer = self.text_view.get_buffer()
        text_buffer.set_text(text)

    def save_text(self):
        text_buffer = self.text_view.get_buffer()
        note_text = text_buffer.get_text(
            text_buffer.get_start_iter(),
            text_buffer.get_end_iter(),
            False,
        )
        if not note_text.endswith('\n'):
            note_text += '\n'
            text_buffer.set_text(note_text)

        with open(self.get_current_path(), 'w') as fp:
            fp.write(note_text)

    def get_current_folder(self):
        return self.notebook_combobox.get_active_text()

    def get_current_title(self):
        text_buffer = self.text_view.get_buffer()
        note_text = text_buffer.get_text(
            text_buffer.get_start_iter(),
            text_buffer.get_end_iter(),
            False,
        )
        index = note_text.find('\n')
        title = note_text[:index] if index > 0 else note_text
        return title.strip()

    def update_title(self):
        title = self.get_current_title()
        self.header.set_title(title if title else '<New Memo>')

    def close_and_save(self, *args, **kwargs):
        self.save_text()
        Gtk.main_quit(*args, **kwargs)

    def setup_header_bar(self):
        self.header = Gtk.HeaderBar(margin=0)
        self.header.set_title(self.get_title())

        toolbar_items = (
            (Gtk.STOCK_CLOSE, "Close", self.close_and_save),
        )
        for stock_item, tooltip, callback_method in toolbar_items:
            button = Gtk.ToolButton(stock_item)
            button.set_tooltip_text(tooltip)
            if callback_method:
                button.connect('clicked', callback_method)

            button.set_is_important(True)
            self.header.pack_end(button)

        self.notebook_combobox = Gtk.ComboBoxText()
        notebooks = glob.glob('{}/*/'.format(self.notes_directory))
        notebooks = [d.split('/')[-2] for d in notebooks]

        for nb in notebooks:
            self.notebook_combobox.append_text(nb)
        self.notebook_combobox.set_active(0)

        self.header.pack_end(self.notebook_combobox)

        self.set_titlebar(self.header)

    def setup_text_area(self):
        def key_release_event(event, user_data):
            self.update_title()

        self.text_view = Gtk.TextView(margin=8)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.connect('key-release-event', key_release_event)
        self.add(self.text_view)


if __name__ == '__main__':
    win = MemoWindow()
    win.show_all()
    Gtk.main()
