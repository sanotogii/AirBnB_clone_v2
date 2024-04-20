import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place

class TestConsoleCreate(unittest.TestCase):
    def setUp(self):
        """Set up the test"""
        self.console = HBNBCommand()
        self.mock_stdout = StringIO()

    def tearDown(self):
        """Clean up after the test"""
        self.console = None
        self.mock_stdout.close()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_state(self, mock_stdout):
        """Test creating a State object with parameters"""
        self.assertFalse(State in storage.all())
        args = "create State name=\"California\""
        self.console.onecmd(args)
        self.assertTrue(State in storage.all())
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) == 36)  # Check if UUID is printed

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_place(self, mock_stdout):
        """Test creating a Place object with parameters"""
        self.assertFalse(Place in storage.all())
        args = "create Place city_id=\"0001\" user_id=\"0001\" name=\"My_little_house\" number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300 latitude=37.773972 longitude=-122.431297"
        self.console.onecmd(args)
        self.assertTrue(Place in storage.all())
        output = mock_stdout.getvalue().strip()
        self.assertTrue(len(output) == 36)  # Check if UUID is printed

if __name__ == "__main__":
    unittest.main()