#ifndef ACN_OSEK_SG_TASKS_H
#define ACN_OSEK_SG_TASKS_H

#include <osek.h>
#include <osek_com.h>

#include <zephyr/kernel/thread_stack.h> /* for stack pointer macro - Zephyr */


enum eTaskType {
	TASK_TASK_A_ID,
	TASK_TASK_B_ID,
	TASK_TASK_C_ID,
	TASK_TASK_D_ID,
	TASK_ECUM_STARTUPTWO_ID,
	TASK_ETHERNET_TASKS_ID,
	TASK_ID_MAX
};


#define TASK_A_APPMODE_MAX	(3)
#define TASK_A_RESOURCE_MAX	(1)
#define TASK_A_EVENT_MAX	(0)
#define TASK_A_MESSAGE_MAX	(0)

#define TASK_B_APPMODE_MAX	(1)
#define TASK_B_RESOURCE_MAX	(0)
#define TASK_B_EVENT_MAX	(1)
#define TASK_B_MESSAGE_MAX	(0)

#define TASK_C_APPMODE_MAX	(1)
#define TASK_C_RESOURCE_MAX	(0)
#define TASK_C_EVENT_MAX	(2)
#define TASK_C_MESSAGE_MAX	(0)

#define TASK_D_APPMODE_MAX	(1)
#define TASK_D_RESOURCE_MAX	(1)
#define TASK_D_EVENT_MAX	(0)
#define TASK_D_MESSAGE_MAX	(0)

#define ECUM_STARTUPTWO_APPMODE_MAX	(3)
#define ECUM_STARTUPTWO_RESOURCE_MAX	(0)
#define ECUM_STARTUPTWO_EVENT_MAX	(0)
#define ECUM_STARTUPTWO_MESSAGE_MAX	(0)

#define ETHERNET_TASKS_APPMODE_MAX	(3)
#define ETHERNET_TASKS_RESOURCE_MAX	(0)
#define ETHERNET_TASKS_EVENT_MAX	(0)
#define ETHERNET_TASKS_MESSAGE_MAX	(0)



typedef void (*TaskFuncType)(void);

typedef struct {
    TaskType id;
    TaskFuncType handler;
    u32 priority;
    SchType sch_type;
    u32 activations;
    bool autostart;
    const AppModeType** appmodes;
    u32 n_appmodes;
    MessageType** msglist;
    u32 n_msglist;
    const EventMaskType** evtmsks;
    u32 n_evtmsks;
    u32 stack_size;
} OsTaskType;

extern const OsTaskType _OsTaskCtrlBlk[];


#define OS_TASK(task)    (OSEK_Task_##task)

DeclareTask(Task_A);
DeclareTask(Task_B);
DeclareTask(Task_C);
DeclareTask(Task_D);
DeclareTask(EcuM_StartupTwo);
DeclareTask(Ethernet_Tasks);

extern const k_thread_entry_t _OsTaskEntryList[];
extern const void* _OsStackPtrList[];


#define OS_MAX_TASK_PRIORITY  (5)
extern const u32 _OsTaskValidPriorities[];
#define OS_NO_OF_PRIORITIES  (6)


#endif
