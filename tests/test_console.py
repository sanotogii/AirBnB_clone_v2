import unittest
import os
import MySQLdb
from console import HBNBCommand

class TestConsoleCreate(unittest.TestCase):
    def setUp(self):
        """Set up the test"""
        self.console = HBNBCommand()
        self.db = MySQLdb.connect(host=os.getenv('HBNB_MYSQL_HOST'),
                                  user=os.getenv('HBNB_MYSQL_USER'),
                                  passwd=os.getenv('HBNB_MYSQL_PWD'),
                                  db=os.getenv('HBNB_MYSQL_DB'))
        self.cursor = self.db.cursor()

    def tearDown(self):
        """Clean up after the test"""
        self.console = None
        self.cursor.close()
        self.db.close()

    def count_states(self):
        """Count the number of records in the states table"""
        self.cursor.execute("SELECT COUNT(*) FROM states")
        result = self.cursor.fetchone()
        return result[0]

    def test_create_state(self):
        """Test creating a State object with parameters"""
        initial_count = self.count_states()
        args = "create State name=\"California\""
        self.console.onecmd(args)
        final_count = self.count_states()
        self.assertEqual(final_count, initial_count + 1)

if __name__ == "__main__":
    unittest.main()