# -*- coding: utf-8 -*-
'''
责任链模式 2017-03-12
'''


class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)


class MainWindow(Widget):
    ''' 仅处理close和default '''

    def handle_clse(self, event):
        print 'MainWindow: {}'.format(event)

    def handle_default(self, event):
        print 'MainWindow Default: {}'.format(event)


class SendDialog(Widget):
    ''' 仅处理paint事件 '''

    def handle_paint(self, event):
        print 'SendDialog: {}'.format(event)


class MsgText(Widget):
    ''' 仅处理down事件 '''

    def handle_down(self, event):
        print 'MsgText: {}'.format(event)


def main():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        print e
        evt = Event(e)
        print '\n'
        print 'Sending event -{}- to MainWindow'.format(evt)
        mw.handle(evt)
        print 'Sending event -{}- to SendDialog'.format(evt)
        sd.handle(evt)
        print 'Sending event -{}- to MsgText'.format(evt)
        msg.handle(evt)


if __name__ == '__main__':
    main()
