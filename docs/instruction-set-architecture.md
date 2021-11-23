# 🔧 ISA

The instruction set architecture is largely focused on ease of use, rather than performance. In some cases, having a specific address mode and instruction combination does increase performance. However, the hardware concessions that were made to enable an instruction set larger than 256 opcodes in size has introduced a small performance hit to approximately 2/3 of the entire instruction space. Efforts have been made to prioritize the most-commonly used opcodes in the 1/3 instruction space which is not affected by these concessions.

An accumulator-based micro architecture was adopted in order to alleviate instruction space concerns. As such, the A, B, or combined E accumulator acts as the destination register for most ALU-based instructions. Because the destination register is implied by the left-hand operand, the accumulator is also an operand for most ALU-based instructions.

There are a total of approximately 50 user-facing instructions, which are implemented via approximately 670 opcodes, which vary the operands and addressing mode of the core instructions.

| Mnemonic | Description |
| --- | --- |
| NOP | No operation |
| BRK | Break |
| WAI | Wait for Interrupt |
| CLC | Clear Carry |
| CLI | Enable Interrupts |
| CLV | Clear Overflow |
| SEC | Set Carry |
| SEI | Disable Interrupts |
| MOV | Move register |
| LOAD | Load register |
| STORE | Store register |
| INC | Increment |
| DEC | Decrement |
| ADD | Add |
| ADC | Add with carry |
| SUB | Subtract |
| SBB | Subtract with borrow |
| AND | Logical AND |
| OR | Logical OR |
| XOR | Logical XOR |
| NOT | Logical NOT |
| NEG | 2s Complement Negation |
| ASR | Arithmetic Shift Right |
| SHR | Logical Shift Right |
| SRC | Logical Shift Right with carry |
| SHL | Logical Shift Left |
| SLC | Logical Shift Left with carry |
| CMP | Compare |
| TST | Test |
| PUSH | Stack Push |
| POP | Stack Pop |
| JMP | Jump |
| JSR | Jump to subroutine |
| RTS | Return from subroutine |
| RTI | Return from interrupt |
| JO | Jump if overflow |
| JNO | Jump if not overflow |
| JN | Jump if negative |
| JP | Jump if positive |
| JZ | Jump if zero |
| JNZ | Jump if not zero |
| JC | Jump if carry |
| JNC | Jump if not carry |
| JA | Jump if above |
| JNA | Jump if not above |
| JL | Jump if less |
| JGE | Jump if greater or equal |
| JG | Jump if greater |
| JLE | Jump if less or equal |

# Addressing Modes