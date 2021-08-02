from Services import Services
import datetime
import json

class Bike:
    def __init__(self, bike_brand, bike_model, bike_year, bike_owner, bike_kilometers, licence_plate):
        self.bike_brand = bike_brand
        self.bike_model = bike_model
        self.bike_year = bike_year
        self.bike_owner = bike_owner
        self.bike_kilometers = bike_kilometers
        self.licence_plate = licence_plate
        self.bike_date = datetime.date.today().strftime("%d-%m-%Y")
        self.services = []
        self.preformed_tasks = []

    def add_service(self, service: Services):
        self.services.append(service)

    def get_services(self):
        return self.services

    def add_preformed_task(self, preformed_task):
        self.preformed_tasks.append(preformed_task)

    def get_preformed_tasks(self):
        return self.preformed_tasks

    def to_json(self):
        
        services_json = json.dumps([ob.__dict__ for ob in self.services])
        preformed_tasks_json = json.dumps([ob.__dict__ for ob in self.preformed_tasks ])

        return  "{"\
        "\"bike_brand\":\""+self.bike_brand+"\","\
        "\"bike_model\":\""+ self.bike_model+"\","\
        "\"bike_year\":\""+ self.bike_year+"\","\
        "\"bike_owner\":\""+ self.bike_owner+"\","\
        "\"bike_kilometers\":\""+ self.bike_kilometers+"\","\
        "\"licence_plate\":\""+ self.licence_plate+"\","\
        "\"bike_date\":\""+ datetime.date.today().strftime("%d-%m-%Y")+"\","\
        "\"services\": "+services_json+""\
        "}"
        #"\"preformed_tasks\": "+preformed_tasks_json+""\ #tengo que ver como hacer para no escribir si no hay


