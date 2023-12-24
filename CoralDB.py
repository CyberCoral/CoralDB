##########################################
##                                                                                       ##
## CoralDB, your simple substitute to a DB Software ##
##                                                                                       ##
##########################################

# ver. Sun/24/Dec/2023
#
# Made by: CyberCoral
# ------------------------------------------------
# Github:
# https://www.github.com/CyberCoral
#

# built-in
import os, sys, subprocess, re

# main directory of file
current_dir = str(sys.argv[0][::-1][10:][::-1]).replace("\\","/")
print("The current directory is:\n{}".format(current_dir))
os.chdir(current_dir)

# main db class
class db:
    def __init__(self, data, location):
        self.data = str(data)
        self.location = str(location)
        self.i = -1
        # Creates file if not found with the specified data in current directory.
        try:
            with open(location,"r") as f:
                f.read()
        except FileNotFoundError:
            with open(location,"w") as f:
                f.write(data)

    def __str__(self):
        a = sys.argv[0][::-1][10:][::-1].replace('\\','/')
        return f"{str(a)}{self.location}"

    def __len__(self):
        with open(self.location,"r") as f:
            a = f.readlines()
            b = 0
            for i in range(len(a)):
                b += len(str(a[i]))

            return b

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.location,"r") as f:
            a = f.readlines()
        self.i = (self.i + 1) % len(a)
        return a[self.i]

    def read(self,*,line = "all"):
        '''
        This program lets you read
        the file you wrote, either all of it
        (with line = 'all')
        or only a specific line.
        '''
        if line != "all" and isinstance(line, int) != True:
            raise SyntaxError("The line that is going to be read has to be an integer or 'all', not ({}).".format(line))
        
        with open(self.location,"r") as f:
            a = f.readlines()

            if isinstance(line, int) == True:
                if line <= 0:
                    raise IndexError("The line has to be a natural number, not zero or negative.")
                elif line > len(a):
                    raise MemoryError("There is no access to memory that has not been created.")
            
            if line == "all":
                for i in range(len(a)):
                    print(a[i])
            elif line:
                print(a[line])

    def read_all_by_line(self,*,loop=True):
        '''
        It's a generator which
        yields the lines of the files,
        so you can read the lines
        one by one.
        It loops if you want to.
        '''
        if isinstance(loop, bool) != True:
            raise SyntaxError("Loop has to be a bool.")
        with open(self.location,"r") as f:
            a = f.readlines()
        for i in range(0, len(a)+1):
            if i == len(a) and loop == True:
                i = 0
                print("It loops back all over again.")
            elif i == len(a):
                return "Done"
            yield a[i]

    def data_alloc(self, data, location1, location2,*, mode: str = "-w"):
        '''
        Allocates any data to a text file:
        "-w": overwrites to file.
        "-a": appends to file.
        "-s": swap lines between files.
        '''
        data_loose = []
        data, location1, location2 = str(data), str(location1), str(location2)
        modes = ["-w","-a","-s"]
        if mode not in modes:
            raise IndexError(f"Mode ({mode}) not in modes ({modes}).")
        
        try:
            #
            # Retrieve data or lose it.
            #
            with open(location1,"r") as f:
                data_loose = f.readlines()
                i = 0
                while True:
                    if i == len(data_loose):
                        print(f"Data ({data}) has not been found from location1 ({location1}).")
                        return 1
                    elif re.search(data, data_loose[i]) != None:
                        print(f"Data ({data}) has been successfully retrieved from location1 ({location1}).")
                        data = (data, location1, i)
                        break
                    i += 1

        except FileNotFoundError:
            print(f"Either file ({location1}) does not exist in your system or in the current directory.")
            return 1

        # Swap mode
        if mode == "-s":
            c = ""
            try:
                with open(location2,"r") as a:
                    search = a.readlines()
                    new = []
                    with open(location2,"a") as b:
                        if len(search)  < data[2] - 1:
                            for i in range(len(data_loose)):
                                if i == data[2] - 1:
                                    c = "".join([str(i) for i in search[i]])
                                    b.write(str(data[0]+"\n"))
                                else:
                                    b.write(str(search[i]+"\n"))
                            print(f"Data ({data[0]}) has been moved to location2 ({location2}).")
                        else:
                            raise MemoryError("Data cannot be written in a non-existant memory space.")
                        
                with open(location1,"r") as d_prime:
                    d_p = d_prime.readlines()
                    
                with open(f"{location1}_copy","a") as d:
                    for i in range(len(d_p)):
                        if i == data[2] - 1:
                            d.write(str(c+"\n"))
                        else:
                            d.write(str(search[i]+"\n"))

                print(f"The other data ({c}) has been swapped from location2 to location1 ({location2}, {location1}).")
                return 0
                                                
            except FileNotFoundError:
                print(f"Either file ({location2}) does not exist in your system or in the current directory.")
            
        # Add mode ("-a") or write mode ("-w")
        with open(location2, mode[1]) as f:
            f.write(str(data[0]+"\n"))
            print(f"Data ({data}) has been successfully {(lambda a: 'added' if a == '-a' else 'written')(data)} to location2 ({location2})!")
            
        return 0

    def make_dir(self, dir_location):
        '''
        Creates a folder from db into
        the main folder.
        '''
        dir_location = str(dir_location)
        try:
            os.mkdir("{}".format(dir_location))
        except FileExistsError:
            print(f"The directory ({current_folder}/{dir_location}) has already been created.")
            return 0


def change_main_dir(new_dir: str = None):
    '''
    Changes the main folder in which
    this program operates.
    Beware of the use of this command,
    because it can cause chaos if misused.\n
    The developer is not responsible of your
    actions.
    '''
    if new_dir == None:
        print("Nothing has changed...")
        return 0
    else:
        try:
            os.chdir(new_dir)
            print("The current directory is:\n{}\n".format(new_dir))
            return 0
        except FileNotFoundError:
            print(f"The directory ({current_folder}/{new_dir}) has not been created yet.\nUse make_dir() in class db first and then use this, with caution of course.")
            return 0

def help_main():
    print("\n\nWelcome new user!\nI'm CyberCoral, the creator of this program and this help() function will serve you as a guide for using the program.")

    print("The first thing is that you can initialize a db() instance by putting in the shell:\n\n<var> = db(<value>,<file>)\n\nIf <file> doesn't exist, the program will create one automatically.\n")

    print("The available functions of the  last version of this program (24/Dec/2023) are:\n\ndata_alloc(data, location1, location2,*,mode (it has to be '-w', '-a' or '-s')):\nIt allocates data from a directory to another one.\nTip: if you assign location1 and location2 the same directory, you can rewrite or append data to your file.")
    print("\n\nmake_dir(dir_location (must not exist beforehand)):\nIt will create a new folder, you can use it to store data in folder and access the files more easily.\n")
    print("\nread(self,*,line=<int var>)\nThe function prints all of the lines (if <var> == 'all') or only one line (if <var> is greater than 0)\n")
    print("\nread_all_by_line(self)\nIt's a generator which yields the lines of text of the db instance.\n")
    print("\nAfter seeing what class db has to offer, there are more functions:\n\nchange_main_dir(new_dir (must not exist beforehand)):\nIt changes the main directory in which the program is working on.\nBeware of its uses, because you could do a great damage to yourself if misused.")

    print("\nYou can always check these instructions with help(), see you later user!\n\n")

help_main()
