#
#********************************************************************************
#   room.py
#   Tehillah Kangamba 7859367
#   Comp4300
#   Assignment 1
#   collection of rooms in chat and its members
#********************************************************************************
#
from os import remove
from re import M


class Member:
    def __init__(self,name,sock) :
        self.name = name
        self.sock = sock

    def __repr__(self):
        return f"{self.name}"
        

class Rooms:
    def __init__(self):
        self.rooms = {
            "movies":[]
        }

    def add_room(self,name):
        self.rooms[name]=[]

    #   add_room_member
    #   returns false if room is full i.e room > 5
    def add_room_member(self,room_name,user_name,sock):
        result = False
       
        if len(self.rooms[room_name]) < 5:
            self.rooms[room_name].append(Member(user_name,sock))
            result = True
        print(self.rooms[room_name])
        return result

    def get_rooms(self):
        print(list(self.rooms.keys()))
        return list(self.rooms.keys())

    def get_members(self,room):
        result = []
        members = self.rooms[room]
        for member in members:
            result.append(member.name)
        return result

    def num_members(self,key):
        return len(self.rooms[key])

    def get_room(self,room_name):
        return self.rooms[room_name]

    def remove_member(self,room,name):
        result = False
        for member in self.rooms[room]:
            if member.name == name:
                self.rooms[room].remove(member)
                #print(self.rooms)
                result = True
        return result