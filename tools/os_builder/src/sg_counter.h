#ifndef ACN_OSEK_SG_COUNTER_H
#define ACN_OSEK_SG_COUNTER_H
#include <osek.h>


typedef struct {
    TickType maxallowedvalue; /* TODO: count in nano (micro?) seconds */
    TickType mincycle;
    TickType ticksperbase;
    uint8_t type;
    char* name;
} OsCounterType; /* == OsCounterCtrlBlkType */

extern const OsCounterType _OsCounterCtrlBlk[];
extern TickType _OsCounterDataBlk[];


#define MSECCOUNTER_INDEX   	(0)
#define USECCOUNTER_INDEX   	(1)


#define OS_TICK_DURATION_ns 	(1000000)
#define OS_TICK_COUNTER_IDX 	(0)
#define OS_MAX_COUNTERS    	(2)


#endif
