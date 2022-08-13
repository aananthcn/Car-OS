#
# Created on Sat Aug 13 2022 1:28:33 PM
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


FreeAUTOSAR_Boards = {
    "GENERIC" :
        ["qemu-versatilepb"],
    "BROADCOM" :
        ["rp2040"],
    "ST" :
        ["stm32f407vet6"]
}

UcView = None
SoCsOfSelectedMaker = []
SoCMakerStr = None
SoCStr = None


###############################################################################
# Local Functions
def SoCMaker_Selected(event):
    global SoCsOfSelectedMaker, SoCMakerStr, FreeAUTOSAR_Boards, SoCStr

    SoCsOfSelectedMaker = FreeAUTOSAR_Boards[SoCMakerStr.get()]
    SoCStr.set(SoCsOfSelectedMaker)


def on_uc_view_close():
    global UcView

    UcView.destroy()
    UcView = None


def generate_makefile():
    print("Generate Makefile is underconstruction")



###############################################################################
# Main Entry Point
def show_microcontroller_block(gui):
    global SoCsOfSelectedMaker, SoCMakerStr, FreeAUTOSAR_Boards, SoCStr, UcView

    # If previous view is active return
    if UcView != None:
        return

    # Create a child window
    UcView = tk.Toplevel()
    UcView.title("Microcontroller Configs")
    UcView.protocol("WM_DELETE_WINDOW", on_uc_view_close)

    col1_width = 22
    col2_width = 30

    # Label - SoC Manufacturer
    row = 1
    label = tk.Label(UcView, text="SoC Manufacturer", width=col1_width, anchor="e")
    label.grid(row=row, column=1, sticky="w")

    # Combobox - SoC Manufacturer
    SoCMakerStr = tk.StringVar()
    cmbsel = ttk.Combobox(UcView, width=col2_width, textvariable=SoCMakerStr, state="readonly")
    chipmakers = []
    for item in FreeAUTOSAR_Boards:
        chipmakers.append(item)
    cmbsel['values'] = chipmakers
    cmbsel.current()
    cmbsel.grid(row=row, column=2)
    cmbsel.bind("<<ComboboxSelected>>", SoCMaker_Selected)

    # Label - SoC
    row = 2
    label = tk.Label(UcView, text="SoC variant", width=col1_width, anchor="e")
    label.grid(row=row, column=1, sticky="w")

    # Combobox - SoC
    SoCStr = tk.StringVar()
    cmbsel = ttk.Combobox(UcView, width=col2_width, textvariable=SoCStr, state="readonly")
    cmbsel['values'] = SoCsOfSelectedMaker
    cmbsel.current()
    cmbsel.grid(row=row, column=2)

    # Generate Makefile Button
    row = 4
    genm = tk.Button(UcView, width=int(2*col2_width/3), text="Generate Makefile",
                     command=generate_makefile, bg="#206020", fg='white')
    genm.grid(row=row, column=2)