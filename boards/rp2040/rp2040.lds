/*
 * Author: Aananth C N
 * Date: 21 Nov 2021
 */

INCLUDE tools/os_builder/src/sg_stack.lds

/* Flash Memory: 2 MB */
/*/
    BOOT_STG2     = 0x10000000;
    ROM_START    = 0x10000100;
    ROM_SIZE     = 0x00200000;
/*/

/* RAM Memory: 256kB + 4kB + 4kB = 264kB */
/*/
    RAM_START    = 0x20000000;
    RAM_SIZE     = 0x00042000;
/*/

MEMORY
{
    FLASH(rx)       : ORIGIN = 0x10000000, LENGTH = 2048k
    RAM(rwx)        : ORIGIN = 0x20000000, LENGTH = 264k
}


ENTRY(StartOS)
SECTIONS
{
    .text : {
        _vectors_start = .;
        KEEP (*(.vectors))
        _vectors_end = .;
        . = ALIGN(4);
        *(.text)
        . = ALIGN(4);
        *(.rodata)
    } > FLASH

    /*
     * Arm stack unwinding.
     * If removed may cause random crashes.
     */
    .ARM.extab :
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > FLASH
    
    __exidx_start = .;
    .ARM.exidx :
    {
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
    } > FLASH
    __exidx_end = .;

    _init_data_rom = .;

    .ram_vector_table (COPY): {
        *(.ram_vector_table)
    } > RAM

    /* INITIALIZED DATA SEGMENT(s) */
    .data : AT (_init_data_rom)
    { 
        _data_start = .;
        *(.data) 
        _data_end = .;
    } > RAM 
    _data_size = _data_end - _data_start;

    /* UNINITIALIZED DATA SEGMENT(s) */
    .bss : 
    { 
        _bss_start = .;
        *(.bss COMMON)
        _bss_end = .;
    } > RAM
    _bss_size = _bss_end - _bss_start;

    . = ALIGN(8);
}
