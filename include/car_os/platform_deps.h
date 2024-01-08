/*
 * Created on Fri Aug 12 2022 9:27:06 PM
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
#ifndef PLATFORM_DEPS_H
#define PLATFORM_DEPS_H

// PLATFORM045
typedef enum {
	CPU_TYPE_8 = 8,
	CPU_TYPE_16 = 16,
	CPU_TYPE_32 = 32,
	CPU_TYPE_64 = 64,
	CPU_TYPE_MAX
} Cpu_Type;


// PLATFORM048, PLATFORM049
enum {
	MSB_FIRST,	/* Bitwise Big Endian */
	LSB_FIRST	/* Bitwise Little Endian */
};


// PLATFORM050, PLATFORM051
enum {
	HIGH_BYTE_FIRST,	/* Bytewise Big Endian */
	LOW_BYTE_FIRST		/* Bytewise Little Endian */
};

#endif