#
# Created on Sat Aug 13 2022 1:03:07 PM
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


import os_builder.scripts.sg_counter as sg_counter
import os_builder.scripts.sg_tasks as sg_tasks
import os_builder.scripts.sg_alarms as sg_alarms
import os_builder.scripts.sg_appmodes as sg_appmodes
import os_builder.scripts.sg_events as sg_events
import os_builder.scripts.sg_messages as sg_messages
import os_builder.scripts.sg_resources as sg_resources
import os_builder.scripts.sg_os_param as sg_os_param
import os_builder.scripts.sg_isrs as sg_isrs

import gui.os.os_cfg as gui_os_tab
import gui.os.mode_cfg as gui_am_tab
import gui.os.cnt_cfg as gui_cr_tab
import gui.os.res_cfg as gui_rs_tab
import gui.os.tsk_cfg as gui_tk_tab
import gui.os.alm_cfg as gui_al_tab
import gui.os.isr_cfg as gui_ir_tab


OsTab = AmTab = CtrTab = ResTab = TskTab = AlmTab = IsrTab = None
OsConfigViewActive = False



# OS Global Variables
Counters = []
Alarms = []
Tasks = []
AppModes = []
ISRs = []
OS_Cfgs = {}


def backup_os_gui_before_save():
    global OsTab, AmTab, CtrTab, ResTab, TskTab, AlmTab, IsrTab
    global OsConfigViewActive

    # Do not backup if the view is not active
    if not OsConfigViewActive:
        return

    # Do the stack memory calculation before save
    OsTab.update()

    # Backup GUI strings to System Generator global data
    OsTab.backup_data()
    AmTab.backup_data()
    CtrTab.backup_data()
    ResTab.backup_data()
    TskTab.backup_data()
    AlmTab.backup_data()
    IsrTab.backup_data()



def os_config_close_event(view):
    global OsConfigViewActive

    backup_os_gui_before_save()
    OsConfigViewActive = False
    view.destroy()


    
def show_os_config(gui):
    global Counters, Alarms, Tasks, AppModes, ISRs, OS_Cfgs
    global OsTab, AmTab, CtrTab, ResTab, TskTab, AlmTab, IsrTab
    global OsConfigViewActive

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 80 / 100
    view = tk.Toplevel()
    view.geometry("%dx%d+%d+%d" % (width, height, width/10, 15))
    view.title("AUTOSAR OS Configuration Tool")
    OsConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: os_config_close_event(view))
    gui.main_view.child_window = view
    notebook = ttk.Notebook(view)
    
    # Create tabs to configure OS
    os_tab = ttk.Frame(notebook)
    am_tab = ttk.Frame(notebook)
    cr_tab = ttk.Frame(notebook)
    rs_tab = ttk.Frame(notebook)
    tk_tab = ttk.Frame(notebook)
    al_tab = ttk.Frame(notebook)
    ir_tab = ttk.Frame(notebook)
    
    # Add tabs to configure OS
    notebook.add(os_tab, text ='   Os     ')
    notebook.add(am_tab, text ='OsAppMode ')
    notebook.add(cr_tab, text ='OsCounter ')
    notebook.add(rs_tab, text ='OsResource')
    notebook.add(tk_tab, text ='OsTasks   ')
    notebook.add(al_tab, text ='OsAlarm   ')
    notebook.add(ir_tab, text ='  OsIsr   ')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del OsTab
    del AmTab
    del CtrTab
    del ResTab
    del TskTab
    del AlmTab
    del IsrTab

    # create new GUI objects
    OsTab = gui_os_tab.OsTab(OS_Cfgs, Tasks)
    OsTab.draw(os_tab, gui)

    AmTab = gui_am_tab.AmTab(AppModes)
    AmTab.draw(am_tab, gui, width, height)
    
    CtrTab = gui_cr_tab.CounterTab(Counters)
    CtrTab.draw(cr_tab, gui, width, height)

    ResTab = gui_rs_tab.ResourceTab(Tasks)
    ResTab.draw(rs_tab, gui, width, height)

    TskTab = gui_tk_tab.TaskTab(Tasks, AmTab, ResTab)
    TskTab.draw(tk_tab, gui, width, height)
    
    AlmTab = gui_al_tab.AlarmTab(Alarms, TskTab, AmTab, CtrTab)
    AlmTab.draw(al_tab, gui, width, height)

    IsrTab = gui_ir_tab.IsrTab(ISRs, ResTab)
    IsrTab.draw(ir_tab, width, height)

    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", lambda event : show_os_tab_switch(event, gui))
    


def generate_code_for_os(path):
    try:
        sg_counter.generate_code(path, Counters)
        sg_appmodes.generate_code(path, AppModes, Tasks)
        sg_events.generate_code(path, Tasks)
        sg_messages.generate_code(path, Tasks)
        ResTaskList = sg_resources.generate_code(path, Tasks)
        sg_tasks.generate_code(path, Tasks)
        sg_alarms.generate_code(path, Alarms, Counters, Tasks)
        sg_os_param.generate_code(path, OS_Cfgs)
        sg_isrs.generate_code(path, ISRs)
    except:
        traceback.print_exc()
        return -1

    return 0



def os_reset():
    global Counters, Alarms, Tasks, AppModes, ISRs, OS_Cfgs

    del Counters[:]
    del Alarms[:]
    del Tasks[:]
    del AppModes[:]
    del ISRs[:]
    OS_Cfgs = {}



def os_block_click_handler(gui):
    show_os_config(gui)