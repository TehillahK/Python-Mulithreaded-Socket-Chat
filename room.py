
class Rooms:
    def __init__(self):
        self.rooms = {
            "movies":[]
        }

    def add_room(self,room_name):
        self.rooms[room_name] = []

    def get_rooms(self):
        return list(self.rooms.keys())