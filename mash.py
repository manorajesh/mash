import os

# MAno SHell - mash

def echo(usrInput):
    print(" ".join(usrInput.split()[1:]))

def help():
    print("""
    help - display this help message
    exit - exit the program
    echo - echo the input to standard output
    manote - text editor
    ls - list the files in the current directory
    rm - remove the file
    """)

def manote(filename):
    print("\nWelcome to the manote, your one stop-shop for text editing\n")
    usrInput = ''
    while True:
        file = open(filename, "a")
        usrInput = input(f"{os.path.abspath(filename)} ^ ")
        if usrInput == "exit":
            file.close()
            exit()
        elif usrInput == "help":
            print("""manote is a very simple text editor.\n
            You can append text to the end of the file and preview the selected file\n
            When the cursor is "^", you can enter text commands such as edit or preview\n
            To enter edit mode, type "e" for edit. You will see the "+" cursor indicating edit mode.\n
            To exit and save, press enter.\n
            To preview the file, type "p" for preview.\n
            To exit the program, type "q" to quit\n
            """)
        elif usrInput == "e":
            usrInput = input(f"{os.path.abspath(filename)} + ")
            file.write(usrInput)
        elif usrInput == "p":
            file = open(filename, "r")
            print(file.read())
        elif usrInput == "q":
            file.close()
            break
        else:
            print(f"\nmanote: unrecognized command\n\t'{usrInput}' is not a valid command\n")

def ls():
    print("\n".join(os.listdir()))

def rm(filename, force=False):
    if os.path.isdir(os.path.abspath(filename)):
        print(f"rm: cannot remove '{filename}': Is a directory")
    elif os.path.exists(filename):
        if not force:
            usrInput = input(f"rm: remove '{filename}'? (y/N) ")
            if usrInput == "y":
                os.remove(filename)
            elif usrInput == "n" or usrInput == "N" or usrInput == "":
                print(f"rm: '{filename}' not removed\n")
        else:
            os.remove(filename)
    else:
        print(f"\nFileError: {filename} does not exist\n")


while True:
    usrInput = input("mash ~ $ ")
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
            manote(usrInput.split()[1])
        except IndexError:
            print("\nSyntaxError: invalid syntax\n\t'manote' requires an argument\n")
    elif usrInput.split()[0] == "ls":
        ls()
    elif usrInput.split()[0] == "rm":
        try:
            if usrInput.split()[1] == "-f":
                rm(usrInput.split()[2], True)
            else:
                rm(usrInput.split()[1])
        except IndexError:
            print("\nSyntaxError: invalid syntax\n\t'rm' requires an argument or -f flag\n")
    else:
        print(f"\nSyntaxError: invalid syntax\n\t'{usrInput}' is not a valid command\n")
