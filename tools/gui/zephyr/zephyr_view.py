#
# Created on Wed Dec 20 2023 10:38:22 PM
#
# The MIT License (MIT)
# Copyright (c) 2023 Aananth C N
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

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


import gui.car_os.main_cgen as main_cgen
import gui.car_os.main_view as main_view
import arxml.mcu.arxml_mcu as arxml_mcu

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box




ZephyrViewWindow = None


###############################################################################
# Local Functions
# this function will be called when the ZephyrViewWindow Toplevel() object is closed.
def on_zephyr_view_close():
    global ZephyrViewWindow

    ZephyrViewWindow.destroy()
    ZephyrViewWindow = None



def zephyr_get_updated_label(gui, zephyrd):
    new_name = None
    cur_name = gui.asr_blocks["Zephyr"].label
    upd_name = cur_name.split("[")[0].strip() + " [" + zephyrd + "]"
    if cur_name != upd_name:
        new_name = upd_name
    return new_name



###############################################################################
# Main Entry Points
def zephyr_constructor(gui, z_blk):
    zephyrd = main_view.get_project_info_zephyrd()

    if zephyrd:
        gui.zephyr_path = zephyrd

        # Update the Microcontroller block in main Gui
        new_label = zephyr_get_updated_label(gui, zephyrd)
        if new_label != None:
            z_blk.label = new_label



def zephyr_click_handler(gui):
    global ZephyrViewWindow

    if ZephyrViewWindow != None:
        return

    # function to create dialog window
    ZephyrViewWindow = tk.Toplevel() # create an instance of toplevel
    ZephyrViewWindow.protocol("WM_DELETE_WINDOW", on_zephyr_view_close)
    ZephyrViewWindow.attributes('-topmost',True)

    # set the geometry
    x = ZephyrViewWindow.winfo_screenwidth()
    y = ZephyrViewWindow.winfo_screenheight()
    width = 700
    height = 95
    ZephyrViewWindow.geometry("%dx%d+%d+%d" % (width, height, 3*x/10, 4*y/10))
    ZephyrViewWindow.title("Zephyr RTOS Configs")

    # create views and draw
    z_view = ZephyrConfig_View(gui)
    z_view.draw(ZephyrViewWindow, width, height)



# Zephyr RTOS
class ZephyrConfig_View:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["ZephyrInstallationPath"]
    zpath = None

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui):
        self.gui = gui
        self.configs = []
        self.zpath = main_view.get_project_info_zephyrd()
        if self.zpath == None:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            z_view = {}
            z_view["ZephyrInstallationPath"] = self.zpath
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, z_view))


    def __del__(self):
        del self.configs[:]


    def create_empty_configs(self):
        z_view = {}
        z_view["ZephyrInstallationPath"] = ""
        return z_view


    def draw_dappas(self):
        # Zephyr path label
        label = tk.Label(self.scrollw.mnf, text="Zephyr Installation Path: ")
        label.grid(row=0, column=0, sticky="e")

        # ZephyrInstallationPath
        dappa.entry(self, "ZephyrInstallationPath", 0, 0, 1, 50, "normal")

        # Zephyr path selection button
        selb = tk.Button(self.scrollw.mnf, width=10, text="Modify", command=self.zephyr_path_select)
        selb.grid(row=0, column=3)

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=2, column=0, sticky="e")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_configs,
                    bg="#206020", fg='white')
        saveb.grid(row=3, column=3)


    def draw(self, view, xsize, ysize):
        self.tab_struct = None
        self.scrollw = window.ScrollableWindow(view, xsize, ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def save_configs(self):
        global ZephyrViewWindow

        # Update installation path from view
        zephyr_insall_path = self.configs[0].dispvar["ZephyrInstallationPath"].get()

        # write to the project info json file
        main_view.update_project_info_zephyrd(zephyr_insall_path)
        ZephyrViewWindow.destroy()
        ZephyrViewWindow = None
    
        # if new zephyrproject path is selected, then display it in autosar view
        new_label = zephyr_get_updated_label(self.gui, zephyr_insall_path)
        if new_label != None:
            self.gui.asr_blocks["Zephyr"].update_label(self.gui, new_label)

        # generate code (mainly to update path_defs.mk)
        self.gui.zephyr_path = zephyr_insall_path
        main_cgen.create_source(self.gui)


    def zephyr_path_select(self):
        global ZephyrViewWindow

        if os.name == 'nt':
            start_dir = "e:"
        else:
            start_dir = "~"
        dpath = filedialog.askdirectory(initialdir=start_dir, parent=ZephyrViewWindow)
        if type(dpath) is not tuple and len(dpath) > 5:
            self.configs[0].dispvar["ZephyrInstallationPath"].set(dpath)

