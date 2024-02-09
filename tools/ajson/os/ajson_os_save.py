#
# Created on Fri Feb 09 2024 3:55:38 PM
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

import gui.os.os_view as os_view


def save_os_os_configs(jdata, gui_obj):
    m_key = "OsOs"
    jdata[m_key] = {}

    jdata[m_key]["OS_Cfgs"] = os_view.OS_Cfgs
    jdata[m_key]["OsHooks"] = {} # TODO: The OS_Cfgs will be split into these 3 once the complete porting is done.
    jdata[m_key]["OsHookStack"] = {}
    jdata[m_key]["CarOsParams"] = {}

    return


def save_os_mode_configs(jdata, gui_obj):
    m_key = "OsModes"
    jdata[m_key] = os_view.AppModes
    return


def save_os_counter_configs(jdata, gui_obj):
    m_key = "OsCounter"
    jdata[m_key] = os_view.Counters
    return


def save_os_task_configs(jdata, gui_obj):
    m_key = "OsTask"
    jdata[m_key] = os_view.Tasks
    return


def save_os_alarm_configs(jdata, gui_obj):
    m_key = "OsAlarm"
    jdata[m_key] = os_view.Alarms
    return


def save_os_isr_configs(jdata, gui_obj):
    m_key = "OsIsr"
    jdata[m_key] = os_view.ISRs

    return


def save_os_configs(jdata, gui_obj):
    m_key = "Os"
    jdata[m_key] = {}

    save_os_os_configs(jdata[m_key], gui_obj)
    save_os_mode_configs(jdata[m_key], gui_obj)
    save_os_counter_configs(jdata[m_key], gui_obj)
    save_os_task_configs(jdata[m_key], gui_obj)
    save_os_alarm_configs(jdata[m_key], gui_obj)
    save_os_isr_configs(jdata[m_key], gui_obj)
    return
