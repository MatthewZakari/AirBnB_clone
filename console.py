#!/usr/bin/python3
"""
Console Module
"""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from shlex import split

def parse(arg):
    matches = re.finditer(r"(\{.*?\}|\[.*?\]|[^,\s]+)", arg)
    return [match.group().strip(",") for match in matches]

class HBNBCommand(cmd.Cmd):
    """
    Defines the HBnB command interpreter.
    """

    prompt = "(hbnb) "
    classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    
    }

    @classmethod
    def get_classes(cls):
        return cls.__classes

    def emptyline(self):
        """Called when an empty line is entered"""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }

        """Splitting the command into command and arguments"""
        command, _, args = arg.partition(' ')
        if '(' in args and args.endswith(')'):
            """Extracting the function name and arguments"""
            function_name, _, arguments = args.partition('(')
            arguments = arguments.rstrip(')')
            if function_name in argdict:
                """Constructing the command call and executing it"""
                call = f"{command} {arguments}"
                return argdict[function_name](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program when End Of File is reached"""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create and print a new class instance and its id.
        """
        argl = parse(arg)
        class_name = argl[0] if argl else None
        if not class_name:
            print("** class name missing **")
        elif class_name not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(class_name)()
            print(new_instance.id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display str representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()

        if not argl:
            print("** class name missing **")
            return
        class_name = argl[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(argl) < 2:
            print("** instance id missing **")
            return
        instance_id = argl[1]

        instance_key = "{}.{}".format(class_name, instance_id)
        if instance_key not in objdict:
            print("** no instance found **")
            return

        print(objdict[instance_key])

    def do_destroy(self, arg):
        """
        Deletes an instance based on its class name and ID.

        Usage:
            destroy <class> <id> or <class>.destroy(<id>)

        Parameters:
            <class>: The class name of the instance to delete.
            <id>: The ID of the instance to delete.
        """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")

        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class.
        """
        
        arg_list = parse(arg)
        """Initialize count variable"""
        count = 0
        """Iterate through all instances in storage"""
        for obj in storage.all().values():
            """Check if the class name matches the specified class"""
            if arg_list[0] == obj.__class__.__name__:
                count += 1
        """Print the count"""
        print(count)

    def do_update(self, arg):
        parsed_args = parse(arg)
        stored_objects = storage.all()
        error_messages = {
                0: "** class name missing **",
                1: "** class doesn't exist **",
                2: "** instance id missing **",
                3: "** no instance found **",
                4: "** attribute name missing **",
                5: "** value missing **"
                }
        for i in range(len(parsed_args)):
            if i == 1 and parsed_args[i] not in self.classes:
                print(error_messages[i])
                return False

            obj_key = "{}.{}".format(parsed_args[0], parsed_args[1])
            if i == 3 and obj_key not in stored_objects.keys():
                print(error_messages[i])
                return False
            if i < len(parsed_args):
                print(error_messages[i])
                return False
        
        obj = stored_objects[obj_key]
        if len(parsed_args) == 4:
            attr_name = parsed_args[2]
            attr_value = parsed_args[3]
            if attr_name in obj.__class__.__dict__.keys():
                attr_type = type(obj.__class__.__dict__[attr_name])
                obj.__dict__[attr_name] = attr_type(attr_value)
            else:
                obj.__dict__[attr_name] = attr_value
        elif type(eval(parsed_args[2])) == dict:
            for key, value in eval(parsed_args[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key]) in {str, int, float}):
                    attr_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = attr_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()

