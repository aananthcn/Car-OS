#include <base_types.h>
#include <stdarg.h>
#include <stdio.h>

#include <osek.h>
#include <sg_appmodes.h>
#include <sg_counter.h>

#include <os_api.h>

#include <Mcu.h>


#include "rp2040.h"



/* Macros */
#define CLOCK_SEC2MSEC          (1000) /* 1000ms = 1 sec */

/* SysTick clk = External Clock = 12 MHz; let us not use 125MHz System clock for SysTick */
#define XOSC_MHz                (12)
#define CPU_CLK_MHz             (125)
#define PERI_CLK_MHz            (125)
#define MHz                     (1000000)


static u32 UartBase;


/* Functions */
int bsp_uart_init(u32 base) {
        u32 baud_divint, baud_divfrac;
        u32 baud_rate_div;

        /* Save the base to a global variable */
        UartBase = base;

        /* NammaAUTOSAR's standard baudrate = 115200, CLK_PERI = 125 MHz */
        baud_rate_div = ((PERI_CLK_MHz * MHz) << 3) / (115200);
        baud_divint = baud_rate_div >> (3+4);
        if (baud_divint == 0) {
                baud_divint = 1;
                baud_divfrac = 0;
        }
        else if (baud_divint >= 65535) {
                baud_divint = 65535;
                baud_divfrac = 0;
        }
        else {
                /* extract 6 bits from baud_divfrac */
                baud_divfrac = ((baud_rate_div & 0x7f) + 1) / 2;
        }

        /* Set computed baudrate values to registers */
        UART_IBRD(base) = baud_divint; //16 bits
        UART_FBRD(base) = baud_divfrac; //6 bits

        /* UART Data Format & configs */
        UART_LCR_H(base) = (0x3 << 5) /* 8-bit */ | (1 << 4) /* FEN */;

        /* Enable Tx, Rx and UART0 */
        UART_CR(base) = (1 << 9) | (1 << 8) | (1 << 0);

        return 0;
}


/* Serial console functions */
int console_fputc(const int c) {
        /* wait if UART0 is busy */
        while(UART_FR(UartBase) & (1<<3)) {
                /* do nothing */
        }

        UART_DR(UartBase) = (unsigned int) (c & 0xFF);

        return 0;
}


int console_fputs(const char *s) {
        int count = 0;

        while (*s != '\0') {
                console_fputc(*s);
                count++;
                s++;
        }

        return count;
}


/* Microcontroller Subsystem Reset - this function should be broken and
   distributed to the respective MCAL layer init function! */
int bsp_ss_reset(void) {
        RESET_CTRL = ~(
                SS_BIT_TIMER |
                SS_BIT_PLL_SYS |
                SS_BIT_PLL_USB |
                SS_BIT_PADS_QSPI |
                SS_BIT_IO_QSPI |
                SS_BIT_PADS_BANK0 |
                SS_BIT_IO_BANK0 |
                SS_BIT_JTAG |
                SS_BIT_UART1 |
                SS_BIT_SPI0
        );
        return 0;
}



int bsp_osc_init(void) {
        XOSC_CTRL    = XOSC_FREQ_RANGE_1_15MHz;
        XOSC_STARTUP = XOSC_DELAY((((XOSC_MHz * MHz) / CLOCK_SEC2MSEC) + 128) / 256);
        XOSC_CTRL   |= XOSC_ENABLE;
        /* wait till XOSC becomes stable */
        while (!(XOSC_STATUS & 0x80000000));
}



int bsp_config_clock(u32 reg_base, u8 clksrc, u8 auxsrc) {
        /* First reset the Clock src, else system may hang */
        *(volatile u32*)(reg_base + CLK_CTRL) &= ~(0x3);
        while(!((*(volatile u32*)(reg_base + CLK_SELECTED)) & (1)));

        /* Clock DIV register */
        *(volatile u32*)(reg_base + CLK_DIV) = (1 << 8);
        /* Clock CTRL register */
        *(volatile u32*)(reg_base + CLK_CTRL) = (auxsrc << 5) | (clksrc);
        /* Wait till the clock source bit in Clock SELECTED register is set */
        while(!((*(volatile u32*)(reg_base + CLK_SELECTED)) & (1 << clksrc)));

        return 0;
}


