# 002 Memory Map Planning

Below is a memory map that I've come up with. I think it strikes a great balance between RAM, ROM, and memory-mapped IO for the purposes of this build. It is ordered from $0000 to $ffff

| Size |   Region   |
| ---- | ---------- |
|  8K  | Fixed ROM  |
|  8K  | Banked ROM |
|  8K  | Banked RAM |
| 39K  | Fixed RAM  |
|  1K  | IO         |

The majority of the address bus decoding will be done via the 3 MSBs, except for the last 8K block, which uses the next 3 MSBs as well, to partition it between Fixed RAM (7K) and IO decoding (1K):

| MSB          | Region         |
| ------------ | -------------- |
| 000          | Fixed ROM      |
| 001          | Banked ROM     |
| 010          | Banked RAM     |
| 011          | Fixed RAM      |
| 100          | Fixed RAM      |
| 101          | Fixed RAM      |
| 110          | Fixed RAM      |
| 111 not(111) | Fixed RAM      |
| 111 111      | IO             |

Each banked region will be managed by an 8 bit register in the IO portion of the memory map. However, only the 4 LSB will be used to select the bank, meaning that each banked region represents 8K x 16 = 128K of memory. This choice was map to reduce the amount of required hardware. I think for the purposes of this project, this provides plenty of memory. Perhaps when hardware design comes around, I will make my best effort to make supporting the full 8 bit register easy to do with a cartridge or expander card.

This brings the total memory count of the computer to:

ROM - 136K
RAM - 167K

A large portion of the Fixed RAM region will be used as a frame buffer for a VGA graphics card, which will be detailed in a new post later. Other citizens of the Fixed RAM region are the 256B stack, and the 256B keyboard buffer. The Fixed ROM region will maintain bootloaders and other kernel/OS-like code, as well as a key map to convert PS/2 scan codes to the system's internally supported character set (it will be an 8-bit extended ASCII variant). Finally, the IO space will have several citizens. These will require additional decoding logic to partion the 1K IO space into something shareable. Currently, I don't have a good handle on IO register requirements by peripheral. It can be expected that the graphics card will maintain at least 2 registers here, 2 registers will be used for RAM and ROM bank selection, and a sound card will maintain several registers. This leaves plenty of room for future peripherals that I haven't planned yet.
