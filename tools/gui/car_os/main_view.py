#
# Created on Fri Aug 19 2022 12:39:35 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os
import sys
import json


# Let us use the System Generator functions to parse OIL and Generate code
if os.path.exists(os.getcwd()+"/car-os"):
    sys.path.insert(0, os.getcwd()+"/car-os/tools/os_builder")
    sys.path.insert(0, os.getcwd()+"/car-os/tools/arxml")
else:
    sys.path.insert(0, os.getcwd()+"/tools/os_builder")
    sys.path.insert(0, os.getcwd()+"/tools/arxml")

import os_builder.scripts.System_Generator as sg
import os_builder.scripts.oil as oil
import arxml.core.main_os as arxml


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import gui.os.os_view as os_view
import gui.car_os.uc_view as uc_view
import gui.car_os.asr_view as a_view

import arxml.core.lib as lib


# Temporary work-around -- for non OS modules, the code is generated from Mcu Code Generator
import gui.car_os.main_cgen as main_cgen
import gui.app.app_gen as app_gen


###############################################################################
#   CLASSES
#
class MainView:
    tk_root = None
    tk_menu = None
    xsize = None
    ysize = None
    child_window = None
    
    def __init__(self):
        self.tk_root = tk.Tk()
        self.tk_root.bind("<Configure>", lambda event : self.window_resize(event))


    def destroy_childwindow(self):
        # incase there any TopLevel() windows floating, delete them
        if self.child_window:
            # for widget in self.child_window.winfo_children():
	        #     widget.destroy()
            self.child_window.destroy()

        # delete all widgets, except menus, that are drawn directly onto the tk_root
        for widget in self.tk_root.winfo_children():
            if widget != self.tk_menu:
                widget.destroy()


    def window_resize(self, event):
        global Gui
        if event.widget == self.tk_root:
            if (self.xsize != event.width) or (self.ysize != event.height):
                print(f"MainView size: {event.width}x{event.height}")
                self.xsize = event.width
                self.ysize = event.height
                if Gui.config_loaded:
                    a_view.show_autosar_modules_view(Gui)




# UI Stuffs - FreeAUTOSAR Configurator Tool
class Car_OS_Builder:
    # Target System Attributes
    uc_info = uc_view.Uc_Info()
    
    # General Attributes
    arxml_file = None
    zephyr_path = None
    config_loaded = False
    
    # Graphical Attributes
    title = "Car-OS Builder"
    main_view = None        # the GUI root frame
    micro_block = None      # the Microcontroller block widget
    recentfiles = None
    asr_blocks = {}

    # Methods
    def __init__(self):
        global Gui
        Gui = self
        self.main_view = MainView()
        self.main_view.tk_root.title(self.title + " [uninitialized]")
        recentfiles = get_project_info_recentf()
        add_menus(self.main_view.tk_root, recentfiles)
        if os.name == 'nt':
            self.main_view.tk_root.state("zoomed")
        else:
            self.main_view.tk_root.wm_state("normal")


    def init_view_setup(self, fpath, ftype):
        if ftype == None or fpath == None:
            return
        elif ftype == "oil":
            open_oil_file(fpath)
        elif ftype == "arxml":
            open_arxml_file(fpath)
        else:
            print("Unsupported filetype argument provided!")


    def show_os_config(self):
        os_view.show_os_config(self)


    def show_uc_view(self):
        uc_view.show_microcontroller_block(self)


    def set_arxml_filepath(self, filepath):
        self.arxml_file = filepath
        lib.setget_ecuc_arpkg_name(filepath)
    



###############################################################################
# Globals
###############################################################################
# GUI stuffs
FileMenu = None

# I/O stuffs
OIL_FileName = None
ProjectInfoFile = os.getcwd()+"/car-os/car-os_info.json"
if os.path.exists(os.getcwd()+"/car-os"):
    ToolsPath = os.getcwd()+"/car-os/tools"
else:
    ToolsPath = os.getcwd()+"/tools"


# UI Stuffs - View
Gui = None



###############################################################################
# Functions
###############################################################################
def about():
    messagebox.showinfo(Gui.title, "This tool is developed to replace the OSEK-Builder.xlsx and to set path for AUTOSAR development")



def new_file():
    global Gui

    sg.sg_reset()
    a_view.show_autosar_modules_view(Gui)
    FileMenu.entryconfig("Save", state="normal")



