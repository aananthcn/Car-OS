#
# Created on Tue Aug 30 2022 10:19:34 PM
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
import tkinter as tk
from tkinter import ttk

import gui.port.port_cfg as port_cfg
import gui.port.port_gen as port_gen
import gui.port.port_cgen as port_cgen
import arxml.port.arxml_port as arxml_port


TabList = []
PortConfigViewActive = False
PortView = {}


class PortTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = port_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def port_save_callback(gui):
    global PortView

    port_cfg = None
    port_gen = None
    for tab in TabList:
        if tab.name == "PortConfigSet":
            port_cfg = []
            for cfg in tab.tab.configs:
                port_cfg.append(cfg.get())
            continue
        if tab.name == "PortGeneral":
            port_gen = tab.tab.configs[0].get()
            continue

    # save the GUI contents to View
    PortView["PortGeneral"] = port_gen
    PortView["PortConfigSet"] = port_cfg
    gui.save()

    # save the GUI contents to ARXML
    arxml_port.update_arxml(gui.arxml_file, port_cfg, port_gen)
    port_cgen.generate_code(gui)



def port_config_close_event(gui, view):
    global PortConfigViewActive

    PortConfigViewActive = False
    view.destroy()


    
def show_port_config(gui):
    global PortConfigViewActive, TabList
    
    if PortConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    view.geometry("%dx%d+%d+%d" % (width, height, width/5, 15))
    view.title("AUTOSAR Port Configuration Tool")
    PortConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: port_config_close_event(gui, view))
    gui.main_view.child_window = ttk.Notebook(view)
    
    # Create tabs to configure OS
    pcs_frame = ttk.Frame(gui.main_view.child_window)
    pgn_frame = ttk.Frame(gui.main_view.child_window)
    
    # Add tabs to configure OS
    gui.main_view.child_window.add(pcs_frame, text ='PortConfigSet')
    gui.main_view.child_window.add(pgn_frame, text ='PortGeneral')
    gui.main_view.child_window.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # read View data from cfg (ARXML/A-JSON) file
    n_pins, port_cfg_f, port_gen_f = arxml_port.parse_arxml(gui.arxml_file)
    PortView["PortGeneral"] = port_gen_f
    PortView["PortConfigSet"] = port_cfg_f

    # create new GUI objects
    ptab = PortTab(pcs_frame, width, height)
    ptab.tab = port_cfg.PortConfigSetTab(gui)
    ptab.name = "PortConfigSet"
    TabList.append(ptab)
    ptab.tab.draw(ptab)

    # create new GUI objects
    ptab = PortTab(pgn_frame, width, height)
    ptab.tab = port_gen.PortGeneralTab(gui)
    ptab.name = "PortGeneral"
    TabList.append(ptab)
    ptab.tab.draw(ptab)
    

# Main Entry Point
def port_block_click_handler(gui):
    show_port_config(gui)