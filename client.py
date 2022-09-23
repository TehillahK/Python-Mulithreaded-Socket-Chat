from lib2to3.pytree import convert
import socket
import json
from unittest import result


class Client:

    def __init__(self):
        self.rooms = []

    def convert_to_dict(self , data):
        result = json.loads(data)
        return result

    def convert_to_json(self,data):
        result = json.dumps(data)
        return result

    def show_rooms(self):
        print("Available chat rooms")
        count = 0
        for room in self.rooms:
            print(f"Room Number: {count}\nRoom Name:  {room}\n")

    def join_room(self):
        print("pick a room to join")

    def make_message(self,type,name,message):
        result = self.convert_to_json( {
            "type":type,
            "name": name,
            "message":message
        })
        return result
        

    def start(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            join_msg = self.make_message("join-netork","Tehillah","")
            s.sendall(join_msg.encode())
            while True:
                data = s.recv(1024)
                if data:
                    self.rooms = self.convert_to_dict(data)
                    self.show_rooms()                    

client = Client()
client.start()
    