def open_oil_file(fpath):
    global Gui, OIL_FileName

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/cfg/oil-files"):
        init_dir = os.getcwd()+"/cfg/oil-files"
    elif os.path.exists(os.getcwd()+"/car-os/cfg/oil-files"):
        init_dir = os.getcwd()+"/car-os/cfg/oil-files"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            OIL_FileName = filename
        else:
            print("Info: no or many OIL file is chosen, hence open_oil_file() returning without processing!")
            return
    else:
        OIL_FileName = fpath

    if Gui.main_view.tk_root != None:
        Gui.main_view.tk_root.title(Gui.title + " [" + str(OIL_FileName).split("/")[-1] +"]")

    # Make System Generator to parse, so that we can use the content in GUI.
    sg.sg_reset()
    sg.parse(OIL_FileName)
    Gui.config_loaded = True
    a_view.show_autosar_modules_view(Gui)
    FileMenu.entryconfig("Save", state="normal")



def save_project():
    global OIL_FileName, Gui

    os_view.backup_os_gui_before_save()

    if os.path.exists(os.getcwd()+"/car-os"):
        init_dir = os.getcwd()+"/car-os/output/arxml"
    else:
        init_dir = os.getcwd()+"/output/arxml"

    # Export if the input file OIL file.
    if OIL_FileName != None:
        file_exts = [('ARXML Files', '*.arxml')]
        saved_filename = filedialog.asksaveasfile(initialdir=init_dir, filetypes = file_exts, defaultextension = file_exts)
        if saved_filename == None:
            messagebox.showinfo(Gui.title, "File to save is not done correctly, saving aborted!")
            return
        Gui.set_arxml_filepath(saved_filename.name)
        print("Info: Exporting "+OIL_FileName+" to "+Gui.arxml_file+" ...")
        OIL_FileName = None

    # Save if the input file is ARXML
    elif Gui.arxml_file != None:
        print("Info: Saving configs to "+Gui.arxml_file+" ...")
    
    # Warn if both file variables are not set
    else:
        messagebox.showinfo(Gui.title, "Invalid input (project) file. Can't save project!")
        return


    # Export and File name clean up
    arxml.export_os_cfgs_2_arxml(Gui.arxml_file, Gui)
    Gui.main_view.tk_root.title(Gui.title + " [" + Gui.arxml_file.split("/")[-1] +"]")



def generate_code():
    global Gui

    # root window
    root = tk.Toplevel()
    root.geometry('400x120')
    root.title('Code Generation Progress')
    root.grid()
    # progressbar
    pb = ttk.Progressbar(root, orient='horizontal', length=380)
    # place the progressbar
    pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
    pb.update()

    # Generate code for OS Module
    srcpath = ToolsPath+"\os_builder\src"
    os_rc = sg.generate_code_for_os(srcpath)
    pb["value"] = 33
    root.update_idletasks()
    
    # Generate code for other BSW Modules
    bsw_rc = main_cgen.create_source(Gui)
    pb["value"] = 66
    root.update_idletasks()

    # Generate code for Application
    app_rc = app_gen.sync_n_create_source(Gui)
    pb["value"] = 100
    root.update_idletasks()

    pb.stop()
    root.destroy()
    if os_rc == 0 and bsw_rc == 0 and app_rc == 0:
        messagebox.showinfo(Gui.title, "Code Generated Successfully!")
    else:
        messagebox.showinfo(Gui.title, "Code Generation Failed!")



def save_as_arxml():
    global Gui

    if os.path.exists(os.getcwd()+"/car-os"):
        init_dir = os.getcwd()+"/car-os/output/arxml"
    else:
        init_dir = os.getcwd()+"/output/arxml"
    
    file_exts = [('ARXML Files', '*.arxml')]
    saved_filename = filedialog.asksaveasfile(initialdir=init_dir, filetypes = file_exts, defaultextension = file_exts)
    if saved_filename == None:
        messagebox.showinfo(Gui.title, "File to save is not done correctly, saving aborted!")
        return

    Gui.set_arxml_filepath(saved_filename.name)
    Gui.main_view.tk_root.title(Gui.title + " [" + str(saved_filename.name).split("/")[-1] +"]")
    os_view.backup_os_gui_before_save()
    arxml.export_os_cfgs_2_arxml(saved_filename.name, Gui)



def open_arxml_file(fpath):
    global Gui

    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/cfg/arxml"):
        init_dir = os.getcwd()+"/cfg/arxml"
    elif os.path.exists(os.getcwd()+"/car-os/cfg/arxml"):
        init_dir = os.getcwd()+"/car-os/cfg/arxml"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            Gui.set_arxml_filepath(filename)
        else:
            print("Info: no or many ARXML file is chosen, hence open_arxml_file() returning without processing!")
            return
    else:
        Gui.set_arxml_filepath(fpath.strip())

    if Gui.main_view.tk_root != None:
        Gui.main_view.tk_root.title(Gui.title + " [" + str(Gui.arxml_file).split("/")[-1] +"]")

    # Import/Parse ARXML file, so that we can use the content in GUI.
    sg.sg_reset()
    imp_status = arxml.import_arxml(Gui.arxml_file)
    if imp_status != 0:
        messagebox.showinfo(Gui.title, "Input file contains errors, hence opening as new file!")
        new_file()
    else:
        update_project_info_recentf(Gui.arxml_file)
        FileMenu.entryconfig("Save", state="normal")
    Gui.config_loaded = True
    a_view.show_autosar_modules_view(Gui)



