#
# Created on Thu Feb 29 2024 1:54:22 PM
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


import os

import utils.search as search
import gui.car_os.code_gen as code_gen
import gui.soad.soad_view as soad_view


SoAdSocketConnectionType_str = "\n\ntypedef struct {\n\
    uint16 rem_skt_id;  /* remote socket id */\n\
    uint16 gen_skt_id;  /* the tool generated id, for verification purposes */\n\
    uint16 skt_grp_id;  /* remote socket group */\n\
    uint16 tcpip_skt_id;  /* local socket id ref */\n\
    uint16 rem_ip[16];  /* remote ip (ipv6 or ipv4) */\n\
    uint16 rem_port;    /* remote port number */\n\
    TcpIp_ProtocolType protocol;\n\
} SoAdSocketConnectionType;\n\
\n"


SoAd_ConfigType_str = "\ntypedef struct {\n\
    SoAdSocketConnectionType *socon;\n\
} SoAd_ConfigType;\n\
\n"


SoAdTxUpperLayerType_str = "\ntypedef enum {\n\
    SOAD_UPPER_LAYER_TYPE_IF,\n\
    SOAD_UPPER_LAYER_TYPE_TP,\n\
    SOAD_UPPER_LAYER_TYPE_MAX\n\
} SoAdTxUpperLayerType;\n\
\n"


SoAdPduRouteType_str = "\ntypedef struct {\n\
    uint16 tx_pdu_id;\n\
    SoAdTxUpperLayerType ul_type;\n\
    uint16 pdu_hdr_id;\n\
    uint16 socon_id;\n\
    uint16 socon_grp_id;\n\
} SoAdPduRouteType;\n\
\n"



def ip_to_string(cfg, ip_str):
    ip_range = 0
    ip_addr = None
    ret_str = "{"
    if cfg["TcpIpDomainType"] == "TCPIP_AF_INET":
        ip_range = 4
        if cfg[ip_str] == "IPADDR_TYPE_ANY" or "ANY" in cfg[ip_str]:
            ip_addr = [0, 0, 0, 0]
        else:
            ip_addr = cfg[ip_str].split(".")
    else:
        ip_range = 16
        if cfg[ip_str] == "IPADDR_TYPE_ANY" or "ANY" in cfg[ip_str]:
            ip_addr = [0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0,  0, 0, 0, 0]
        else:
            ip_addr = cfg[ip_str].split(":")
    for j in range(16):
        if j < ip_range:
            ret_str += str(ip_addr[j])
        else:
            ret_str += "0"

        # end of initializer
        if j < 15:
            ret_str += ", "
    ret_str += "}"
    return ret_str



def generate_sourcefile(soad_src_path, soad_configs, sock_conns):
    cf = open(soad_src_path+"/cfg/SoAd_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"SoAd_cfg.h\"\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    soad_skt_grp = soad_configs["SoAdConfig"][0]["SoAdSocketConnectionGroup"]

    # create a group-unified socket conn. list (decision on 29-Feb-24 10:31 PM)
    cf.write("\nconst SoAdSocketConnectionType SoAdSocketConnectionConfigs[MAX_REMOTE_SOCKET_CONNS] = {\n")
    for i, socon in enumerate(sock_conns):
        cf.write("\t{\n")
        cf.write("\t\t/* SoAd Socket Connection - "+str(i)+" */\n")
        cf.write("\t\t.rem_skt_id = "+socon["SoAdSocketId"]+",\n")
        cf.write("\t\t.gen_skt_id = "+str(i)+",\n")
        cf.write("\t\t.skt_grp_id = "+socon["SoAdSocketConnectionGroupId"]+",\n")
        cf.write("\t\t.tcpip_skt_id = "+socon["TcpIpAddrId"]+",\n")

        cf.write("\t\t.rem_ip = "+ip_to_string(socon, "SoAdSocketRemoteIpAddress")+",\n")

        cf.write("\t\t.rem_port = "+socon["SoAdSocketRemotePort"]+",\n")
        cf.write("\t\t.protocol = "+socon["SoAdSocketProtocolChoice"]+",\n")
        cf.write("\t},\n")
    cf.write("};\n\n")

    # create SoAdPduRoute list
    pdu_routes = soad_configs["SoAdConfig"][0]["SoAdPduRoute"]
    cf.write("\nconst SoAdPduRouteType SoAdPduRouteConfigs[SOAD_TOTAL_PDU_ROUTES] = {\n")
    for i, route in enumerate(pdu_routes):
        cf.write("\t{\n")
        cf.write("\t\t/* SoAd PDU Route - "+str(i)+" */\n")

        cf.write("\t\t.tx_pdu_id    = "+route["SoAdTxPduId"]+",\n")
        if "IF" in route["SoAdTxUpperLayerType"]:
            cf.write("\t\t.ul_type      = SOAD_UPPER_LAYER_TYPE_IF,\n")
        else:
            cf.write("\t\t.ul_type      = SOAD_UPPER_LAYER_TYPE_TP,\n")

        cf.write("\t\t.pdu_hdr_id   = "+route["SoAdPduRouteDest"][0]["SoAdTxPduHeaderId"]+",\n")
        socon_grp = route["SoAdPduRouteDest"][0]["SoAdTxSocketConnOrSocketConnBundleRef"].split("-")
        cf.write("\t\t.socon_id     = "+socon_grp[0].split("_")[-1]+",\n")
        cf.write("\t\t.socon_grp_id = "+socon_grp[1].split("_")[-1]+",\n")
        cf.write("\t},\n")
    cf.write("};\n\n")

    cf.write("\nconst SoAd_ConfigType SoAd_Config = {\n")
    cf.write("\t.socon = &SoAdSocketConnectionConfigs\n")
    cf.write("};\n\n")

    cf.close()



def generate_headerfile(soad_src_path, soad_configs):
    hf = open(soad_src_path+"/cfg/SoAd_cfg.h", "w")
    hf.write("#ifndef CAR_OS_SOAD_CFG_H\n")
    hf.write("#define CAR_OS_SOAD_CFG_H\n\n")
    hf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")
    hf.write("#include <Platform_Types.h>\n")
    hf.write("#include <TcpIp.h>\n\n")


    hf.write(SoAdTxUpperLayerType_str)
    hf.write(SoAdPduRouteType_str)
    hf.write(SoAdSocketConnectionType_str)

    pdu_routes = soad_configs["SoAdConfig"][0]["SoAdPduRoute"]
    hf.write("\n#define SOAD_TOTAL_PDU_ROUTES ("+str(len(pdu_routes))+")")
    sock_conns = soad_view.get_consolidated_socket_connections()
    hf.write("\n#define SOAD_TOTAL_SOCKET_CONNS ("+str(len(sock_conns))+")")

    max_socks = soad_configs["SoAdGeneral"][0]["SoAdSoConMax"]
    hf.write("\n#define SOAD_SOCK_CONNS_MAX_CFG ("+str(max_socks)+")\n\n")

    hf.write(SoAd_ConfigType_str)
    hf.write("\nextern const SoAd_ConfigType SoAd_Config;\n")


    hf.write("\n\n#endif\n")
    hf.close()
    return sock_conns



def generate_code(gui, view):
    cwd = os.getcwd()
    if os.path.exists(os.getcwd()+"/car-os"):
        soad_src_path = search.find_dir("SoAd", cwd+"/car-os/submodules/SL/")
    else:
        soad_src_path = search.find_dir("SoAd", cwd+"/submodules/SL/")

    sock_conns = generate_headerfile(soad_src_path, view)
    generate_sourcefile(soad_src_path, view, sock_conns)
    return
    code_gen.create_build_files(gui)
