#!/usr/bin/python3
"""
console
"""
import cmd
import re
from shlex import split
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def parse(arg):
    """Converts an input line to a list of toke/argument"""
    curly = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly is None and brackets is None:
        return [i.strip(',') for i in split(arg)]
    if curly is not None:
        pre = split(arg[:curly.span()[0]])
        tokens = [i.strip(',') for i in pre]
        tokens.append(curly.group())
    elif brackets is not None:
        pre = split(arg[:brackets.span()[0]])
        tokens = [i.strip(',') for i in pre]
        tokens.append(brackets.group())
    return tokens


class HBNBCommand(cmd.Cmd):
    """Entry point for the command interpreter"""

    prompt = '(hbnb) '

    __articles = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def do_quit(self, arg):
        """Quit command to exit the program\n"""

        return True

    def do_EOF(self, arg):
        """Defines what happens when an end-of-file is passed back.\n"""\
            """end-of-file is passed back as the string 'EOF'."""

        print()
        return True

    def emptyline(self):
        """ Do nothing when an empty line is entered"""
        pass

    def default(self, arg):
        """Default invalid input handling """

        meth_dic = {
            "all": self.do_all,
            "count": self.do_count,
            "create": self.do_create,
            "destroy": self.do_destroy,
            "show": self.do_show,
            "update": self.do_update
        }

        dot = re.search(r"\.", arg)
        if dot is not None:
            arg_list = [arg[:dot.span()[0]], arg[dot.span()[1]:]]
            par = re.search(r"\((.*?)\)", arg_list[1])
            if par is not None:
                command = [arg_list[1][:par.span()[0]], par.group()[1:-1]]
                if command[0] in meth_dic.keys():
                    input_args = "{} {}".format(arg_list[0], command[1])
                    meth_to_func = meth_dic[command[0]]
                    return meth_to_func(input_args)
        print("*** Unknown syntax: {}".format(arg))
        return

    def do_create(self, arg):
        """Usage: create <class>.\n"""\
            """Creates a new instance of the class in arg and prints it id."""

        tokens = parse(arg)
        if len(tokens) == 0:
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.__articles:
            print("** class doesn't exist **")
        else:
            print(eval(tokens[0])().id)
            storage.save()

    def do_count(self, arg):
        """Usage: <class name>.count().\n"""\
            """Retrieve the number of instances of a class."""

        count = 0
        tokens = parse(arg)
        if len(tokens) < 1:
            return
        store = storage.all()
        for obj in store.values():
            if obj.__class__.__name__ == tokens[0]:
                count += 1
        print(count)

    def do_show(self, arg):
        """Usage: show <class name> <id>.\n"""\
            """Displays the string representation of class instance"""\
            """based on given id."""

        store = storage.all()
        tokens = parse(arg)
        if len(tokens) == 0:
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.__articles:
            print("** class doesn't exist **")
        elif len(tokens) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(tokens[0], tokens[1]) not in store.keys():
            print("** no instance found **")
        else:
            print(store["{}.{}".format(tokens[0], tokens[1])])

    def do_destroy(Self, arg):
        """Usage: delete <class name> <id>.\n"""\
            """Deletes the class instance with the given id."""
        store = storage.all()
        tokens = parse(arg)
        if len(tokens) == 0:
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.__articles:
            print("** class doesn't exist **")
        elif len(tokens) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(tokens[0], tokens[1]) not in store.keys():
            print("** no instance found **")
        else:
            del store["{}.{}".format(tokens[0], tokens[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all <class name> or all.\nPrint """\
            """all string representation of all instances of a given class."""\
            """\nIf no class is specified, print all instantiated objects."""
        store = storage.all()
        tokens = parse(arg)
        if len(tokens) == 0:
            _all = [str(obj) for obj in store.values()]
        else:
            if tokens[0] not in HBNBCommand.__articles:
                print("** class doesn't exist **")
                return
            else:
                _all = []
                for obj in store.values():
                    if obj.__class__.__name__ == tokens[0]:
                        _all.append(str(obj))
        print(_all)

    def do_update(self, arg):
        """Usage: update <class name> <id> <attribute name> """\
            """\"<attribute value>\". \nUpdate class instance with """\
            """a given id by adding or updating attribute."""
        store = storage.all()
        tokens = parse(arg)
        print(tokens)
        if len(tokens) == 0:
            print("** class name missing **")
        elif tokens[0] not in HBNBCommand.__articles:
            print("** class doesn't exist **")
        elif len(tokens) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(tokens[0], tokens[1]) not in store.keys():
            print("** no instance found **")
        elif len(tokens) == 2:
            print("** attribute name missing **")
        elif len(tokens) == 3:
            if (type(eval(tokens[2])) != dict):
                print("** value missing **")
            else:
                obj = store["{}.{}".format(tokens[0], tokens[1])]
                for k, v in eval(tokens[2]).items():
                    if (k in obj.__class__.__dict__.keys() and
                            type(obj.__class__.__dict__[k] in
                                 {str, int, float})):
                        valtype = type(obj.__class__.__dict__[k])
                        obj.__dict__[k] = valtype(v)
                    else:
                        obj.__dict__[k] = v
        else:
            obj = store["{}.{}".format(tokens[0], tokens[1])]
            if tokens[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[tokens[2]])
                obj.__dict__[tokens[2]] = valtype(tokens[3])
            else:
                obj.__dict__[tokens[2]] = tokens[3]
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
