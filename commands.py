import os
import readchar as rc
import mash
import time

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
    python - run a python file
    uname - display the system information
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
        mash.main()

    def quit(self):
        print('\033[?25h', end="") # show cursor
        try:
            self.file.close()
            mash.main()
        except (NameError, AttributeError):
            mash.main()

    def writeMode(self):
        print('\033[?25l', end="") # remove cursor
        index = len(self.textBuffer)
        while True:
            print("\033[2J\033[;H", end='') # clear the screen
            try:
                print(self.textBuffer[:index] + u"\u001b[7m" + self.textBuffer[index] + "\u001b[0m" + self.textBuffer[index+1:])
            except IndexError:
                print(self.textBuffer + "█")
            
            keyInput = rc.readkey()

            if keyInput == "\x7f":
                self.textBuffer = self.textBuffer[:index-1] + self.textBuffer[index:]
                index = index - 1 if index > 0 else 0
            elif keyInput == "\r":
                self.textBuffer += "\n"
                index += 1
            elif keyInput == "\x1b[D":
                index = index - 1 if index > 0 else 0
            elif keyInput == "\x1b[C":
                if index < len(self.textBuffer):
                    index += 1
            else:
                try:
                    if 32 <= ord(keyInput) <= 126:
                        self.textBuffer = self.textBuffer[:index] + keyInput + self.textBuffer[index:]
                        index += 1
                except TypeError:
                    print('\033[?25h', end="") # show cursor
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
        elif usrInput == "h":
            print("\nEnter w for write mode\nEnter q to quit\nEnter x to save and quit\nPress ESC twice to get to commands\n")
            timeout()
            self.commandMode()
        else:
            print(f"\nmanote: invalid syntax\n\t'{usrInput}' is not a valid command\n")
            timeout()
            self.commandMode()
    
    def syntaxHighlight(self, input):
        stripped = input.rstrip()
        return stripped + u"\u001b[41m" + " " *  (len(input) - len(stripped)) + u"\u001b[0m" 


def timeout(given_timeout=5, division=5):
    division = int(division)
    duration = given_timeout/division
    
    print('\033[?25l', end="") # remove cursor
    for i in range(division):
        print(".", end='')
        time.sleep(duration)
    print('\033[?25h', end="") # show cursor

def ls(dirname=None):
    try:
        print("\n".join(os.listdir(dirname)))
    except FileNotFoundError:
        print(f"\nDirectoryError: '{dirname}' does not exist\n")


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

def uname():
    print(" ".join(os.uname()))

if __name__ == "__main__":
    mash.main()