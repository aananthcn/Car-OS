#
# Created on Sun Feb 18 2024 10:01:46 PM
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

import gui.tcpip.tcpip_addr_assign as addr_assign
import gui.tcpip.tcpip_static_ip as static_ip



class TcpIpChildView:
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



class TcpIpLocalAddrView:
    n_tcpip_local_addr = 0
    max_tcpip_local_addr = 255
    n_tcpip_local_addr_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["TcpIpAddrId", "TcpIpDomainType", "TcpIpAddressType", "TcpIpAddrAssignment",
                "TcpIpStaticIpAddressConfig"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None


    def __init__(self, gui, view):
        self.gui = gui
        self.configs = []
        self.n_tcpip_local_addr = 0
        self.n_tcpip_local_addr_str = tk.StringVar()

        if not view:
            return

        if "TcpIpLocalAddr" not in view:
            return

        for cfg in view["TcpIpLocalAddr"]:
            if not cfg:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
            else:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_tcpip_local_addr += 1
        self.n_tcpip_local_addr_str.set(self.n_tcpip_local_addr)



    def __del__(self):
        del self.n_tcpip_local_addr_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}

        gen_dict["TcpIpAddrId"]      = str(self.n_tcpip_local_addr-1)
        gen_dict["TcpIpDomainType"] = "TCPIP_AF_INET"
        gen_dict["TcpIpAddressType"]  = "TCPIP_UNICAST"
        gen_dict["TcpIpAddrAssignment"]  = {}
        gen_dict["TcpIpStaticIpAddressConfig"]  = {}

        return gen_dict



    def draw_dappa_row(self, i):
        dappa.label(self, "Config #", self.header_row+i, 0, "e")
        dmn_type_cmbsel = ("TCPIP_AF_INET", "TCPIP_AF_INET6")
        addr_type_cmbsel = ("TCPIP_UNICAST", "TCPIP_ANYCAST", "TCPIP_MULTCAST")

        dappa.entry(self, "TcpIpAddrId", i, self.header_row+i, 1, 20, "readonly")
        dappa.combo(self, "TcpIpDomainType", i, self.header_row+i, 2, 25, dmn_type_cmbsel)
        dappa.combo(self, "TcpIpAddressType", i, self.header_row+i, 3, 23, addr_type_cmbsel)

        cb = lambda id = i : self.tcpip_addr_assign_select(id)
        text = "SELECT   ["+self.configs[i].datavar["TcpIpAddrAssignment"]["TcpIpAssignmentMethod"]+"]"
        dappa.button(self, "TcpIpAddrAssignment", i, self.header_row+i, 4, 24, text, cb)

        cb = lambda id = i : self.tcpip_static_ip_select(id)
        text = "SELECT   ["+self.configs[i].datavar["TcpIpStaticIpAddressConfig"]["TcpIpStaticIpAddress"]+"]"
        dappa.button(self, "TcpIpStaticIpAddressConfig", i, self.header_row+i, 5, 30, text, cb)



    def update(self):
        # get dappas to be added or removed
        self.n_tcpip_local_addr = int(self.n_tcpip_local_addr_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_tcpip_local_addr > n_dappa_rows:
            for i in range(self.n_tcpip_local_addr - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_tcpip_local_addr:
            for i in range(n_dappa_rows - self.n_tcpip_local_addr):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="TcpIp Interfaces:")
        label.grid(row=0, column=0, sticky="w")
        tcpipnb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_tcpip_local_addr_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_tcpip_local_addr+1)))
        self.n_tcpip_local_addr_str.set(self.n_tcpip_local_addr)
        tcpipnb.grid(row=0, column=1, sticky="w")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()


    def on_tcpip_addr_assign_close(self, row):
        # backup data
        self.configs[row].datavar["TcpIpAddrAssignment"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def tcpip_addr_assign_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_tcpip_addr_assign_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 310
        height = 110
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/5, y/5))
        self.active_dialog.title("TcpIpAddrAssignment")

        # create views and draw
        gen_view = TcpIpChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = addr_assign.TcpIpAddrAssignmentChildView(self.gui, row, self.configs[row].datavar["TcpIpAddrAssignment"] )
        gen_view.name = "TcpIpAddrAssignment"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def on_tcpip_static_ip_close(self, row):
        # backup data
        self.configs[row].datavar["TcpIpStaticIpAddressConfig"] = self.active_view.view.configs[0].get()

        # destroy view
        del self.active_view
        self.active_dialog.destroy()
        del self.active_dialog

        # re-draw all boxes (dappas) of this row
        dappa.delete_dappa_row(self, row)
        self.draw_dappa_row(row)


    def tcpip_static_ip_select(self, row):
        if self.active_dialog != None:
            return

        # function to create dialog window
        self.active_dialog = tk.Toplevel() # create an instance of toplevel
        self.active_dialog.protocol("WM_DELETE_WINDOW", lambda : self.on_tcpip_static_ip_close(row))
        self.active_dialog.attributes('-topmost',True)

        # set the geometry
        x = self.active_dialog.winfo_screenwidth()
        y = self.active_dialog.winfo_screenheight()
        width = 320
        height = 95
        self.active_dialog.geometry("%dx%d+%d+%d" % (width, height, x/3, y/5))
        self.active_dialog.title("TcpIpStaticIpAddressConfig")

        # create views and draw
        gen_view = TcpIpChildView(self.active_dialog, width, height, self.save_data)
        gen_view.view = static_ip.TcpIpStaticIpAddressConfigChildView(self.gui, row,
                self.configs[row].datavar["TcpIpStaticIpAddressConfig"] )
        gen_view.name = "TcpIpStaticIpAddressConfig"
        self.active_view = gen_view
        gen_view.view.draw(gen_view)


    def save_data(self):
        self.tab_struct.save_cb(self.gui)
