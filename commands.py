import os
import readchar

def echo(usrInput):
    print(" ".join(usrInput.split()[1:]))

def help():
    print("""
    help - display this help message
    exit - exit the program
    echo - echo the input to standard output
    manote - text editor
    ls - list the files in the current directory or in the specified directory
    rm - remove the file
    cd - change the current working directory
    cls - clear the screen
    cat - display the contents of a file
    """)

## Simple text editor
## Extremely high CPU usage (30%) because of the readchar.readkey() function
## The function detects each keypress and invokes a code block

def manote(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        file = open(filename, "r+")
    textBuffer = file.read()

    keyInput = ''
    # \x11 == CTRL-Q
    # \x18 == CTRL-X
    # Enter does not work properly

    while keyInput != "\x11" or keyInput != "\x18":
        os.system("clear")
        print(textBuffer + "█")
        keyInput = readchar.readkey()

        if keyInput == "\x7f":
            textBuffer = textBuffer[0:len(textBuffer)-1]
        elif keyInput == "\r":
            textBuffer = textBuffer + "\n"
        else:
            textBuffer += keyInput
    
    # save file if combo was CRTL+X
    # quit program if combo was CRTL+Q
    if keyInput == "\x18":
        file.close()
        file = open(filename, "w")
        file.write(textBuffer)
        file.close()
    else:
        file.close()
        exit()

def manote_deprecated(filename):
    print("\nWelcome to the manote, your one stop-shop for text editing\n")
    usrInput = ''
    while True:
        file = open(filename, "a")
        usrInput = input(f"{os.path.abspath(filename)} ^ ")
        if usrInput == "exit":
            file.close()
            exit()
        elif usrInput == "help":
            print("""
            manote is a very simple text editor.\n
            You can append text to the end of the file and preview the selected file\n
            When the cursor is "^", you can enter text commands such as edit or preview\n
            To enter edit mode, type "e" for edit. You will see the "+" cursor indicating edit mode.\n
            To exit and save, press enter.\n
            To preview the file, type "p" for preview.\n
            To exit the program, type "q" to quit
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

def ls(dirname=None):
    print("\n".join(os.listdir(dirname)))

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

def cd(path):
    if path == '~':
        os.chdir(os.path.expanduser('~'))
    elif os.path.exists(path):
        os.chdir(path)
    elif not os.path.isdir(path):
        print(f"\nDirectoryError: {path} is not a directory\n")
    else:
        print(f"\nDirectoryError: {path} is invalid\n")

def cls():
    os.system("clear")

def cat(filename):
    if os.path.isdir(filename):
        print(f"\ncat: {filename} is a directory\n")
    elif os.path.exists(filename):
        file = open(filename, "r")
        print(file.read())
    else:
        print(f"\nFileError: {filename} does not exist\n")