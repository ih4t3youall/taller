from Services import Services
import datetime

class Bike:
    def __init__(self, bike_brand, bike_model, bike_year, bike_owner, bike_kilometers):
        self.bike_brand = bike_brand.get_edit_text()
        self.bike_model = bike_model.get_edit_text()
        self.bike_year = bike_year.get_edit_text()
        self.bike_owner = bike_owner.get_edit_text()
        self.bike_kilometers = bike_kilometers.get_edit_text()
        self.bike_date = datetime.date.today().strftime("%d-%m-%Y")
        self.services = []

    def add_service(self, service: Services):
        self.services.append(service)

    def get_services(self):
        return self.services

