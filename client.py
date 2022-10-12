#
#********************************************************************************
#   client.py
#   Tehillah Kangamba 7859367
#   Comp4300
#   Assignment 1
#   This is tcp client of a messaging protocal
#********************************************************************************
#

from doctest import FAIL_FAST
import socket
import json
import os
import select
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

    def get_user_input(self,prompt):
        return input(prompt)

    def send_message(self,type,name,msg):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server
        message = self.convert_to_json({
            "type":type,
            "name":name,
            "message":msg
        })
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(15)
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            data = s.recv(1024)
            if data:
                self.handle_req(data)
            s.close()



    def send_room_message(self,msg):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        msg = self.make_room_message(self.screen_name,self.room,msg)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            s.sendall(msg.encode())
            s.close()

        

    def show_rooms(self):
        print("Enter room number to join a room or enter c to create room")
        print("Available chat rooms")
        count = 0
        for room in self.rooms:
            print(f"Room:{count} --- {room}\n")
            count = count + 1
            


    def join_room(self ):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server
        leave = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            join_msg = self.make_message("join-room",self.screen_name,"movies")
            s.sendall(join_msg.encode())
            s.setblocking(False)
            #self.send_room_message("")
            while not leave:
                inputs = [sys.stdin, s]
                readable, writable, exceptional = select.select(inputs,[],[])
                for source in readable:
                    if source == s:
                        data = s.recv(1024)
                        if data:
                            self.handle_req(data)
                    else:
                       # print('sending >>>>>',end="")
                        
                        message = sys.stdin.readline()
                        if message == "#\n":
                            print("leaving room")
                            self.send_message("leave-room",self.screen_name,self.room)
                            leave = True
                        elif message == '*\n':
                            print("find out whose currently in room")
                            self.send_message("stats",self.screen_name,self.room)
                        else:
                            self.send_room_message(message)
                            print(f"You : {message}")
                        
        
               

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
            #print(self.rooms)
    #        self.show_rooms()    
        #    print(command)
           # self.join_room()
        elif command["type"] == "join-room-reply" and command["status"] == "success":
            os.system('clear')
            members = command["members"]
            member_count = len(members)
            print(f"Welcome to {self.room} room.")
            print(f"Members in chat: {members}")
            print(f"Member Count: {member_count}")
            print("Enter # to leave room and * to see current room stats")
        elif command["type"] == "join-room-reply" and command["status"] == "failed":
            print("failed to join room because room is full")
        elif command["type"] == "room-message":
            user_name = command["name"]
            user_msg = command["message"]
            if user_name != self.screen_name:
               # print("here")
                print(f"{user_name} : {user_msg}")
        elif command["type"] == "stats-reply":
            members = command["members"]
            member_count = len(members)
        #    print(f"Welcome to {self.room} room.")
            print(f"Members in chat: {members}")
            print(f"Member Count: {member_count}")
            print("Enter # to leave room and * to see current room stats")
        

    def join_network(self):
        HOST = "127.0.0.1"  # The server's hostname or IP address
        PORT = 3000  # The port used by the server

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            join_msg = self.make_message("join-netork",self.screen_name,"")
            s.sendall(join_msg.encode())
            data = s.recv(1024)
            self.handle_req(data)
            s.close()
    def create_room(self):
        return input("Enter room name")


    def start(self):
        self.join_network()
        self.show_rooms()
        room_number = self.get_user_input("Select room number:")
        if room_number.isdigit():
            room_number = int(room_number)
            self.room = self.rooms[room_number]
            self.join_room()
        elif not room_number.isdigit() and room_number == "c":
            print("create a room,press enter after putting i name")
            room_name = self.get_user_input("Name:")
           # self.make_message("create-room",self.screen_name,room_name)
            self.send_message(type = "create-room", name = self.screen_name, msg = room_name)
            self.start()

                                   



def main():
    print(sys.argv[1])
    client = Client(sys.argv[1])
    client.start()



if __name__ == "__main__":
    main()
