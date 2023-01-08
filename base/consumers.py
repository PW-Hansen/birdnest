import json
from time import sleep
from channels.generic.websocket import WebsocketConsumer
from . import functions

# URL for drone data to be downloaded.

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        while True:
            time, drone_list = functions.read_guardb1rd_xml()

            self.send(json.dumps({'message': time}))
            sleep(1)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

