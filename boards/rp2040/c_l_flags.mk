# 
# Created on Fri Dec 23 2022 7:12:40 AM
# 
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
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

# following flags will be included in all SWCs for building their static library
CFLAGS  += -mcpu=cortex-m0plus -mthumb -mabi=aapcs -mfp16-format=ieee -mtp=soft 
ASFLAGS += -mcpu=cortex-m0plus -mthumb -mabi=aapcs -mfp16-format=ieee -mtp=soft 
LDFLAGS += -mthumb -mthumb-interwork -marmelf 

# following definitions would be used by the main Makefile
BOARD_NAME := rp2040
LINK_DEF_F := ${CAR_OS_BOARDS_PATH}/${BOARD_NAME}.lds