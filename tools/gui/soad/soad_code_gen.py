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


SoAdSocketConnectionType_str = "\n\ntypedef struct {\n\
    uint16 rem_skt_id;  /* remote socket id */\n\
    uint16 gen_skt_id;  /* the tool generated id, for verification purposes */\n\
    uint16 skt_grp_id;  /* remote socket group */\n\
    uint16 loc_skt_id;  /* local socket id ref */\n\
    uint16 rem_ip[16];  /* remote ip (ipv6 or ipv4) */\n\
    uint16 rem_port;    /* remote port number */\n\
    TcpIp_ProtocolType protocol;\n\
    TcpIpDomainType domain_type;\n\
} SoAdSocketConnectionType;\n\
\n"

# SoAdDomainType_str = "\ntypedef enum {\n\
#     TCPIP_AF_INET = 0x02,\n\
#     TCPIP_AF_INET6 = 0x1c,\n\
#     TCPIP_MAX_DOMAIN_TYPE\n\
# } SoAdDomainType;\n\
# \n"

# SoAdAddressType_str = "\ntypedef enum {\n\
#     TCPIP_UNICAST,\n\
#     TCPIP_ANYCAST,\n\
#     TCPIP_MULTCAST,\n\
#     TCPIP_MAX_ADDR_TYPE\n\
# } SoAdAddressType;\n\
# \n"

# SoAdAssignmentLifetime_str = "\ntypedef enum {\n\
#     TCPIP_FORGET,\n\
#     TCPIP_STORE,\n\
#     TCPIP_MAX_ASSN_LIFETIME\n\
# } SoAdAssignmentLifetime;\n\
# \n"

# SoAdAssignmentMethod_str = "\ntypedef enum {\n\
#     TCPIP_STATIC,\n\
#     TCPIP_DHCP,\n\
#     TCPIP_LINKLOCAL,\n\
#     TCPIP_IPV6_ROUTER,\n\
#     TCPIP_LINKLOCAL_DOIP,\n\
#     TCPIP_MAX_ASSN_METHOD\n\
# } SoAdAssignmentMethod;\n\
# \n"

# SoAdAssignmentTrigger_str = "\ntypedef enum {\n\
#     TCPIP_MANUAL,\n\
#     TCPIP_AUTOMATIC,\n\
#     TCPIP_MAX_ASSN_TRIGGER\n\
# } SoAdAssignmentTrigger;\n\
# \n"

# SoAdLocalAddr_str = "\ntypedef struct {\n\
#     uint16                    addr_id;\n\
#     SoAdDomainType           domain_type;\n\
#     SoAdAddressType          addr_type;\n\
#     SoAdAssignmentLifetime   addr_assn_life;\n\
#     SoAdAssignmentMethod     addr_assn_method;\n\
#     uint8                     addr_assn_prio;\n\
#     SoAdAssignmentTrigger    addr_assn_trig;\n\
#     uint16                    ip_addr[16]; /* supports both ipv6 and ipv4 */\n\
#     uint16                    ip_netmask[16]; /* supports both ipv6 and ipv4 */\n\
#     uint16                    ip_dfroutr[16]; /* supports both ipv6 and ipv4 */\n\
# } SoAdLocalAddr;\n\
# \n"

SoAd_ConfigType_str = "\ntypedef struct {\n\
    SoAdSocketConnectionType *socon;\n\
} SoAd_ConfigType;\n\
\n"


# def ip_to_string(cfg, item):
#     ip_range = 0
#     ip_addr = None
#     ret_str = "{"
#     if cfg["SoAdDomainType"] == "TCPIP_AF_INET":
#         ip_range = 4
#         ip_addr = cfg["SoAdStaticIpAddressConfig"][item].split(".")
#     else:
#         ip_range = 16
#         ip_addr = cfg["SoAdStaticIpAddressConfig"][item].split(":")
#     for j in range(16):
#         if j < ip_range:
#             ret_str += str(ip_addr[j])
#         else:
#             ret_str += "0"

#         # end of initializer
#         if j < 15:
#             ret_str += ", "
#     ret_str += "}"
#     return ret_str



def get_consolidated_socket_connections(soad_configs):
    sock_conns = []

    soad_skt_grp = soad_configs["SoAdConfig"][0]["SoAdSocketConnectionGroup"]
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


