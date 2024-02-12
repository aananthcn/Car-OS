#
# Created on Fri Feb 09 2024 10:50:45 AM
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

import json
import os

import ajson.uc.ajson_uc as ajson_uc
import ajson.os.ajson_os as ajson_os

import ajson.port.ajson_port as ajson_port
import ajson.dio.ajson_dio as ajson_dio
import ajson.spi.ajson_spi as ajson_spi
import ajson.lin.ajson_lin as ajson_lin
import ajson.eth.ajson_eth as ajson_eth

import ajson.ethif.ajson_ethif as ajson_ethif
import ajson.soad.ajson_soad as ajson_soad


AJSON_Dump = None

def save_project(gui_obj, filepath):
    jfile = jdata = None

    if not gui_obj or not filepath:
        print("ERROR: save_project() invalid arguments!")
        return

    # change filename extension to Car-OS standard file extension
    if "ajson" not in os.path.basename(filepath):
        filename = os.path.basename(filepath).split(".")[0]+".json"
        gui_obj.caros_cfg_file = filepath.split("car-os")[0]+"/car-os/cfg/ajson/"+filename 
    print("Info: Saving", gui_obj.caros_cfg_file, "...")

    # take a copy of json file into RAM
    with open(gui_obj.caros_cfg_file) as jfile:
        jdata = json.load(jfile)
        jfile.close()

    # raise error if RAM area of A-JSON is empty
    if not jdata:
        print("Error: A-JSON file read failed. Can't save project!")
        return

    # reopen file as write only (to flush the previous content)
    jfile = open(gui_obj.caros_cfg_file, "w")

    # transfer the data from View(s) to A-JSON file
    ajson_uc.save_uc_configs(jdata, gui_obj)

    # MCAL Views
    ajson_port.save_port_configs(jdata, gui_obj)
    ajson_dio.save_dio_configs(jdata, gui_obj)
    ajson_spi.save_spi_configs(jdata, gui_obj)
    ajson_lin.save_lin_configs(jdata, gui_obj)
    ajson_eth.save_eth_configs(jdata, gui_obj)

    # ECU Abstraction Views
    ajson_ethif.save_ethif_configs(jdata, gui_obj)

    # Service layer views
    ajson_os.save_os_configs(jdata, gui_obj)
    ajson_soad.save_soad_configs(jdata, gui_obj)
    

    json.dump(jdata, jfile, indent=4)
    jfile.close()



def read_project(filepath):
    global AJSON_Dump
    retval = 0

    if not os.path.isfile(filepath):
        return -1

    with open(filepath) as jfile:
        AJSON_Dump = json.load(jfile)
        jfile.close()

    return retval