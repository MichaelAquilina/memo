# -*- coding: utf-8 -*-

import glob
import os

import gi
gi.require_version('Gtk', '3.0')  # noqa

from gi.repository import Gtk  # noqa


def slugify(text):
    tokens = text.split(' ')
    return '_'.join([t.lower() for t in tokens])


class Note(Gtk.Window):
    def __init__(self, memo_storage, note_path):
        self.note_path = note_path
        self.memo_storage = memo_storage

        self.setup_notebook_directory()

        Gtk.Window.__init__(
            self,
            title="Memo",
            icon_name="tomboy",
        )
        self.resize(600, 600)
        self.connect('delete-event', self._close_and_save)

        self._setup_header_bar()
        self._setup_text_area()
        self._load_text()
        self._update_title()

    def setup_notebook_directory(self):
        self.memo_directory = os.path.expanduser(self.memo_storage)
        if not os.path.exists(self.memo_directory):
            os.mkdir(self.memo_directory)

    def get_current_path(self):
        return os.path.join(
            self.memo_directory,
            self.get_current_folder(),
            '{}.md'.format(slugify(self.get_current_title())),
        )

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

    def _load_text(self):
        full_path = os.path.join(self.memo_storage, self.note_path)
        print(full_path)

        if not os.path.exists(full_path):
            # should display a warning here
            return

        with open(full_path, 'r') as fp:
            text = fp.read()
        text_buffer = self.text_view.get_buffer()
        text_buffer.set_text(text)

    def _save_text(self):
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

    def _update_title(self):
        title = self.get_current_title()
        self.header.set_title(title if title else '<New Memo>')

    def _close_and_save(self, *args, **kwargs):
        self._save_text()
        Gtk.main_quit(*args, **kwargs)

    def _setup_header_bar(self):
        self.header = Gtk.HeaderBar(margin=0)
        self.header.set_title(self.get_title())

        toolbar_items = (
            (Gtk.STOCK_CLOSE, "Close", self._close_and_save),
        )
        for stock_item, tooltip, callback_method in toolbar_items:
            button = Gtk.ToolButton(stock_item)
            button.set_tooltip_text(tooltip)
            if callback_method:
                button.connect('clicked', callback_method)

            button.set_is_important(True)
            self.header.pack_end(button)

        self.notebook_combobox = Gtk.ComboBoxText()
        notebooks = glob.glob('{}/*/'.format(self.memo_directory))
        notebooks = [d.split('/')[-2] for d in notebooks]

        for nb in notebooks:
            self.notebook_combobox.append_text(nb)
        self.notebook_combobox.set_active(0)

        self.header.pack_end(self.notebook_combobox)

        self.set_titlebar(self.header)

    def _setup_text_area(self):
        def key_release_event(event, user_data):
            self._update_title()

        self.text_view = Gtk.TextView(margin=8)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.connect('key-release-event', key_release_event)
        self.add(self.text_view)
