# 🗺 Memory Map

The memory map was designed to maximize contiguous RAM space and provide ample banking to work around the 64 KB addressing limitation imposed by the 16-bit address bus.

    $E000 - $FFFF:   Banked RAM (8K)
    $C000 - $DFFF:   Banked RAM (8K)
    $8000 - $BFFF:   Banked RAM (16K)
    $7800 - $7FFF:   Stack (2K)
    $2200 - $77FF:   Fixed RAM (21.5K)
    $2100 - $21FF:   DP Initial (256B)
    $2000 - $20FF:   MMIO (256B)
    $0000 - $1FFF:   Shadow RAM (8K)

There is 23.75 KB of contiguous fixed RAM from $2100 to $7FFF, with the highest 2K of that allocated for stack usage. This is supplemented by the banked regions that follow. The two 8 KB high banks are general purpose banks that the system does not tie to any particular IO device. As such, it may be a useful location to load sound data or other data for later usage. The 16 KB bank is also general purpose, a number of pages that will mapped into this region are utilized by the video card. As such, this is the CPU's window into modifying video RAM - sprite tables, pattern tables, color palettes, etc. At the moment, I've not decided how much RAM to physically install into any of these banked regions. However, if one byte is allocated for bank determination per bank, that allows 256 unique RAM pages to be mapped into each bank region. If enough RAM is installed to take full advantage of this, then the system will have on the order of 8 MB in additional banked RAM, in addition to the 23.75 KB of contiguous fixed RAM.

Specification of the active page in each bank will be done via an as-of-yet undetermined MMIO address. The MMIO region will be divided into 16 regions, each containing 16 addresses. As such, this forms a nice interface capable of supporting 16 unique IO devices, each containing 16 registers of their own. These IO ports will be utilized as such:

1. Programmable Interrupt Controller 1 (PIC)
2. Programmable Interrupt Controller 2
3. Memory Mapping Unit (MMU)
4. [UART](uart.md)
5. [SPI](spi.md)
6. [Video Card](video-card.md)
7. [Sound Card](sound-card.md) 1 
8. Sound Card 2
...

Note that these IO devices largely correspond to those mentioned in the [readme](../readme.md). The new comers are the PIC and the MMU. The PIC is responsible for coalescing interrupts from multiple sources into a single IRQ input for the CPU. It contains registers for specifying the addresses of unique ISRs for each interrupt source. When the CPU reads from its ISR Vector, the PIC is responsible for making the highest-priority, non-masked, active interrupt's ISR address available at the vector location. The MMU contains various registers used to configure the active page in each bankable location. One of this IO device's registers will be directly responsible for controlling the banking behavior described above.

Note that the Sound Card and the PIC each use 2 IO ports a piece - this is due to the number of expected registers each device will require. I've elected to keep the number of registers per IO port relatively small, as doing so allows for devices which do in fact only need a few registers to be integrated in a less wasteful manner.

Another useful feature of the reference computer's memory configuration is that the kernel ROM space is actually implemented as RAM, rather than a true read only memory. At system start up, an external sub circuit will hold the CPU at reset until its finished copying the contents of a ROM into a RAM chip, which then maps into the CPU's address space at runtime. This is useful, because if the programmer should elect to forgo any of the subroutines or data made available to them via the kernel, they can do so - this is an 8 KB region that is truly capable of being used for anything - its just the default and base case of this region is to be used as ROM-like location.

The initial location of the DP and the SP are specified by the state of Constant Generators internal to the CPU. These are configurable via DIP switches on the appropriate CG boards. However, both values can be modified at runtime, should the user decide to relocate the stack or direct page prior to starting the core of a program. Though there aren't direct LOAD opcodes for the SP, values can be moved into it via the index registers X and Y, or the dual accumulator E. Similarly, the DP register can not be loaded directly from memory, except via a POP opcode (there is also the corresponding PUSH opcode). DP has MOV opcodes associated with it for moving its value between the A register. Further, the stack's size is not hardware limited in any way - 2 KB is merely a suggestion made by the reference computer's memory map. So not only can the stack move, but it can be grown to fill the entire address space, if needed.