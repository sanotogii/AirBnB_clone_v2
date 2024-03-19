import unittest

"""test_console
Module for testing the HBNBCommand console.
"""

from io import StringIO
from unittest.mock import patch
import unittest


class TestHBNBCommand(unittest.TestCase):
    """
    Test for the HBNBCommand console.
    """

    def test_do_create(self):
        """
        Test create command. Includes checks for errors.
        """
        for classname in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.cmd.onecmd(f"create {classname}")
            uid = f.getvalue()[:-1]
            self.assertTrue(len(uid) > 0)
            key = (f"{classname}.{uid}")

            with patch('sys.stdout', new=StringIO()) as f:
                self.cmd.onecmd(f"all {classname}")
            self.assertTrue(uid in f.getvalue())

        # no class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("create")
        self.assertEqual(f.getvalue()[:-1], "** class name missing **")

        # nonexistent class name
        with patch('sys.stdout', new=StringIO()) as f:
            self.cmd.onecmd("create srhbk")
        self.assertEqual(f.getvalue()[:-1], "** class doesn't exist **")


if __name__ == '__main__':
    unittest.main()