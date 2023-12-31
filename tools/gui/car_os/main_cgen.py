#
# Created on Sat Aug 13 2022 10:19:54 PM
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
import json

import arxml.mcu.arxml_mcu as arxml_mcu
import utils.search as search



def generate_platform_header(gui):
    cwd = os.getcwd()
    if os.path.exists(cwd+"/car-os"):
        board_path = search.find_dir("cgen", cwd+"/car-os/include")
    else:
        board_path = search.find_dir("bsp", cwd+"/submodules/MCAL/Mcu")
    platform_h = open(board_path+"/platform.h", "w")
    platform_h.write("#ifndef CAR_OS_CGEN_PLATFORM_H\n")
    platform_h.write("#define CAR_OS_CGEN_PLATFORM_H\n\n")
    platform_h.write("/* This file is autogenerated by Car-OS builder */\n\n")
    platform_h.write("#include <"+gui.uc_info.micro+".h>\n")
    platform_h.write("#include <platform_"+gui.uc_info.micro+".h>\n")
    platform_h.write("#include <config_"+gui.uc_info.micro+".h>\n")
    platform_h.write("\n\n#endif\n")
    platform_h.close()



# This function creates app_paths.mk by reading applications.json file
# The app_paths.mk will be included by main Makefile to build all apps
def generate_make_list_for_apps(cwd, swc_list):
    app_layer_path = cwd+"/submodules/AL/"
    apps_json_file = app_layer_path+"/applications.json"
    app_data = None
    with open(apps_json_file) as jfile:
        app_data = json.load(jfile)
    jfile.close()

    app_paths_mk = cwd+"/app_paths.mk"
    with open(app_paths_mk, "w") as apfile:
        apfile.write("# This file is autogenerated, any hand modifications will be lost!\n\n")
        components = []

        # parse all application entries in json file
        for app in app_data:
            # ignore None entries
            if not app:
                continue
            app_name = app["git"].split("/")[-1].split(".git")[0]
            components.append(app_name)
            app_path = search.find_dir(app_name, cwd+"/submodules").replace("\\", "/")
            if app_path:
                apfile.write(app_name+"_path := "+app_path)
                swc_list.append(app_path)

        # create a dependency list for main makefile to invoke it
        apfile.write("\n\nAPP_LIST := ")
        for app_name in components:
            apfile.write(" $("+app_name+"_path)")
        apfile.write("\n\n")
        apfile.close()

    return swc_list



# This function creates c_l_flags.mk based on the micro and board selected.
# The c_l_flags.mk will be included by main Makefile to provide target specific
# CFLAGS and LDFLAGS to all other makefiles.
def generate_c_l_flags_file(gui, car_os_path):
    boards_path = car_os_path+"/boards/"+gui.uc_info.micro
    if not os.path.exists(boards_path):
        print("Error: Path verification failed!", boards_path)
        print("Info: Maybe the micro is not supported!")
        return -1

    c_l_flags_mk = car_os_path+"/c_l_flags.mk"
    with open(c_l_flags_mk, "w") as clfile:
        clfile.write("# This file is autogenerated, any hand modifications will be lost!\n\n")
        clfile.write("include "+boards_path+"/c_l_flags.mk\n")
        clfile.close()
 
    return 0



# This function parses "makefile"(s) that are part of the SWC's of AUTOSAR
# and generate a list of TARGETs (libObjects) for linking in main Makefile
def generate_link_lib_list(swc_paths):
    ll_list = []
    for dpath in swc_paths:
        fpath = dpath+"/makefile"
        if not os.path.exists(fpath):
            print("Warning: Path \""+fpath+"\" doesn't exist. [main_cgen.py:114]");
            continue
        with open(fpath, "r", encoding="utf-8") as mfile:
            lines = mfile.readlines()
        for line in lines:
            if "TARGET" in line and ":=" in line:
                lfile = line.split(":=")[-1].strip()
                ll_list.append(dpath+"/"+lfile)
    return ll_list



