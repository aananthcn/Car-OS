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

import arxml.port.arxml_port as arxml_port
import utils.search as search

# Temporary work-around
import gui.car_os.code_gen as code_gen


def generate_dtsi_file(port_src_path, pins, port_info):
    df = open(port_src_path+"/cfg/Port.dtsi", "w")
    df.write("/* This file is auto-generated by "+__file__+ "\n   file. Any hand-modification will be lost! */\n")
    df.write("#include <zephyr/dt-bindings/gpio/gpio.h>\n\n")
    df.write("/ {\n\tzephyr,user {")

    # Dio ports
    for port in port_info:
        if port["PortPinMode"] == "PORT_PIN_MODE_DIO":
            pin_id = port["PortPinId"].zfill(2)
            if port["PortPinLevelValue"] == "PORT_PIN_LEVEL_HIGH":
                pin_lv = "GPIO_ACTIVE_HIGH"
            else:
                pin_lv = "GPIO_ACTIVE_LOW"
            df.write("\n\t\tgpiopin"+pin_id+"-gpios = <&gpio0 "+pin_id+" "+pin_lv+">;")

    df.write("\n\t};\n};")
    df.close


def generate_headerfile(port_src_path, pins, port_info):
    hf = open(port_src_path+"/cfg/Port_cfg.h", "w")
    hf.write("#ifndef NAMMA_AUTOSAR_PORT_CFG_H\n")
    hf.write("#define NAMMA_AUTOSAR_PORT_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Port_Types.h>\n\n\n")
    
    hf.write("typedef struct {\n")
    hf.write("\tPort_PinType pin_id;\n")
    hf.write("\tPort_PinDirectionType pin_dir;\n")
    hf.write("\tboolean pin_dir_changeable;\n")
    hf.write("\tPort_PinModeType pin_mode;\n")
    hf.write("\tPort_PinModeType pin_initial_mode;\n")
    hf.write("\tuint8 pin_level;\n")
    hf.write("\tboolean pin_mode_changeable;\n")
    hf.write("} PortPin;\n\n")
    
    hf.write("\n#define PORT_NUM_OF_PINS  ("+str(pins)+")\n")
    
    hf.write("typedef struct {\n")
    hf.write("\tPort_PinType num_pins;\n")
    hf.write("\tPortPin pin[PORT_NUM_OF_PINS];\n")
    hf.write("} Port_ConfigType;\n\n")
    hf.write("extern Port_ConfigType PortConfigs;\n\n")
    
    max_port_id = 0
    for item in port_info:
        if int(item["PortPinId"]) > max_port_id:
            max_port_id = int(item["PortPinId"])
    hf.write("#define MAX_PORT_ID  ("+str(max_port_id)+")\n\n\n")
    
    # Device tree spec structure pointer declaration for Dio ports
    for port in port_info:
        if port["PortPinMode"] == "PORT_PIN_MODE_DIO":
            pin_id = port["PortPinId"].zfill(2)
            hf.write("\nextern const struct gpio_dt_spec gpiopin"+pin_id+";")

    hf.write("\n\nconst struct gpio_dt_spec *port_get_zephyr_dt_spec(int port_id);\n")

    hf.write("\n\n#endif\n")
    hf.close()