###############################################################################
# Fuction: add_menus
# args: rv - root view
#    
def add_menus(rv, flst):
    global FileMenu
    Gui.main_view.tk_menu = tk.Menu(rv, background='#ff8000', foreground='black', activebackground='white', activeforeground='black')
    FileMenu = tk.Menu(Gui.main_view.tk_menu, tearoff=0)
    FileMenu.add_command(label="New", command=new_file)
    FileMenu.add_command(label="Import OIL File", command=lambda: open_oil_file(None))
    FileMenu.add_command(label="Import ARXML File", command=lambda: open_arxml_file(None))
    FileMenu.add_separator()
    FileMenu.add_command(label="Save", command=save_project, state="disabled")
    FileMenu.add_command(label="Save As", command=save_as_arxml)
    FileMenu.add_separator()
    if len(flst) > 0:
        for file_path in flst:
            FileMenu.add_command(label=file_path, command=lambda fp = file_path: open_arxml_file(fp))
        FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=rv.quit)
    Gui.main_view.tk_menu.add_cascade(label="File", menu=FileMenu)

    view = tk.Menu(Gui.main_view.tk_menu, tearoff=0)
    view.add_command(label="OS Config", command=lambda: os_view.show_os_config(Gui))
    view.add_command(label="AUTOSAR Module View", command=lambda: a_view.show_autosar_modules_view(Gui))
    Gui.main_view.tk_menu.add_cascade(label="View", menu=view)

    gen = tk.Menu(Gui.main_view.tk_menu, tearoff=0)
    gen.add_command(label="Generate Source", command=generate_code)
    Gui.main_view.tk_menu.add_cascade(label="Generate", menu=gen)

    help = tk.Menu(Gui.main_view.tk_menu, tearoff=0)
    help.add_command(label="About", command=about)
    Gui.main_view.tk_menu.add_cascade(label="Help", menu=help)
    
    rv.config(menu=Gui.main_view.tk_menu)



def textBox():
    print(textb.get())



def update_project_info_zephyrd(filepath):
    global ProjectInfoFile

    proj_data = None
    if ProjectInfoFile == None:
        print("Error: ProjectInfoFile is not initialized")
        return

    if os.path.exists(ProjectInfoFile):
        with open(ProjectInfoFile, "r") as jfile:
            try:
                proj_data = json.load(jfile)
            except ValueError:
                print("Decoding json ("+ProjectInfoFile+") failed in update_project_info_recentf()!")
                proj_data = {}
            jfile.close()

    if os.path.exists(filepath):
        proj_data["zephyr_path"] = filepath
        with open(ProjectInfoFile, "w") as jfile:
            json.dump(proj_data, jfile)



def get_project_info_zephyrd():
    zephyrd = None
    if os.path.exists(ProjectInfoFile):
        with open(ProjectInfoFile, "r") as jfile:
            try:
                proj_data = json.load(jfile)
                zephyrd = proj_data["zephyr_path"]
            except ValueError:
                print("Decoding json ("+ProjectInfoFile+") failed in get_project_info_recentf()!")
                zephyrd = None
            jfile.close()

    return zephyrd



def update_project_info_recentf(filepath):
    global ProjectInfoFile

    proj_data = None
    if ProjectInfoFile == None:
        print("Error: ProjectInfoFile is not initialized")
        return

    if os.path.exists(ProjectInfoFile):
        with open(ProjectInfoFile, "r") as jfile:
            try:
                proj_data = json.load(jfile)
            except ValueError:
                print("Decoding json ("+ProjectInfoFile+") failed in update_project_info_recentf()!")
                proj_data = None
            jfile.close()

    if proj_data:
        rflist = proj_data["recent_files"]
    else:
        rflist = []
        proj_data = {}


    if filepath not in rflist:
        rflist.append(filepath)
    proj_data["recent_files"] = rflist

    with open(ProjectInfoFile, "w") as jfile:
        json.dump(proj_data, jfile)



def get_project_info_recentf():
    file_list = None
    if os.path.exists(ProjectInfoFile):
        with open(ProjectInfoFile, "r") as jfile:
            try:
                proj_data = json.load(jfile)
                file_list = proj_data["recent_files"]
            except ValueError:
                print("Decoding json ("+ProjectInfoFile+") failed in get_project_info_recentf()!")
                file_list = None
            jfile.close()

    return file_list
