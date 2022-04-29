import os
import readchar as rc
import sys
import mash

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

class Manote:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = open(filename, "r")
            self.textBuffer = self.file.read()
        except FileNotFoundError:
            self.textBuffer = ''
        self.commandMode()

    def save(self):
        print('\033[?25h', end="") # show cursor
        try:
            self.file.close()
        except AttributeError: # if the file doesn't exist
            pass
        self.file = open(self.filename, "w")
        self.file.write(self.textBuffer)
        self.file.close()

    def quit(self):
        print('\033[?25h', end="") # show cursor
        try:
            self.file.close()
        except (NameError, AttributeError):
            pass

    def writeMode(self):
        keyInput = ''
        
        print('\033[?25l', end="") # remove cursor
        index = 0
        while keyInput == '' or keyInput != chr(27):
            print("\033[2J\033[;H", end='') # clear the screen
            print(self.textBuffer[index:] + "█")
            
            keyInput = rc.readkey()

            if keyInput == "\x7f":
                self.textBuffer = self.textBuffer[:-1]
                input -= 1
            elif keyInput == "\r":
                self.textBuffer += "\n"
            elif keyInput == "\x1b[A":
                if index > 0:
                    index -= 1
            elif keyInput == "\x1b[B":
                if index < len(self.textBuffer):
                    index += 1
            else:
                self.textBuffer = self.textBuffer[index:] + keyInput + self.textBuffer[:index]
        self.commandMode()
    
    def commandMode(self):
        print("\033[2J\033[;H", end='') # clear the screen
        self.columns, self.lines = os.get_terminal_size()
        print(self.textBuffer)
        usrInput = input("\n" * self.lines + ":")
        if usrInput == "x":
            self.save()
        elif usrInput == "q":
            self.quit()
        elif usrInput == "w":
            self.writeMode()
        else:
            print("\nSyntaxError: invalid syntax\n\t'{}' is not a valid command\n".format(usrInput))
            self.commandMode()
    
    def syntaxHighlight(self, input):
        stripped = input.rstrip()
        return stripped + u"\u001b[41m" + " " *  (len(input) - len(stripped)) + u"\u001b[0m" 


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

    print('\033[?25l', end="") # remove cursor
    while keyInput != rc.key.CTRL_Q or keyInput != rc.key.CTRL_X:
        os.system("clear")
        print(textBuffer + "█")
        keyInput = rc.readkey()

        if keyInput == "\x7f":
            textBuffer = textBuffer[:-1]
        elif keyInput == "\r":
            textBuffer += "\n"
        else:
            textBuffer += keyInput
    
    # save file if combo was CRTL+X
    # quit program if combo was CRTL+Q

    print('\033[?25h', end="") # show cursor
    if keyInput == rc.key.CTRL_X:
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
    print("\033[2J\033[;H", end='') # clear the screen

def cat(filename):
    if os.path.isdir(filename):
        print(f"\ncat: {filename} is a directory\n")
    elif os.path.exists(filename):
        file = open(filename, "r")
        print(file.read())
    else:
        print(f"\nFileError: {filename} does not exist\n")

def python(filename):
    exec(open(filename).read())

if __name__ == "__main__":
    mash.main()