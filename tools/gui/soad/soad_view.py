#
# Created on Sat Feb 04 2023 6:35:41 PM
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

import gui.soad.soad_gen as soad_gen
import gui.soad.soad_config as soad_cfg
import gui.soad.soad_bsw_mod as soad_bswm


import ajson.soad.ajson_soad as ajson_soad
import gui.soad.soad_code_gen as soad_cgen


TabList = []
SoAdConfigViewActive = False
SoAdView = {}


class SoAdTab:
    tab = None
    name = None
    xsize = None
    ysize = None
    frame = None
    save_cb = None
    
    def __init__(self, f, w, h):
        self.save_cb = soad_save_callback
        self.frame = f
        self.xsize = w
        self.ysize = h




def get_consolidated_socket_connections():
    global SoAdView

    sock_conns = []

    soad_skt_grp = SoAdView["SoAdConfig"][0]["SoAdSocketConnectionGroup"]
    for g, skt_grp in enumerate(soad_skt_grp):
        skt_conn = skt_grp["SoAdSocketConnection"]
        for conn in skt_conn:
            skt_con = {}
            skt_con["SoAdSocketConnectionGroupId"] = str(g)
            skt_con["TcpIpAddrId"] = skt_grp["SoAdSocketLocalAddressRef"].split("_")[-1].split("-")[0]
            skt_con["SoAdSocketId"] = conn["SoAdSocketId"]
            ip_addr = conn["SoAdSocketRemoteIpAddress"]
            skt_con["SoAdSocketRemoteIpAddress"] = ip_addr
            skt_con["SoAdSocketRemotePort"] = conn["SoAdSocketRemotePort"]

            # ipv6 or ipv4?
            if "." in ip_addr and len(ip_addr.split(".")) == 4:
                skt_con["TcpIpDomainType"] = "TCPIP_AF_INET"
            else:
                skt_con["TcpIpDomainType"] = "TCPIP_AF_INET6"

            # TCP or UDP?
            if "TCP" == skt_grp["SoAdSocketProtocolChoice"]:
                skt_con["SoAdSocketProtocolChoice"] = "TCPIP_IPPROTO_TCP"
            else:
                skt_con["SoAdSocketProtocolChoice"] = "TCPIP_IPPROTO_UDP"

            sock_conns.append(skt_con)

    return sock_conns




def soad_config_close_event(gui, view):
    global SoAdConfigViewActive

    SoAdConfigViewActive = False
    view.destroy()



def soad_save_callback(gui):
    global SoAdView

    # soad_configs = {}
    SoAdView.clear()

    # pull all configs from UI tabs
    for tab in TabList:
        tab_cfgs = []
        for cfg in tab.tab.configs:
            tab_cfgs.append(cfg.get())

        # copy to configs to dict
        SoAdView[tab.name] = tab_cfgs

    # copy to SoadView in order to write into A-JSON file 
    gui.save()

    # generate code
    soad_cgen.generate_code(gui, SoAdView)


    
def show_soad_tabs(gui):
    global SoAdConfigViewActive, TabList, SoAdView
    
    if SoAdConfigViewActive:
        return

    # Create a child window (tabbed view)
    width = gui.main_view.xsize * 80 / 100
    height = gui.main_view.ysize * 40 / 100
    view = tk.Toplevel()
    gui.main_view.child_window = view
    xoff = (gui.main_view.xsize - width)/2
    yoff = (gui.main_view.ysize - height)/3
    view.geometry("%dx%d+%d+%d" % (width, height, xoff, yoff))
    view.title("AUTOSAR Socket Adapter Configuration Tool")
    SoAdConfigViewActive = True
    view.protocol("WM_DELETE_WINDOW", lambda: soad_config_close_event(gui, view))
    notebook = ttk.Notebook(view)

    # Create tabs to configure SoAd
    gen_frame = ttk.Frame(notebook)
    bswm_frame = ttk.Frame(notebook)
    cfg_frame = ttk.Frame(notebook)
    
    # Add tabs to configure SoAd
    notebook.add(gen_frame, text ='SoAdGeneral')
    notebook.add(bswm_frame, text ='SoAdBswModules')
    notebook.add(cfg_frame, text ='SoAdConfig')
    notebook.pack(expand = 1, fill ="both")

    # destroy old GUI objects
    del TabList[:]

    # read SoAd content from A-JSON file
    SoAdView = ajson_soad.read_soad_configs()
    
    # create the SoAdGeneral GUI tab
    soad_gen_view = SoAdTab(gen_frame, width, height)
    soad_gen_view.tab = soad_gen.SoAdGeneralView(gui, SoAdView)
    soad_gen_view.name = "SoAdGeneral"
    TabList.append(soad_gen_view)

    # create the SoAdBswModules GUI tab
    soad_bswm_view = SoAdTab(bswm_frame, width, height)
    soad_bswm_view.tab = soad_bswm.SaOdBswModulesView(gui, SoAdView)
    soad_bswm_view.name = "SoAdBswModules"
    TabList.append(soad_bswm_view)

    # create the SoAdGeneral GUI tab
    soad_configset_view = SoAdTab(cfg_frame, width, height)
    soad_configset_view.tab = soad_cfg.SoAdConfigView(gui, SoAdView)
    soad_configset_view.name = "SoAdConfig"
    TabList.append(soad_configset_view)

    # Draw all tabs
    soad_gen_view.tab.draw(soad_gen_view)
    soad_bswm_view.tab.draw(soad_bswm_view)
    soad_configset_view.tab.draw(soad_configset_view)

    # gui.main_view.child_window.bind("<<NotebookTabChanged>>", show_os_tab_switch)



# Main Entry Point
def soad_block_click_handler(gui):
    show_soad_tabs(gui)