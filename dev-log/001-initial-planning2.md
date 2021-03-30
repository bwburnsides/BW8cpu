# Initial Planning

Here is a summary of the specifications I hope to support:

- 32 KB onboard RAM for program and data use
- 32 KB onboard RAM for system bootloader and programs
- 4 8 bit GPRs (A, B, C, D)
- 2 16 bit ARs (X, Y)
- 4 8 bit transfer registers (T1, T2)
- Hardware stack pointer
- Memory banking to support up to 255 additional banks of 65K memory (up to 16.7M total)

Below is a description of the components I currently expect to build, and their control signals.

| Abbr      | Name                            | Size   | CF Abbr                                | Control Flags                      | Notes                                                      |
| -------   | ------------------------------- | ------ | -------------------------------------- | ---------------------------------- | ---------------------------------------------------------- |
| CLK       | Clock                           | --     | HLT                                    |                                    | targeting 1-3 MHz                                          |
| DBUS      | Data Bus                        | 8 bit  | --                                     |                                    |                                                            |
| MBUS      | Memory Address Bus              | 16 bit | --                                     |                                    |                                                            |
| PC        | Program Counter                 | 8 bit  | CE, J, CO                              | Counter Enable, Jump, Counter Out  | specifies lower 8 bits of next instruction address         |
| PR        | Page Register                   | 8 bit  | PRO, PRI                               | Register Out/In                    | specifies upper 8 bits of next instruction address         |
| AR        | A Register                      | 8 bit  | ARO, ARI                               | Register Out/In                    | GPR/ALU input                                              |
| BR        | B Register                      | 8 bit  | BRO, BRI                               | Register Out/In                    | GPR/ALU input                                              |
| CR        | C Register                      | 8 bit  | CRO, CRI                               | Register Out/In                    | GPR/ALU input                                              |
| DR        | D Register                      | 8 bit  | DRO, DRI                               | Register Out/In                    | GPR/ALU input                                              |
| XR        | X Register                      | 16 bit | XRO, XRI                               | Register Out/In                    |                                                            |
| YR        | Y Register                      | 16 bit | YRO, YRI                               | Register Out/In                    |                                                            |
| TR1       | Transfer Register 1             | 16 bit | TR1I, TR1O, TR1LI, TR1LO, TR1HI, TR1HO | TR1 In/Out, TR1 Low/High In/Out    |                                                            |
| TR2       | Transfer Register 2             | 16 bit | TR2I, TR2O, TR2LI, TR2LO, TR2HI, TR2HO | TR2 In/Out, TR2 Low/High In/Out    |                                                            |
| ALU       | Arithmetic and Logic Unit       | 8 bit  | EO, SU, XOR, AND                       | ALU Out, Subtract, Logical XOR/AND | support Add/Sub/Mul/Div/AND/XOR                            |
| FR        | Flags Register                  | 8 bit  | FO                                     | Flags Out                          | contains ALU flags for conditional jumps, etc              |
| MAR       | Memory Address Register         | 16 bit | MI                                     | MAR In                             | upper 8 bits of memory address                             |
| BR        | Memory Bank Register            | 8 bit  | BRI                                    | BR In                              | allows specifying 255 external memory banks of 65K         |
| RAM/ROM   | Random Access/ Read Only Memory | 32 KB  | RI, RO                                 | RAM/ROM In/Out                     |                                                            |
| IR        | Instruction Register            | 8 bit  | IO, II                                 | IR Out/In                          | op-code to fetch/decode/execute                            |
| SQ        | Sequencer                       | 4 bit  | --                                     |                                    |                                                            |
| ID        | Instruction Decoder             | --     | --                                     |                                    | EEPROMs for cobinatorial decoding of op-codes to microcode |
| Total: 23 |                                 |        | Total: 41                              |                                    |                                                            |

## Instruction Decoding

I plan to use 2KB EEPROMs, which have 11 address lines and and 8 data lines, where the address lines serve as inputs and the data lines serve as outputs to some large combinatorial circuit. Because there are 41 control lines, an initial estimate is that 6 EEPROMs will need to be programmed and wired in series to the instruction decoder input. However, as EEPROMS are space and money expensive, some attempts to decrease this value will be made. Because these are discrete control lines, they represent "one-hot" encoded values. This is beneficial, because it means the output of the decoder can be directly used to manage the system control lines. However, at the expense of some additional decoding hardware, some of these control lines can be compacted significantly. One such example of a place where this can be done is with the control lines representing data bus output, as there is no case where multiple componenets will need to output on the data bus in the same instruction cycle. Here are the control signals belonging to this group:

- PRO
- CO
- ARO
- BRO
- CRO
- DRO
- TR1LO
- TR1HO
- TR2LO
- TR2HO
- EO
- FO
- RO
- IO
Total: 14

15 values can be represented in binary with 4 bits, where the 15th value represents "all off." This saves 10 output lines, with space for one additional signal.

A similar technique can be used for address bus-outputting flags:

- XRO
- YRO
- TR1O
- TR2O
Total: 4

5 values can be represented in binary with 3 bits, where again the 5th value represents "all off." The saves 1 output lines, with space for one additional signal. Other additional patterns are not immediately visible to me. However, after the instruction set and its corresponding microinstruction steps are developed, other mutually exclusive groups of signals can be found. Anyways, with these two reductions alone, 11 data lines are saved, meaning only 30 EEPROM data lines are needed. 4 EEPROMs are needed for this scheme, which saves a significant amount of money and space.

The bigger issue to resolve is that of the address lines. The op-code, operand, and flags all need to be encoded in 11 bits. Each of these are 8 bit values, so natively we'd need 24 address lines. There are no EEPROMs available with this number of input lines.