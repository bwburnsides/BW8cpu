# 🧮 ALU

The arithmetic and logic unit is divided into 5 sections:

1. Instruction Decoder Unit
2. Flag Determination Unit
3. Arithmetic Unit
4. Logic Unit
5. Shift Unit

The ALU is controlled via the Control Unit's 5-bit ALU-op field on the 32-bit Control Bus. The IDU is responsible for decoding this 5-bit field into all the control signals needed by the ALU. The IDU is implemented via a diode matrix, and the 5-bit ALU-op allows for up to 32 unique instructions to be performed by the ALU. However, the IDU implements only 30 of them, and even fewer are used by the reference ISA. The operations are presented below - you will see a strong similarity between these operations and the instructions that exist in the ISA.

| Operation | Description |
| --- | --- |
| NOP | No operation |
| ADD | Add |
| ADC | Add with carry |
| SUB | Subtract |
| SBB | Subtract with borrow |
| AND | Logical AND |
| OR | Logical OR |
| XOR | Logical XOR |
| NOT | Logical NOT |
| NEG | Two's complement negation |
| LSR | Logical right shift |
| LRC | Logical right shift with carry |
| ASR | Arithmetic right shift |
| INC | Increment |
| DEC | Decrement |
| SEI | Set I |
| CLI | Clear I |
| SEC | Set C |
| CLC | Clear C |
| SEV | Set V |
| CLV | Clear V |
| SEZ | Set Z |
| CLZ | Clear Z |
| SEN | Set N |
| CLN | Clear N |
| LHS | LHS to result |
| RHS | RHS to result |
| LHS_C | LHS with carry to result |
| RHS_C | RHS with carry to result |
| ZERO | Zero to result |