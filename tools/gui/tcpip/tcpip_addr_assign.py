#
# Created on Mon Feb 19 2024 9:41:40 AM
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



class TcpIpAddrAssignmentChildView:
    gui = None
    scrollw = None
    tab_struct = None # passed from *_view.py file
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["TcpIpAssignmentLifetime", "TcpIpAssignmentMethod",
               "TcpIpAssignmentPriority", "TcpIpAssignmentTrigger"]

    non_header_objs = []
    dappas_per_col = len(cfgkeys)


    def __init__(self, gui, index, ofl_cfg):
        self.gui = gui
        self.configs = []

        # Create config string for AUTOSAR configs on this tab
        if not ofl_cfg:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
        else:
            self.configs.append(dappa.AsrCfgStr(self.cfgkeys, ofl_cfg))


    def __del__(self):
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}
        
        gen_dict["TcpIpAssignmentLifetime"] = "TCPIP_FORGET"
        gen_dict["TcpIpAssignmentMethod"]   = "TCPIP_STATIC"
        gen_dict["TcpIpAssignmentPriority"] = "1"
        gen_dict["TcpIpAssignmentTrigger"]  = "TCPIP_MANUAL"
        
        return gen_dict



    def draw_dappas(self):
        life_cmbsel = ("TCPIP_FORGET", "TCPIP_STORE")
        meth_cmbsel = ("TCPIP_STATIC", "TCPIP_DHCP", "TCPIP_LINKLOCAL", "TCPIP_IPV6_ROUTER", "TCPIP_LINKLOCAL_DOIP")
        prio_cmbsel = ("1", "2", "3")
        trig_cmbsel = ("TCPIP_MANUAL", "TCPIP_AUTOMATIC")

        dappa.combo(self, "TcpIpAssignmentLifetime", 0, 0, 1, 20, life_cmbsel)
        dappa.combo(self, "TcpIpAssignmentMethod", 0, 1, 1, 20, meth_cmbsel)
        dappa.combo(self, "TcpIpAssignmentPriority", 0, 2, 1, 20, prio_cmbsel)
        dappa.combo(self, "TcpIpAssignmentTrigger", 0, 3, 1, 20, trig_cmbsel)



    def draw(self, view):
        self.tab_struct = view
        self.scrollw = window.ScrollableWindow(view.frame, view.xsize, view.ysize)

        # Table heading @0th row, 0th column
        dappa.place_column_heading(self, row=0, col=0)
        self.draw_dappas()

        # Support scrollable view
        self.scrollw.scroll()
