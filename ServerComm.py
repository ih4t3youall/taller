import requests
import json

class ServerComm:

    def backup(self, bikes):
        data = {"config": "tu_tia"}
        url = "http://localhost:8080/save_config"
        response = requests.post(url, data)
        #jsonObject = json.dumps(bikes.__dict__)
        writer = open("file.txt","w")
        to_save = ""
        to_save += "["
        for bike in bikes:
            to_save += bike.to_json()
            to_save += ","
        to_save = to_save[:-1]
        to_save += "]"
        writer.write(to_save)
        writer.close()
        print(response)

