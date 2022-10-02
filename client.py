
import socket
import json
import os
import sys


class Client:

    def __init__(self,screen_name):
        self.rooms = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.room = ""
        self.screen_name = screen_name

    def convert_to_dict(self , data):
        result = json.loads(data)
        return result

    def convert_to_json(self,data):
        result = json.dumps(data)
        return result

    def send_room_message(self,msg):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        msg = self.make_room_message(self.screen_name,"movies","yo")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(msg.encode())
            s.close()

    def show_rooms(self):
        print("Available chat rooms")
        count = 0
        for room in self.rooms:
            print(f"Room:{count} --- {room}\n")


    def join_room(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            join_msg = self.make_message("join-room",self.screen_name,"movies")
            s.sendall(join_msg.encode())
            self.send_room_message("")
            while True:
                data = s.recv(1024)
                if data:
                    self.handle_req(data)
           
            

    def make_room_message(self,user_name,room_name,message):
        result = self.convert_to_json({
            "type": "room-message",
            "room":room_name,
            "name": user_name,
            "message": message
        })
        return result
        

    def make_message(self,type,name,message):
        result = self.convert_to_json( {
            "type":type,
            "name": name,
            "message":message
        })
        return result
        
    def handle_req(self,data):
        command =  self.convert_to_dict(data)
        if command["type"] == "join-network-reply":
            self.rooms = command["message"]
            self.show_rooms()    
            self.join_room()
        elif command["type"] == "join-room-reply" and command["message"] == "success":
            os.system('clear')
            print("welcom to room ")
        elif command["type"] == "join-room-reply" and command["message"] == "success":
            print("failed to join room because room is full")
        elif command["type"] == "room-message":
            user_name = command["name"]
            user_msg = command["message"]
            print(f"{user_name} : {user_msg}")

    def join_network(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            join_msg = self.make_message("join-netork",self.screen_name,"")
            s.sendall(join_msg.encode())
            s.close()

    def start(self):
        self.join_network()
        self.join_room()
                                   



def main():
    print(sys.argv[1])
    client = Client(sys.argv[1])
    client.start()



if __name__ == "__main__":
    main()
