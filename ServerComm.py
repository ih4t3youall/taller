import requests
import json

class ServerComm:

    def backup(self, bikes):
        data = {"config": "tu_tia"}
        url = "http://localhost:8080/save_config"
        response = requests.post(url, data)
        #jsonObject = json.dumps(bikes.__dict__)
        writer = open("file.txt","w")
        writer.write("[")
        for bike in bikes:
            writer.write(bike.to_json())
            #hay que sacar esa comma
            writer.write(",")
        writer.write("]")
        writer.close()
        print(response)

