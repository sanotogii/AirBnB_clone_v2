#!/usr/bin/python3

"""
Console that runs commands for the airbnb project.
Importing the cmd and other necessary modules
"""
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):

    """
    HBNBCommand class for handling commands in the HBNB application.

    Attributes:
    - prompt (str): The prompt displayed to the user.

    Methods:
    - dict_update(...): updates with dictionary
    - do_all(arg): Prints all instances.
    - do_count(arg): counts the instances of a class.
    - do_create(arg): Creates a new instance of BaseModel.
    - do_destroy(arg): Deletes an instance.
    - emptyline: handles empty line as input
    - do_EOF: implements end of file.
    - do_exit(arg): Alias for the quit command.
    - do_quit(arg): Exits the program.
    - do_show(arg): Prints the string representation of an instance.
    - do_update(arg): Updates an instance.
    """

    prompt = "(hbnb) "
    classes = ["BaseModel", "User", "Place", "State", "City",
               "Amenity", "Review"]

    def default(self, line):
        """Called when input command prefix is not recognized."""
        if '.' in line:
            commands = line.split('.')
            class_name = commands[0]
            method_with_args = commands[1]

            method_name, arg_with_end_bracket = method_with_args.split('(')

            # Check if the class name exists
            if class_name in self.classes:

                if len(arg_with_end_bracket) > 1:
                    # Remove the closing parenthesis
                    arg_with_quotes = arg_with_end_bracket.strip(')')
                    pattern = r"\{[^{}]*\}"
                    matches = re.findall(pattern, arg_with_quotes)
                    if matches and method_name == "update":
                        id_dict = arg_with_quotes.split(',', 1)[0].strip('"')
                        attr_dict = eval(matches[0])
                        # Call dict_update with dictionary
                        self.dict_update(class_name, id_dict, attr_dict)
                        return
                    if ' ' in arg_with_quotes:
                        update_array = arg_with_quotes.split(', ')
                        update_args = []
                        for i in update_array:
                            split_i = i.strip().strip('"').split('"')
                            update_args.extend(split_i)

                        if method_name == "update":
                            update_str = ' '.join([class_name] + update_args)
                            # Call do_update method with update_str
                            self.do_update(update_str)
                            return

                    # Check if arg starts and ends with quotes
                    if '"' in arg_with_quotes and '"' in arg_with_quotes[::-1]:
                        argument = arg_with_quotes[1:-1]  # Remove quotes

                    # assign id to argument
                    id_arg = argument
                    arg = f"{class_name} {id_arg}"

                    if method_name == "destroy":
                        self.do_destroy(arg)
                        return

                    elif method_name == "show":
                        self.do_show(arg)
                        return
                else:
                    if method_name == "create":
                        self.do_create(class_name)
                        return
                    elif method_name == "all":
                        self.do_all(class_name)
                    elif method_name == "count":
                        self.do_count(class_name)
            elif not class_name:
                print("** class name missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("Unknown command:", line)

    def dict_update(self, class_name, id_dict, attribute_dict):
        """Updates an instance with a dictionary of attributes"""
        all_objs = storage.all()
        obj_key = "{}.{}".format(class_name, id_dict)
        if obj_key not in all_objs:
            print("** no instance found **")
            return
        obj = all_objs[obj_key]
        for attribute, value in attribute_dict.items():
            setattr(obj, attribute, value)
        obj.save()

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """Implements EOF input."""
        print()
        return True

    # aliasing the command
    do_exit = do_quit

    def do_count(self, arg):
        """ Count the instances of a class."""
        args = arg.split(' ')
        if not args[0]:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            matches = [
                key for key in storage.all() if key.startswith(
                    args[0] + '.')]
            print(len(matches))

    def emptyline(self):
        """Emptyline method"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel"""
        if not arg:
            print("** class name missing **")
            return
        elif arg not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = eval(arg)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        obj_key = "{}.{}".format(args[0], args[1])
        if obj_key not in all_objs:
            print("** no instance found **")
            return

        print(all_objs[obj_key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()

        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        obj_key = "{}.{}".format(args[0], args[1])

        if obj_key not in all_objs:
            print("** no instance found **")
            return

        del all_objs[obj_key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances.
        Can filter with optional class name.

        Usage:
            (hbnb) all <optional class_name>
            (hbnb) <optional class_name>.all()
        """
        args = arg.split()
        all_objs = storage.all()

        if args and args[0] not in self.classes:
            print("** class doesn't exist **")
            return

        instances = [str(all_objs[obj]) for obj in all_objs
                     if not args or obj.startswith(args[0] + ".")]
        print(instances)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return
        elif len(args) < 3:
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            print("** value missing **")
            return

        all_objs = storage.all()
        obj_key = "{}.{}".format(args[0], args[1])
        if obj_key not in all_objs:
            print("** no instance found **")
            return

        obj = all_objs[obj_key]
        setattr(obj, args[2], args[3])
        obj.save()


# Gracefully handle wrong input eg BaseModel.User, user.count

if __name__ == '__main__':
    HBNBCommand().cmdloop()
