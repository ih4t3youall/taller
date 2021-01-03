class Bike:
    def __init__(self, bike_brand, bike_model, bike_year, bike_owner):
        self.bike_brand = bike_brand.get_edit_text()
        self.bike_model = bike_model.get_edit_text()
        self.bike_year = bike_year.get_edit_text()
        self.bike_owner = bike_owner.get_edit_text()


