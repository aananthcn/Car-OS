#
# Created on Wed Feb 22 2023 8:26:46 AM
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
import tkinter as tk
from tkinter import ttk

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box


# SoAdConfig container structure
# 
# SoAd
#     + SoAdConfig
#         + SoAdSocketConnectionGroup (1..*)
#             + SoAdSocketConnection
#                 + SoAdSocketId
#                 + SoAdSocketRemoteAddress
#                     + SoAdSocketRemoteIpAddress
#                     + SoAdSocketRemotePort


class SoAdChildView:
    view = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h, cb):
        self.save_cb = cb
        self.frame = f
        self.xsize = w
        self.ysize = h



class SoAdSocketConnView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["SoAdSocketId", "SoAdSocketRemoteIpAddress",
               "SoAdSocketRemotePort"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None

    max_sockets = 65536
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None

    skt_grp_class = None


    def __init__(self, gui, index, sktc_cfgs, skt_grp):
        self.gui = gui
        self.configs = []
        self.n_skt = 0
        self.n_skt_str = tk.StringVar()
        self.skt_grp_class = skt_grp

        # Create config string for AUTOSAR configs on this tab
        if sktc_cfgs:
            for cfg in sktc_cfgs:
                self.configs.append(dappa.AsrCfgStr(self.cfgkeys, cfg))
                self.n_skt += 1

    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self, index):
        gen_dict = {}
        
        gen_dict["SoAdSocketId"]              = str(index)
        gen_dict["SoAdSocketRemoteIpAddress"] = ""
        gen_dict["SoAdSocketRemotePort"]      = "0"
        
        return gen_dict



    def draw_dappa_row(self, i):
        dappa.label(self, "Sock #", self.header_row+i, 0, "e")
        dappa.entry(self, "SoAdSocketId", i, self.header_row+i, 1, 15, "normal")
        dappa.entry(self, "SoAdSocketRemoteIpAddress", i, self.header_row+i, 2, 32, "normal")
        dappa.spinb(self, "SoAdSocketRemotePort", i, self.header_row+i, 3, 20, tuple(range(0,65536)))



    def update(self):
        # get dappas to be added or removed
        self.n_skt = int(self.n_skt_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_skt > n_dappa_rows:
            for i in range(self.n_skt - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys,
                    self.create_empty_configs(self.skt_grp_class.n_sock_conns)))
                self.skt_grp_class.n_sock_conns += 1
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_skt:
            for i in range(n_dappa_rows - self.n_skt):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                self.skt_grp_class.n_sock_conns -= 1
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="No. Sockets:")
        label.grid(row=0, column=0, sticky="w")
        spinb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_skt_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_sockets+1)))
        self.n_skt_str.set(self.n_skt)
        spinb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()
