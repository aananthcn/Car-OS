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

import ajson.soad.ajson_soad as ajson_soad



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







class TcpIpSocketOwnerView:
    n_tcpip_skt_owner = 0
    max_tcpip_skt_owner = 255
    n_tcpip_skt_owner_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["TcpIpSocketOwnerId", "TcpIpSocketOwnerUpperLayerType", 
            "TcpIpSocketOwnerCopyTxDataName", "TcpIpSocketOwnerHeaderFileName",
            "TcpIpSocketOwnerLocalIpAddrAssignmentChgName", "TcpIpSocketOwnerRxIndicationName",
            "TcpIpSocketOwnerTcpAcceptedName", "TcpIpSocketOwnerTcpConnectedName", 
            "TcpIpSocketOwnerTcpIpEventName", "TcpIpSocketOwnerTxConfirmationName"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None

    sock_con_list = [] # AUTOSAR is a mess, you need SoAd info in TcpIp (search for "mess")

    def __init__(self, gui, view):
        self.gui = gui
        self.configs = []
        self.n_tcpip_skt_owner = 0
        self.n_tcpip_skt_owner_str = tk.StringVar()

        if not view:
            return

        if "TcpIpSocketOwner" not in view:
            return

        for cfg in view["TcpIpSocketOwner"]:
            if not cfg:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
            else:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_tcpip_skt_owner += 1
        self.n_tcpip_skt_owner_str.set(self.n_tcpip_skt_owner)



    def __del__(self):
        del self.n_tcpip_skt_owner_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}

        gen_dict["TcpIpSocketOwnerId"]             = str(self.n_tcpip_skt_owner-1)
        gen_dict["TcpIpSocketOwnerUpperLayerType"] = "SOAD"
        gen_dict["TcpIpSocketOwnerCopyTxDataName"] = ""
        gen_dict["TcpIpSocketOwnerHeaderFileName"] = ""
        gen_dict["TcpIpSocketOwnerLocalIpAddrAssignmentChgName"] = ""
        gen_dict["TcpIpSocketOwnerRxIndicationName"]   = ""
        gen_dict["TcpIpSocketOwnerTcpAcceptedName"]    = ""
        gen_dict["TcpIpSocketOwnerTcpConnectedName"]   = ""
        gen_dict["TcpIpSocketOwnerTcpIpEventName"]     = ""
        gen_dict["TcpIpSocketOwnerTxConfirmationName"] = ""

        return gen_dict



    def draw_dappa_row(self, i):
        dappa.label(self, "Config #", self.header_row+i, 0, "e")
        upl_type_cmbsel = ("SOAD", "CDD")
        skt_conn_cmbsel = tuple(self.sock_con_list)

        # dappa.entry(self, "TcpIpSocketOwnerId", i, self.header_row+i, 1, 20, "readonly")
        dappa.combo(self, "TcpIpSocketOwnerId", i, self.header_row+i, 1, 20, skt_conn_cmbsel, is_rw="normal")
        dappa.combo(self, "TcpIpSocketOwnerUpperLayerType", i, self.header_row+i, 2, 30, upl_type_cmbsel)
        dappa.entry(self, "TcpIpSocketOwnerCopyTxDataName", i, self.header_row+i, 3, 33, "normal")
        dappa.entry(self, "TcpIpSocketOwnerHeaderFileName", i, self.header_row+i, 4, 34, "normal")
        dappa.entry(self, "TcpIpSocketOwnerLocalIpAddrAssignmentChgName", i, self.header_row+i, 5, 47, "normal")
        dappa.entry(self, "TcpIpSocketOwnerRxIndicationName", i, self.header_row+i, 6, 35, "normal")
        dappa.entry(self, "TcpIpSocketOwnerTcpAcceptedName", i, self.header_row+i, 7, 35, "normal")
        dappa.entry(self, "TcpIpSocketOwnerTcpConnectedName", i, self.header_row+i, 8, 35, "normal")
        dappa.entry(self, "TcpIpSocketOwnerTcpIpEventName", i, self.header_row+i, 9, 33, "normal")
        dappa.entry(self, "TcpIpSocketOwnerTxConfirmationName", i, self.header_row+i, 10, 35, "normal")



    def update(self):
        # get dappas to be added or removed
        self.n_tcpip_skt_owner = int(self.n_tcpip_skt_owner_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_tcpip_skt_owner > n_dappa_rows:
            for i in range(self.n_tcpip_skt_owner - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_tcpip_skt_owner:
            for i in range(n_dappa_rows - self.n_tcpip_skt_owner):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="SoCon #:")
        label.grid(row=0, column=0, sticky="w")
        tcpipnb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_tcpip_skt_owner_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_tcpip_skt_owner+1)))
        self.n_tcpip_skt_owner_str.set(self.n_tcpip_skt_owner)
        tcpipnb.grid(row=0, column=1, sticky="w")

        # Save Button
        saveb = tk.Button(self.scrollw.mnf, width=10, text="Save Configs", command=self.save_data, bg="#206020", fg='white')
        saveb.grid(row=0, column=2)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        # regenerate socket connection list from SoAd view
        soad_cfg = ajson_soad.read_soad_configs()
        if soad_cfg:
            soad_skt_grp = soad_cfg["SoAdConfig"][0]["SoAdSocketConnectionGroup"]
            for skt_grp in soad_skt_grp:
                skt_conn = skt_grp["SoAdSocketConnection"]
                for conn in skt_conn:
                    self.sock_con_list.append(conn["SoAdSocketId"])

        self.update()



    def save_data(self):
        self.tab_struct.save_cb(self.gui)
