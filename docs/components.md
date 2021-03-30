# Components and Control Words

| Abbr | Name                          | Size   | Notes                                                           |
| ---- | ----------------------------- | ------ | --------------------------------------------------------------- |
| CLK  | Clock                         | --     | targeting 1 MHz                                                 |
| DBUS | Data Bus                      | 8 b    |                                                                 |
| MBUS | Memory Address Bus            | 16 b   |                                                                 |
| PC   | Program Counter               | 16 b   | specifies lower 8 bits of next instruction address              |
| AR   | A Register                    | 8 b    | ALU input                                                       |
| BR   | B Register                    | 8 b    | ALU input                                                       |
| CR   | C Register                    | 8 b    | ALU input                                                       |
| DR   | D Register                    | 8 b    | ALU input                                                       |
| XR   | X Register                    | 8 b    |                                                                 |
| YR   | Y Register                    | 8 b    |                                                                 |
| SP   | Stack Pointer                 | 8 b    | 8 bit up/down counter of next available mem address<sup>*</sup> |
| ALU  | Arithmetic and Logic Unit     | 8 b    | support Add/Sub/Mul/Div/AND/XOR                                 |    
| FR   | Flags Register                | 4 b    | contains ALU flags for conditional jumps, etc                   |
| MAR  | Memory Address Register       | 16 b   | memory address being targetted in mem map                       |
| MBR  | Memory Bank Register          | 8 b    | allows specifying 255 external memory banks of 65K              |
| RAM  | Random Access Memory          | 32 KiB |                                                                 |
| ROM  | Read-Only Memory              | 32 KiB |                                                                 |
| IR   | Instruction Register          | 8 b    | op-code to fetch/decode/execute                                 |
| OR   | Operand Register              | 16 b   | operand to op-code in IR                                        |
| IC   | Instruction Counter           | 4 b    |                                                                 |
| CL   | Control Logic                 | --     | EEPROMs for cobinatorial decoding of op-codes to microcode      |

<sup>*</sup> Contains only lower byte of address, because its relative to the RAM stack, which is the first RAM
page from $8000 to $80FF.

# Control Flags

| Num | Abbr | Name                       | Component | Notes                       |
| --- | ---- | -------------------------- | --------- | --------------------------- |
| 1   | HLT  | Halt                       | --        | Stop the CPU Clock          |
| 2   | PCO  | Program Counter Out        | PC        | Contents of PC to MBUS      |
| 3   | PCE  | Program Counter Enable     | PC        | Increment PC value          |
| 4   | PCJ  | Program Counter Jump       | PC        | Contents of MBUS to PC      |
| 5   | AO   | A Register Out             | AR        | Contents of AR to DBUS      |
| 6   | AI   | A Register In              | AR        | Contents of DBUS to AR      |
| 7   | BO   | B Register Out             | BR        | Contents of BR to DBUS      |
| 8   | BI   | B Register In              | BR        | Contents of DBUS to BR      |
| 9   | CO   | C Register Out             | CR        | Contents of CR to DBUS      |
| 10  | CI   | C Register In              | CR        | Contents of DBUS to CR      |
| 11  | DO   | D Register Out             | DR        | Contents of DR to DBUS      |
| 12  | DI   | D Register In              | DR        | Contents of DBUS to DR      |
| 13  | XO   | X Register Out             | XR        | Contents of XR to DBUS      |
| 14  | XI   | X Register In              | XR        | Contents of DBUS to XR      |
| 15  | YO   | Y Register Out             | YR        | Contents of YR to DBUS      |
| 16  | YI   | Y Register In              | YR        | Contents of DBUS to YR      |
| 17  | SI   | Stack Pointer Increment    | SP        | Increment SP                |
| 18  | SD   | Stack Pointer Decrement    | SP        | Decrement SP                |
| 19  | EO   | Sum Out                    | ALU       | Contents of ALU to DBUS     |
| 20  | SU   | Subtract                   | ALU       | Convert BR to 2s Complement |
| 21  | MI   | Memory Address Register In | MAR       | Contents of MBUS to MAR     |
| 22  | MBO  | Memory Bank Register Out   | MBR       | Contents of MBR to DBUS     |
| 23  | RI   | ROM/RAM In                 | RAM/ROM   | Contents of DBUS to RAM/ROM |
| 24  | RO   | ROM/RAM Out                | RAM/ROM   | Contents of RAM/ROM to DBUS |
| 25  | IO   | Instruction Register Out   | IR        | Contents of IR to DBUS      |
| 26  | II   | Instruction Register In    | IR        | Contents of DBUS to IR      |
| 27  | OO   | Operand Register Out       | OR        | Contents of OR to MBUS      |
| 28  | OI   | Operand Register In        | OR        | Contents of MBUS to OR      |
| 29  | ICR  | Instruction Counter Reset  | IC        | Reset IC to 0               |

