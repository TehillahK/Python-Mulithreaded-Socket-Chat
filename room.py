
class Rooms:
    def __init__(self):
        self.rooms = {
            "movies":[]
        }

    def add_room_member(self,room_name,sock):
        self.rooms[room_name].append(sock)
        print(self.rooms[room_name])

    def get_rooms(self):
        return list(self.rooms.keys())

    def get_room(self,room_name):
        return self.rooms[room_name]