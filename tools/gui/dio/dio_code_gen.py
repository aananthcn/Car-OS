#
# Created on Sat Sep 03 2022 10:56:29 PM
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
import os

import arxml.dio.arxml_dio_parse as arxml_dio
import utils.search as search

# Temporary work-around
import gui.car_os.main_cgen as main_cgen


def generate_headerfile(dio_src_path, dio_info):
    hf = open(dio_src_path+"/cfg/Dio_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_DIO_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_DIO_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Dio.h>\n")
    hf.write("#include <Port_cfg.h>\n\n\n")
    
    hf.write("extern Dio_ChannelType DioChan2PortLookup[MAX_PORT_ID+1];\n\n")
    
    hf.write("\n\n#endif\n")
    hf.close()



def generate_sourcefile(dio_src_path, dio_info):
    cf = open(dio_src_path+"/cfg/Dio_cfg.c", "w")
    cf.write("#include <Dio_cfg.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    pins = len(dio_info)
    max_port_id = 0
    dio_port_ids = []
    dio_port_dict = {}
    for dio in dio_info:
        dio_port_ids.append(int(dio["DioPortId"]))
        dio_port_dict[int(dio["DioPortId"])] = int(dio["DioChannelId"])
        if int(dio["DioPortId"]) > max_port_id:
            max_port_id = int(dio["DioPortId"])
    cf.write("Dio_ChannelType DioChan2PortLookup[] = {\n\t")
    for i in range(max_port_id+1):
        comma_str = ", "
        if i == max_port_id:
            comma_str = "\n"
        if i in dio_port_ids:
            cf.write(str(dio_port_dict[i])+comma_str)
        else:
            cf.write("0xFFFF"+comma_str)
        if i % 10  == 0:
            cf.write("\n\t")
    cf.write("};\n")
    cf.close()



def generate_code(gui):
    cwd = os.getcwd()
    if os.path.exists(os.getcwd()+"/car-os"):
        dio_src_path = search.find_dir("Dio", cwd+"/car-os/submodules/MCAL/")
    else:
        dio_src_path = search.find_dir("Dio", cwd+"/submodules/MCAL/")
    pins, dio_configs, dio_groups, dio_general = arxml_dio.parse_arxml(gui.caros_cfg_file)
    generate_headerfile(dio_src_path, dio_configs)
    generate_sourcefile(dio_src_path, dio_configs)
    main_cgen.create_source(gui) # calling main_cgen.create_source() is a work-around. This will be corrected later.
    
