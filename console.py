#!/usr/bin/python3
"""define HNNBCommand"""
import cmd
from models.base_model import BaseModel
from models import storage
import json
import re


class HBNBCommand(cmd.Cmd):
    """"contain entry point of the command interpreter"""
    prompt = "(hbnb) "

    def default(self, args):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(args)

    def _precmd(self, args):
        """Intercepts commands to test for class.syntax()"""
        # print("PRECMD:::", args)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", args)
        if not match:
            return args
        classname = match.group(1)
        method = match.group(2)
        arg = match.group(3)
        match_uid_and_arg = re.search('^"([^"]*)"(?:, (.*))?$', arg)
        if match_uid_and_arg:
            uid = match_uid_and_arg.group(1)
            attr_or_dict = match_uid_and_arg.group(2)
        else:
            uid = arg
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def emptyline(self):
        """do nothing upon recieving an empty line"""
        pass

    def do_EOF(self, args):
        """handle End of file"""
        print()
        return True

    def do_quit(self, args):
        """quit the command to exit the.. program"""
        return True

    def do_create(self, args):
        """Creates an instance.
        """
        if args == "" or args is None:
            print("** class name missing **")
        elif args not in storage.classes():
            print("** class doesn't exist **")
        else:
            i = storage.classes()[args]()
            i.save()
            print(i.id)

    def do_show(self, args):
        """Prints the string representation of an instance.
        """
        if args == "" or args is None:
            print("** class name missing **")
        else:
            string = args.split(' ')
            if string[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(string) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(string[0], string[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id.
        """
        if args == "" or args is None:
            print("** class name missing **")
        else:
            string = args.split(' ')
            if string[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(string) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(string[0], string[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, args):
        """Prints all string representation of all instances.
        """
        if args != "":
            string = args.split(' ')
            if string[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                n_args = [str(obj) for key,
                          obj in storage.all().items()
                          if type(obj).__name__ == string[0]]
                print(n_args)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_count(self, args):
        """Counts the instances of a class.
        """
        string = args.split(' ')
        if not string[0]:
            print("** class name missing **")
        elif string[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    string[0] + '.')]
            print(len(matches))

    def do_update(self, args):
        """Updates an instance by adding or updating attribute.
        """
        if args == "" or args is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, args)
        class_name = match.group(1)
        uuid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif class_name not in storage.classes():
            print("** class doesn't exist **")
        elif uuid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(class_name, uuid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[class_name]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
