#!/usr/bin/python3

"""
Console that runs commands for the airbnb project.
Importing the cmd and other necessary modules
"""
import cmd
import re
import models
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
import shlex


classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

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

    def default(self, line):
        """Called when input command prefix is not recognized."""
        if '.' in line:
            commands = line.split('.')
            class_name = commands[0]
            method_with_args = commands[1]

            method_name, arg_with_end_bracket = method_with_args.split('(')

            # Check if the class name exists
            if class_name in classes:

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

    def do_EOF(self, arg):
        """Implements EOF input."""
        return True

    # aliasing the command
    do_exit = do_quit

    def do_count(self, arg):
        """ Count the instances of a class."""
        args = arg.split(' ')
        if not args[0]:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        else:
            matches = [
                key for key in storage.all() if key.startswith(
                    args[0] + '.')]
            print(len(matches))

    def emptyline(self):
        """Emptyline method"""
        pass

    def kv_parser(self, args):
        kwargs = {}
        for arg in args:
            kv = arg.split('=', 1)
            key = kv[0]
            value = kv[1]
            if value[0] == value[-1] == '"':
                value = shlex.split(value)[0].replace('_', ' ')
            else:
                try:
                    value = int(value)
                except:
                    try:
                        value = float(value)
                    except:
                        continue
            kwargs[key] = value
        return kwargs
    
    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] in classes:
            kwargs = self.kv_parser(args[1:])
            new_instance = classes[args[0]](**kwargs)
        else:
            print("** class doesn't exist **")
            return False

        print(new_instance.id)
        new_instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")



if __name__ == '__main__':
    HBNBCommand().cmdloop()
