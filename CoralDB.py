######################################################
##                                                  ##
## CoralDB, your simple substitute to a DB Software ##
##                                                  ##
######################################################

# ver. Sun/24/Dec/2023
#
# Made by: CyberCoral
# ------------------------------------------------
# Github:
# https://www.github.com/CyberCoral
#

# built-in
import os, sys, re

# main directory of file
current_dir = str(sys.argv[0][::-1][10:][::-1]).replace("\\","/")
print("The current directory is:\n{}".format(current_dir))
os.chdir(current_dir)

# main db class
class db:
    def __init__(self, data, location):
        self.data = str(data)
        self.location = str(location)
        # Creates file if not found with the specified data in current directory.
        try:
            with open(location,"r") as f:
                f.read()
        except FileNotFoundError:
            with open(location,"w") as f:
                f.write(data)

    def __str__(self):
        a = sys.argv([0][::-1][10:][::-1]).replace('\\','/')
        return f"{str(a)}/{self.location}"

    def data_alloc(self, data, location1, location2,*, mode: str = "-w"):
        '''
        Allocates any data to a text file:
        "-w": overwrites to file.
        "-a": appends to file.
        "-s": swap lines between files.
        data = "all": all the data from a file.
        '''
        data_loose = []
        location1, location2 = str(location1), str(location2)
        modes = ["-w","-a","-s"]

        # Check if mode is in modes (no foreign modes).
        if mode not in modes:
            raise IndexError(f"Mode ({mode}) not in modes ({modes}).")
        
        try:
            #
            # Retrieve data or lose it.
            #
            with open(location1,"r") as f:
                data_loose = f.readlines()
                i = 0
                
                if data == -1:
                    data = (data_loose, location1, -1)
                    print("All the data has been obtained.")
                else:
                    data = str(data)
                    
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

        #
        # Swap mode here.
        #
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
            
        # Add mode ("-a") or write mode ("-w").
        with open(location2, mode[1]) as f:
            if data[2] == -1:
                for i in range(len(data[0])):
                    f.write(str(data[0][i]+"\n"))
            else:
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
            print(f"The directory ({current_dir}/{dir_location}) has already been created.")
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
            print(f"The directory ({current_dir}/{new_dir}) has not been created yet.\nUse make_dir() in class db first and then use this, with caution of course.")
            return 0

def help_main():
    print("\n\nWelcome new user!\nI'm CyberCoral, the creator of this program and this help() function will serve you as a guide for using the program.")

    print("The first thing is that you can initialize a db() instance by putting in the shell:\n\n<var> = db(<value>,<file>)\n\nIf <file> doesn't exist, the program will create one automatically.\n")

    print("The available functions of the  last version of this program (24/Dec/2023) are:\n\ndata_alloc(data, location1, location2,*,mode (it has to be '-w', '-a' or '-s')):\nIt allocates data from a directory to another one. It can assign all data from a file if data is -1 (not string -1, integer -1)\nTip: if you assign location1 and location2 the same directory, you can rewrite or append data to your file.")
    print("\n\nmake_dir(dir_location (must not exist beforehand)):\nIt will create a new folder, you can use it to store data in folder and access the files more easily.\n")
    print("\nAfter seeing what class db has to offer, there are more functions:\n\nchange_main_dir(new_dir (must not exist beforehand)):\nIt changes the main directory in which the program is working on.\nBeware of its uses, because you could do a great damage to yourself if misused.")

    print("\nYou can always check these instructions with help(), see you later user!\n\n")

help_main()
