# Definitions
NAMMATESTAPP_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/AL/NammaTestApp
CWD := D:/_E/projects/oss/NammaAUTOSAR
ROOT_PATH := D:/_E/projects/oss/NammaAUTOSAR
MCU_BOARD_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/src/bsp
MCU_MICRO_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/src/bsp/rp2040
MCU_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu
ECUM_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/EcuM
PORT_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Port
DIO_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Dio
SPI_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Spi
OS_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/Os
OS_BUILDER_PATH := D:/_E/projects/oss/NammaAUTOSAR/tools/os_builder

# Inclusions
include D:/_E/projects/oss/NammaAUTOSAR/submodules/AL/NammaTestApp/namma_test_app.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/src/bsp/startup/rp2040/rp2040.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/src/bsp/arch/arm/cortex-m0/cortex-m0.mk

NAMMATESTAPP_PATH := D:/_E/projects/oss/NammaAUTOSAR/submodules/AL/NammaTestApp
include D:/_E/projects/oss/NammaAUTOSAR/submodules/AL/NammaTestApp/namma_test_app.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Mcu/Mcu.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/EcuM/EcuM.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Port/Port.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Dio/Dio.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/MCAL/Spi/Spi.mk
include D:/_E/projects/oss/NammaAUTOSAR/tools/os_builder/src/os-objs.mk
include D:/_E/projects/oss/NammaAUTOSAR/submodules/SL/Os/os-common.mk
include D:/_E/projects/oss/NammaAUTOSAR/common.mk

