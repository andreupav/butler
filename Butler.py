import os, platform
from tkinter import *
from tkinter import filedialog, messagebox
from os import walk
from tkinter import ttk

global pathconfig
pathconfig = "config.txt"

def get_format(patharxiu):
    #Returns the format of a file, given its path
    #get_format("H:/Libraries/Music/Duele.mp3") returns ".mp3"
    return os.path.splitext(patharxiu)[1]

def get_name(patharxiu):
    #Returns the name of a file, given its path
    #get_name("H:/Libraries/Music/Duele.mp3") returns "Duele"
    s = os.path.splitext(patharxiu)[0]
    return s[s.rfind("/")+1:]

def move_file(patharxiu, pathdesti):
    #Moves a file from originpath/../file.format to destinationpath/../file.format
    os.rename(patharxiu, pathdesti)
    
def process_file(patharxiu):
    #Given a file path, puts it where the config.txt wants it to go
    config = open(pathconfig,'r')
    formato = get_format(patharxiu)
    for e in config:
        linia = e.strip()
        if linia[0:linia.find("#")] == formato:
            move_file(patharxiu, linia[linia.find("#")+1:] + "/" + get_name(patharxiu) + formato)
    config.close()

def get_files_from_folder(path):
    #Given a folder path, returns a list of all file paths within said folder
    files1 = []
    for (dirpath, dirnames, filenames) in walk(path):
        files1.extend(filenames)
        break
    files2 = []
    for e in files1:
        files2.append(path + "/" + e)
    return files2

def choose_files():
    #Returns a list of file paths (from user)
    return list(filedialog.askopenfilenames(title = "Choose files"))

def choose_folder():
    #Returns a folder path (from user)
    return filedialog.askdirectory(title = "Choose folders")

def button_addfiles():
    files2manage = choose_files()
    for file in files2manage:
        process_file(file)

def button_addfolder():
    folder = choose_folder()
    files2manage = get_files_from_folder(folder)
    for file in files2manage:
        process_file(file)

def formatstofolder(folderpath):
    #Given a destination folder path, returns all format types that are meant to be ordered into that folder
    formats = []
    config = open(pathconfig,'r')
    for e in config:
        linia = e.strip()
        if folderpath in linia:
            formats.append(linia[0:linia.find("#")])
    config.close()
    return formats

def folder_nice_name(folderpath):
    #Given a folder path, returns the last folder in the path in plaintext
    return folderpath[folderpath.rfind("/")+1:]

def target_folders_list():
    #Returns a list of all the destination folders in config.txt
    tfl = []
    config = open(pathconfig,'r')
    for e in config:
        linia = e.strip()
        target_path = linia[linia.find("#")+1:]
        if target_path not in tfl:
            tfl.append(target_path)
    config.close()
    return tfl    
       
