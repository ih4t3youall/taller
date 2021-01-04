from pathlib import Path
import pickle
import os
import urwid
from Bike import Bike
from Services import Services


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
        self.interactions.append(ActionButton('Exit', exit_program))
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


class DoService(urwid.WidgetWrap):
    def __init__(self, bike_selected):
        super(DoService, self)
        self.bike_selected = bike_selected
        self.heading = urwid.Text([u"\nLocation: ", 'Do workshop', "\n"])
        self.oil = ''
        self.oil_filter = ''
        self.air_filter = ''
        self.fbf = ''
        self.rbf = ''
        self.text = ''
        self.kilometers = ''

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text(self.bike_selected.bike_brand))
        interactions.append(urwid.Text(self.bike_selected.bike_model))
        interactions.append(urwid.Text(self.bike_selected.bike_year))
        interactions.append(urwid.Text(self.bike_selected.bike_owner))
        interactions.append(urwid.Text("***************************"))
        self.oil = urwid.CheckBox('oil change', False)
        interactions.append(self.oil)
        self.oil_filter = urwid.CheckBox('oil filter change', False)
        interactions.append(self.oil_filter)
        self.air_filter = urwid.CheckBox('air filter change', False)
        interactions.append(self.air_filter)
        self.fbf = urwid.CheckBox('front break fluid', False)
        interactions.append(self.fbf)
        self.rbf = urwid.CheckBox('rear break fluid', False)
        interactions.append(self.rbf)
        self.kilometers = urwid.Edit("Kilometers: ")
        interactions.append(self.kilometers)
        self.text = urwid.Edit("Preformed tasks (oil used, etc): ")
        interactions.append(self.text)
        interactions.append(ActionButton("Aceptar", self.save_service))
        return interactions

    def save_service(self, object):
        service_done = Services(self.oil.get_state(), self.oil_filter.get_state(),self.air_filter.get_state(), self.fbf.get_state(), self.rbf.get_state(), self.kilometers.get_edit_text(), self.text.get_edit_text())
        self.bike_selected.add_service(service_done)
        save_bike()
        game.update_place(Main())


class DoWorkshop(urwid.WidgetWrap):
    def __init__(self,bike_selected):
        super(DoWorkshop, self)
        self.bike_selected = bike_selected
        self.heading = urwid.Text([u"\nLocation: ", 'Do service', "\n"])

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text(self.bike_selected.bike_brand))
        interactions.append(urwid.Text(self.bike_selected.bike_model))
        interactions.append(urwid.Text(self.bike_selected.bike_year))
        interactions.append(urwid.Text(self.bike_selected.bike_owner))
        interactions.append(urwid.Text("***************************"))
        interactions.append(urwid.Text("Preformed tasks"))
        interactions.append(urwid.Edit())
        interactions.append(ActionButton("Aceptar",self.save_workshop))
        return interactions

    def save_workshop(self, object):
        print("save stuff")
        game.update_place(Main())

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

    def go_back(self, object):
        if self.type == 'Workshop':
            game.update_place(Workshop())
        else:
            game.update_place(Service())

    def go_to_workshop(self, button):
        game.update_place(DoWorkshop(button.get_selection()))
        print("do owrkshop")

    def go_to_service(self, button):
        game.update_place(DoService(button.get_selection()))




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

