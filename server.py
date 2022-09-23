
import socket
import json
from room import Rooms
class Server:
    def __init__(self,port=3000):
        self._port = port
        self._host = ''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms = Rooms()

    def get_chat_names(self):
        pass
        


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
                conn.sendall(json.dumps(self.rooms.get_rooms()).encode())



def main():
    server = Server()
    server.start()

if __name__=="__main__":
    main()