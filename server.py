
import socket
import json
from room import Rooms
class Server:
    def __init__(self,port=3000):
        self._port = port
        self._host = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms = Rooms()

    def convert_to_json(self,data):
        return json.dumps(data)

    def convert_to_dict(self,data):
        return json.loads(data)

    def get_room_names(self):
        return self.rooms.get_rooms()

    def handle_req(self,req,conn):
        command = self.convert_to_dict(req)
        if command["type"] == "join-netork":
            return self.get_room_names()


    def start(self): 
        self.socket.bind((self._host,self._port))
        self.socket.listen()
        while True:
            print("server has started")
            conn,addr = self.socket.accept()
            print(f"connected ${conn}")
            data = conn.recv(1024)
            if data:
                print(data)
                conn.sendall(self.convert_to_json(self.handle_req(data,conn)).encode())



def main():
    server = Server()
    server.start()

if __name__=="__main__":
    main()