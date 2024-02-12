#
# Created on Sun Oct 02 2022 10:09:29 AM
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
from os_builder.scripts.common import print_info
from os_builder.scripts.ob_globals import ISR_Params

import colorama
from colorama import Fore, Back, Style


def generate_code(path, IsrData):
    # create header file
    filename = path + "/" + "sg_ivector.h"
    hf = open(filename, "w")
    hf.write("#ifndef ACN_OSEK_IVECTOR_H\n")
    hf.write("#define ACN_OSEK_IVECTOR_H\n")
    hf.write("\n#include <osek.h>\n")
    hf.write("#include <osek_com.h>\n")

    # create source file
    filename = path + "/" + "sg_ivector.c"
    cf = open(filename, "w")
    cf.write("#include <stddef.h>\n")
    cf.write("#include \"sg_ivector.h\"\n\n")
    
    # compute min & max interrupt vector number configured
    ivec_max = 0
    ivec_min = 9999999999999
    for isr in IsrData:
        if int(isr[ISR_Params[1]]) > ivec_max:
            ivec_max = int(isr[ISR_Params[1]])
        if int(isr[ISR_Params[1]]) < ivec_min:
            ivec_min = int(isr[ISR_Params[1]])
    
    hf.write("\n\n#define NUMBER_OF_IVECTORS \t("+str(len(IsrData))+")\n")
    hf.write("#define MAX_IVECTOR_NUMBER  \t("+str(ivec_max)+")\n")
    hf.write("#define MIN_IVECTOR_NUMBER  \t("+str(ivec_min)+")\n\n")
   
    # ISR handler declaration loop 
    for isr in IsrData:
        cf.write("extern void "+isr[ISR_Params[0]]+"(void);\n")
        
    # ISR handler array definition loop
    cf.write("\n/*  Interrupt Vector Handlers */\n")
    cf.write("void (*_IsrHandler[])(void) = {\n")
    for i in range(ivec_max+1):
        match_found = None
        for isr in IsrData:
            match_found = False    
            if int(isr[ISR_Params[1]]) == i:
                cf.write("\t"+isr[ISR_Params[0]]+",\n")
                match_found = True
                break
        if not match_found:
            cf.write("\tNULL,\n")
    cf.write("};\n")
    hf.write("\nextern void (*_IsrHandler[])(void);\n")
    
    
    cf.close()
    hf.write("\n\n#endif\n")
    hf.close()
