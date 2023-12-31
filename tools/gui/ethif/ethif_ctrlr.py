#
# Created on Tue Jan 17 2023 8:38:20 AM
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




class EthIfControllerView:
    n_ethif_ctrlr = 0
    max_ethif_ctrlr = 255
    n_ethif_ctrlr_str = None

    gui = None
    tab_struct = None # passed from *_view.py file
    scrollw = None
    configs = None # all UI configs (tkinter strings) are stored here.
    cfgkeys = ["EthIfCtrlIdx", "EthIfPhysControllerRef", "EthIfVlanId",
               "EthIfCtrlMtu", "EthIfMaxTxBufsTotal", "EthIfEthTrcvRef",
               "EthIfSwitchRef", "EthIfSwitchPortGroupRef"]
    
    n_header_objs = 0 #Objects / widgets that are part of the header and shouldn't be destroyed
    header_row = 3
    non_header_objs = []
    dappas_per_row = len(cfgkeys) + 1 # +1 for row labels
    init_view_done = False

    active_dialog = None
    active_widget = None


    def __init__(self, gui, lsc_cfg):
        self.gui = gui
        self.configs = []
        self.n_ethif_ctrlr = 0
        self.n_ethif_ctrlr_str = tk.StringVar()

        for cfg in lsc_cfg:
            if not cfg:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
            else:
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, cfg))
            self.n_ethif_ctrlr += 1
        self.n_ethif_ctrlr_str.set(self.n_ethif_ctrlr)



    def __del__(self):
        del self.n_ethif_ctrlr_str
        del self.non_header_objs[:]
        del self.configs[:]



    def create_empty_configs(self):
        gen_dict = {}

        gen_dict["EthIfCtrlIdx"] = str(self.n_ethif_ctrlr-1)
        gen_dict["EthIfPhysControllerRef"] = "..."
        gen_dict["EthIfVlanId"] = "0"
        gen_dict["EthIfCtrlMtu"] = "64"
        gen_dict["EthIfMaxTxBufsTotal"] = "1"
        gen_dict["EthIfEthTrcvRef"] = "..."
        gen_dict["EthIfSwitchRef"] = "..."
        gen_dict["EthIfSwitchPortGroupRef"] = "..."

        return gen_dict



    def draw_dappa_row(self, i):
        dappa.label(self, "Config #", self.header_row+i, 0, "e")
        bool_cmbsel = ("FALSE", "TRUE")
        ref_cmbsel = ("Ref1", "Ref2", "...")

        dappa.entry(self, "EthIfCtrlIdx", i, self.header_row+i, 1, 12, "readonly")
        dappa.combo(self, "EthIfPhysControllerRef", i, self.header_row+i, 2, 21, ref_cmbsel)
        dappa.entry(self, "EthIfVlanId", i, self.header_row+i, 3, 15, "normal")
        dappa.entry(self, "EthIfCtrlMtu", i, self.header_row+i, 4, 15, "normal")
        dappa.entry(self, "EthIfMaxTxBufsTotal", i, self.header_row+i, 5, 20, "normal")
        dappa.combo(self, "EthIfEthTrcvRef", i, self.header_row+i, 6, 18, ref_cmbsel)
        dappa.combo(self, "EthIfSwitchRef", i, self.header_row+i, 7, 18, ref_cmbsel)
        dappa.combo(self, "EthIfSwitchPortGroupRef", i, self.header_row+i, 8, 23, ref_cmbsel)



    def update(self):
        # get dappas to be added or removed
        self.n_ethif_ctrlr = int(self.n_ethif_ctrlr_str.get())

        # Tune memory allocations based on number of rows or boxes
        n_dappa_rows = len(self.configs)
        if not self.init_view_done:
            for i in range(n_dappa_rows):
                self.draw_dappa_row(i)
            self.init_view_done = True
        elif self.n_ethif_ctrlr > n_dappa_rows:
            for i in range(self.n_ethif_ctrlr - n_dappa_rows):
                self.configs.insert(len(self.configs), dappa.AsrCfgStr(self.cfgkeys, self.create_empty_configs()))
                self.draw_dappa_row(n_dappa_rows+i)
        elif n_dappa_rows > self.n_ethif_ctrlr:
            for i in range(n_dappa_rows - self.n_ethif_ctrlr):
                dappa.delete_dappa_row(self, (n_dappa_rows-1)+i)
                del self.configs[-1]

        # Set the self.cv scrolling region
        self.scrollw.scroll()



    def draw(self, tab):
        self.tab_struct = tab
        self.scrollw = window.ScrollableWindow(tab.frame, tab.xsize, tab.ysize)
        
        #Number of modes - Label + Spinbox
        label = tk.Label(self.scrollw.mnf, text="EthIf Ctrls:")
        label.grid(row=0, column=0, sticky="w")
        ethifnb = tk.Spinbox(self.scrollw.mnf, width=10, textvariable=self.n_ethif_ctrlr_str, command=lambda : self.update(),
                    values=tuple(range(0,self.max_ethif_ctrlr+1)))
        self.n_ethif_ctrlr_str.set(self.n_ethif_ctrlr)
        ethifnb.grid(row=0, column=1, sticky="w")

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        self.scrollw.update()

        # Table heading @2nd row, 1st column
        dappa.place_heading(self, 2, 1)

        self.update()