# returns non-zero in case of error
def create_source(gui):
    cwd = os.getcwd().replace("\\", "/")
    if os.path.exists(cwd+"/car-os"):
        car_os_path = cwd+"/car-os"
    else:
        car_os_path = cwd
    paths_mk = open(car_os_path+"/path_defs.mk", "w")
    paths_cmake = open(car_os_path+"/path_defs.cmake", "w")
    submodules_path = car_os_path+"/submodules"
    paths_mk.write("# This file is autogenerated, any hand modifications will be lost!\n\n")
    swc_paths = []

    # Makefile Paths Definitions
    #---------------------------
    paths_mk.write("# Makefile Paths Definitions\n")
    paths_mk.write("CAR_OS_PATH := "+car_os_path+"\n")
    paths_mk.write("CAR_OS_INC_PATH := "+car_os_path+"/include\n")

    zephyr_path = gui.zephyr_path.replace("\\", "/")
    car_os_board_path = search.find_dir("boards", car_os_path).replace("\\", "/")
    car_os_soc_path = car_os_board_path+"/"+gui.uc_info.micro
    paths_mk.write("CAR_OS_BOARDSOC_PATH := "+car_os_soc_path+"\n")
    paths_cmake.write("set(CAR_OS_BASE_DIR_PATH "+car_os_path+")\n")
    paths_cmake.write("set(CAR_OS_BOARDSOC_PATH "+car_os_soc_path+")\n")
    # swc_paths.append(car_os_soc_path) # TODO: check if this path is necessary, there won't be any library created in this path, I think.
    paths_cmake.write("set(CAR_OS_SYSGEN_S_PATH "+car_os_path+"/tools/os_builder/src)\n")
    paths_cmake.write("set(CAR_OS_ASR_APPL_PATH "+car_os_path+"/submodules/AL)\n")
    paths_cmake.write("set(CAR_OS_ASR_SRVC_PATH "+car_os_path+"/submodules/SL)\n")
    paths_cmake.write("set(CAR_OS_ASR_ECAL_PATH "+car_os_path+"/submodules/ECU-AL)\n")
    paths_cmake.write("set(CAR_OS_ASR_MCAL_PATH "+car_os_path+"/submodules/MCAL)\n")

    paths_mk.write("ZEPHYR_INC_PATH := "+zephyr_path+"/zephyr/include\n")
    paths_mk.write("ZEPHYR_INC_Z_PATH := "+zephyr_path+"/zephyr/include/zephyr\n")
    paths_mk.write("ZEPHYR_STDLIB_PATH := "+zephyr_path+"/zephyr/lib/libc/minimal/include\n")
    paths_mk.write("ZEPHYR_INSTALL_PATH := "+zephyr_path+"\n")
    paths_mk.write("ZEPHYR_GEN_INC_PATH := "+cwd+"/build/zephyr/include/generated\n")

    mcu_path = search.find_dir("Mcu", submodules_path).replace("\\", "/")
    paths_mk.write("MCU_PATH := "+mcu_path+"\n")
    swc_paths.append(mcu_path)
 
    ecum_path = search.find_dir("EcuM", submodules_path).replace("\\", "/")
    paths_mk.write("ECUM_PATH := "+ecum_path+"\n")
    swc_paths.append(ecum_path)

    port_path = search.find_dir("Port", submodules_path).replace("\\", "/")
    paths_mk.write("PORT_PATH := "+port_path+"\n")
    swc_paths.append(port_path)

    dio_path = search.find_dir("Dio", submodules_path).replace("\\", "/")
    paths_mk.write("DIO_PATH := "+dio_path+"\n")
    swc_paths.append(dio_path)

    spi_path = search.find_dir("Spi", submodules_path).replace("\\", "/")
    paths_mk.write("SPI_PATH := "+spi_path+"\n")
    swc_paths.append(spi_path)

    lin_path = search.find_dir("Lin", submodules_path).replace("\\", "/")
    paths_mk.write("LIN_PATH := "+lin_path+"\n")
    swc_paths.append(lin_path)

    eth_path = search.find_dir("Eth", submodules_path).replace("\\", "/")
    paths_mk.write("ETH_PATH := "+eth_path+"\n")
    swc_paths.append(eth_path)

    ethif_path = search.find_dir("EthIf", submodules_path).replace("\\", "/")
    paths_mk.write("ETHIF_PATH := "+ethif_path+"\n")
    swc_paths.append(ethif_path)

    tcpip_path = search.find_dir("TcpIp", submodules_path).replace("\\", "/")
    paths_mk.write("TCPIP_PATH := "+tcpip_path+"\n")
    swc_paths.append(tcpip_path)

    os_path = search.find_dir("Os", submodules_path).replace("\\", "/")
    paths_mk.write("OS_PATH := "+os_path+"\n")
    os_builder_path = search.find_dir("os_builder", car_os_path).replace("\\", "/")
    paths_mk.write("OS_BUILDER_PATH := "+os_builder_path+"\n")
    swc_paths.append(os_path)


    # Link Archive File Path Definitions
    #-----------------------------------
    # Build a path list for applications to invoke their makefiles
    swc_paths = generate_make_list_for_apps(car_os_path, swc_paths)
    libs_list = generate_link_lib_list(swc_paths)
    objs_list = []

    # Start writing the link archive file paths
    paths_mk.write("\n\n")
    paths_mk.write("# Link Archive File Path Definitions\n")
    for lib in libs_list:
        objname = lib.split("/")[-1].split(".")[0].upper()
        objs_list.append(objname)
        paths_mk.write(objname+" := "+lib+"\n")
    paths_mk.write("\n\n")


    # Link Archive Object List
    #-------------------------
    paths_mk.write("# Link Archive Object List\n")
    paths_mk.write("LA_OBJS := ")
    for i, obj in enumerate(objs_list):
        paths_mk.write(" $("+obj+")")
        if (i % 6 == 0) and (i > 1):
            paths_mk.write(" \\\n\t   ")
    paths_mk.write("\n")
    rc = generate_c_l_flags_file(gui, car_os_path)
    if rc < 0:
        return -1

    # Generate micro & arch specifc header files
    generate_platform_header(gui)

    # Update ARXML file
    arxml_mcu.update_arxml(gui.arxml_file, gui.uc_info)
    
    paths_mk.close()
    paths_cmake.close()
    
    return 0
