#!/usr/bin/python3
"""define HNNBCommand"""
import cmd


class HBNBCommand(cmd.Cmd):
    """"contain entry point of the command interpreter"""
    prompt = "(hbnb) "
    
    def emptyline(self):
        """do nothing upon recieving an empty line"""
        pass
    
    def do_EOF(self, args):
        """handle End of file"""
        print()
        return True       
    def do_quit(self, args):
        """quit the command to exit the program"""
        return True

if __name__ == '__main__':
    HBNBCommand().cmdloop()

