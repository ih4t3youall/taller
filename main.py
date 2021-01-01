import urwid

class ActionButton(urwid.Button):
    def __init__(self, caption, callback):
        super(ActionButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                                None, focus_map='reversed')

class Main(urwid.WidgetWrap):
    def __init__(self, choices):
        super(Main, self).__init__(
            ActionButton([u" > go to ", 'Main'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Main', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)


class Workshop(urwid.WidgetWrap):
    def __init__(self, choices):
        super(Workshop, self).__init__(
            ActionButton([u" > go to ", 'Workshop'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Workshop', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)

class SelectBike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(SelectBike, self).__init__(
            ActionButton([u" > go to ", 'Select Bike'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Select Bike', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)

class WorkshopBike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(WorkshopBike, self).__init__(
            ActionButton([u" > go to ", 'Workshop Bike'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'workshop bike', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)


class Service(urwid.WidgetWrap):
    def __init__(self,  choices):
        super(Service, self).__init__(
            ActionButton([u" > go to ", 'Service'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Service', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)


class ServiceBike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(ServiceBike, self).__init__(
            ActionButton([u" > go to ", 'Service Bike'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Service Bike', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)


class Bike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(Bike, self).__init__(
            ActionButton([u" > go to ", 'Bike'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Bike', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)

class Load(urwid.WidgetWrap):
    def __init__(self, choices):
        super(Load, self).__init__(
            ActionButton([u" > go to ", 'Load'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'Load', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)


class New(urwid.WidgetWrap):
    def __init__(self, choices):
        super(New, self).__init__(
            ActionButton([u" > go to ", 'New'], self.enter_place))
        self.heading = urwid.Text([u"\nLocation: ", 'New', "\n"])
        self.choices = choices
        # create links back to ourself
        for child in choices:
            getattr(child, 'choices', []).insert(0, self)

    def enter_place(self, button):
        game.update_place(self)

class Start(object):
    def __init__(self):
        self.log = urwid.SimpleFocusListWalker([],wrap_around=False)

        self.top = urwid.ListBox(self.log)
        self.inventory = set()
        self.update_place(map_top)
        self.header

    def update_place(self, place):
        if self.log: # disable interaction with previous place
            self.log[-1] = urwid.WidgetDisable(self.log[-1])
        self.log.append(urwid.Pile([place.heading] + place.choices))
        #prueba text
        name_edit = urwid.Edit("Name: ")
        self.header = urwid.Text('Fill your details')
        self.log.append(self.header)
        self.log.append(name_edit)
        urwid.connect_signal(name_edit, 'change', self.name_changed)
        #prueba text
        self.top.focus_position = len(self.log) - 1
        self.place = place

    def name_changed(self, w, x):
        self.header.set_text('Hello % s!' % x)

    def take_thing(self, thing):
        self.inventory.add(thing.name)
        if self.inventory >= set([u'sugar', u'lemon', u'jug']):
            response = urwid.Text(u'You can make lemonade!\n')
            done = ActionButton(u' - Joy', exit_program)
            self.log[:] = [response, done]
        else:
            self.update_place(self.place)


def exit_program(button):
    raise urwid.ExitMainLoop()

map_top = Main([Service([SelectBike([])]),Workshop([SelectBike([])]),Bike([Load([]),New([])])])


game = Start()
urwid.MainLoop(game.top, palette=[('reversed', 'standout', '')]).run()
