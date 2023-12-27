######################################################
##                                                  ##
## CoralDB, your simple substitute to a DB Software ##
##                                                  ##
######################################################

# ver. Wed/27/Dec/2023
#
# Made by: CyberCoral
# ------------------------------------------------
# Github:
# https://www.github.com/CyberCoral
#

# built-in
import os, sys, re

# main directory of file
current_dir = sys.argv[0][::-1][10:][::-1].replace("\\","/")
print("The current directory is:\n{}".format(current_dir))
os.chdir(current_dir)

# main db class
class db:
    def __init__(self, data, location,*,create_: bool = True):
        self.data = str(data)
        self.location = str(location)
        # Creates file if not found with the specified data in current directory.
        try:
            with open(location,"r") as f:
                f.read()
        except FileNotFoundError:
            if create_ == True:
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

    def one_liner_file(self):
        with open(self.location,"r") as f:
            a = f.readlines()
        a = "\\n".join(a)
        return a

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
                return 0
            else:
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
        data = "all": all the data from a file.
        location1 = "None": input from user.
        '''
        data_loose = []
        if location1 != None:
            location1 = str(location1)
            
        location2 = str(location2)
        
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

                data = str(data).replace("all","-1")
                
                if data == "-1":
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
            if location1 != None and (mode != "-s" and location1 == None):
                print(f"Either file ({location1}) does not exist in your system or in the current directory.")
                return 1
            data = (data, location1, 0)
        except TypeError:
            if location1 != None and (mode != "-s" and location1 == None):
                raise TypeError
            data = (data, location1, 0)

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

    def gen_security_key(self, magic_word,*,own_location: bool = False):
        '''
        Generates a security key for the database.
        Useful for give_permissions() and other
        admin functions.
        '''
        if isinstance(own_location, bool) != True:
            raise TypeError("Own_location must be a bool.")
        
        try:
            os.chdir(self.location)
            locate = self.location
        except NotADirectoryError:
            pass
        except FileNotFoundError:
            if own_location != True:
                raise FileNotFoundError("File is not found.")
        try:
            os.chdir("/"+self.location)
            locate = "/"+ self.location
        except FileNotFoundError:
            try:
                os.chdir(sys.argv[0][::-1][10:][::-1]+"/")
                locate = sys.argv[0][::-1][10:][::-1]+"/"
            except NotADirectoryError:
                return SyntaxError("'What did you do to make the current directory not a directory??????' Error")
        
        magic_word = str(magic_word)
        try:
            with open((lambda x: x[::-1][4:][::-1] if  x[::-1][4:][::-1] == ".txt" else x)(locate)+"/new_text_file.txt","w") as f:
                f.write(magic_word)
        except FileNotFoundError:
            raise KeyError("Location not found or cannot be written to.")
            
        os.chdir(current_dir)
        
        print("The security key has been generated.")
            
        return 0
    
    def give_permissions(self,*,key_location: str, magic_word: str,permission: int):
        '''
        Gives permissions to the user who is
        using the program of any kind.
        You must use the database key
        (input the name of the file and the
        key) to do this.
        '''
        magic_word = str(magic_word)
        if isinstance(permission, int) != True:
            raise TypeError("Permission has to be an int.")
        try:
            with open(key_location,"r") as f:
                magic_word_0 = f.readlines()[0]
                if magic_word != magic_word_0:
                    raise KeyError("Not valid key.")
        except FileNotFoundError:
            raise KeyError("The location of the key does not exist.")
        
        os.chmod(sys.argv[0].replace("\\","/"),permission)

        print("Operation done.")

        return 0

    def search(self, data_to_search, *, dir_location: str = None, times = 1, amplitude: int = -1,  list_format: bool = True, mute: bool = False):
        '''
        Searches instances of
        data (data_to_search),
        from 'dir_location' directory,
        an int(times) number of times.
        The directory that is being used
        must have enough permissions.

        The amplitude determines the
        number of characters
        searched at a time.
        
        - If amplitude equals -1, it will be
        relative to len(data_to_search)

        - If times equals -1, it will check for
        all the possible matches.
        '''

        if isinstance(data_to_search, list) != True and isinstance(data_to_search, str) != True:
            raise TypeError("data_to_search must be either a string or a list.")
        elif isinstance(data_to_search, str) == True:
            data_to_search = [data_to_search]

        if isinstance(mute, bool) != True:
            raise TypeError("")
            
        results = []
    

        if dir_location == None:
            dir_location = sys.argv[0][::-1][11:][::-1].replace("\\","/")+"/"+self.location

        if isinstance(times, int) != True:
            raise TypeError("times must be an int.")
        elif times < 0:
            raise ValueError("times must be a natural number.")

        if isinstance(amplitude, int) != True:
            raise TypeError("amplitude must be an int.")
        elif times < 1 and times != -1:
            raise ValueError("amplitude must be greater than 1.")
        elif amplitude < len(data_to_search) and amplitude != -1:
            raise IndexError("amplitude must be greater than the length of the string 'data_to_search'.")
        

        if isinstance(list_format, bool) != True:
            return TypeError("list_format must be a bool.")
        
        try:
            with open(dir_location,"r") as f:
                a = f.readlines()
        except FileNotFoundError:
            print("The folder has not been found.")
            return 1
        except OSError:
            raise SyntaxError("The file returned OSError, maybe you asked for a folder in {}?".format(dir_location))


        # A list which registers the regex searches done by re.search()
        boo = []

        i = 0
        # Converts all the data into a one-liner for a moment
        a = "".join(a)
        
        # A dynamic variable that only increases that serves as a counter.
        increment = 0

        # A static variable.
        len_a=len(a)
        
        while times > 0 or times == -1:
            c = 0
            
            if increment >= len_a:
                break
            
            for k in range(len(data_to_search)):
                
                if amplitude == -1:
                    amplitude = len(data_to_search[k])
                    
                b = re.search(data_to_search[k],a[(i*amplitude):(i+1)*amplitude])

                boo.append(b)
                
                if b is not None:
                    c = b.end()
                    results.append([a[b.start():b.end()],(b.start()+increment,b.end()+increment)])
                    if times != -1:
                        times -= 1
                    i = 0
                
                else:
                    i += 1
                    c = i*(amplitude+1)

                increment += c
                a = a[c:]

        if mute != True:
            print("The total successful matches are {}.".format(len(results)))
            
        if list_format == True:
            return results
        elif mute != True:
            for i in range(len(results)):
                print("The match number {} between characters {} and {} is:\n".format(i,results[i][1], results[i][2]))
                print(f"{results[i][0]}\n")
                
        return 0

    def search_all(self,data_to_search,*,directory = sys.argv[0][::-1][11:][::-1].replace("\\","/")+"/",times: int = 1, amplitude: int = -1, list_format: bool = True):
        '''
        Searches all instances of data (data to search)
        from all the possible files of the directory.
        It only sees .txt files, but it has
        the same settings as search().
        '''

        directory = directory.replace("\\","/")
        if directory == None:
            directory = sys.argv[0][::-1][11:][::-1]+"/"+self.location

        if isinstance(data_to_search, list) != True and isinstance(data_to_search, str) != True:
            raise TypeError("data_to_search must be either a string or a list.")
        elif isinstance(data_to_search, str) == True:
            data_to_search = [data_to_search]

        if isinstance(times, int) != True:
            return TypeError("times must be an int.")
        elif times < 0 and times != -1:
            return ValueError("times must be a natural number.")

        if isinstance(list_format, bool) != True:
            return TypeError("list_format must be a bool.")
        
        results = []

        print("The directory that was introduced is named:\n{}\n".format(directory))

        possible_dirs = os.listdir(path = directory)

        if [x[::-1][:4][::-1] == ".txt" for x in possible_dirs].count(False) >= 1:
            while True:
                try:
                    a = [x[::-1][:4][::-1] == ".txt" for x in possible_dirs].index(False)
                    del possible_dirs[a]
                except ValueError:
                    break

        print("The files that will be inspected are in this list:\n{}\n".format(possible_dirs))

        for i in range(len(possible_dirs)):
            results.append([self.search(data_to_search,dir_location=possible_dirs[i], times=times, amplitude = amplitude, mute = True),directory+possible_dirs[i]])

        for j in range(len(results)):
            if results[0][0] == []:
                del results[0]
            
        print("The total successful file matches are {}.".format(len(results)))
        if list_format == True:
            return results
        for i in range(len(results)):
            print("The total successful matches in file\n{}\nare {}.\n".format(results[i][1],len(results[i][0])))
            print(f"{results[i][0]}")
        return 0

    def replace(self,*,data_to_search,replace_word,dir_location: str = None, times = -1, mute: bool = False):
        '''
        Replaces a string (or strings)
        with (only) other one
        in a file a number of (times) times.
        '''
        if isinstance(data_to_search, list) != True and isinstance(data_to_search, str) != True:
            raise TypeError("data_to_search must be either a string or a list.")
        elif isinstance(data_to_search, str) == True:
            data_to_search = [data_to_search]

        if isinstance(mute, bool) != True:
            raise TypeError("")
            
        results = []

        if dir_location == None:
            dir_location = sys.argv[0][::-1][11:][::-1].replace("\\","/")+"/"+self.location

        if isinstance(times, int) != True:
            raise TypeError("times must be an int.")
        elif times < 0 and times != -1:
            raise ValueError("times must be a natural number.")        
        
        try:
            with open(dir_location,"r") as f:
                a = (lambda a: [a][0] if isinstance(a[0], list) != True else a)(f.readlines())
        except FileNotFoundError:
            print("The folder has not been found.")
            return 1
        except OSError:
            raise SyntaxError("The file returned OSError, maybe you asked for a folder in {}?".format(dir_location))

        i = 0
        len_a=len(a)

        with open(dir_location,"w") as f:
            f.write("")
            f.close()

        with open(dir_location,"a") as f:
        
            while times > 0 or times == -1:

                if i >= len_a:
                     break

                a[i] = (lambda a: a[::-1][1:][::-1] if a[::-1][0] == "\n" else a)(a[i])
                
                for k in range(len(data_to_search)):
                        
                    b = re.search(data_to_search[k],a[i])
                    
                    if b is not None:
                        a[i] = a[i].replace(data_to_search[k],replace_word)
                        if times != -1:
                            times -= 1
                    
                f.write(f"{a[i]}\n")
                i += 1
                                        
        if mute != True:
            print("All the instances of {} have been replaced with {}.".format(data_to_search, replace_word))
                
        return 0

    def replace_all(self,*,data_to_search,replace_word,directory: str = sys.argv[0][::-1][10:][::-1], times = -1, key_location: str, magic_word: str, mute: bool = False):
        '''
        Replace key word(s) <data_to_search>
        for replace_words 'times' times
        in all of directory files.
        You must introduce the correct magic_word
        and the key_location to do this as admin.
        '''

        directory = directory.replace("\\","/")
        if directory == None:
            directory = sys.argv[0][::-1][11:][::-1]+"/"+self.location

        if isinstance(data_to_search, list) != True and isinstance(data_to_search, str) != True:
            raise TypeError("data_to_search must be either a string or a list.")
        elif isinstance(data_to_search, str) == True:
            data_to_search = [data_to_search]

        if isinstance(times, int) != True:
            return TypeError("times must be an int.")
        elif times < 0 and times != -1:
            return ValueError("times must be a natural number.")

        magic_word = str(magic_word)
        try:
            with open(key_location,"r") as f:
                magic_word_0 = f.readlines()[0]
                if re.search(magic_word, magic_word_0) == None:
                    raise KeyError("Not valid pass key.")
                elif re.search(magic_word, magic_word_0).start() != 0:
                    raise KeyError("Not valid pass key.")
                    
        except FileNotFoundError:
            raise KeyError("The location of the key does not exist.")
        
        print("The directory that was introduced is named:\n{}\n".format(directory))

        possible_dirs = os.listdir(path = directory)

        if [x[::-1][:4][::-1] == ".txt" for x in possible_dirs].count(False) >= 1:
            while True:
                try:
                    a = [x[::-1][:4][::-1] == ".txt" for x in possible_dirs].index(False)
                    del possible_dirs[a]
                except ValueError:
                    break

        for i in range(len(possible_dirs)):
            self.replace(data_to_search = data_to_search,replace_word = replace_word, dir_location = possible_dirs[i], times = times, mute = True)

        print("The files that will be inspected are in this list:\n{}\n".format(possible_dirs))

        return 0

    def delete(self, dir_location,*, key_location: str, magic_word: str):
        '''
        Removes a file from dir_location.
        This is very dangerous, as it can
        destroy your data forever.
        You need to use magic_word
        to confirm you are able to do this.
        '''
        
        magic_word = str(magic_word)
        try:
            with open(key_location,"r") as f:
                magic_word_0 = f.readlines()[0]
                if magic_word != magic_word_0:
                    raise KeyError("Not valid key.")
        except FileNotFoundError:
            raise KeyError("The location of the key does not exist.")
        
        try:
            os.remove(dir_location)
        except OSError:
            print("File {} is innacessible or does not exist.".format(dir_location))
            return 1

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
    '''
    It explains the syntax of the program
    and gives tips to the user about
    the program.
    '''
    try:
        with open("help.txt","r") as f:
            a = f.readlines()
            for i in range(len(a)):
                print(a[i])
    except FileNotFoundError:
        raise ModuleNotFoundError("The situation is helpless, there is no help.txt to read.")

    return 0

print("\nYou can always check the syntax with help_main(), see you later user!\n\n")
