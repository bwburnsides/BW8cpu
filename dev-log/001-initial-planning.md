# 001 Initial Planning

**Note**: This document is not currently fully up to date with my plans. They have developed beyond what is described here.
A more full picture can be found [here](001-initial-planning2.md), though that document is also not up to snuff. Eventually
these documents will be merged here.

At the risk of getting ahead of myself, I've started to think about the concrete differences I'd like to see between my own build and the SAP-1, which is Ben Eater's initial build. Of course, there is a lot I don't know, so this list is likely not all-inclusive, and also might be ill-formed due to misconceptions of core ideas. However, here are the core components I expect to see in my build.

## Components

| Abbr | Name                          | Size   | Notes                                                      |
| ---- | ----------------------------- | ------ | ---------------------------------------------------------- |
| CLK  | Clock                         | --     | targeting 2 MHz                                            |
| BUS  | Data Bus                      | 8 bit  |                                                            |
| PC   | Program Counter               | 8 bit  | specifies lower 8 bits of next instruction address         |
| PR   | Page Register                 | 8 bit  | specifies upper 8 bits of next instruction address         |
| AR   | A Register                    | 8 bit  | ALU input                                                  |
| BR   | B Register                    | 8 bit  | ALU input                                                  |
| CR   | C Register                    | 8 bit  | ALU input                                                  |
| DR   | D Register                    | 8 bit  | ALU input                                                  |
| XR   | X Register                    | 8 bit  |                                                            |
| YR   | Y Register                    | 8 bit  |                                                            |
| ALU  | Arithmetic and Logic Unit     | 8 bit  | support Add/Sub/Mul/Div/AND/XOR                            |    
| FR   | Flags Register                | 8 bit  | contains ALU flags for conditional jumps, etc              |
| MARH | Memory Address Register, High | 8 bit  | upper 8 bits of memory address                             |
| MARL | Memory Address Register, Low  | 8 bit  | lower 8 bits of memory address                             |
| BR   | Memory Bank Register          | 8 bit  | allows specifying 255 external memory banks of 65K         |
| RAM  | Random Access Memory          | 32 KiB |                                                            |
| ROM  | Read-Only Memory              | 32 KiB |                                                            |
| IR   | Instruction Register          | 8 bit  | op-code to fetch/decode/execute                            |
| OR   | Operand Register              | 8 bit  | operand to op-code in IR                                   |
| IC   | Instruction Counter           | 4 bit  |                                                            |
| CL   | Control Logic                 | --     | EEPROMs for cobinatorial decoding of op-codes to microcode |

There will be other components, which are not listed here. These include interrupt handling hardware, and potentially additional hardware to support a CPU stack (though, this might just be a renaming of PC/PR). I don't know enough about the required hardware for this functionality to describe as of yet.

## Memory Map

The CPU will use 16 bit addressing via the 8 bit data bus. The upper 8 bits of the address will be specified via the Page Register, and the lower 8 bits of the address will be specified by the Program Counter. The CPU will have 65 KiB onboard to fill this address space. The upper half will be used by the ROM, which will contain the bootloader and other programs. The lower hald will be used by the RAM, which will contain the stack and be usable by running programs and peripherals (ie, it may be used as a frame buffer by a graphics card).

The memory will be subdivided into 256 pages of 256 bytes each. The page is specified by the PR, and programs can take advantage of this by ensuring that their instructions and data all fall within a single page, so that clock cycles do not need to be used during every instruction to move the PR into the MARH.

The stack will reside as the first RAM page.

The memory map looks like this:

| Addr  | Page | Note                                         |
| ----- | ---- | -------------------------------------------- |
| Start of ROM                                                |
| $0000 | $00  | Page $00 Begins                              |
| $0100 | $01  | Page $01 begins                              |
| ....  | .... |                                              |
| ....  | .... |                                              |
| ....  | .... |                                              |
| Start of RAM                                                |
| $8000 | $80  | RAM begins, Start of Stack (1 page)          |
| $8100 | $81  | Reserved for ISR 1 (1 page)                  |
| $8200 | $82  | Reserved for ISR 2 (1 page)                  |
| $8300 | $83  | Reserved for ISR 3 (1 page)                  |
| $FFFF | $FF  | End of addressable memory for Bank $00       | 

The CPU will also contain an 8 bit bank register, which may be used to refer to a 65 KiB bank of memory that may not be directly installed on the computer. This may be useful for peripherals which contain their own software. The bank register accomodates 256 possible banks of memory, which each may be 16 bit addressable via MAR H/L. In total, the system will accomodate 2<sup>16</sup> * 2<sup>8</sup> = 16 MiB of memory, 65 KiB of which are mapped as shown above, of course.

## Steps Forward

From here, I hope to finish building the SAP-1 digitally via Logisim. From there, I'd like to begin to implement basic support for the 65K of memory described above. After that, I may acquire the Ben Eater 8 bit Breadboard kit, and begin building. At some point after that, I will start to look at the hardware BOM I will need to implement my memory upgrades.

My current Logisim build contains the clock, bus, A and B registers, simplified ALU as designed in the SAP-1, an instruction register, and the beginnings of the initial 16 byte RAM system.

I do look forward to writing some Python for producing the Logisim ROM binaries which will be used in the control logic!