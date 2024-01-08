#include "sg_counter.h"


const OsCounterType _OsCounterCtrlBlk[] =  {
	{
		.mincycle = 1,
		.maxallowedvalue = 1000000,
		.ticksperbase = 1,
		.maxallowedvalue = 1000000,
		.name = "mSecCounter"
	},
	{
		.mincycle = 100,
		.maxallowedvalue = 1000,
		.ticksperbase = 1,
		.maxallowedvalue = 1000,
		.name = "uSecCounter"
	}
};

TickType _OsCounterDataBlk[OS_MAX_COUNTERS];
