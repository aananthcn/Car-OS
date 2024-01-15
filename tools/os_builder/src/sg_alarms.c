#include <stddef.h>
#include <stdbool.h>
#include "sg_alarms.h"
#include "sg_appmodes.h"
#include "sg_tasks.h"
#include "sg_events.h"


#define TRUE    true
#define FALSE    false

/*   A P P M O D E S   F O R   A L A R M S   */
#define ALARM_WAKETASKA_APPMODES_MAX (2)
const AppModeType Alarm_WakeTaskA_AppModes[] = {
	OSDEFAULTAPPMODE,
	MANUFACT_MODE
};

#define ALARM_WAKETASKD_APPMODES_MAX (1)
const AppModeType Alarm_WakeTaskD_AppModes[] = {
	OSDEFAULTAPPMODE
};

#define ALARM_ALARM_ETHERNET_APPMODES_MAX (3)
const AppModeType Alarm_ALARM_Ethernet_AppModes[] = {
	OSDEFAULTAPPMODE,
	MANUFACT_MODE,
	HW_TEST_MODE
};


/*   A L A R M S   D E F I N I T I O N S   */
OsAlarmDataBlkType OsAlarms_mSecCounter_DataBlk[4] = {
	{
		.counter = 40,
		.cycle = 500,
		.is_active = TRUE,
	},
	{
		.counter = 0,
		.cycle = 0,
		.is_active = FALSE,
	},
	{
		.counter = 40,
		.cycle = 1000,
		.is_active = TRUE,
	},
	{
		.counter = 500,
		.cycle = 100,
		.is_active = TRUE,
	}
};



const OsAlarmCtrlBlkType OsAlarms_mSecCounter_CtrlBlk[] = {
	{
		.name = "WakeTaskA",
		.cntr_id = 0,
		.alarm_id = OS_ALARM_ID_WAKETASKA,
		.aat = AAT_ACTIVATETASK,
		.aat_arg1 = (intptr_t) 0,
		.aat_arg2 = (intptr_t)NULL,
		.is_autostart = TRUE,
		.alarmtime = 40,
		.cycletime = 500,
		.n_appmodes = ALARM_WAKETASKA_APPMODES_MAX,
		.appmodes = (const AppModeType *) &Alarm_WakeTaskA_AppModes
	},
	{
		.name = "WakeTaskB",
		.cntr_id = 0,
		.alarm_id = OS_ALARM_ID_WAKETASKB,
		.aat = AAT_SETEVENT,
		.aat_arg1 = (intptr_t) 1,
		.aat_arg2 = (intptr_t) OS_EVENT(Task_B, event1),
		.is_autostart = FALSE,
		.alarmtime = 0,
		.cycletime = 0,
		.n_appmodes = 0,
		.appmodes = NULL
	},
	{
		.name = "WakeTaskD",
		.cntr_id = 0,
		.alarm_id = OS_ALARM_ID_WAKETASKD,
		.aat = AAT_ACTIVATETASK,
		.aat_arg1 = (intptr_t) 3,
		.aat_arg2 = (intptr_t)NULL,
		.is_autostart = TRUE,
		.alarmtime = 40,
		.cycletime = 1000,
		.n_appmodes = ALARM_WAKETASKD_APPMODES_MAX,
		.appmodes = (const AppModeType *) &Alarm_WakeTaskD_AppModes
	},
	{
		.name = "ALARM_Ethernet",
		.cntr_id = 0,
		.alarm_id = OS_ALARM_ID_ALARM_ETHERNET,
		.aat = AAT_ACTIVATETASK,
		.aat_arg1 = (intptr_t) 5,
		.aat_arg2 = (intptr_t)NULL,
		.is_autostart = TRUE,
		.alarmtime = 500,
		.cycletime = 100,
		.n_appmodes = ALARM_ALARM_ETHERNET_APPMODES_MAX,
		.appmodes = (const AppModeType *) &Alarm_ALARM_Ethernet_AppModes
	}
};



OsAlarmDataBlkType OsAlarms_uSecCounter_DataBlk[1] = {
	{
		.counter = 0,
		.cycle = 0,
		.is_active = FALSE,
	}
};



const OsAlarmCtrlBlkType OsAlarms_uSecCounter_CtrlBlk[] = {
	{
		.name = "uSecAlarm",
		.cntr_id = 1,
		.alarm_id = OS_ALARM_ID_USECALARM,
		.aat = AAT_ALARMCALLBACK,
		.aat_arg1 = (intptr_t)Alarm_uSecAlarm_callback,
		.aat_arg2 = (intptr_t)NULL,
		.is_autostart = FALSE,
		.alarmtime = 0,
		.cycletime = 0,
		.n_appmodes = 0,
		.appmodes = NULL
	}
};




const OsAlarmGroupsType _OsAlarmsGroups[] = {
	{
		.ctrl_blk = (const OsAlarmCtrlBlkType *) &OsAlarms_mSecCounter_CtrlBlk,
		.data_blk = (const OsAlarmDataBlkType *) &OsAlarms_mSecCounter_DataBlk,
		.len = 4
	},
	{
		.ctrl_blk = (const OsAlarmCtrlBlkType *) &OsAlarms_uSecCounter_CtrlBlk,
		.data_blk = (const OsAlarmDataBlkType *) &OsAlarms_uSecCounter_DataBlk,
		.len = 1
	},
};


// _AlarmID2CounterID_map will be used by OSEK functions to identify the Ctrl and Data blocks of Alarms 
const AlarmType _AlarmID2CounterID_map[] = {
	0, 0, 1, 0, 0, 
};

// OSEK Alarm APIs access Ctrl & Data blocks parameters of Alarms using this 
const AlarmType _AlarmID2BlkIndex_map[] = {
	0, 1, 0, 2, 3, 
};
