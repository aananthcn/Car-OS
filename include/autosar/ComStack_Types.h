/*
 * Created on Wed Jan 25 2023 10:33:57 PM
 *
 * The MIT License (MIT)
 * Copyright (c) 2023 Aananth C N
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
#ifndef CAR_OS_COM_STACK_TYPES_H
#define CAR_OS_COM_STACK_TYPES_H

#include <stdint.h>


typedef enum {
        BUFREQ_OK,
        BUFREQ_E_NOT_OK,
        BUFREQ_E_BUSY,
        BUFREQ_E_OVFL
} BufReq_ReturnType;



typedef uint16_t PduIdType;
typedef uint16_t PduLengthType;


typedef struct {
	uint8_t *SduDataPtr; /* Pointer to the SDU (i.e. payload data) of the PDU. */
	uint8_t *MetaDataPtr; /* Pointer to the meta data (e.g. CAN ID, socket ID, diagnostic addresses) of the PDU */
	PduLengthType SduLength;
} PduInfoType;



typedef enum {
	TP_STMIN, /* Separation Time */
	TP_BS, /* Block Size */
	TP_BC /* The Band width control parameter used in FlexRay transport protocol module */
} TPParameterType;



#endif
