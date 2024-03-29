#
# Created on Sun Feb 18 2024 9:24:36 PM
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

import gui.lib.window as window
import gui.lib.asr_widget as dappa # dappa in Tamil means box



class TcpIpGeneralView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["TcpIpBufferMemory", "TcpIpMainFunctionPeriod"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)
    active_dialog = None
    active_view = None


    def __init__(self, gui, view):
        self.gui = gui
        self.configs = []
        
        if view:
            gen_cfg = view["TcpIpGeneral"][0]
        else:
            gen_cfg = None

        # Create config string for AUTOSAR configs on this tab
        if not gen_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, gen_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["TcpIpBufferMemory"]              = "1500" # Memory size in bytes reserved for TCP/IP buffers.
        gen_dict["TcpIpMainFunctionPeriod"]        = "0.1"  # Seconds (floating point) 
        
        return gen_dict



    def draw_dappas(self):
        # insert column separator at 0
        dappa.colsep(self, 0)

        # column = 2; label at 1
        dappa.entryg(self, "TcpIpBufferMemory",        0, 0, 1, 23, "normal")

        # insert column separator at 3
        dappa.colsep(self, 3)

        # column = 5; label at 4
        dappa.entryg(self, "TcpIpMainFunctionPeriod",  0, 0, 5, 23, "normal")

        # empty space
        label = tk.Label(self.scrollw.mnf, text="")
        label.grid(row=17, column=0, sticky="e")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=18, column=1)



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # # Table heading @0th row, 0th column
        # dappa.place_column_heading(self, row=0, col=0)
        dappa.place_no_heading(self)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()


    def save_data(self):
        self.tab_struct.save_cb(self.gui)

