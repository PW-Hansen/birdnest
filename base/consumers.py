import json
from time import sleep
from channels.generic.websocket import WebsocketConsumer
from .functions import generate_violating_pilots_string

# URL for drone data to be downloaded.

class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        while True:
            violating_pilots = generate_violating_pilots_string()

            self.send(json.dumps({'message': violating_pilots}))
            sleep(1)

    def disconnect(self, close_code):
        pass