# -*- coding: utf-8 -*-

import os, platform
from tkinter import *
from tkinter import filedialog, messagebox
from os import walk
from tkinter import ttk

global pathconfig

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
        if folderpath == linia[linia.find("#")+1:]:
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
        x.select()
        folders.append(x)
        x.grid(row = i, sticky = W+E+N+S)
    x.deselect()
    return folders

def add_format_destination(*event):
    #Asks the user for a destination path. If no format is given, halts and asks for it
    #If the format is already in config.txt, offers the choice to keep the old one
    #or establish the new destination.
    newformat = new_format_type.get()
    if len(newformat) == 0:
        return 0
    if newformat[0] != ".":
        newformat = "." + newformat
    dest_path = filedialog.askdirectory(title = "Choose destination path")
    config_a = open(pathconfig, 'a')
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

def myfunction(event):
    #Does something
    canvas.configure(scrollregion=canvas.bbox("all"),width=w//2,height=3*h//4)

def destination_folder_selected(path):
    #Once a folder from the folders list has been selected, calls these three functions
    global displayed_formats
    displayed_formats = formatstofolder(path)
    path_to_label(path)
    formats_scroll(displayed_formats)

def path_to_label(pathh):
    #Creates the appropiate text for the label on top of the filetypes
    dirpathvar.set(pathh)

def formats_scroll(lista):
    #Takes a Listbox and inserts an element for each of a given list of filetypes
    formats_list.delete(0, END)
    for line in lista:
        formats_list.insert(END,str(line))
    formats_list.pack( side = RIGHT, fill = "both", expand=True)

def erase_format(format_to_erase):
    #Given a format type, erases said type and its destination folder from config.txt
    f = open(pathconfig, 'r')
    lines = f.readlines()
    f.close()
    f = open(pathconfig, 'w')
    for line in lines:
        if line[0:line.find("#")] != format_to_erase:
            f.write(line)
    f.close()

def scrollbar_select(event):
    #Sets a global variable with the index of the current selected element of the filetypes
    #scrolling bar
    i = event.widget
    global selected_format_index
    selected_format_index = int(i.curselection()[0])
    
def eraseing(format_to_erase):
    #Makes sure the user wants to delete a format and its destination folder
    f = open(pathconfig, 'r')
    for e in f:
        line = e.strip()
        if line[0:line.find("#")] == format_to_erase:
            path = line[line.find("#") + 1:]
    yn = messagebox.askyesno("Delete?", "Are you sure you want stop ordering " + format_to_erase + " files to" +  path + " ?")
    if yn:
        erase_format(format_to_erase)
        
def create_config_file(pathconfig, urlMusic, urlVideos, urlImages, UrlDocs):
    #Given the location of config.txt and the 4 main user libraries, creates the config.txt
    #file with some filetypes directed to the 4 main user libraries
    filee = open(pathconfig, 'a')
    filee.write(".mp3#" + urlMusic)
    filee.write(".flac#" + urlMusic)
    filee.write(".ogg#" + urlMusic)
    filee.write(".wav#" + urlMusic)
    filee.write(".aac#" + urlMusic)

    filee.write(".avi#" + urlVideos)
    filee.write(".mp4#" + urlVideos)
    filee.write(".wmv#" + urlVideos)
    filee.write(".mkv#" + urlVideos)

    filee.write(".jpg#" + urlImages)
    filee.write(".jpeg#" + urlImages)
    filee.write(".gif#" + urlImages)
    filee.write(".png#" + urlImages)
    filee.write(".bmp#" + urlImages)
    filee.write(".tiff#" + urlImages)

    filee.write(".docx#" + UrlDocs)
    filee.write(".odt#" + UrlDocs)
    filee.write(".pdf#" + UrlDocs)
    filee.write(".doc#" + UrlDocs)
    filee.write(".xls#" + UrlDocs)
    filee.write(".xlxs#" + UrlDocs)
    filee.write(".ppt#" + UrlDocs)
    filee.write(".pptx#" + UrlDocs)
    filee.write(".ods#" + UrlDocs)
    filee.write(".odp#" + UrlDocs)
    
    filee.close()

def file_exists(urll):
    return  os.path.isfile(urll)

#MAIN

if(platform.system() == "Darwin"):
    #MacOSX
    pathconfig = "/Library/Preferences/config.txt"
    tunombre = os.getlogin()
    if(not file_exists(pathconfig)):
        music = "/Users/" + tunombre +"/Music\n"
        movies = "/Users/" + tunombre +"/Movies\n"
        pics = "/Users/" + tunombre +"/Pictures\n"
        docs = "/Users/" + tunombre +"/Documents\n"
        create_config_file(pathconfig, music, movies,pics, docs)#path, music, videos, images , docs		
elif(platform.system() == "Linux"):
    #Linux
    tunombre = os.getlogin()
    pathconfig = "/etc/config.txt"#cambiar a path de config
    if(not file_exists(pathconfig)):
        if(os.path.isdir("/home/" + tunombre +"/Música")): #check if spanish
            tunombre = os.getlogin()
            music = "/home/" + tunombre +"/Música\n"
            movies = "/home/" + tunombre +"/Videos\n"
            pics = "/home/" + tunombre +"/Imagenes\n"
            docs = "/home/" + tunombre +"/Documents\n"
            create_config_file(pathconfig, music, movies,pics, docs)
        elif (os.path.isdir("/home/" + tunombre +"/music")): #check if english
            tunombre = os.getlogin()
            music = "/home/" + tunombre +"/Music\n"
            movies = "/home/" + tunombre +"/Videos\n"
            pics = "/home/" + tunombre +"/Images\n"
            docs = "/home/" + tunombre +"/Documents\n"
            create_config_file(pathconfig, music, movies,pics, docs)
else:
    #Windows
    username = os.getlogin()
    pathconfig = "C:/Users/" + username + "/Documents/config.txt"#cambiar a path de config
    if(not file_exists(pathconfig)):
        music = "C:/Users/" + username +"/Music\n"
        movies = "C:/Users/" + username +"/Videos\n"
        pics = "C:/Users/" + username +"/Pictures\n"
        docs = "C:/Users/" + username +"/Documents\n"
        create_config_file(pathconfig, music, movies, pics, docs)
		
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

formats_list = Listbox(Formats, yscrollcommand = scrollformats.set, exportselection = 0)
scrollformats.config(command = formats_list.yview)

espaiador_perque_quadri = Label(Formats, text="___________________________________________________").pack(fill = "y")
formats_list.bind('<<ListboxSelect>>', scrollbar_select)
erase_format_button = Button(Formats, text="Erase format", justify = "right", command = lambda: eraseing(displayed_formats[selected_format_index])).pack()

#Top Left
canvas = Canvas(Folders)
Folders_bis = Frame(canvas)
folderscrollbar = Scrollbar(Folders, orient = "vertical",command=canvas.yview)
canvas.configure(yscrollcommand = folderscrollbar.set)
folderscrollbar.grid(row = 1, sticky = E+N+S)
canvas.grid(row = 1)

ask_for_new_format = Label(Folders, text = 'Insert format for new destination folder below:').grid(row = 2, column = 0, sticky = W+E+N+S)
new_dest_folder = Button(Folders, text = 'Add new destination folder', command = add_format_destination).grid(row = 4, column = 0, sticky = W+E+N+S)

new_format_type = StringVar()
new_format = ttk.Entry(Folders, width=7, textvariable=new_format_type)
new_format.grid(column = 0, row = 3, sticky = (W, E))
new_format.bind('<Return>', add_format_destination)

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