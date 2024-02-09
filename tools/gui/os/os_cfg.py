#
# Created on Sun Oct 02 2022 10:07:18 AM
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

import arxml.core.main_os as arxml_os


class OsTab:
    N_StrVar = 13
    OS_StrVar = []
    osv_oscfg = None # os_view's OS_Cfgs
    osv_tasks = None # os_view's Tasks
    stack_idx = 0

    def __init__(self, oscfg, tasks):
        self.osv_oscfg = oscfg
        if not oscfg:
            self.create_empty_os_config()
        self.osv_tasks = tasks
        self.stack_idx = self.N_StrVar - 1
        for i in range(self.N_StrVar):
            self.OS_StrVar.insert(i, tk.StringVar())


    def __del__(self):
        del self.OS_StrVar[:]
        self.osv_oscfg = None


    def draw(self, tab, gui):
        self.gui = gui

        # 1) CPU / SoC - Label + Edit-box
        row = 1
        label = tk.Label(tab, text="CPU / SoC name")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab,text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if gui.uc_info.micro != None:
            self.OS_StrVar[row-1].set(gui.uc_info.micro)
        elif "CPU" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["CPU"])
        else:
            print("Error: OS_Cfg does't have key: CPU")
        textb.grid(row=row, column=2)
    
        # 2) OS Name - Label + Edit-box
        row = 2
        label = tk.Label(tab, text="Image Name")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["OS"])
        else:
            print("Error: OS_Cfg does't have key: OS")
        textb.grid(row=row, column=2)
    
        # 3) OSEK Standard - Label + Combo-box
        row = 3
        label = tk.Label(tab, text="OSEK Standard")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("STANDARD", "EXTENDED")
        if "STATUS" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["STATUS"])
        else:
            print("Error: OS_Cfg does't have key: STATUS")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 4) STARTUPHOOK - Label + Combo-box
        row = 4
        label = tk.Label(tab, text="STARTUPHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "STARTUPHOOK" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["STARTUPHOOK"])
        else:
            print("Error: OS_Cfg does't have key: STARTUPHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)
    
        # 5) ERRORHOOK - Label + Combo-box
        row = 5
        label = tk.Label(tab, text="ERRORHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "ERRORHOOK" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["ERRORHOOK"])
        else:
            print("Error: OS_Cfg does't have key: ERRORHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 6) SHUTDOWNHOOK - Label + Combo-box
        row = 6
        label = tk.Label(tab, text="SHUTDOWNHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "SHUTDOWNHOOK" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["SHUTDOWNHOOK"])
        else:
            print("Error: OS_Cfg does't have key: SHUTDOWNHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 7) PRETASKHOOK - Label + Combo-box
        row = 7
        label = tk.Label(tab, text="PRETASKHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "PRETASKHOOK" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["PRETASKHOOK"])
        else:
            print("Error: OS_Cfg does't have key: PRETASKHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 8) POSTTASKHOOK - Label + Combo-box
        row = 8
        label = tk.Label(tab, text="POSTTASKHOOK")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "POSTTASKHOOK" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["POSTTASKHOOK"])
        else:
            print("Error: OS_Cfg does't have key: POSTTASKHOOK")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 9) OsProtectionHook - Label + Combo-box
        row = 9
        label = tk.Label(tab, text="OsProtectionHook")
        label.grid(row=row, column=1, sticky="w")
        cmbsel = ttk.Combobox(tab, width=27, textvariable=self.OS_StrVar[row-1], state="readonly")
        cmbsel['values'] = ("FALSE", "TRUE")
        if "OsProtectionHook" in self.osv_oscfg:
            self.OS_StrVar[row-1].set(self.osv_oscfg["OsProtectionHook"])
        else:
            print("Warn: OS_Cfg does't have key: OsProtectionHook")
        cmbsel.current()
        cmbsel.grid(row=row, column=2)

        # 10) OS_STACK_SIZE - Label + Edit-box
        row = 10
        label = tk.Label(tab, text="OS STACK SIZE")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS_STACK_SIZE" not in self.osv_oscfg:
            print("Error: OS_Cfg does't have key: OS_STACK_SIZE")
            self.osv_oscfg["OS_STACK_SIZE"] = 512
        self.OS_StrVar[row-1].set(self.osv_oscfg["OS_STACK_SIZE"])
        textb.grid(row=row, column=2)
        
        # 11) IRQ_STACK_SIZE - Label + Edit-box
        row = 11
        label = tk.Label(tab, text="IRQ STACK SIZE")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "IRQ_STACK_SIZE" not in self.osv_oscfg:
            print("Error: OS_Cfg does't have key: IRQ_STACK_SIZE")
            self.osv_oscfg["IRQ_STACK_SIZE"] = 512
        self.OS_StrVar[row-1].set(self.osv_oscfg["IRQ_STACK_SIZE"])
        textb.grid(row=row, column=2)
        
        # 12) OS_CTX_SAVE_SZ - Label + Edit-box
        row = 12
        label = tk.Label(tab, text="CONTEXT SAVE SIZE FOR TASKS", width=30, anchor="w")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[row-1])
        if "OS_CTX_SAVE_SZ" not in self.osv_oscfg:
            print("Error: OS_Cfg does't have key: OS_CTX_SAVE_SZ")
            self.osv_oscfg["OS_CTX_SAVE_SZ"] = 512
        self.OS_StrVar[row-1].set(self.osv_oscfg["OS_CTX_SAVE_SZ"])
        textb.grid(row=row, column=2)

        # 13) TASK_STACK_SIZE - Label + Edit-box
        row = 13
        self.stack_idx = row - 1
        label = tk.Label(tab, text="TASK STACK SIZE (Total)")
        label.grid(row=row, column=1, sticky="w")
        textb = tk.Entry(tab, text="Entry", width=30, textvariable=self.OS_StrVar[self.stack_idx], state="readonly")
        if "TASK_STACK_SIZE" not in self.osv_oscfg:
            print("Error: OS_Cfg does't have key: TASK_STACK_SIZE")
            self.osv_oscfg["TASK_STACK_SIZE"] = 0
        self.OS_StrVar[self.stack_idx].set(self.osv_oscfg["TASK_STACK_SIZE"])
        textb.grid(row=row, column=2)
        select = tk.Button(tab, width=6, text="Update", command=self.update)
        select.grid(row=row, column=3)

        # Save Button
        saveb = tk.Button(tab, width=10, text="Save Configs", command=self.save_data,
                          padx=0, pady=0, bg="#206020", fg='white')
        saveb.grid(row=row+1, column=2)



    def update(self):
        self.backup_data()
        # Recalculate parameters and update
        task_stack_size = 0
        for tsk in self.osv_tasks:
            try:
                task_stack_size += int(self.osv_oscfg["OS_CTX_SAVE_SZ"])
                task_stack_size += int(tsk["STACK_SIZE"])
            except:
                print("Error: stack size computation input validation error!")
        
        if self.stack_idx > 0:
            self.OS_StrVar[self.stack_idx].set(task_stack_size)


    def backup_data(self):
        # Backup to system generator global variables
        self.osv_oscfg["CPU"]                   = self.OS_StrVar[0].get()
        self.osv_oscfg["OS"]                    = self.OS_StrVar[1].get()
        self.osv_oscfg["STATUS"]                = self.OS_StrVar[2].get()
        self.osv_oscfg["STARTUPHOOK"]           = self.OS_StrVar[3].get()
        self.osv_oscfg["ERRORHOOK"]             = self.OS_StrVar[4].get()
        self.osv_oscfg["SHUTDOWNHOOK"]          = self.OS_StrVar[5].get()
        self.osv_oscfg["PRETASKHOOK"]           = self.OS_StrVar[6].get()
        self.osv_oscfg["POSTTASKHOOK"]          = self.OS_StrVar[7].get()
        self.osv_oscfg["OsProtectionHook"]      = self.OS_StrVar[8].get()
        self.osv_oscfg["OS_STACK_SIZE"]         = self.OS_StrVar[9].get()
        self.osv_oscfg["IRQ_STACK_SIZE"]        = self.OS_StrVar[10].get()
        self.osv_oscfg["OS_CTX_SAVE_SZ"]        = self.OS_StrVar[11].get()
        self.osv_oscfg["TASK_STACK_SIZE"]       = self.OS_StrVar[12].get()
    
    
    def create_empty_os_config(self):
        self.osv_oscfg["CPU"]                   = ""
        self.osv_oscfg["OS"]                    = ""
        self.osv_oscfg["STATUS"]                = "STANDARD"
        self.osv_oscfg["STARTUPHOOK"]           = "FALSE"
        self.osv_oscfg["ERRORHOOK"]             = "FALSE"
        self.osv_oscfg["SHUTDOWNHOOK"]          = "FALSE"
        self.osv_oscfg["PRETASKHOOK"]           = "FALSE"
        self.osv_oscfg["POSTTASKHOOK"]          = "FALSE"
        self.osv_oscfg["OS_STACK_SIZE"]         = "512"
        self.osv_oscfg["IRQ_STACK_SIZE"]        = "512"
        self.osv_oscfg["OS_CTX_SAVE_SZ"]        = "128"
        self.osv_oscfg["TASK_STACK_SIZE"]       = "0"



    def save_data(self):
        self.backup_data()
        arxml_os.export_os_cfgs_2_arxml(self.gui.arxml_file, self.gui)