def folder_list():
    #Makes a Radiobutton for every destination folder in config.txt
    folders = []
    tfl = target_folders_list()
    for i, folder in enumerate(tfl):
        x = Radiobutton(Folders_bis, text = folder_nice_name(folder), value = i, indicatoron = False, padx = w//4.5, command = lambda folder=folder: destination_folder_selected(folder))
        folders.append(x)
        x.grid(row = i, sticky = W+E+N+S)
    return folders

def add_format_destination(event):
    #Asks the user for a destination path. If no format is given, halts and asks for it
    #If the format is already in config.txt, offers the choice to keep the old one
    #or establish the new destination.
    dest_path = filedialog.askdirectory(title = "Choose destination path")
    config_a = open(pathconfig, 'a')
    newformat = new_format_type.get()
    creada = False
    if len(newformat) != 0:
        config_r = open(pathconfig,'r')
        res = False
        for e in config_r:
            linia = e.strip()
            if (linia[0:linia.find("#")] == newformat):
                res = messagebox.askyesno("Overwrite?", "Do you want overwrite your existing path (" + linia[linia.find("#")+1:] + ") for the format: " + linia[0:linia.find("#")], default="no")
                if (res):
                    creada=True
                    config_a.close()
                    f = open(pathconfig, 'r')
                    lines = f.readlines()
                    f.close()
                    f = open(pathconfig, 'w')
                    for line in lines:
                        if line != linia + "\n":
                            f.write(line)
                            f.write(newformat + "#" + dest_path + "\n")
                            f.close()
        config_r.close()
        if(not creada):
            config_a.write(newformat + "#" + dest_path + "\n")
        else:
            messagebox.showinfo(title = "Choose a file format for this folder", message = "Choose a file format for this folder")
    config_a.close()
    folder_list()
    new_format_type.set("")
    Formats.update_idletasks()

def myfunction(event):
    #Does something
    canvas.configure(scrollregion=canvas.bbox("all"),width=w//2,height=3*h//4)

def destination_folder_selected(path):
    path_to_label(path)
    formats_scroll(formatstofolder(path))
    Formats.update_idletasks()

def path_to_label(pathh):
    dirpathvar.set(pathh)

def formats_scroll(lista):
    mylist.delete(0, END)
    for line in lista:
        mylist.insert(END,str(line))
    mylist.pack( side = RIGHT, fill = "both", expand=True)


#MAIN
root = Tk()
root.title("Butler")

#Root sizing
X = root.winfo_screenwidth()
Y = root.winfo_screenheight()
w = X//2
h = Y//2
root.geometry(str(w) + "x" + str(h) + '+' + str(X//2 - w//2) + '+' + str(Y//2 - h//2))
root.resizable(width=FALSE, height=FALSE)

#Dividing Root into fourths
Top = Frame(root)
Bottom = Frame(root)
Top.pack(side = TOP, fill = "both", expand = True)
Bottom.pack(side = BOTTOM, fill = "both", expand=True)

Folders = Frame(Top)
Formats = Frame(Top)
AddFolder = Frame(Bottom)
AddFiles = Frame(Bottom)

Folders.pack(side = LEFT, fill="both", expand=True)
Formats.pack(side = RIGHT, fill="both", expand=True)
AddFolder.pack(side = LEFT, fill="both", expand=True)
AddFiles.pack(side = RIGHT, fill="both", expand=True)

#Top Right
dirpathvar = StringVar()
dirpathvar.set("Directory....")
pathlabel = Label(Formats, textvariable=dirpathvar).pack(fill = "y")
scrollformats = Scrollbar(Formats)
scrollformats.pack(side = RIGHT, fill="both")
mylist = Listbox(Formats, yscrollcommand = scrollformats.set)
scrollformats.config(command = mylist.yview)

#Top Left
canvas = Canvas(Folders)
Folders_bis = Frame(canvas)
folderscrollbar = Scrollbar(Folders, orient = "vertical",command=canvas.yview)
canvas.configure(yscrollcommand = folderscrollbar.set)
folderscrollbar.grid(row = 1, sticky = E+N+S)
canvas.grid(row = 1)

ask_for_new_format = Label(Folders, text = 'Insert format for new destination folder below:').grid(row = 2, column = 0, sticky = W+E+N+S)
new_format_type = StringVar()
new_format = ttk.Entry(Folders, width=7, textvariable=new_format_type)
new_format.grid(column = 0, row = 3, sticky = (W, E))
new_format.bind('<Return>', add_format_destination)

Button(Folders, text = 'Add new destination folder', command = add_format_destination).grid(row = 4, column = 0, sticky = W+E+N+S)

canvas.create_window((0,0),window=Folders_bis,anchor='nw')
Folders_bis.bind("<Configure>",myfunction)
list_of_folders = folder_list()


#Bottom Right
Add_Folder = Button(AddFolder, text="Add Folder", command=button_addfolder)
Add_Folder.pack(fill="both", expand=True)

#Bottom Left
Add_Files = Button(AddFiles, text="Add Files", command=button_addfiles)
Add_Files.pack(fill="both", expand=True)

root.mainloop()