def generate_sourcefile(port_src_path, pins, port_info):
    cf = open(port_src_path+"/cfg/Port_cfg.c", "w")
    cf.write("#include <Port_cfg.h>\n\n")
    cf.write("#include <zephyr/kernel.h>\n")
    cf.write("#include <zephyr/drivers/gpio.h>\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    #TODO: Port_ConfigType declaration and definitions are not required for Car-OS. Remove them once stable!
    cf.write("Port_ConfigType PortConfigs = {\n")
    cf.write("\t.num_pins = PORT_NUM_OF_PINS,\n")
    for i, item in enumerate(port_info):
        cf.write("\t.pin["+str(i)+"] = {\n")
        cf.write("\t\t.pin_id = "+item["PortPinId"]+",\n")
        cf.write("\t\t.pin_dir = "+item["PortPinDirection"]+",\n")
        cf.write("\t\t.pin_mode = "+item["PortPinMode"]+",\n")
        cf.write("\t\t.pin_level = "+item["PortPinLevelValue"]+",\n")
        cf.write("\t\t.pin_initial_mode = "+item["PortPinInitialMode"]+",\n")
        cf.write("\t\t.pin_dir_changeable = "+item["PortPinDirectionChangeable"]+",\n")
        cf.write("\t\t.pin_mode_changeable = "+item["PortPinModeChangeable"]+"\n")
        if i+1 < pins:
            cf.write("\t},\n")
        else:
            cf.write("\t}\n")
    cf.write("};\n")

    # Dio ports
    for port in port_info:
        if port["PortPinMode"] == "PORT_PIN_MODE_DIO":
            pin_id = port["PortPinId"].zfill(2)
            cf.write("\nconst struct gpio_dt_spec gpiopin"+pin_id+" = GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), gpiopin"+pin_id+"_gpios);")

    # port_zephyr_dt_init()
    cf.write("\n\n\nint port_zephyr_dt_init(void) {\n")
    cf.write("\tint retval = 0;\n")
    for port in port_info:
        if port["PortPinMode"] == "PORT_PIN_MODE_DIO":
            pin_id = port["PortPinId"].zfill(2)
            cf.write("\n\t/* check if pin "+pin_id+" is configured properly in dts file */\n")
            cf.write("\tretval = gpio_is_ready_dt(&gpiopin"+pin_id+");\n")
            cf.write("\tif (!retval)\n\t\treturn -"+str(int(pin_id))+";\n\n")
            if port["PortPinDirection"] == "PORT_PIN_OUT":
                pin_dr = "GPIO_OUTPUT_ACTIVE"
            else:
                pin_dr = "GPIO_INPUT"
            cf.write("\t/* configure the pin "+pin_id+" for Car-OS (AUTOSAR) */\n")
            cf.write("\tretval = gpio_pin_configure_dt(&gpiopin"+pin_id+", "+pin_dr+");\n")
            cf.write("\tif (retval < 0)\n\t\treturn -"+str(int(pin_id))+";\n\n")
    cf.write("\treturn 0;\n}\n\n")

    # port_get_zephyr_dt_spec()
    cf.write("\n\n\nconst struct gpio_dt_spec *port_get_zephyr_dt_spec(int port_id) {\n")
    cf.write("\tconst struct gpio_dt_spec *dt_spec = NULL;\n\n")
    cf.write("\tif ((port_id < 0) || (port_id > MAX_PORT_ID))\n\t\treturn NULL;\n\n")
    cf.write("\tswitch(port_id) {\n")
    for port in port_info:
        if port["PortPinMode"] == "PORT_PIN_MODE_DIO":
            pin_id = port["PortPinId"].zfill(2)
            cf.write("\t\tcase "+str(int(pin_id))+":\n")
            cf.write("\t\t\tdt_spec = &gpiopin"+pin_id+";\n")
            cf.write("\t\t\tbreak;\n")
        
    cf.write("\t\tdefault:\n")
    cf.write("\t\t\tbreak;\n\t}\n\n")
    cf.write("\treturn dt_spec;\n}\n\n")

    cf.close()



def generate_code(gui):
    cwd = os.getcwd()
    if os.path.exists(cwd+"/car-os"):
        port_src_path = search.find_dir("Port", cwd+"/car-os/submodules/MCAL/")
    else:
        port_src_path = search.find_dir("Port", cwd+"/submodules/MCAL/")

    pins, port_info, port_gen = arxml_port.parse_arxml(gui.arxml_file)
    generate_headerfile(port_src_path, pins, port_info)
    generate_sourcefile(port_src_path, pins, port_info)
    generate_dtsi_file(port_src_path, pins, port_info)
    code_gen.create_build_files(gui) # calling code_gen.create_build_files() is a work-around. This will be corrected later.
    
