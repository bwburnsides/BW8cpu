# 🚥 CU

The CPU is orchestrated by the Control Unit, which takes in 19 bits of state input, and translates them to a 32 bit micro-instruction every clock cycle. Those 19 bits of state input are as follows

- 3 bits - Tstate
- 8 bits - opcode
- 5 bits - flags
- 1 bit - IRQ
- 2 bits - mode select

The 3 bits of Tstate allow an instruction to take up to 8 clock cycles. However, most instructions take less than that. Instruction with complex indexed addressing modes or things like subroutine jumps tend to take more clocks. Simple loads, stores, 8-bit ALU operations, and register moves are much quicker.

The 2 bits of mode select allow for 4 CPU modes to exist:

1. Normal
2. Extended 1
3. Extended 2
4. Reset

The CPU will be in reset mode at power-up. This mode ignores the current opcode value and instead orchestrates a series of micro-instructions that are responsible for setting up the initial Direct Page (DP) register value, the initial Stack Pointer (SP) value, clearing the registers, and reading the Reset Vector (RSTv). At the conclusion of this sequence, it exits reset mode. The remaining 3 CPU modes each contain up to 256 valid opcodes that the CU is capable of executing. Its here where the 768 opcode upper limit comes from.