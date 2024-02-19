#
# Created on Sat Feb 17 2024 8:19:20 PM
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

import tkinter as tk
from tkinter import ttk

import gui.tcpip.tcpip_gen as tcpip_gen
import gui.tcpip.tcpip_local_addr as local_addr

import ajson.tcpip.ajson_tcpip as ajson_tcpip
import gui.tcpip.tcpip_code_gen as tcpip_cgen


TabList = []
TcpIpConfigViewActive = False
TcpIpView = {}


class TcpIp_Tab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None

    def __init__(self, f, w, h):
        self.save_cb = tcpip_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h



def tcpip_backup_view():
    global TcpIpView

    # copy from Gui to TcpIp view
    for tab in TabList:
        tcpip_cfg = []
        for cfg in tab.tab.configs:
            tcpip_cfg.append(cfg.get())
        TcpIpView[tab.name] = tcpip_cfg



def tcpip_config_close_event(gui, view):
    global TcpIpConfigViewActive

    tcpip_backup_view()
    TcpIpConfigViewActive = False
    view.destroy()



def tcpip_save_callback(gui):
    # copy from Gui to TcpIp view
    tcpip_backup_view()

    # save TcpIpView into A-JSON file
    gui.save()

    tcpip_cgen.generate_code(gui, TcpIpView)



def set_view_geometry(gui, view, x_perc, y_perc):
    width = gui.main_view.xsize * x_perc / 100
    height = gui.main_view.ysize * y_perc / 100
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/2
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    return width, height



def show_tcpip_tabs(gui):
    global TcpIpConfigViewActive, TabList, TcpIpView

    if TcpIpConfigViewActive:
        return

    # Create a child window (tabbed view)
    view = tk.Toplevel()
    gui.main_view.child_window = view
    width, height = set_view_geometry(gui, view, 80, 80)
    view.title("AUTOSAR TcpIp Configuration Tool")
    TcpIpConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: tcpip_config_close_event(gui, view))
    notebook = ttk.Notebook(view)

    # Create tabs to configure TcpIp
    general_frame  = ttk.Frame(notebook)
    local_addr_frame  = ttk.Frame(notebook)

    # Add tabs to configure TcpIp
    notebook.add(general_frame, text ='TcpIpGeneral')
    notebook.add(local_addr_frame, text ='TcpIpLocalAddr')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    for obj in TabList:
        del obj

    # read TcpIp content from A-JSON file
    jview = ajson_tcpip.read_tcpip_configs()
    if jview:
        TcpIpView = jview

    # create new GUI objects
    tcpipgen_tab = TcpIp_Tab(general_frame, width, height)
    tcpipgen_tab.tab = tcpip_gen.TcpIpGeneralView(gui, TcpIpView)
    tcpipgen_tab.name = "TcpIpGeneral"
    TabList.append(tcpipgen_tab)

    local_addr_tab = TcpIp_Tab(local_addr_frame, width, height)
    local_addr_tab.tab = local_addr.TcpIpLocalAddrView(gui, TcpIpView)
    local_addr_tab.name = "TcpIpLocalAddr"
    TabList.append(local_addr_tab)


    # Draw all tabs
    tcpipgen_tab.tab.draw(tcpipgen_tab)
    local_addr_tab.tab.draw(local_addr_tab)



# Main Entry Point
def tcpip_block_click_handler(gui):
    show_tcpip_tabs(gui)