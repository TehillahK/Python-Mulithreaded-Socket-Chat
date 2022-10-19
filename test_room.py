from room import Rooms
import unittest

rooms = Rooms()

class TestRoom(unittest.TestCase):
    def test_add_room_member(self):
        result = rooms.add_room_member("movies", "John Doe", None)
        self.assertTrue(result ,"adding room member failed")

    def test_get_rooms(self):
        self.assertEqual(rooms.get_rooms(), ["movies"], "get rooms did not work")

    def test_get_memebers(self):
        self.assertEqual(rooms.get_members("movies"),["John Doe"])

    def test_num_members(self):
        self.assertEqual(rooms.num_members("movies"),1,"number of members worked")

    def test_remove_member(self):
        self.assertEqual(rooms.remove_member("movies","John Doe"),True,"failed to remove room member from a room")


if __name__ == '__main__':
    unittest.main()