class PopUp(urwid.WidgetWrap):
    def __init__(self, bikeService):
        super(PopUp, self)
        self.index_bike = bikeService[0]
        self.index_service = bikeService[1]
        self.heading = urwid.Text([u"\nconfirm window ", '', "\n"])

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text("are you sure you want to remove this bike?"))
        interactions.append(ActionButton('Ok',self.delete))
        interactions.append(ActionButton('No',self.go_back))
        return interactions

    def delete(self, object):
        if self.index_service != -1:
            bikes[self.index_bike].get_services().pop(self.index_service)
        else:
            bikes.pop(self.index_bike)
        save_bike()
        game.update_place(Load())

    def go_back(self,object):
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
        bike_cont = 0
        for bike in bikes:
            self.interactions.append(urwid.Text('**********************************'))
            self.interactions.append(urwid.Text('Brand: ' + bike.bike_brand))
            self.interactions.append(urwid.Text('Model: ' + bike.bike_model))
            self.interactions.append(urwid.Text('Year: ' + bike.bike_year))
            self.interactions.append(urwid.Text('Owner: ' + bike.bike_owner))
            self.interactions.append(urwid.Text('Kilometers in admission: ' + bike.bike_kilometers))
            self.interactions.append(urwid.Text('Licence Plate: ' + bike.licence_plate))
            self.interactions.append(urwid.Text('Date of admission: ' + bike.bike_date))
            self.interactions.append(urwid.Text("---------------------------------------"))
            self.interactions.append(SelectionButton('Delete Bike. ', self.delete_bike, [bike_cont, -1]))
            self.interactions.append(urwid.Text('Service history'))
            if bike.get_services():
                service_cont = 0
                for service in bike.get_services():
                    self.interactions.append(urwid.Text('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))
                    self.interactions.append(urwid.Text("Oil change: "+str(service.oil)))
                    self.interactions.append(urwid.Text("Oil filter change: "+str(service.oil_filter)))
                    self.interactions.append(urwid.Text("Air filter: "+str(service.air_filter)))
                    self.interactions.append(urwid.Text("Front break fluid: "+str(service.fbf)))
                    self.interactions.append(urwid.Text("Rear break fluid: "+str(service.rbf)))
                    self.interactions.append(urwid.Text("Kilometers: "+str(service.kilometers)))
                    self.interactions.append(urwid.Text("Description: "+str(service.description)))
                    self.interactions.append(urwid.Text("Date: " + str(service.date)))
                    self.interactions.append(SelectionButton('Delete Service. ',self.delete_service, [bike_cont, service_cont]))
                    self.interactions.append(urwid.Text('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'))
                    service_cont = service_cont +1
            bike_cont = bike_cont+1
            self.interactions.append(urwid.Text('**********************************'))
            self.interactions.append(urwid.Text(''))

        return self.interactions

    def go_back(self, object):
        game.update_place(BikeView())

    def delete_service(self, button):
        #el primero es la posicion de la moto y el segundo la posicion del service dentro de la  moto
        service_to_delete = button.get_selection()
        #le mando las coordenandas que tiene que borrar
        game.update_place(PopUp(service_to_delete))

    def delete_bike(self, button):
        bike_to_delete = button.get_selection()
        game.update_place(PopUp(bike_to_delete))

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
        self.bike_kilometers = ''
        self.licence_plate = ''

    def get_interactions(self):
        interactions = []
        interactions.append(urwid.Text('fill bike details'))
        self.bike_brand = urwid.Edit("brand: ")
        self.bike_model = urwid.Edit("model: ")
        self.bike_year = urwid.Edit("year: ")
        self.bike_owner = urwid.Edit("owner: ")
        self.bike_kilometers = urwid.Edit("kilometers: ")
        self.licence_plate = urwid.Edit("Licence plate: ")
        interactions.append(self.bike_brand)
        interactions.append(self.bike_model)
        interactions.append(self.bike_year)
        interactions.append(self.bike_owner)
        interactions.append(self.bike_kilometers)
        interactions.append(self.licence_plate)
        interactions.append(ActionButton([u" > Create  ", 'Bike'], self.create_bike))
        interactions.append(ActionButton("go Back: ", self.go_back))
        return interactions

    def enter_place(self, button):
        game.update_place(self)

    def go_back(self, object):
        game.update_place(BikeView())

    def create_bike(self, bikeAux):
        bike = Bike(self.bike_brand, self.bike_model, self.bike_year, self.bike_owner, self.bike_kilometers, self.licence_plate)
        bikes.append(bike)
        save_bike()
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
        #setea el menu seleccionado
        self.top.focus_position = 1



def exit_program(button):
    raise urwid.ExitMainLoop()

class SelectedBike():
    def __init__(self):
        self.selectedBike: Bike
    def select_bike(self,bike):
        self.selectedBike = bike
    def get_bike(self):
        return self.selectedBike

def check_folders(folder):
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
        except OSError:
            print("Creation of the directory %s failed" % folder)
def load_bikes(dataFile):
    if os.path.exists(dataFile):
        bikes = None
        with open(dataFile, 'rb') as tallerData:
            bikes = pickle.load(tallerData)
        return bikes
    return []

def save_bike():
    with open(dataFile, 'wb') as to_save:
        pickle.dump(bikes, to_save)



folder = str(Path.home()) + "/Taller"
dataFile = folder + "/taller.data"
check_folders(folder)
bikes = []
bikes = load_bikes(dataFile)







game = Start()
urwid.MainLoop(game.top, palette=[('reversed', 'standout', '')]).run()
