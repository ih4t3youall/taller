import datetime

class Services:

    def __init__(self, oil, oil_filter, air_filter, fbf, rbf, kilometers, description):
        self.oil = oil
        self.oil_filter = oil_filter
        self.air_filter = air_filter
        #front brake fluid
        self.fbf = fbf
        #rear breake fluid
        self.rbf = rbf
        self.kilometers = kilometers
        self.description = description
        self.date = datetime.date.today().strftime("%d-%m-%Y")



