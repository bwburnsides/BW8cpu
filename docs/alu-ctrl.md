# 🧮 ALU Control Design

The ALU supports many operations, and various operations should allow specific flags to be set, while disallowing other flags from being set. For example, any unary operation should not allow the carry or overflow flags to be set, as those flags only have meaning in binary operations. (Here the terms binary and unary refer only to the number of operands that an operation has)

Further, the ALU must allow for a flag to be explicitly set or cleared, overriding any other computed flag state. This is useful in cases where the SEC or CLC (set / clear carry) instructions are used, for example. Finally, the ALU must allow for all flags to be simultaneously set to the value of the RHS operand. This is used when the status register is restored from the stack.

So for each clock cycle, a flag’s new value can be any of the following:

0. Old value
1. Computed value
2. Forced to 0
3. Forced to 1
4. RHS operand

Because this is 5 values, the true flag value can be selected via an 8:1 multiplexer, where 3 control bits are used to select which potential value should be stored in the status register.

These three bits can come directly from the ALU's control unit. At 5 flags and 3 bits per, the control unit must produce at most 15 lines just to cover flag determination. However, many of these control lines can be shared as certain groups of ALU instructions will require the same type of update to certain flags. To visualize this, I produced a table showing the desired result for each flag and instruction combination.

| ALU OP | C | Z | V | N | I |
| ------ | - | - | - | - | - |
| NOP    | 0 | 0 | 0 | 0 | 0 |    
| ZERO   | 0 | 0 | 0 | 0 | 0 |    
| LHS    | 0 | 0 | 0 | 0 | 0 |    
| RHS    | 0 | 0 | 0 | 0 | 0 |    
| LHS C  | 0 | 0 | 0 | 0 | 0 |    
| RHS C  | 0 | 0 | 0 | 0 | 0 |    
| ADD    | 1 | 1 |   |   | 0 |    
| ADC    | 1 | 1 |   |   | 0 |    
| SUB    | 1 | 1 |   |   | 0 |    
| SBB    | 1 | 1 |   |   | 0 |    
| NEG    | 0 | 1 |   |   | 0 |    
| INC    | 1 | 1 |   |   | 0 |    
| DEC    | 1 | 1 |   |   | 0 |    
| AND    |   | 1 |   |   | 0 |    
| OR     |   | 1 |   |   | 0 |    
| XOR    |   | 1 |   |   | 0 |    
| NOT    |   | 1 |   |   | 0 |    
| LSR    |   | 1 |   |   | 0 |    
| LRC    |   | 1 |   |   | 0 |    
| ASR    |   | 1 |   |   | 0 |    
| SEI    | 0 | 0 | 0 | 0 | 3 |    
| CLI    | 0 | 0 | 0 | 0 | 2 |    
| SEC    | 3 | 0 | 0 | 0 | 0 |    
| CLC    | 2 | 0 | 0 | 0 | 0 |    
| SEV    | 0 | 0 | 3 | 0 | 0 |    
| CLV    | 0 | 0 | 2 | 0 | 0 |    
| SEZ    | 0 | 3 | 0 | 0 | 0 |    
| CLZ    | 0 | 2 | 0 | 0 | 0 |    
| SEN    | 0 | 0 | 0 | 3 | 0 |    
| CLN    | 0 | 0 | 0 | 2 | 0 |    
| SSR    | 4 | 4 | 4 | 4 | 4 |    