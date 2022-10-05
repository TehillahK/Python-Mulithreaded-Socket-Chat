#
#********************************************************************************
#   server.py
#   Tehillah Kangamba 7859367
#   Comp4300
#   Assignment 1
#   This is tcp server for chat app
#********************************************************************************
#

import threading
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
    
    def make_message(self,type,name,message,status="success",members = None):
        result = self.convert_to_json( {
            "type":type,
            "name": name,
            "message":message,
            "members":members,
            "status":status
        })
        return result
        
    def broadcast_to_room(self,name,message):
        room = self.rooms.get_room(name)
        for member in room:
            member.sock.sendall(message)


    def get_room_names(self):
        return self.rooms.get_rooms()

    def handle_req(self,req,conn):
        command = self.convert_to_dict(req)
        print(command)
        if command["type"] == "join-netork":
            return self.make_message("join-network-reply","Tehillah",self.rooms.get_rooms())
        elif command["type"] == "create-room":
            self.rooms.add_room(command["message"])
            return self.make_message("create-room-reply","Tehillah","success")
        elif command["type"] == "join-room":
            print("joined room")
            room = command["message"]
            name  = command["name"]
            isSpace = self.rooms.add_room_member(room,name,conn)
            if isSpace:
                msg = self.make_message(
                    "join-room-reply", "server", self.rooms.get_members(room),members = self.rooms.get_members(room))
            else:
                msg = self.make_message(
                    "join-room-reply", "server", "failed",status="failed")
            return msg
        elif command["type"] == "room-message":
            print(command)
            room_name = command["room"]
            self.broadcast_to_room(name = room_name, message = req)
            return  self.make_message("room-message-reply","server","success")


    def threading_func(self,conn):
        threading.Lock().acquire()
        data = conn.recv(1024)
        if data:
            print(data)
            conn.sendall(self.handle_req(data,conn).encode())
        threading.Lock().locked()


    def start(self): 
        self.socket.bind((self._host,self._port))
        self.socket.listen(5)
        
        while True:
            try:
                print("server has started")
                conn,addr = self.socket.accept()
                print(f"connected ${conn}")
                new_thread = threading.Thread(target=self.threading_func,args=(conn,))
                new_thread.start()
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                self.socket.close()
            except Exception as e:
                print("failed for some reason")
                pass


            



def main():
    server = Server()
    server.start()


if __name__ == "__main__":
    main()