def generate_sourcefile(soad_src_path, soad_configs, sock_conns):
    cf = open(soad_src_path+"/cfg/SoAd_cfg.c", "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"SoAd_cfg.h\"\n\n\n")
    cf.write("// This file is autogenerated, any hand modifications will be lost!\n\n")

    soad_skt_grp = soad_configs["SoAdConfig"][0]["SoAdSocketConnectionGroup"]

    # create a group-unified socket conn. list (decision on 29-Feb-24 10:31 PM)
    cf.write("\nconst SoAdSocketConnectionType SoAdSocketConnectionConfigs[MAX_SOCKET_CONNS] = {\n")
    for i, socon in enumerate(sock_conns):
        cf.write("\t{\n")
        cf.write("\t\t/* SoAd Socket Connection - "+str(i)+" */\n")
        cf.write("\t\t.rem_skt_id = "+socon["SoAdSocketId"]+",\n")
        cf.write("\t\t.gen_skt_id = "+str(i)+",\n")
        cf.write("\t\t.skt_grp_id = "+socon["SoAdSocketConnectionGroupId"]+",\n")
        cf.write("\t\t.loc_skt_id = "+socon["TcpIpAddrId"]+",\n")

        # cf.write("\t\t.rem_ip = "+socon["SoAdAddressType"]+",\n")

        cf.write("\t\t.rem_port = "+socon["SoAdSocketRemotePort"]+",\n")
        cf.write("\t\t.protocol = "+socon["SoAdSocketProtocolChoice"]+",\n")
        cf.write("\t\t.domain_type = "+socon["TcpIpDomainType"]+"\n")
        cf.write("\t},\n")
    cf.write("};\n\n")


    # cf.write("\n\nconst SoAdGeneralCfgType SoAdGeneralConfigs = {\n")
    # cf.write("\t.mainfn_period_ms = "+str(int(1000*float(SoAdGeneral_cfg["SoAdMainFunctionPeriod"])))+",\n")
    # cf.write("\t.soad_buffer_mem = "+str(SoAdGeneral_cfg["SoAdBufferMemory"])+"\n")
    # cf.write("};\n")


    # cf.write("\nconst SoAdLocalAddr SoAdLocalAddrConfigs[MAX_TCPIP_LOCAL_ADDRESS] = {\n")
    # for i, cfg in enumerate(SoAdLocalAddr_cfg):
    #     cf.write("\t{\n")
    #     cf.write("\t\t/* SoAd local address - "+str(i)+" */\n")
    #     cf.write("\t\t.addr_id = "+cfg["SoAdAddrId"]+",\n")
    #     cf.write("\t\t.domain_type = "+cfg["SoAdDomainType"]+",\n")
    #     cf.write("\t\t.addr_type = "+cfg["SoAdAddressType"]+",\n")
    #     cf.write("\t\t.addr_assn_life = "+cfg["SoAdAddrAssignment"]["SoAdAssignmentLifetime"]+",\n")
    #     cf.write("\t\t.addr_assn_method = "+cfg["SoAdAddrAssignment"]["SoAdAssignmentMethod"]+",\n")
    #     cf.write("\t\t.addr_assn_prio = "+cfg["SoAdAddrAssignment"]["SoAdAssignmentPriority"]+",\n")
    #     cf.write("\t\t.addr_assn_trig = "+cfg["SoAdAddrAssignment"]["SoAdAssignmentTrigger"]+",\n")
    #     cf.write("\t\t.ip_addr = "+ip_to_string(cfg, "SoAdStaticIpAddress")+",\n")
    #     cf.write("\t\t.ip_netmask = "+ip_to_string(cfg, "SoAdNetmask")+",\n")
    #     cf.write("\t\t.ip_dfroutr = "+ip_to_string(cfg, "SoAdDefaultRouter")+"\n")
    #     cf.write("\t}\n")
    # cf.write("};\n\n")


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


    hf.write(SoAdSocketConnectionType_str)
    sock_conns = get_consolidated_socket_connections(soad_configs)
    hf.write("\n#define MAX_SOCKET_CONNS ("+str(len(sock_conns))+")\n")

    # hf.write(SoAdAddressType_str)
    # hf.write(SoAdAssignmentMethod_str)
    # hf.write(SoAdAssignmentTrigger_str)
    # hf.write(SoAdAssignmentLifetime_str)

    # hf.write(SoAdGeneralCfgType_str)
    # hf.write(SoAdLocalAddr_str)
    # hf.write("\nextern const SoAdLocalAddr SoAdLocalAddrConfigs[MAX_TCPIP_LOCAL_ADDRESS];\n\n\n")

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
