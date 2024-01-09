#include <stddef.h>
#include <stdbool.h>
#include "sg_tasks.h"
#include "sg_appmodes.h"
#include "sg_events.h"
#include "sg_messages.h"
#include "sg_resources.h"

#include <zephyr/kernel.h> /* for k_sleep() */ 


/*   T A S K   D E F I N I T I O N S   */
const OsTaskType _OsTaskCtrlBlk[] = {
	{
		.handler = OS_TASK(Task_A),
		.id = 0,
		.sch_type = NON_PREEMPTIVE,
		.priority = 1,
		.activations = 1,
		.autostart = true,
		.appmodes = (const AppModeType **) &Task_A_AppModes,
		.n_appmodes = TASK_A_APPMODE_MAX,
		.evtmsks = NULL,
		.n_evtmsks = TASK_A_EVENT_MAX,
		.msglist = NULL,
		.n_msglist = TASK_A_MESSAGE_MAX,
		.stack_size = 512
	},
	{
		.handler = OS_TASK(Task_B),
		.id = 1,
		.sch_type = NON_PREEMPTIVE,
		.priority = 2,
		.activations = 1,
		.autostart = true,
		.appmodes = (const AppModeType **) &Task_B_AppModes,
		.n_appmodes = TASK_B_APPMODE_MAX,
		.evtmsks = (const EventMaskType**) &Task_B_EventMasks,
		.n_evtmsks = TASK_B_EVENT_MAX,
		.msglist = NULL,
		.n_msglist = TASK_B_MESSAGE_MAX,
		.stack_size = 512
	},
	{
		.handler = OS_TASK(Task_C),
		.id = 2,
		.sch_type = NON_PREEMPTIVE,
		.priority = 3,
		.activations = 1,
		.autostart = true,
		.appmodes = (const AppModeType **) &Task_C_AppModes,
		.n_appmodes = TASK_C_APPMODE_MAX,
		.evtmsks = (const EventMaskType**) &Task_C_EventMasks,
		.n_evtmsks = TASK_C_EVENT_MAX,
		.msglist = NULL,
		.n_msglist = TASK_C_MESSAGE_MAX,
		.stack_size = 512
	},
	{
		.handler = OS_TASK(Task_D),
		.id = 3,
		.sch_type = NON_PREEMPTIVE,
		.priority = 4,
		.activations = 1,
		.autostart = true,
		.appmodes = (const AppModeType **) &Task_D_AppModes,
		.n_appmodes = TASK_D_APPMODE_MAX,
		.evtmsks = NULL,
		.n_evtmsks = TASK_D_EVENT_MAX,
		.msglist = NULL,
		.n_msglist = TASK_D_MESSAGE_MAX,
		.stack_size = 512
	},
	{
		.handler = OS_TASK(EcuM_StartupTwo),
		.id = 4,
		.sch_type = NON_PREEMPTIVE,
		.priority = 5,
		.activations = 1,
		.autostart = true,
		.appmodes = (const AppModeType **) &EcuM_StartupTwo_AppModes,
		.n_appmodes = ECUM_STARTUPTWO_APPMODE_MAX,
		.evtmsks = NULL,
		.n_evtmsks = ECUM_STARTUPTWO_EVENT_MAX,
		.msglist = NULL,
		.n_msglist = ECUM_STARTUPTWO_MESSAGE_MAX,
		.stack_size = 512
	}
};


/*   T A S K ' S   E N T R Y   P O I N T   F O R   Z E P H Y R   */
bool OsTaskSchedConditionsOk(uint16_t task_id);
void OsTaskSchedEndLoop(uint16_t task_id);

static void _entry_Task_A(void *p1, void *p2, void *p3) {
	while(TRUE) {
		if (OsTaskSchedConditionsOk(0)) {
			OS_TASK(Task_A)();
		}
		OsTaskSchedEndLoop(0);
	}
}

static void _entry_Task_B(void *p1, void *p2, void *p3) {
	while(TRUE) {
		if (OsTaskSchedConditionsOk(1)) {
			OS_TASK(Task_B)();
		}
		OsTaskSchedEndLoop(1);
	}
}

static void _entry_Task_C(void *p1, void *p2, void *p3) {
	while(TRUE) {
		if (OsTaskSchedConditionsOk(2)) {
			OS_TASK(Task_C)();
		}
		OsTaskSchedEndLoop(2);
	}
}

static void _entry_Task_D(void *p1, void *p2, void *p3) {
	while(TRUE) {
		if (OsTaskSchedConditionsOk(3)) {
			OS_TASK(Task_D)();
		}
		OsTaskSchedEndLoop(3);
	}
}

static void _entry_EcuM_StartupTwo(void *p1, void *p2, void *p3) {
	while(TRUE) {
		if (OsTaskSchedConditionsOk(4)) {
			OS_TASK(EcuM_StartupTwo)();
		}
		OsTaskSchedEndLoop(4);
	}
}


const k_thread_entry_t _OsTaskEntryList[] = {
	_entry_Task_A,
	_entry_Task_B,
	_entry_Task_C,
	_entry_Task_D,
	_entry_EcuM_StartupTwo,
};


/*   T A S K ' S   S T A C K   P O I N T E R S   F O R   Z E P H Y R   */
static K_THREAD_STACK_DEFINE(_Task_A_sp, 512);
static K_THREAD_STACK_DEFINE(_Task_B_sp, 512);
static K_THREAD_STACK_DEFINE(_Task_C_sp, 512);
static K_THREAD_STACK_DEFINE(_Task_D_sp, 512);
static K_THREAD_STACK_DEFINE(_EcuM_StartupTwo_sp, 512);

const void* _OsStackPtrList[] = {
	_Task_A_sp,
	_Task_B_sp,
	_Task_C_sp,
	_Task_D_sp,
	_EcuM_StartupTwo_sp,
};


const u32 _OsTaskValidPriorities[] = {
	1, 2, 3, 4, 5
};
