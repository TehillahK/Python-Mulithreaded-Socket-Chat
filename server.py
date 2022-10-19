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

    # convert_to_json
    # converts dict to json object
    # data param ,is a dict object to be conveted
    # returns a json obj
    def convert_to_json(self, data):
        return json.dumps(data)

    # convert_to_dict
    # converts json to python dictionay
    # data param , is the json object to be converted
    # returns a dictionary  obj
    def convert_to_dict(self,data):
        return json.loads(data)

    # make_message
    # this is a helper method that creates a regular message dict object
    # type param is the type of message being sent
    # name param is the name of the user sending the message
    # message param is the name of the  message is being sent to
    # returns dict object of a message
    def make_message(self,type,name,message,status="success",members = None):
        result = self.convert_to_json( {
            "type":type,
            "name": name,
            "message":message,
            "members":members,
            "status":status
        })
        return result
    
    # broadcast_to_room
    # sends a message to all members of a room
    # name param is the name of the room a message is being broadcasted to
    # message is the message being broadcasted
    # returns none object
    def broadcast_to_room(self,name,message):
        room = self.rooms.get_room(name)
        for member in room:
            try:
                member.sock.sendall(message)
            except Exception as e:
                print("something went wrong , a member of a room must be disconnected")
                continue

    # get_room_names
    # returns a list of room names
    def get_room_names(self):
        return self.rooms.get_rooms()

    # handle_req
    # handle requests made to server
    # conn is the socket that connected to the server
    # returns reply message as a dict to clients
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
        elif command["type"] == "leave-room":
            name = command["name"]
            room = command["message"]
            print(f"{name} is leaving a room")
            del_member = self.rooms.remove_member(room , name)
            if del_member:
                return self.make_message("leave-room-reply","server", "success")
            else:
                return self.make_message("leave-room-reply","server","failed")
        elif command["type"] == "stats":
           room = command["message"]
           name = command["name"]
           print(f"{name} wants to see stats")
           return self.make_message(
               "stats-reply", "server", self.rooms.get_members(room), members=self.rooms.get_members(room))

    # threading_func
    # defines what the  threads by sending and reply to client message
    # returns None object
    def threading_func(self,conn):
        threading.Lock().acquire()
        data = conn.recv(1024)
        if data:
            print(data)
            conn.sendall(self.handle_req(data,conn).encode())
        threading.Lock().locked()

    # start
    # starts the server
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
                continue
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
