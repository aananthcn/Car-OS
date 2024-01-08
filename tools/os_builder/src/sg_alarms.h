#ifndef ACN_OSEK_SG_ALARMS_H
#define ACN_OSEK_SG_ALARMS_H
#include <osek.h>


typedef enum {
	OS_ALARM_ID_WAKETASKA,
	OS_ALARM_ID_WAKETASKB,
	OS_ALARM_ID_USECALARM,
	OS_ALARM_ID_WAKETASKD,
	OS_ALARM_ID_MAX
} AlarmIdType;



typedef enum {
    AAT_ACTIVATETASK,
    AAT_SETEVENT,
    AAT_ALARMCALLBACK,
    AAT_MAX_TYPE
} AlarmActionType;



typedef struct {
    char* name;                     /* short name of alarm */ 
    AlarmType alarm_id;             /* AlarmID, used by OSEK interface */ 
    AlarmType cntr_id;              /* OS Counter ID (= index of _OsCounterCtrlBlk + 1) */ 
    AlarmActionType aat;            /* Refer enum AlarmActionType */ 
    intptr_t aat_arg1;              /* arg1: task_name | callback_fun */
    intptr_t aat_arg2;              /* arg2: event | NULL */
    bool is_autostart;              /* does this alarm start at startup? */
    u32 alarmtime;                  /* when does it expire? */
    u32 cycletime;                  /* cyclic time - for repetition */
    const AppModeType* appmodes;    /* alarm active in which modes? */
    u32 n_appmodes;                 /* how may appmodes for this entry? */
} OsAlarmCtrlBlkType;



typedef struct {
    TickType counter;               /* Alarm Counter */ 
    TickType cycle;                 /* Alarm Repetition Value. If 0, then no repetition! */ 
    bool is_active;                 /* Alarm State */ 
} OsAlarmDataBlkType;



typedef struct {
    const OsAlarmCtrlBlkType* ctrl_blk;
    const OsAlarmDataBlkType* data_blk;
    u32 len;
} OsAlarmGroupsType;


extern const AppModeType Alarm_WakeTaskA_AppModes[];
extern const AppModeType Alarm_WakeTaskD_AppModes[];

#define MAX_ALARM_COUNTERS  (2)
#define MAX_OS_ALARMS       (OS_ALARM_ID_MAX)


extern const OsAlarmGroupsType _OsAlarmsGroups[MAX_ALARM_COUNTERS];
extern const AlarmType _AlarmID2CounterID_map[];
extern const AlarmType _AlarmID2BlkIndex_map[];


#endif
extern void Alarm_uSecAlarm_callback(void);
