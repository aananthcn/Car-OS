COMPILER=arm-none-eabi-
CC=${COMPILER}gcc
LD=${COMPILER}ld
AS=${COMPILER}as
OBJCOPY=${COMPILER}objcopy
ARCH = arm32
BOARD_NAME=stm32f407vet6

CC_VERS := $(shell ${CC} -dumpfullversion)
ifeq ($(OS),Windows_NT)
LIB_GCC_A_PATH=${MINGW_ROOT}/lib/gcc/arm-none-eabi/${CC_VERS}
else
LIB_GCC_A_PATH=/usr/lib/gcc/arm-none-eabi/${CC_VERS}
endif

INCDIRS  := -I ${MCU_PATH}/start-up/include \
            -I ${MCU_PATH}/start-up/include/arch/aarch32/ \
	    -I ${MCU_PATH}/src/bsp/startup/${BOARD_NAME} \
	    -I ${MCU_PATH}/start-up/include/arch/aarch32/cortex_m/ \
	    -I ${MCU_PATH}/start-up/include/arch/aarch32/cortex_m/cmsis/ \
	    -I ${MCU_PATH}/start-up/lib/include

LDFLAGS  += -nostdlib -g -L${LIB_GCC_A_PATH} -lgcc
CFLAGS   += -Werror ${INCDIRS} -g
ASFLAGS  += ${INCDIRS} -g

$(info  )
$(info compiling stm32f407vet6 board specific files)
#CFLAGS  += -march=armv7e-m 
#ASFLAGS += -march=armv7e-m
CFLAGS  += -mthumb -mthumb-interwork -march=armv7e-m -mcpu=cortex-m4 
ASFLAGS += -mthumb -mthumb-interwork -march=armv7e-m -mcpu=cortex-m4 
LDFILE	:= ${MCU_PATH}/src/bsp/startup/${BOARD_NAME}/${BOARD_NAME}.lds
LDFLAGS += -m armelf -T ${LDFILE}


BRD_OBJS	:= \
	${MCU_PATH}/src/bsp/startup/stm32f407vet6/board.o \
	${MCU_PATH}/src/bsp/startup/stm32f407vet6/vector_handlers.o \
	${MCU_PATH}/src/bsp/startup/stm32f407vet6/vectors.o \
	${MCU_PATH}/src/bsp/startup/stm32f407vet6/startup.o

