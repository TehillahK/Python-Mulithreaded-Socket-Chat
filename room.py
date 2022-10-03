class Member:
    def __init__(self,name,sock) :
        self.name = name
        self.sock = sock
        

class Rooms:
    def __init__(self):
        self.rooms = {
            "movies":[]
        }

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