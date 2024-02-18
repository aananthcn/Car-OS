#
# Created on Sat Feb 17 2024 8:32:22 PM
#
# The MIT License (MIT)
# Copyright (c) 2024 Aananth C N
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

# This tool depends on MSYS2 package "poppler", install it using following command:
#       pacman -S mingw-w64-x86_64-poppler

import sys
import os
import subprocess

from tkinter import filedialog
from tkinter import messagebox


class ConfigItem:
    def __init__(self):
        self.valid = False
        self.param_name = ""
        self.modul_name = ""
        self.cntnr_name = ""
        self.parent_ctnr = "" 
        self.multiplicity = ""
        self.type = ""
        self.description = ""

    def is_name_found(self):
        if self.cntnr_name or self.modul_name or self.param_name:
            return True
        else:
            return False

    def print(self, ostream):
        config = None
        if self.param_name:
            config = self.param_name
        elif self.modul_name:
            config = self.modul_name
        elif self.cntnr_name:
            config = self.cntnr_name

        if not config:
            return

        print(config +"," + self.parent_ctnr +"," + self.type +"," + self.multiplicity +"," + self.description, file=ostream)



row_separator = ["SWS Item"]
col_separator = ["Parameter", "Module", "Container", "Parent", "Multiplicity", "Type"]
valid_name_tokens = ["Module", "Parameter", "Container"]



def is_line_valid_to_proceed(cfg, tokens):
    retval = False

    if len(tokens) == 0 or not cfg:
        return retval

    if any(sep in tokens[0] for sep in col_separator):
        retval = True
    
    return retval



def is_cfg_ok_to_push(cfg):
    retval = False

    if not cfg:
        return retval

    # for modules there are no other parameters required
    if cfg.modul_name:
        return True

    # for containers, only parent container is required
    if cfg.cntnr_name:
        if cfg.parent_ctnr:
            return True

    # for parameters, all are required
    if cfg.param_name:
        # now if all of these are filled, then not ok to proceed
        if cfg.parent_ctnr and cfg.multiplicity and cfg.type:
            retval = True

    return retval



file_exts = [('PDF files', '*.pdf')]
open_file = filedialog.askopenfile(filetypes = file_exts, defaultextension = file_exts)
if open_file == None:
    messagebox.showinfo("AUTOSAR Cfg extractor", "Unable to open the PDF file!")
    exit()
pdf_file = open_file.name
print("PDF file:", pdf_file)
basename = os.path.basename(pdf_file)
basepath = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/output/"
txt_file = basepath + basename.split(".")[0]+".txt"
print("Txt File:", txt_file)
csv_file = basepath + basename.split(".")[0]+".csv"
print("CSV File:", csv_file)
subprocess.run(["pdftotext", "-q", pdf_file, txt_file])


avoid_parsing = True
config_line_count = 0


cfg = None
cfg_objs = []

with open(txt_file, encoding="utf8") as file:
    lines = file.readlines()
    lstln = len(lines)
    print("total lines: ", lstln)
    i = 0
    while i < lstln:
        # read a line
        line = lines[i]
        i = i + 1
        new_item_found = False

        # skip all other sections other than configuration section of SWS spec
        if "Configuration specification" in line:
            config_line_count += 1
            if config_line_count > 1:
                avoid_parsing = False
        if avoid_parsing:
            continue

        # detect if this is a new config item line in pdf
        if any(sep in line for sep in row_separator):
            # search line by line backward but not more than 10 lines
            new_item_found = True
            if cfg: # check if already pushed
                cfg_objs.append(cfg)

            # Create a new cfg object
            cfg = ConfigItem() # new obj
            continue # continue to search for column separator

        # are we done with current cfg and wait for new row_separator event?
        if is_cfg_ok_to_push(cfg):
            cfg_objs.append(cfg)
            cfg = None

        # let us split line to parse the columns
        tokens = line.split()

        # enter into this loop only if the new cfg line (in PDF) is detected but end of cfg line is not reached
        if is_line_valid_to_proceed(cfg, tokens):
            if tokens[0] in valid_name_tokens:
                if cfg.is_name_found():
                    continue
                if len(tokens) > 1:
                    if "Name" not in tokens[1]:
                        continue
                elif "Name" not in lines[i]: # the next line 
                        continue

                cfg_name = None
                if len(tokens) > 2:
                    cfg_name = tokens[2]
                    cfg.valid = True
                elif len(lines[i+1].split()) > 0:
                    cfg_name = lines[i+1].split()[0]
                    cfg.valid = True
                    i = i+1
                elif len(lines[i+2].split()) > 0:
                    cfg_name = lines[i+2].split()[0]
                    cfg.valid = True
                    i = i+2

                if tokens[0] == "Parameter":
                    cfg.param_name = cfg_name
                elif tokens[0] == "Module":
                    cfg.modul_name = cfg_name
                elif tokens[0] == "Container":
                    cfg.cntnr_name = cfg_name


            # there is no point in parsig other parameter if we don't have the param_name captured
            if not cfg.valid:
                continue

            # name alone is valid for Modules
            if cfg.modul_name:
                continue

            # The string "Parent Container" may be split across 2 lines in PDF
            if "Parent" in line:
                if len(tokens) > 1:
                    if "Container" not in tokens[1]:
                        continue
                elif "Container" not in lines[i]: # the next line 
                        continue
            
                if len(tokens) > 2:
                    cfg.parent_ctnr = line.split()[2]
                elif len(lines[i+1].split()) > 0:
                    cfg.parent_ctnr = lines[i+1].split()[0]
                    i = i+1
                elif len(lines[i+2].split()) > 0:
                    cfg.parent_ctnr = lines[i+2].split()[0]
                    i = i+2

            # name and parent details are valid for Containers
            if cfg.cntnr_name:
                continue

            if "Type" in line:
                if len(tokens) > 2:
                    cfg.type = line.split()[2]
                elif len(lines[i+1].split()) > 0:
                    cfg.type = lines[i+1].split()[0]

            if "Multiplicity" in line:
                if len(tokens) > 2:
                    cfg.multiplicity = line.split()[2]
                elif len(lines[i+1].split()) > 0:
                    cfg.multiplicity = lines[i+1].split()[0]

        # End of current loop
    # Exit for loop
    if cfg:
        cfg_objs.append(cfg) # finally push the last obj
    
with open(csv_file, 'w') as f:
    title = ""
    for col in col_separator:
        title += col + ","
    print(title, file=f)
    for obj in cfg_objs:
        obj.print(f)