import urwid
from Bike import Bike

class BikeCreator:
    def __init__(self):
        self.bike_brand = urwid.Edit("brand: ")
        self.bike_model = urwid.Edit("model: ")
        self.bike_year = urwid.Edit("year: ")
        self.bike_owner = urwid.Edit("owner: ")
        self.bike_kilometers = urwid.Edit("kilometers: ")
        self.licence_plate = urwid.Edit("Licence plate: ")
        self.date = ''
        self.services = []

    def populate_interactions(self, interactions):
        interactions.append(self.bike_brand)
        interactions.append(self.bike_model)
        interactions.append(self.bike_year)
        interactions.append(self.bike_owner)
        interactions.append(self.bike_kilometers)
        interactions.append(self.licence_plate)

    def populate_interactions_with_bike(self, interactions, bike:Bike):
        self.populate_interactions(interactions)
        self.bike_brand.set_edit_text(bike.bike_brand)
        self.bike_model.set_edit_text(bike.bike_model)
        self.bike_year.set_edit_text(bike.bike_year)
        self.bike_owner.set_edit_text(bike.bike_owner)
        self.bike_kilometers.set_edit_text(bike.bike_kilometers)
        self.licence_plate.set_edit_text(bike.licence_plate)
        self.date = bike.bike_date
        self.services = bike.get_services()
        return self

    def submit(self):
        bike = Bike(self.bike_brand.get_edit_text(), self.bike_model.get_edit_text(), self.bike_year.get_edit_text(),
             self.bike_owner.get_edit_text(), self.bike_kilometers.get_edit_text(), self.licence_plate.get_edit_text())
        return bike

    def editted(self):
        new_bike = Bike(self.bike_brand.get_edit_text(), self.bike_model.get_edit_text(), self.bike_year.get_edit_text(),
                    self.bike_owner.get_edit_text(), self.bike_kilometers.get_edit_text(), self.licence_plate.get_edit_text())
        if self.date:
            new_bike.bike_date = self.date
        if self.services:
            new_bike.services = self.services

        return new_bike



