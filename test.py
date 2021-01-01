#!/usr/bin/env python

from __future__ import print_function, absolute_import, division
import urwid


def show_or_exit(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()

def name_changed(w, x):
    header.set_text('Hello % s!' % x)


if __name__ == '__main__':
    name_edit = urwid.Edit("Name: ")
    header = urwid.Text('Fill your details')
    widget = urwid.Pile([
        urwid.Padding(header, 'center', width=('relative', 6)),
        name_edit,
        urwid.Edit('Address: '),
    ])
    urwid.connect_signal(name_edit, 'change', name_changed)

    widget = urwid.Filler(widget, 'top')
    loop = urwid.MainLoop(widget, unhandled_input=show_or_exit)
    loop.run()