## Control Logic Output Line Considerations

These controls flags will be modified via a set of microcode EEPROMs, which have 11 address pins and 8 output pins.
If the control lines are implemented in a directly one-hot manner as described in this table, then 4 EEPROMs will be
needed in order to have enough output lines.

However, many of these control words are mutually exclusive. The most apparent
example of this are all control words that correspond to outputting on DBUS, as only one component can use the bus at a time. The same goes for any control words that correspond to outputting on MBUS, for the same reason. In the case of DBUS, there are 10 control words, and 10 unique states can be represented in binary with 4 bits, meaning 6 bits are saved. A decoder will be needed
to break the values back out into their "one-hot" style to be sent to each control word. With 4 bits, 16 states can be represented, meaning that 5 more control words that represent a DBUS output can be added without requiring an extra EEPROM output line. The final 6th state can be used to represent a none state, where none of 10 control lines are active.

In the case of MBUS, there are 2 lines. There is currently no benefit from utilizing this technique with the control words described here. As the computer evolves, this may change.

This can potentially be applied to additional control word groups once the op-codes have been specified, and the control words can be directly analyzed for more combinations that never occur simulataneously.

At the moment, the op-codes haven't been developed. It currently looks like I will need 23 control word lines, which requires 3 EEPROMs.

## Control Logic Input Line Considerations

The microcode retrieved from the control logic EEPROMs depend on three things:

1. The op-code being executed
2. The instruction step of the op-code being executed
3. The state of an ALU flags

Because the EEPROMs have 11 address lines, this information needs to be stored in 11 bits. In the original Eater build, op-codes are represented as 4 bits, the instruction step is represented in 3 bits, and the flags are represented in 2 bits.

In my build, the instruction register is 8 bits, leaving only 3 to encode the instruction step, and the state of the flag register. This is not feasible, but wait it gets worse. Whereas the SAP-1 needs 3 bits to encode the instruction step, I intend to
implement CALL and RET op-codes, which I anticipate to take 18 instruction steps, according to Rolf Electronics. So, now I need 5 bits to encode the instruction step. Additionally, I have a 4 bit flag register. In total, that is 18 bits, far more than the 11 limitation.

This is not a show stopper, though some strict scrutiny will need to be applied. Here are some considerations that will alleviate this issue:

1. 8 bits for the op-code allow for 256 instructions, far more than needed. 6 bits give 64 instructions, which may be enough for my purposes, and will permanently reduce our input width by 2 bits. However, this is not very future proof. 7 bits would be more comfortable, but that only reduces our width by 1 bit.

2. Many instructions will not need knowledge of the flags, so for some cases, that reduces the input width by 5 bits. Hardware will need to be developed to optionally block flag inputs and move up/down the step input.

3. Many instructions will not take 18 steps, so 1-2 bits may be saved via a reduction of the timing bits sent in.

This will need to be revisited down the road, potentially after op-codes have been developed.