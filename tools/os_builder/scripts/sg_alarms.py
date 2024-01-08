#
# Created on Sun Oct 02 2022 10:08:51 AM
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
from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import AlarmParams, ANME, AAAT, AAT1, AAT2, AIAS, ATIM, ACYT, ACNT
from os_builder.scripts.ob_globals import CntrParams, CNME
from os_builder.scripts.ob_globals import TaskParams, TNMI

import colorama
from colorama import Fore, Back, Style


AAT_PyList = {
    "OsAlarmActivateTask" : "AAT_ACTIVATETASK", # AUTOSAR
    "ACTIVATETASK" : "AAT_ACTIVATETASK",        # OSEK
    "OsAlarmSetEvent" : "AAT_SETEVENT",         # AUTOSAR
    "SETEVENT" : "AAT_SETEVENT",                # OSEK
    "OsAlarmCallback" : "AAT_ALARMCALLBACK",    # AUTOSAR
    "ALARMCALLBACK" : "AAT_ALARMCALLBACK"       # OSEK
}


C_AlarmAction_Type = "\n\ntypedef enum {\n\
    AAT_ACTIVATETASK,\n\
    AAT_SETEVENT,\n\
    AAT_ALARMCALLBACK,\n\
    AAT_MAX_TYPE\n\
} AlarmActionType;\n\n"


C_Alarm_CtrlType = "\n\ntypedef struct {\n\
    char* name;                     /* short name of alarm */ \n\
    AlarmType alarm_id;             /* AlarmID, used by OSEK interface */ \n\
    AlarmType cntr_id;              /* OS Counter ID (= index of _OsCounterCtrlBlk + 1) */ \n\
    AlarmActionType aat;            /* Refer enum AlarmActionType */ \n\
    intptr_t aat_arg1;              /* arg1: task_name | callback_fun */\n\
    intptr_t aat_arg2;              /* arg2: event | NULL */\n\
    bool is_autostart;              /* does this alarm start at startup? */\n\
    u32 alarmtime;                  /* when does it expire? */\n\
    u32 cycletime;                  /* cyclic time - for repetition */\n\
    const AppModeType* appmodes;    /* alarm active in which modes? */\n\
    u32 n_appmodes;                 /* how may appmodes for this entry? */\n\
} OsAlarmCtrlBlkType;\n\n"


C_Alarm_DataType = "\n\ntypedef struct {\n\
    TickType counter;               /* Alarm Counter */ \n\
    TickType cycle;                 /* Alarm Repetition Value. If 0, then no repetition! */ \n\
    bool is_active;                 /* Alarm State */ \n\
} OsAlarmDataBlkType;\n\n"


C_AlarmGroups_Type = "\n\ntypedef struct {\n\
    const OsAlarmCtrlBlkType* ctrl_blk;\n\
    const OsAlarmDataBlkType* data_blk;\n\
    u32 len;\n\
} OsAlarmGroupsType;\n\n"




def get_task_id(Tasks, taskName):
    retval = "TASK_ID_MAX"
    for i, task in enumerate(Tasks):
        if task[TaskParams[TNMI]] == taskName:
            retval = str(i)
            break
    return retval


def get_counter_id(Counters, cntrName):
    retval = "OS_MAX_COUNTERS"
    for i, cntr in enumerate(Counters):
        if cntr[CntrParams[CNME]] == cntrName:
            retval = str(i)
            break
    return retval


