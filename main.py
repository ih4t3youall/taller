import pickle

import urwid
from Bike import Bike


class ActionButton(urwid.Button):
    def __init__(self, caption, callback):
        super(ActionButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                                None, focus_map='reversed')

class SelectionButton(urwid.Button):
    def __init__(self, caption, callback, selected):
        super(SelectionButton, self).__init__("")
        self.selection = selected
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 1),
                                None, focus_map='reversed')

    def get_selection(self):
        return self.selection


class Main(urwid.WidgetWrap):
    def __init__(self):
        super(Main, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Main', "\n"])
        self.interactions = []

    def get_interactions(self):
        self.interactions = []
        self.interactions.append(ActionButton('Service', self.go_to_service))
        self.interactions.append(ActionButton('Workshop', self.go_to_workshop))
        self.interactions.append(ActionButton('Bike', self.go_to_bike))
        return self.interactions

    def enter_place(self, object):
        game.update_place(self)

    def go_to_service(self, object):
        game.update_place(Service())

    def go_to_workshop(self, object):
        game.update_place(Workshop())

    def go_to_bike(self, object):
        game.update_place(BikeView())


class Workshop(urwid.WidgetWrap):
    def __init__(self):
        super(Workshop, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Workshop', "\n"])
        # create links back to ourself
        self.interactions = []

    def get_interactions(self):
        self.interactions = []
        self.interactions.append(ActionButton('Select bike', self.go_to_select_bike))
        self.interactions.append(ActionButton('Go back', self.go_back))
        return self.interactions

    def go_to_select_bike(self, object):
        game.update_place(SelectBike('Workshop'))

    def go_back(self, object):
        game.update_place(Main())

    def enter_place(self, button):
        game.update_place(self)


class SelectBike(urwid.WidgetWrap):
    def __init__(self, type):
        super(SelectBike, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Select Bike', "\n"])
        self.type = type

    def get_interactions(self):
        interactions = []
        interactions.append(ActionButton('Go back',self.go_back))
        interactions.append(urwid.Text('select bike'))
        for bike in bikes:
            interactions.append(urwid.Text('**********************************'))
            interactions.append(urwid.Text('brand: ' + bike.bike_brand))
            interactions.append(urwid.Text('model: ' + bike.bike_model))
            interactions.append(urwid.Text('year: ' + bike.bike_year))
            interactions.append(urwid.Text('owner: ' + bike.bike_owner))
            if self.type == 'Workshop':
                interactions.append(SelectionButton('load bike. ', self.go_to_workshop, bike))
            elif self.type == 'Service':
                interactions.append(SelectionButton('load bike. ', self.go_to_service, bike))
            interactions.append(urwid.Text('**********************************'))
        return interactions

    def go_back(self,object):
        game.update_place(Workshop())

    def go_to_workshop(self, object):
        print("do owrkshop")

    def go_to_service(self,object):
        print("do service")

    def go_back(self):
        game.update_place(Main())

    def grab_bike(self, selector):
        selected_bike.select_bike(selector.get_selection())
        game.update_place(TestView())


class WorkshopBike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(WorkshopBike, self)
        self.heading = urwid.Text([u"\nLocation: ", 'workshop bike', "\n"])
        self.choices = choices
        self.interactions = []
        # create links back to ourself

    def get_interactions(self):
        interactions = []
        interactions.append(ActionButton('nothjing',[]))
        return interactions

    def enter_place(self, button):
        game.update_place(self)


class Service(urwid.WidgetWrap):
    def __init__(self):
        super(Service, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Service', "\n"])
        # create links back to ourself

    def get_interactions(self):
        interactions = []
        interactions.append(ActionButton('select bike', self.go_to_selectBike))
        interactions.append(ActionButton('goBack: ', self.go_back))
        return interactions

    def go_to_selectBike(self,bike):
        game.update_place(SelectBike('Service'))

    def go_back(self, place):
        game.update_place(Main())


class ServiceBike(urwid.WidgetWrap):
    def __init__(self, choices):
        super(ServiceBike, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Service Bike', "\n"])
        self.choices = choices
        # create links back to ourself

    def get_interactions(self):
        interactions = []
        interactions.append(ActionButton('doNothing',[]))
        return interactions

    def enter_place(self, button):
        game.update_place(self)


class BikeView(urwid.WidgetWrap):
    def __init__(self):
        super(BikeView, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Bike', "\n"])

    def get_interactions(self):
        interactions = []
        interactions.append(ActionButton("New", self.go_to_new))
        interactions.append(ActionButton("Load", self.go_to_load))
        interactions.append(ActionButton("go Back", self.go_to_main))
        return interactions

    def go_to_main(self, object):
        game.update_place(Main())

    def go_to_new(self, object):
        game.update_place(New())

    def go_to_load(self, object):
        game.update_place(Load())


class Load(urwid.WidgetWrap):
    def __init__(self):
        super(Load, self)
        self.heading = urwid.Text([u"\nLocation: ", 'Load', "\n"])
        self.interactions = []
        # create links back to ourself

    def get_interactions(self):
        self.interactions = []
        self.interactions.append(ActionButton('go Back',self.go_back))
        self.interactions.append(urwid.Text('select bike'))
        for bike in bikes:
            self.interactions.append(urwid.Text('**********************************'))
            self.interactions.append(urwid.Text('brand: ' + bike.bike_brand))
            self.interactions.append(urwid.Text('model: ' + bike.bike_model))
            self.interactions.append(urwid.Text('year: ' + bike.bike_year))
            self.interactions.append(urwid.Text('owner: ' + bike.bike_owner))
            self.interactions.append(SelectionButton('load bike. ', self.grab_bike, bike))
            self.interactions.append(urwid.Text('**********************************'))

        return self.interactions

    def go_back(self, object):
        game.update_place(BikeView())

    def grab_bike(self, selector):
        selected_bike.select_bike(selector.get_selection())
        game.update_place(TestView())

    def enter_place(self, button):
        game.update_place(self)

class TestView(urwid.WidgetWrap):
    def __init__(self):
        super(TestView, self)
        self.heading = urwid.Text([u"\nLocation: ", 'New', "\n"])

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text(selected_bike.get_bike().bike_brand))
        interactions.append(urwid.Text(selected_bike.get_bike().bike_owner))
        interactions.append(urwid.Text(selected_bike.get_bike().bike_model))
        interactions.append(urwid.Text(selected_bike.get_bike().bike_year))
        interactions.append(ActionButton('go back', self.go_back))
        return interactions

    def go_back(self, object):
        game.update_place(Main())

    def enter_place(self, button):
        game.update_place(self)


class New(urwid.WidgetWrap):
    def __init__(self):
        super(New, self)
        self.heading = urwid.Text([u"\nLocation: ", 'New', "\n"])
        self.bike_brand = ''
        self.bike_model = ''
        self.bike_year = ''
        self.bike_owner = ''

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text('fill bike details'))
        self.bike_brand = urwid.Edit("brand: ")
        self.bike_model = urwid.Edit("model: ")
        self.bike_year = urwid.Edit("year: ")
        self.bike_owner = urwid.Edit("owner: ")
        interactions.append(self.bike_brand)
        interactions.append(self.bike_model)
        interactions.append(self.bike_year)
        interactions.append(self.bike_owner)
        interactions.append(ActionButton([u" > Create  ", 'Bike'], self.create_bike))
        interactions.append(ActionButton("go Back: ", self.go_back))
        return interactions

    def enter_place(self, button):
        game.update_place(self)

    def go_back(self, object):
        game.update_place(BikeView())

    def create_bike(self, bikeAux):
        bike = Bike(self.bike_brand, self.bike_model, self.bike_year, self.bike_owner)
        bikes.append(bike)
        game.update_place(BikeView())


class Start(object):
    def __init__(self):
        self.log = urwid.SimpleFocusListWalker([], wrap_around=False)
        self.top = urwid.ListBox(self.log)
        self.update_place(Main())

    def update_place(self, place):
        self.log.clear()
        self.log.append(urwid.Pile([place.heading]))
        if place.get_interactions():
            for i in place.get_interactions():
                self.log.append(i)
        self.top.focus_position = len(self.log) - 1



def exit_program(button):
    raise urwid.ExitMainLoop()

class SelectedBike():
    def __init__(self):
        self.selectedBike: Bike
    def select_bike(self,bike):
        self.selectedBike = bike
    def get_bike(self):
        return self.selectedBike


bikes: Bike = []
selected_bike = SelectedBike()

game = Start()
urwid.MainLoop(game.top, palette=[('reversed', 'standout', '')]).run()
