/*
 * Created on Fri Aug 12 2022 9:49:26 PM
 *
 * The MIT License (MIT)
 * Copyright (c) 2022 Aananth C N
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software
 * and associated documentation files (the "Software"), to deal in the Software without restriction,
 * including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial
 * portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
 * TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
#ifndef PLATFORM_RP2040_H
#define PLATFORM_RP2040_H

#include "platform_deps.h"

// PLATFORM044
#define CPU_TYPE	CPU_TYPE_32
// PLATFORM048, PLATFORM049
#define CPU_BIT_ORDER	LSB_FIRST
// PLATFORM050, PLATFORM051
#define CPU_BYTE_ORDER	LOW_BYTE_FIRST


typedef unsigned char   uint8_least;
typedef unsigned short  uint16_least;
typedef unsigned int    uint32_least;
typedef signed char     sint8_least;
typedef signed short    sint16_least;
typedef signed int      sint32_least;


#endif