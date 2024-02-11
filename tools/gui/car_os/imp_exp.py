#
# Created on Sun Feb 11 2024 7:51:25 PM
#
# The MIT License (MIT)
# Copyright (c) 2024 Aananth C N
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


import os_builder.scripts.System_Generator as sg
import os_builder.scripts.oil as oil
import arxml.core.main_os as arxml

import tkinter as tk
from tkinter import filedialog

import gui.os.os_view as os_view
import gui.car_os.uc_view as uc_view
import gui.car_os.asr_view as a_view


###############################################################################
# Globals



###############################################################################
# Oil file support is kept for legacy (OSEK) reasons. These days this function
# is not tested, so, plan to remove this. 
def open_oil_file(fpath, gui):
    OIL_FileName = None

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

    if gui.main_view.tk_root != None:
        gui.main_view.tk_root.title(gui.title + " [" + str(OIL_FileName).split("/")[-1] +"]")

    # Reset OS view to flush the contents from previous view
    os_view.os_reset()

    # Make System Generator to parse, so that we can use the content in GUI.
    sg.parse(OIL_FileName)
    gui.config_loaded = True
    a_view.show_autosar_modules_view(gui)
    # FileMenu.entryconfig("Save", state="normal")



###############################################################################
# ARXML open and save functions. Note ARXML is no longer (Feb 2024) the default
# format of storage. It is decided to go with A-JSON format.
def save_as_arxml(gui):
    if os.path.exists(os.getcwd()+"/car-os"):
        init_dir = os.getcwd()+"/car-os/output/arxml"
    else:
        init_dir = os.getcwd()+"/output/arxml"

    file_exts = [('ARXML Files', '*.arxml')]
    saved_filename = filedialog.asksaveasfile(initialdir=init_dir, filetypes = file_exts, defaultextension = file_exts)
    if saved_filename == None:
        messagebox.showinfo(gui.title, "File to save is not done correctly, saving aborted!")
        return

    gui.set_caros_cfg_filepath(saved_filename.name)
    gui.main_view.tk_root.title(gui.title + " [" + str(saved_filename.name).split("/")[-1] +"]")
    os_view.backup_os_gui_before_save()
    arxml.export_os_cfgs_2_arxml(saved_filename.name, gui)



def open_arxml_file(fpath, gui):
    init_dir = os.getcwd()
    if os.path.exists(os.getcwd()+"/cfg/arxml"):
        init_dir = os.getcwd()+"/cfg/arxml"
    elif os.path.exists(os.getcwd()+"/car-os/cfg/arxml"):
        init_dir = os.getcwd()+"/car-os/cfg/arxml"

    if fpath == None:
        filename = filedialog.askopenfilename(initialdir=init_dir)
        if type(filename) is not tuple and len(filename) > 5:
            gui.set_caros_cfg_filepath(filename)
        else:
            print("Info: no or many ARXML file is chosen, hence open_arxml_file() returning without processing!")
            return
    else:
        gui.set_caros_cfg_filepath(fpath.strip())

    if gui.main_view.tk_root != None:
        gui.main_view.tk_root.title(gui.title + " [" + str(gui.arxml_file).split("/")[-1] +"]")

    # Reset OS view to flush the contents from previous view
    os_view.os_reset()

    # Import/Parse ARXML file, so that we can use the content in GUI.
    imp_status = arxml.import_arxml(gui.arxml_file)
    if imp_status != 0:
        # TODO: Add code to handle FILE NOT FOUND ERRORs
        # TODO: If FILE NOT FOUND, then delete the file information in .project-cfg.json file
        messagebox.showinfo(gui.title, "Input file contains errors, hence opening as new file!")
        new_file()
    else:
        gui.arxml_file = filename
        # FileMenu.entryconfig("Save", state="normal")
    gui.config_loaded = True
    a_view.show_autosar_modules_view(gui)


