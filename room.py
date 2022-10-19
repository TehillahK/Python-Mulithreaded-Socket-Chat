#
#********************************************************************************
#   room.py
#   Tehillah Kangamba 7859367
#   Comp4300
#   Assignment 1
#   collection of rooms in chat and its members
#********************************************************************************
#


# Member class
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

    # add_room
    # name param is the name of the room being added
    # returns None
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

    #   get_rooms
    #   returns a list of current available rooms
    def get_rooms(self):
        return list(self.rooms.keys())

    # get_members
    # room param is the room we want the members of
    # returns a list of members in a room's names
    def get_members(self,room):
        result = []
        members = self.rooms[room]
        for member in members:
            result.append(member.name)
        return result

    # num_members
    # key param is the name of the room
    # gets number of members in room
    def num_members(self,key):
        return len(self.rooms[key])

    # get_room
    # room_name param is the name of the room
    # returns members of a room with member objects that includes socket objects
    def get_room(self,room_name):
        return self.rooms[room_name]

    # remove_member
    # room param is the room of the member we want to 
    # remove and name is the name of member we want to remove
    # returns true if removing that member worked
    def remove_member(self,room,name):
        result = False
        for member in self.rooms[room]:
            if member.name == name:
                self.rooms[room].remove(member)
                result = True
        return result