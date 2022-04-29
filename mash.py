from commands import *
import os
import sys

# MAno SHell - mash

def main():
    print("\033[2J\033[;H", end='') # clear the screen
    try:
        while True:
            try:
                usrInput = input(f"{os.getcwd()} @ mash ~ $ ")
                if usrInput == "":
                    continue
                elif usrInput == "exit":
                    exit()
                elif usrInput == "help":
                    help()
                elif usrInput.split()[0] == "echo":
                    echo(usrInput)
                elif usrInput.split()[0] == "manote":
                    try:
                        manote = Manote(usrInput.split()[1])
                    except IndexError:
                        print("\nSyntaxError: invalid syntax\n\t'manote' requires an argument\n")
                elif usrInput.split()[0] == "ls":
                    try:
                        ls(usrInput.split()[1])
                    except IndexError:
                        ls()
                elif usrInput.split()[0] == "rm":
                    try:
                        if usrInput.split()[1] == "-f":
                            rm(usrInput.split()[2], True)
                        else:
                            rm(usrInput.split()[1])
                    except IndexError:
                        print("\nSyntaxError: invalid syntax\n\t'rm' requires an argument or -f force flag\n")
                elif usrInput.split()[0] == "cd":
                    try:
                        cd(usrInput.split()[1])
                    except IndexError:
                        print("\nSyntaxError: invalid syntax\n\t'cd' requires an argument\n")
                elif usrInput.split()[0] == "cat":
                    try:
                        cat(usrInput.split()[1])
                    except IndexError:
                        print("\nSyntaxError: invalid syntax\n\t'cat' requires an argument\n")
                elif usrInput.split()[0] == "cls" or usrInput.split()[0] == "clr" or usrInput.split()[0] == "clear":
                    cls()
                elif usrInput.split()[0] == "python":
                    try:
                        python(usrInput.split()[1])
                    except IndexError:
                        print("\nSyntaxError: invalid syntax\n\t'python' requires an argument\n")
                else:
                    print(f"\nSyntaxError: invalid syntax\n\t'{usrInput}' is not a valid command\n")
            except PermissionError:
                print(f"\nPermissionError: cannot access '{usrInput.split()[1]}'\n")
    except KeyboardInterrupt:
        print(f"\nKeyboardInterrupt: exiting\n")
        exit()

if __name__ == "__main__":
    main()