def alarm_action_type_args(aat, alarm, cf, hf, Tasks):
    aat_arg1 = str(alarm[AlarmParams[AAT1]]).replace('"','')

    if aat == "ACTIVATETASK" or aat == "OsAlarmActivateTask":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t) "+get_task_id(Tasks, aat_arg1)+",\n")
        else:
            print(Fore.RED+"Error: Task to activate for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
            cf.write("\t\t.aat_arg1 = (intptr_t)NULL,\n")

        # for ACTIVATETASK type, arg2 is not required
        cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

    elif aat == "SETEVENT" or aat == "OsAlarmSetEvent":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t) "+get_task_id(Tasks, aat_arg1)+",\n")
        else:
            print(Fore.RED+"Error: Task to activate for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
        if AlarmParams[AAT2] in alarm:
            cf.write("\t\t.aat_arg2 = (intptr_t) OS_EVENT("+aat_arg1+", "+alarm[AlarmParams[AAT2]]+"),\n")
        else:
            print(Fore.RED+"Error: Event to trigger for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")
            cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

    elif aat == "ALARMCALLBACK" or aat == "OsAlarmCallback":
        if AlarmParams[AAT1] in alarm:
            cf.write("\t\t.aat_arg1 = (intptr_t)"+aat_arg1+",\n")
        else:
            print(Fore.RED+"Error: Callback for alarm: "+alarm[AlarmParams[ANME]]+" not configured!\n")

        # for ALARMCALLBACK type, arg2 is not required
        cf.write("\t\t.aat_arg2 = (intptr_t)NULL,\n")

        # declare call back function here. Definition will be part of "app"
        hf.write("extern void "+ aat_arg1 +"(void);\n")

    else:
        print(Fore.RED+"Error: Unknown action type for alarm: "+alarm[AlarmParams[ANME]]+"!\n")
        print("\n\n",aat, "\n\n")



# Compute how many times each counters are used in alarms
# Return value: dictionary with {'<counter-name>':<size>} 
def get_counter_size_list_for_alarms(Alarms):
    CounterSizeList = {}
    for alarm in Alarms:
        if alarm[AlarmParams[ACNT]] not in CounterSizeList:
            CounterSizeList[alarm[AlarmParams[ACNT]]] = 1
        else:
            CounterSizeList[alarm[AlarmParams[ACNT]]] += 1

    return CounterSizeList



def define_alarm_data_block(i, cntr, Alarms, Tasks, cf, hf):
    CounterSizeList = get_counter_size_list_for_alarms(Alarms)
    alarm_blk_size = str(CounterSizeList[cntr[CntrParams[CNME]]])

    cf.write("OsAlarmDataBlkType OsAlarms_"+cntr[CntrParams[CNME]]+"_DataBlk["+alarm_blk_size+"] = {\n")
    print_count = 0
    for alarm in Alarms:
        if cntr[CntrParams[CNME]] != alarm[AlarmParams[ACNT]]:
            continue
        cf.write("\t{\n")
        if AlarmParams[ATIM] in alarm and alarm[AlarmParams[ATIM]]:
            cf.write("\t\t.counter = "+alarm[AlarmParams[ATIM]]+",\n")
        else:
            cf.write("\t\t.counter = 0,\n")
        if AlarmParams[ACYT] in alarm and alarm[AlarmParams[ACYT]]:
            cf.write("\t\t.cycle = "+alarm[AlarmParams[ACYT]]+",\n")
        else:
            cf.write("\t\t.cycle = 0,\n")
        cf.write("\t\t.is_active = "+alarm[AlarmParams[AIAS]]+",\n")
        # if this is the last element in this list, then don't print a comma
        print_count += 1
        if print_count < CounterSizeList[alarm[AlarmParams[ACNT]]]:
            cf.write("\t},\n")
        else:
            cf.write("\t}\n")
    # for alarms loop
    cf.write("};\n\n\n\n")




def define_alarm_ctrl_block(i, cntr, Alarms, Tasks, cf, hf):
    CounterSizeList = get_counter_size_list_for_alarms(Alarms)

    cf.write("const OsAlarmCtrlBlkType OsAlarms_"+cntr[CntrParams[CNME]]+"_CtrlBlk[] = {\n")
    print_count = 0
    for alarm in Alarms:
        if cntr[CntrParams[CNME]] != alarm[AlarmParams[ACNT]]:
            continue
        cf.write("\t{\n")
        cf.write("\t\t.name = \""+alarm[AlarmParams[ANME]]+"\",\n")
        cf.write("\t\t.cntr_id = "+str(i)+",\n")
        cf.write("\t\t.alarm_id = OS_ALARM_ID_"+alarm[AlarmParams[ANME]].upper()+",\n")
        alarmActionType = alarm[AlarmParams[AAAT]]
        cf.write("\t\t.aat = "+AAT_PyList[alarmActionType]+",\n")

        alarm_action_type_args(alarmActionType, alarm, cf, hf, Tasks)

        cf.write("\t\t.is_autostart = "+alarm[AlarmParams[AIAS]]+",\n")
        if AlarmParams[ATIM] in alarm and alarm[AlarmParams[ATIM]]:
            cf.write("\t\t.alarmtime = "+str(alarm[AlarmParams[ATIM]])+",\n")
        else:
            cf.write("\t\t.alarmtime = 0,\n")
        if AlarmParams[ACYT] in alarm and alarm[AlarmParams[ACYT]]:
            cf.write("\t\t.cycletime = "+str(alarm[AlarmParams[ACYT]])+",\n")
        else:
            cf.write("\t\t.cycletime = 0,\n")

        if "APPMODE" in alarm and alarm["APPMODE"]:
            cf.write("\t\t.n_appmodes = ALARM_"+alarm[AlarmParams[ANME]].upper()+"_APPMODES_MAX,\n")
            cf.write("\t\t.appmodes = (const AppModeType *) &Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes\n")
        else:
            cf.write("\t\t.n_appmodes = 0,\n")
            cf.write("\t\t.appmodes = NULL\n")

        cf.write("\t}")

        # if this is the last element in this list, then don't print a comma
        print_count += 1
        if print_count < CounterSizeList[alarm[AlarmParams[ACNT]]]:
            cf.write(",\n")
        else:
            cf.write("\n")
    # for alarms loop
    cf.write("};\n\n\n\n")




def generate_source_file(path, Alarms, Counters, Tasks, cf, hf):
    cf.write("#include <stddef.h>\n")
    cf.write("#include <stdbool.h>\n")
    cf.write("#include \"sg_alarms.h\"\n")
    cf.write("#include \"sg_appmodes.h\"\n")
    cf.write("#include \"sg_tasks.h\"\n")
    cf.write("#include \"sg_events.h\"\n")

    cf.write("\n\n#define TRUE    true\n#define FALSE    false");
    cf.write("\n\n/*   A P P M O D E S   F O R   A L A R M S   */\n")

    for alarm in Alarms:
        if "APPMODE" in alarm and alarm["APPMODE"]:
            max_i = len(alarm["APPMODE"])
            cf.write("#define ALARM_"+alarm[AlarmParams[ANME]].upper()+"_APPMODES_MAX ("+str(max_i)+")\n")
            cf.write("const AppModeType Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes[] = {\n")
            i = 0
            for m in alarm["APPMODE"]:
                i += 1
                cf.write("\t"+m)
                if i != max_i:
                    cf.write(",\n")
                else:
                    cf.write("\n")
            cf.write("};\n\n")


    # define the alarms configured in OSEK builder or oil file
    cf.write("\n/*   A L A R M S   D E F I N I T I O N S   */\n")

    # OsAlarmDataBlkType & OsAlarmCtrlBlkType definition
    for i, cntr in enumerate(Counters):
        define_alarm_data_block(i, cntr, Alarms, Tasks, cf, hf)
        define_alarm_ctrl_block(i, cntr, Alarms, Tasks, cf, hf)

    # define _OsAlarmsGroups[];
    CounterSizeList = get_counter_size_list_for_alarms(Alarms)
    cf.write("\nconst OsAlarmGroupsType _OsAlarmsGroups[] = {\n")
    for cntr in Counters:
        cf.write("\t{\n")
        cf.write("\t\t.ctrl_blk = (const OsAlarmCtrlBlkType *) &OsAlarms_"+cntr[CntrParams[CNME]]+"_CtrlBlk,\n")
        cf.write("\t\t.data_blk = (const OsAlarmDataBlkType *) &OsAlarms_"+cntr[CntrParams[CNME]]+"_DataBlk,\n")
        cf.write("\t\t.len = "+str(CounterSizeList[cntr[CntrParams[CNME]]])+"\n")
        cf.write("\t},\n")
    cf.write("};\n\n")

    # define AlarmID to CounterID mapping
    cf.write("\n// _AlarmID2CounterID_map will be used by OSEK functions to identify the Ctrl and Data blocks of Alarms \n")
    cf.write("const AlarmType _AlarmID2CounterID_map[] = {\n\t")
    for alarm in Alarms:
        cf.write(get_counter_id(Counters, alarm[AlarmParams[ACNT]])+", ")
    cf.write("\n};\n")

    # define AlarmID to Block Index within a control block mapping
    cf.write("\n// OSEK Alarm APIs access Ctrl & Data blocks parameters of Alarms using this \n")
    cf.write("const AlarmType _AlarmID2BlkIndex_map[] = {\n\t")
    AlarmID_mapList = {}
    for alarm in Alarms:
        if alarm[AlarmParams[ACNT]] not in AlarmID_mapList:
            AlarmID_mapList[alarm[AlarmParams[ACNT]]] = 0
        else:
            AlarmID_mapList[alarm[AlarmParams[ACNT]]] += 1
        cf.write(str(AlarmID_mapList[alarm[AlarmParams[ACNT]]])+", ")
    cf.write("\n};\n")




def generate_header_file(path, Alarms, Counters, Tasks, cf, hf):
    hf.write("#ifndef ACN_OSEK_SG_ALARMS_H\n")
    hf.write("#define ACN_OSEK_SG_ALARMS_H\n")
    hf.write("#include <osek.h>\n")

    # AlarmIdType declaration
    hf.write("\n\ntypedef enum {\n")
    for alarm in Alarms:
        hf.write("\tOS_ALARM_ID_"+alarm[AlarmParams[ANME]].upper()+",\n")
    hf.write("\tOS_ALARM_ID_MAX\n} AlarmIdType;\n\n")

    hf.write(C_AlarmAction_Type)
    hf.write(C_Alarm_CtrlType)
    hf.write(C_Alarm_DataType)
    hf.write(C_AlarmGroups_Type);

    hf.write("\n")
    for alarm in Alarms:
        if "APPMODE" in alarm and alarm["APPMODE"]:
            hf.write("extern const AppModeType Alarm_"+alarm[AlarmParams[ANME]]+"_AppModes[];\n")
    hf.write("\n")

    CounterSizeList = get_counter_size_list_for_alarms(Alarms)

    # Macros
    hf.write("#define MAX_ALARM_COUNTERS  ("+str(len(CounterSizeList))+")\n")
    hf.write("#define MAX_OS_ALARMS       (OS_ALARM_ID_MAX)\n")

    # Global Variables
    hf.write("\n\nextern const OsAlarmGroupsType _OsAlarmsGroups[MAX_ALARM_COUNTERS];\n")

    # define AlarmID to CounterID mapping, will be used by OSEK functions to reach ctrl and data blocks
    hf.write("extern const AlarmType _AlarmID2CounterID_map[];\n")
    hf.write("extern const AlarmType _AlarmID2BlkIndex_map[];\n")

    hf.write("\n\n#endif\n")




def generate_code(path, Alarms, Counters, Tasks):
    print_info("Generating code for Alarms")

    # Header file generation
    filename = path + "/" + "sg_alarms.h"
    hf = open(filename, "w")

    # source file generation
    filename = path + "/" + "sg_alarms.c"
    cf = open(filename, "w")

    generate_header_file(path, Alarms, Counters, Tasks, cf, hf)
    generate_source_file(path, Alarms, Counters, Tasks, cf, hf)


    hf.close()
    cf.close()