int bsp_clock_init(void) {
        u32 clksrc, auxsrc;

        /* CLK_REF: SRC = XOSC = 12 MHz, No AUXSRC */
        bsp_config_clock(CLK_REF_BASE, 2, 0);

        /* CLK_SYS: SRC = SYS_AUX, AUXSRC = PLL_SYS = 125 MHz */
        bsp_config_clock(CLK_SYS_BASE, 1, 0);

        /* CLK_PERI: AUXSRC = CLK_SYS = 125 MHz */
        CLK_PERI_CTRL = PERI_ENABLE | PERI_AUXSRC(0);

        /* CLK_USB: SRC = none, AUXSRC = PLL_USB = 48 MHz */
        bsp_config_clock(CLK_USB_BASE, 0, 0);

        /* CLK_ADC: SRC = none, AUXSRC = PLL_USB = 48 MHz */
        bsp_config_clock(CLK_ADC_BASE, 0, 0);

        /* CLK_RTC: SRC = none, AUXSRC = PLL_USB = 48 MHz */
        bsp_config_clock(CLK_RTC_BASE, 0, 0);

        return 0;
}



/*/               REFDIV   XOSC    REF   VCO       POSTDIV   SYS_PLL
    SYS PLL: 12 / 1    =   12MHz * 125 = 1500 MHz / 6 / 2  = 125 MHz
    USB PLL: 12 / 1    =   12MHz * 40  =  480 MHz / 5 / 2  =  48 MHz
/*/
int bsp_pll_init(u32 base, u32 vco_freq_mhz, u8 post_div1, u8 post_div2) {
        u32 vco_freq = (vco_freq_mhz * MHz); 
        u32 refdiv = 1;
        u32 fbdiv, ref_mhz;

        /* let us switch to ROSC clock before PLL power down */
        bsp_config_clock(CLK_SYS_BASE, 0, 2);
        bsp_config_clock(CLK_REF_BASE, 0, 0);

        /* power down PLL to configure it correctly */
        *((volatile u32*)(base+PLL_PWR_OFFSET)) = (1 << 5) | (1 << 3) | (1 << 2) | (1 << 0);

        /* do frequency checks */
        fbdiv = vco_freq / (XOSC_MHz * MHz);
        if ((fbdiv < 16) || (fbdiv >320)) {
                pr_log("Error: fbdiv out of range!\n");
                return -1;
        }
        if (post_div2 > post_div1) {
                pr_log("Error: post_div2 greater than post_div1\n");
                return -1;
        }
        ref_mhz = XOSC_MHz / refdiv;
        if (ref_mhz > (vco_freq / 16)) {
                pr_log("Error: reference freq greater than vco / 16\n");
                return -1;
        }

        /* configure the SYS PLL */
        *((volatile u32*)(base+PLL_FBDIV_INT_OFFSET)) = fbdiv;
        *((volatile u32*)(base+PLL_PWR_OFFSET)) &= ~((1 << 5) | (1 << 0)); /* clear VCOPD and PD bits */

        /* wait till PLL gets locked */
        while (!(*((volatile u32*)(base+PLL_CS_OFFSET)) & 0x80000000));

        /* configure post dividers */
        *((volatile u32*)(base+PLL_PRIM_OFFSET)) = post_div1 << 16 | post_div2 << 12;
        *((volatile u32*)(base+PLL_PWR_OFFSET)) &= ~(1 << 3); /* clear POSTDIVPD bit */

        return 0;
}


int bsp_setup_systimer(void) {
        register u32 tick_count = OS_TICK_DURATION_ns * CPU_CLK_MHz / CLOCK_SEC2MSEC;

        /* Setup SysTick clock source and enable interrupt */
        SYST_CVR = 0;
        SYST_RVR = tick_count & 0x00FFFFFF;
        SYST_CSR = (1 << 2) | (1 << 1) | (1 << 0); /* CLK SRC = Proc. Clk; TICKINT = ISR Trig.; ENABLE = 1 */

        /* Setup Watchdog timer TICK register to use TIMELR values */
        WDG_TICK = (1 << 9) /* ENABLE */ | 12 /* CYCLES = 12 for 12 MHz clock */;

        return 0;
}


int bsp_get_usec_syscount(u32 *ucount) {
        u32 count;

        *ucount = TIMELR; /* lower 32-bit of a 64-bit counter, incremented once per microsecond */

        return 0;
}


int bsp_sys_enable_interrupts() {
#if 0
        /* Enable interrupts */
        VIC_INTENABLE = 1 << ISR_SN_TIMER01;
#endif

        return 0;
}


int bsp_console_init(void) {
        bsp_uart_init(UART1_BASE);
        pr_log_init();

        return 0;
}


int bsp_mcu_startup(void) {
        bsp_ss_reset();
        bsp_osc_init();
        bsp_pll_init(PLL_SYS_BASE, 1500, 6, 2); /*SYS_VCO: min = 5 MHz, max = 1600 MHz */
        bsp_pll_init(PLL_USB_BASE, 480, 5, 2);
        bsp_clock_init();
        bsp_setup_systimer();
        bsp_console_init();
        bsp_sys_enable_interrupts();

        return 0;
}
