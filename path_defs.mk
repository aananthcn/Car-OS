# This file is autogenerated, any hand modifications will be lost!

# Makefile Paths Definitions
CAR_OS_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os
CAR_OS_INC_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/include
CAR_OS_BOARDSOC_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/boards/rp2040
ZEPHYR_INC_PATH := E:/zephyrproject/zephyr/include
ZEPHYR_INC_Z_PATH := E:/zephyrproject/zephyr/include/zephyr
ZEPHYR_STDLIB_PATH := E:/zephyrproject/zephyr/lib/libc/minimal/include
ZEPHYR_INSTALL_PATH := E:/zephyrproject
ZEPHYR_GEN_INC_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/build/zephyr/include/generated
MCU_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Mcu
ECUM_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/EcuM
PORT_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Port
DIO_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Dio
SPI_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Spi
LIN_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Lin
ETH_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Eth
ETHIF_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/ECU-AL/EthIf
TCPIP_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/TcpIp
OS_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/Os
OS_BUILDER_PATH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/tools/os_builder


# Link Archive File Path Definitions
LIBMCU := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Mcu/libMcu.a
LIBECUM := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/EcuM/libEcuM.a
LIBPORT := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Port/libPort.a
LIBDIO := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Dio/libDio.a
LIBSPI := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Spi/libSpi.a
LIBLIN := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Lin/libLin.a
LIBETH := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/MCAL/Eth/libEth.a
LIBETHIF := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/ECU-AL/EthIf/libEthIf.a
LIBTCPIP := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/TcpIp/libTcpIp.a
LIBOS := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/SL/Os/libOs.a
LIBCAR_OS_TESTAPP := E:/labs/zephyr-lab/Car-OS.Zephyr/car-os/submodules/AL/Car_Os_TestApp/libCar_OS_TestApp.a


# Link Archive Object List
LA_OBJS :=  $(LIBMCU) $(LIBECUM) $(LIBPORT) $(LIBDIO) $(LIBSPI) $(LIBLIN) $(LIBETH) \
	    $(LIBETHIF) $(LIBTCPIP) $(LIBOS) $(LIBCAR_OS_TESTAPP)
