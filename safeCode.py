from typing import List, Any

import urwid
from Bike import Bike


class ActionButton(urwid.Button):
  def __init__(self, caption, callback):
    super(ActionButton, self).__init__("")
    urwid.connect_signal(self, 'click', callback)
    self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                            None, focus_map='reversed')


class Main(urwid.WidgetWrap):
  def __init__(self):
    super(Main, self).__init__(
      ActionButton([u" > go to ", 'Main'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Main', "\n"])
    self.interactions = []

  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class Workshop(urwid.WidgetWrap):
  def __init__(self, choices):
    super(Workshop, self).__init__(
      ActionButton([u" > go to ", 'Workshop'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Workshop', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)

  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class SelectBike(urwid.WidgetWrap):
  def __init__(self, choices):
    super(SelectBike, self).__init__(
      ActionButton([u" > go to ", 'Select Bike'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Select Bike', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)


  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class WorkshopBike(urwid.WidgetWrap):
  def __init__(self, choices):
    super(WorkshopBike, self).__init__(
      ActionButton([u" > go to ", 'Workshop Bike'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'workshop bike', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)


  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class Service(urwid.WidgetWrap):
  def __init__(self, choices):
    super(Service, self).__init__(
      ActionButton([u" > go to ", 'Service'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Service', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)

  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class ServiceBike(urwid.WidgetWrap):
  def __init__(self, choices):
    super(ServiceBike, self).__init__(
      ActionButton([u" > go to ", 'Service Bike'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Service Bike', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)


  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class BikeView(urwid.WidgetWrap):
  def __init__(self, choices):
    super(BikeView, self).__init__(
      ActionButton([u" > go to ", 'Bike'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Bike', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)

  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)


class Load(urwid.WidgetWrap):
  def __init__(self, choices):
    super(Load, self).__init__(
      ActionButton([u" > go to ", 'Load'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'Load', "\n"])
    self.choices = choices
    self.interactions = []
    # create links back to ourself
    for bike in bikes:
      self.interactions.append(urwid.Text(bike.bike_brand))

    for child in choices:
      getattr(child, 'choices', []).insert(0, self)

  def initialize(self):
    print('initialize')
  def grab_bike(self, button):
    selected_bike = 'a bike'
  def enter_place(self, button):
    game.update_place(self)


class New(urwid.WidgetWrap):
  def __init__(self, choices):
    super(New, self).__init__(
      ActionButton([u" > go to ", 'New'], self.enter_place))
    self.heading = urwid.Text([u"\nLocation: ", 'New', "\n"])
    self.choices = choices
    self.interactions = []
    self.bike_brand = ''
    self.bike_model = ''
    self.bike_year = ''
    self.bike_owner = ''
    self.get_interactions()
    # create links back to ourself
    for child in choices:
      getattr(child, 'choices', []).insert(0, self)

  def get_interactions(self):
    self.interactions.append(urwid.Text('fill bike details'))
    self.bike_brand = urwid.Edit("brand: ")
    self.bike_model = urwid.Edit("model: ")
    self.bike_year = urwid.Edit("year: ")
    self.bike_owner = urwid.Edit("owner: ")
    self.interactions.append(self.bike_brand)
    self.interactions.append(self.bike_model)
    self.interactions.append(self.bike_year)
    self.interactions.append(self.bike_owner)
    self.interactions.append(ActionButton([u" > Create  ", 'Bike'], self.create_bike))

  def initialize(self):
    print('initialize')

  def enter_place(self, button):
    game.update_place(self)

  def create_bike(self, other_arg):
    bike = Bike(self.bike_brand, self.bike_model, self.bike_year, self.bike_owner)
    bikes.append(bike)
    game.update_place(self)


class Start(object):
  def __init__(self):
    self.log = urwid.SimpleFocusListWalker([], wrap_around=False)
    self.top = urwid.ListBox(self.log)
    self.inventory = set()
    self.update_place(map_top)

  def update_place(self, place):
    if self.log:  # disable interaction with previous place
      self.log[-1] = urwid.WidgetDisable(self.log[-1])
    self.log.append(urwid.Pile([place.heading]))
    if len(place.interactions) > 0:
      for i in place.interactions:
        self.log.append(i)
    self.top.focus_position = len(self.log) - 1
    self.place = place
    self.place.initialize()

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


bikes: Bike = []
selected_bike = ''
map_top = Main()

game = Start()
urwid.MainLoop(game.top, palette=[('reversed', 'standout', '')]).run()

