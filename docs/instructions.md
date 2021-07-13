# Instructions

| Idx | Mnemonic | Name                                      | Operands | Notes                                                  |
| --- | -------- | ----------------------------------------- |--------- | ------------------------------------------------------ |
|   0 | NOP      | No Operation                              | --       | No-operation                                           |
| 196 | HLT      | Halt                                      | --       | Stops execution of the processor                       |
| 197 | BRK      | Halt until Interrupt                      | --       | Stops execution of the processor until an interrupt    |
| Load and Store                                                                                                             |||||
|   1 | LDA      | Load A                                    | 2        | Load the address's data to register A                  |
|   2 | LDB      | Load B                                    | 2        | Load the address's data to register B                  |
|   3 | LDC      | Load C                                    | 2        | Load the address's data to register C                  |
|   4 | LDD      | Load D                                    | 2        | Load the address's data to register D                  |
|   5 | LIA      | Load Immediate A                          | 1        | Load the value to register A                           |
|   6 | LIB      | Load Immediate B                          | 1        | Load the value to register B                           |
|   7 | LIC      | Load Immediate C                          | 1        | Load the value to register C                           |
|   8 | LID      | Load Immediate D                          | 1        | Load the value to register D                           |
|   9 | STA      | Store A                                   | 2        | Store register A to the address                        |
|  10 | STB      | Store B                                   | 2        | Store register B to the address                        |
|  11 | STC      | Store C                                   | 2        | Store register C to the address                        |
|  12 | STD      | Store D                                   | 2        | Store register D to the address                        |
| Branching and Jumping                                                                                                      |||||
|  13 | BEQ      | Branch if Equal                           | 2        | Branch to address if Z flag is set                     |
|  14 | BNQ      | Branch if Not Equal                       | 2        | Branch to address if Z flag is clear                   |
|  15 | BMI      | Branch if Minus                           | 2        | Branch to address if N flag is set                     |
|  16 | BPL      | Branch if Positive                        | 2        | Branch to address if N flag is clear                   |
|  17 | BCC      | Branch if Carry Clear                     | 2        | Branch to address if C flag is clear                   |
|  18 | BCS      | Branch if Carry Set                       | 2        | Branch to address if C flag is set                     |
|  19 | BVC      | Branch if Overflow Clear                  | 2        | Branch to address if V flag is clear                   |
|  20 | BVS      | Branch if Overflow Set                    | 2        | Branch to address if V flag is set                     |
|  21 | BLC      | Branch if Logical Carry Clear             | 2        | Branch to addrss if L flag is clear                    |
|  22 | BLS      | Branch if Logical Carry Set               | 2        | Branch to addrss if L flag is set                      |
|  23 | JMP      | Jump to address                           | 2        | Loads the PC with the address                          |
|  24 | JSR      | Jump to subroutine                        | 2        | Pushes PC to stack and jumps to address                |
|  25 | RTS      | Return from subroutine                    | --       | Pops PC from stack                                     |
|  26 | RTI      | Return from Interrupt                     | --       | Pops PC, CPU Status, and registers from stack          |
| Clear and Set Flags                                                                                                        |||||
|  27 | CLZ      | Clear Zero Flag                           | --       | Set the Z flag to 0                                    |
|  28 | CLC      | Clear Carry Flag                          | --       | Set the C flag to 0                                    |
|  29 | CLV      | Clear Overflow Flag                       | --       | Set the V flag to 0                                    |
|  30 | CLN      | Clear Negative Flag                       | --       | Set the N flag to 0                                    |
|  31 | CLL      | Clear Logical Carry Flag                  | --       | Set the L flag to 0                                    |
|  33 | CLI      | Clear Interrupt Inhibit                   | --       | Stops ignoring all interrupts                          |
| 191 | SEZ      | Set Zero Flag                             | --       |                                                        |
| 192 | SEC      | Set Carry Flag                            | --       |                                                        |
| 193 | SEV      | Set Overflow Flag                         | --       |                                                        |
| 194 | SEN      | Set Negative Flag                         | --       |                                                        |
| 195 | SEL      | Set Logical Carry Flag                    | --       |                                                        |
|  32 | SEI      | Set Interrupt Inhibit                     | --       | Ignores all interrupts until CLI                       |
| Stack Operations                                                                                                           |||||
|  34 | PHA      | Push A                                    | --       | Stores A to [SP] and increments SP                     |
|  35 | PHB      | Push B                                    | --       | Stores B to [SP] and increments SP                     |
|  36 | PHC      | Push C                                    | --       | Stores C to [SP] and increments SP                     |
|  37 | PHD      | Push D                                    | --       | Stores D to [SP] and increments SP                     |
|  38 | PHS      | Push Status                               | --       | Stores Status to [SP] and increments SP                |
|  39 | PHP      | Push Program Counter                      | --       | Stores Program Counter to [SP] and increments SP       |
|  40 | PHI      | Push Immediate                            | 1        | Pushes value to the stack                              |   
|  41 | PLA      | Pull A                                    | --       | Loads [SP] to A and decrements SP                      |
|  42 | PLB      | Pull B                                    | --       | Loads [SP] to B and decrements SP                      |
|  43 | PLC      | Pull C                                    | --       | Loads [SP] to C and decrements SP                      |
|  44 | PLD      | Pull D                                    | --       | Loads [SP] to D and decrements SP                      |
|  45 | PLS      | Pull Status                               | --       | Loads [SP] to Status and decrements SP                 |
|  46 | PLP      | Pull Program Counter                      | --       | Loads [SP] to Program Counter and decrements SP        |
| Adding                                                                                                                     |||||
|  47 | ADD AB   | Add Registers A and B                     | --       | Add the contents of Registers A and B                  |
|  48 | ADD AC   | Add Registers A and C                     | --       | Add the contents of Registers A and C                  |
|  49 | ADD AD   | Add Registers A and D                     | --       | Add the contents of Registers A and D                  |
|  50 | ADD BC   | Add Registers B and C                     | --       | Add the contents of Registers B and C                  |
|  51 | ADD BD   | Add Registers B and D                     | --       | Add the contents of Registers B and D                  |
|  52 | ADD CD   | Add Registers C and D                     | --       | Add the contents of Registers C and D                  |
|  53 | ADD A    | Add Immediate to Register A               | 1        | Add the value to Register A                            |
|  54 | ADD B    | Add Immediate to Register B               | 1        | Add the value to Register B                            |
|  55 | ADD C    | Add Immediate to Register C               | 1        | Add the value to Register C                            |
|  56 | ADD D    | Add Immediate to Register D               | 1        | Add the value to Register D                            |
| Adding with Carry                                                                                                          |||||
|  58 | ADC AB   | Add Registers A and B with Carry          | --       | Add the contents of Registers A and B with Carry       |
|  59 | ADC AC   | Add Registers A and C with Carry          | --       | Add the contents of Registers A and C with Carry       |
|  60 | ADC AD   | Add Registers A and D with Carry          | --       | Add the contents of Registers A and D with Carry       |
|  61 | ADC BC   | Add Registers B and C with Carry          | --       | Add the contents of Registers B and C with Carry       |
|  62 | ADC BD   | Add Registers B and D with Carry          | --       | Add the contents of Registers B and D with Carry       |
|  63 | ADC CD   | Add Registers C and D with Carry          | --       | Add the contents of Registers C and D with Carry       |
|  64 | ADC A    | Add Immediate to Register A with Carry    | 1        | Add the value to Register A                            |
|  65 | ADC B    | Add Immediate to Register B with Carry    | 1        | Add the value to Register B                            |
|  66 | ADC C    | Add Immediate to Register C with Carry    | 1        | Add the value to Register C                            |
|  67 | ADC D    | Add Immediate to Register D with Carry    | 1        | Add the value to Register D                            |
| Subtracting                                                                                                                |||||
|  68 | SUB AB   | Sub Registers A and B                     | --       | Subtract the contents of Registers A and B             |
|  69 | SUB AC   | Sub Registers A and C                     | --       | Subtract the contents of Registers A and C             |
|  70 | SUB AD   | Sub Registers A and D                     | --       | Subtract the contents of Registers A and D             |
|  71 | SUB BA   | Sub Registers B and A                     | --       | Subtract the contents of Registers B and A             |
|  72 | SUB BC   | Sub Registers B and C                     | --       | Subtract the contents of Registers B and C             |
|  73 | SUB BD   | Sub Registers B and D                     | --       | Subtract the contents of Registers B and D             |
|  74 | SUB CA   | Sub Registers C and A                     | --       | Subtract the contents of Registers C and A             |
|  75 | SUB CB   | Sub Registers C and B                     | --       | Subtract the contents of Registers C and B             |
|  76 | SUB CD   | Sub Registers C and D                     | --       | Subtract the contents of Registers C and D             |
|  77 | SUB DA   | Sub Registers D and A                     | --       | Subtract the contents of Registers D and A             |
|  78 | SUB DB   | Sub Registers D and B                     | --       | Subtract the contents of Registers D and B             |
|  79 | SUB DC   | Sub Registers D and C                     | --       | Subtract the contents of Registers D and C             |
|  80 | SUB A    | Sub Immediate from Register A             | 1        | Sub the value from Register A                          |
|  81 | SUB B    | Sub Immediate from Register B             | 1        | Sub the value from Register B                          |
|  82 | SUB C    | Sub Immediate from Register C             | 1        | Sub the value from Register C                          |
|  83 | SUB D    | Sub Immediate from Register D             | 1        | Sub the value from Register D                          |
|  84 | A SUB    | Sub Register A from Immediate             | 1        | Sub Register A from value                              |
|  85 | B SUB    | Sub Register B from Immediate             | 1        | Sub Register B from value                              |
|  86 | C SUB    | Sub Register C from Immediate             | 1        | Sub Register C from value                              |
|  87 | D SUB    | Sub Register D from Immediate             | 1        | Sub Register D from value                              |
| Subtracting with Borrow                                                                                                    |||||
|  88 | SBB AB   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  89 | SBB AC   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
|  90 | SBB AD   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  91 | SBB BA   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
|  92 | SBB BC   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  93 | SBB BD   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
|  94 | SBB CA   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  95 | SBB CB   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
|  96 | SBB CD   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  97 | SBB DA   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
|  98 | SBB DB   | Sub Registers B and D with Borrow         | --       | Subtract the contents of Registers B and D with Borrow |
|  99 | SBB DC   | Sub Registers C and D with Borrow         | --       | Subtract the contents of Registers C and D with Borrow |
| 100 | SBB A    | Sub Immediate from Register A with Borrow | 1        | Sub the value from Register A with Borrow              |
| 101 | SBB B    | Sub Immediate from Register B with Borrow | 1        | Sub the value from Register B with Borrow              |
| 102 | SBB C    | Sub Immediate from Register C with Borrow | 1        | Sub the value from Register C with Borrow              |
| 103 | SBB D    | Sub Immediate from Register D with Borrow | 1        | Sub the value from Register D with Borrow              |
| 104 | A SBB    | Sub Register A from Immediate with Borrow | 1        | Sub Register A from value with Borrow                  |
| 105 | B SBB    | Sub Register B from Immediate with Borrow | 1        | Sub Register B from value with Borrow                  |
| 106 | C SBB    | Sub Register C from Immediate with Borrow | 1        | Sub Register C from value with Borrow                  |
| 107 | D SBB    | Sub Register D from Immediate with Borrow | 1        | Sub Register D from value with Borrow                  |
| ANDing                                                                                                                     |||||
| 108 | AND AB   | AND Registers A and B                     | --       | AND the contents of Registers A and B with flags       |
| 109 | AND AC   | AND Registers A and C                     | --       | AND the contents of Registers A and C with flags       |
| 110 | AND AD   | AND Registers A and D                     | --       | AND the contents of Registers A and D with flags       |
| 111 | AND BC   | AND Registers B and C                     | --       | AND the contents of Registers B and C with flags       |
| 112 | AND BD   | AND Registers B and D                     | --       | AND the contents of Registers B and D with flags       |
| 113 | AND CD   | AND Registers C and D                     | --       | AND the contents of Registers C and D with flags       |
| 114 | AND A    | AND Immediate and Register A              | 1        | AND the value and Register A                           |
| 115 | AND B    | AND Immediate and Register B              | 1        | AND the value and Register B                           |
| 116 | AND C    | AND Immediate and Register C              | 1        | AND the value and Register C                           |
| 117 | AND D    | AND Immediate and Register D              | 1        | AND the value and Register D                           |
| ORing                                                                                                                      |||||
| 118 | OR AB    | OR Registers A and B                      | --       | OR the contents of Registers A and B with flags        |
| 119 | OR AC    | OR Registers A and C                      | --       | OR the contents of Registers A and C with flags        |
| 120 | OR AD    | OR Registers A and D                      | --       | OR the contents of Registers A and D with flags        |
| 121 | OR BC    | OR Registers B and C                      | --       | OR the contents of Registers B and C with flags        |
| 122 | OR BD    | OR Registers B and D                      | --       | OR the contents of Registers B and D with flags        |
| 123 | OR CD    | OR Registers C and D                      | --       | OR the contents of Registers C and D with flags        |
| 124 | OR A     | OR Immediate and Register A               | 1        | OR the value and Register A                            |
| 125 | OR B     | OR Immediate and Register B               | 1        | OR the value and Register B                            |
| 126 | OR C     | OR Immediate and Register C               | 1        | OR the value and Register C                            |
| 127 | OR D     | OR Immediate and Register D               | 1        | OR the value and Register D                            |
| XORing                                                                                                                     |||||
| 128 | XOR AB   | XOR Registers A and B                     | --       | XOR the contents of Registers A and B with flags       |
| 129 | XOR AC   | XOR Registers A and C                     | --       | XOR the contents of Registers A and C with flags       |
| 130 | XOR AD   | XOR Registers A and D                     | --       | XOR the contents of Registers A and D with flags       |
| 131 | XOR BC   | XOR Registers B and C                     | --       | XOR the contents of Registers B and C with flags       |
| 132 | XOR BD   | XOR Registers B and D                     | --       | XOR the contents of Registers B and D with flags       |
| 133 | XOR CD   | XOR Registers C and D                     | --       | XOR the contents of Registers C and D with flags       |
| 134 | XOR A    | XOR Immediate and Register A              | 1        | XOR the value and Register A                           |
| 135 | XOR B    | XOR Immediate and Register B              | 1        | XOR the value and Register B                           |
| 136 | XOR C    | XOR Immediate and Register C              | 1        | XOR the value and Register C                           |
| 137 | XOR D    | XOR Immediate and Register D              | 1        | XOR the value and Register D                           |
| NOTing                                                                                                                     |||||
| 138 | NOT A    | NOT Register A                            | --       | NOT the contents of Register A with flags              |
| 139 | NOT B    | NOT Register B                            | --       | NOT the contents of Register B with flags              |
| 140 | NOT C    | NOT Register C                            | --       | NOT the contents of Register C with flags              |
| 141 | NOT D    | NOT Register D                            | --       | NOT the contents of Register D with flags              |
| 142 | NOT I    | NOT Immediate                             | 1        | NOT the value                                          |
| LSLing                                                                                                                     |||||
| 143 | LSL A    | LSL Register A                            | --       | LSL the contents of Register A with flags              |
| 144 | LSL B    | LSL Register B                            | --       | LSL the contents of Register B with flags              |
| 145 | LSL C    | LSL Register C                            | --       | LSL the contents of Register C with flags              |
| 146 | LSL D    | LSL Register D                            | --       | LSL the contents of Register D with flags              |
| 147 | LSL I    | LSL Immediate                             | 1        | LSL the value                                          |
| LSRing                                                                                                                     |||||
| 148 | LSR A    | LSR Register A                            | --       | LSR the contents of Register A with flags              |
| 149 | LSR B    | LSR Register B                            | --       | LSR the contents of Register B with flags              |
| 150 | LSR C    | LSR Register C                            | --       | LSR the contents of Register C with flags              |
| 151 | LSR D    | LSR Register D                            | --       | LSR the contents of Register D with flags              |
| 152 | LSR I    | LSR Immediate                             | --       | LSR the value                                          |
| INCing                                                                                                                     |||||
| 153 | INC A    | INC Register A                            | --       | INC the contents of Register A with flags              |
| 154 | INC B    | INC Register B                            | --       | INC the contents of Register B with flags              |
| 155 | INC C    | INC Register C                            | --       | INC the contents of Register C with flags              |
| 156 | INC D    | INC Register D                            | --       | INC the contents of Register D with flags              |
| 157 | INC I    | INC Immediate                             | 1        | INC the value                                          |
| DECing                                                                                                                     |||||
| 158 | DEC A    | DEC Register A                            | --       | DEC the contents of Register A with flags              |
| 159 | DEC B    | DEC Register B                            | --       | DEC the contents of Register B with flags              |
| 160 | DEC C    | DEC Register C                            | --       | DEC the contents of Register C with flags              |
| 161 | DEC D    | DEC Register D                            | --       | DEC the contents of Register D with flags              |
| 162 | DEC I    | DEC Immediate                             | 1        | DEC the value                                          |
| Transfers                                                                                                                  |||||
| 163 | TAB      | Transfer Register A to B                  | --       |                                                        |
| 164 | TAC      | Transfer Register A to C                  | --       |                                                        |
| 165 | TAD      | Transfer Register A to D                  | --       |                                                        |
| 166 | TBA      | Transfer Register B to A                  | --       |                                                        |
| 167 | TBC      | Transfer Register B to C                  | --       |                                                        |
| 168 | TBD      | Transfer Register B to D                  | --       |                                                        |
| 169 | TCA      | Transfer Register C to A                  | --       |                                                        |
| 170 | TCB      | Transfer Register C to B                  | --       |                                                        |
| 171 | TCD      | Transfer Register C to D                  | --       |                                                        |
| 172 | TDA      | Transfer Register D to A                  | --       |                                                        |
| 173 | TDB      | Transfer Register D to B                  | --       |                                                        |
| 174 | TDC      | Transfer Register D to C                  | --       |                                                        |
| 175 | TEA      | Transfer Accumulator to Register A        | --       |                                                        |
| 176 | TEB      | Transfer Accumulator to Register B        | --       |                                                        |
| 177 | TEC      | Transfer Accumulator to Register C        | --       |                                                        |
| 178 | TED      | Transfer Accumulator to Register D        | --       |                                                        |
| 179 | TPH A    | Transfer PC High to Register A            | --       |                                                        |
| 180 | TPH B    | Transfer PC High to Register B            | --       |                                                        |
| 181 | TPH C    | Transfer PC High to Register C            | --       |                                                        |
| 182 | TPH D    | Transfer PC High to Register D            | --       |                                                        |
| 183 | TPL A    | Transfer PC Low to Register A             | --       |                                                        |
| 184 | TPL B    | Transfer PC Low to Register B             | --       |                                                        |
| 185 | TPL C    | Transfer PC Low to Register C             | --       |                                                        |
| 186 | TPL D    | Transfer PC Low to Register D             | --       |                                                        |
| 187 | TSA      | Transfer SP to Register A                 | --       |                                                        |
| 188 | TSB      | Transfer SP to Register B                 | --       |                                                        |
| 189 | TSC      | Transfer SP to Register C                 | --       |                                                        |
| 190 | TSD      | Transfer SP to Register D                 | --       |                                                        |
