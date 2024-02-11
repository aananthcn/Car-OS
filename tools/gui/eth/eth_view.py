#
# Created on Fri Dec 09 2022 5:40:07 AM
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

import gui.eth.eth_maincfg as eth_cfg
import ajson.eth.ajson_eth as ajson_eth
import gui.eth.eth_code_gen as eth_cgen


TabList = []
EthConfigViewActive = False
EthView = []  # the view Object that contains the configs


class EthTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = eth_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def eth_config_close_event(gui, view):
    global EthConfigViewActive

    EthConfigViewActive = False
    view.destroy()



def eth_save_callback(gui, eth_configs):
    global EthView

    EthView.clear()
    for eth_cfg in eth_configs:
        EthView.append(eth_cfg.get())
    gui.save()
    
    eth_cgen.generate_code(gui, eth_configs)


    
def show_eth_tabs(gui):
    global EthConfigViewActive, TabList, EthView
    
    if EthConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 60 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Ethernet Driver (MAC) Configuration Tool")
    EthConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: eth_config_close_event(gui, view))

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # read Eth content from ARXML file
    EthView = ajson_eth.read_eth_configs()
    # eth_configs = arxml_eth_r.parse_arxml(gui.arxml_file)
    
    # create the main Ethernet GUI object
    ethcfg_view = EthTab(view, width, height)
    ethcfg_view.tab = eth_cfg.EthernetConfigMainView(gui, EthView, ethcfg_view.save_cb)
    ethcfg_view.name = "EthernetConfigs"
    TabList.append(ethcfg_view)

    # Draw all tabs
    ethcfg_view.tab.draw(ethcfg_view)
    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def eth_block_click_handler(gui):
    show_eth_tabs(gui)