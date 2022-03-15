# BW8 Instruction Set Architecture Specification

The BW8cpu instruction set contains the following instructions. Each instruction has several opcodes that implement various combinations of operands and addressing mode variations on their base behavior. These will be discussed below.

Mnemonic   | Name                           | Opcode Count
---------- | ------------------------------ | ------------
`NOP`      | No Operation                   | 1
`BRK`      | Break Clock                    | 1
`EXT`      | Extended Mode                  | 1
`CLC`      | Clear Carry                    | 1
`CLI`      | Enable Interrupts              | 1
`CLV`      | Clear Overflow                 | 1
`SEC`      | Set Carry                      | 1
`SEI`      | Disable Interrupts             | 1
`MOV`      | Move Register                  | 22
`LOAD`     | Load Register                  | 84
`STORE`    | Store Register                 | 78
`LEA`      | Load Effective Address         | 24
`ADC`      | Add with Carry                 | 30
`SBB`      | Subtract with Borrow           | 26
`AND`      | Bitwise AND                    | 30
`OR`       | Bitwise OR                     | 26
`XOR`      | Bitwise XOR                    | 30
`NOT`      | Bitwise NOT                    | 5
`NEG`      | 2s Complement Negation         | 5
`LSR`      | Logical Shift Right            | 5
`LRC`      | Logical Shift Right with Carry | 5
`ASR`      | Arithmetic Shift Right         | 5
`INC`      | Increment                      | 7
`DEC`      | Decrement                      | 7
`PUSH`     | Push to Stack                  | 7
`POP`      | Pop from Stack                 | 7
`CMP`      | Compare                        | 25
`TST`      | Bit Test                       | 5
`WAI`      | Wait for Interrupt             | 1
`SWI`      | Software Interrupt             | 2
`RTI`      | Return from Interrupt          | 1
`JSR`      | Jump to Subroutine             | 4
`RTS`      | Return from Subroutine         | 1
`JMP`      | Jump                           | 4
`JO`       | Jump if Overflow               | 4
`JNO`      | Jump if not Overflow           | 4
`JS`       | Jump if Sign                   | 4
`JNS`      | Jump if not Sign               | 4
`JE`       | Jump if Equal                  | 4
`JNE`      | Jump if not Equal              | 4
`JC`       | Jump if Carry                  | 4
`JNC`      | Jump if not Carry              | 4
`JBE`      | Jump if Below or Equal         | 4
`JA`       | Jump if Above                  | 4
`JL`       | Jump if Less                   | 4
`JGE`      | Jump if Greater or Equal       | 4
`JLE`      | Jump if Less or Equal          | 4
`JG`       | Jump if Greater                | 4

The BW8 has an 8-bit Instruction Register, so there is some trickery involved to support up to 512 opcodes, rather than just 256. This is done with the `EXT` instruction. This is a 1 byte, 2 cycle instruction which transitions the CPU from normal "`NRM`" mode to extended "`EXT`" mode, and then fetches the next instruction. This next instruction is interpretted differently due to the system being in `EXT` Mode. At the conclusion of these instructions, they return the CPU to `NRM` Mode.

The `NRM` Mode instructions are those which are commonly used, have long cycle counts, or have larger operand counts. The idea is to limit the cycle penalty incurred by `EXT` Mode opcodes to those which already execute quickly, or are not commonly used. In addition, by making sure that large operand count instructions exist in NRM Mode, we limit the maximum instruction size to 3 bytes, thereby keeping the program size penalty down.

# Programming Model

The CPU programming model includes four 8-bit General Purpose Registers (GPRs): `a`, `b`, `c`, `d`, and two 16-bit General Purpose Pointers (GPPs): `x`, `y`. There are three special purpose programmer facing registers:

1. `dp` - 8-bit, the location of the Direct Page
2. `e` - 16-bit, a pointer constructed with `a` in the high byte and `b` in the low byte
3. `sp` - 16-bit, the system Stack Pointer

These three registers have limited direct support, and are generally interacted with via `MOV`s. The `e` register provides a mechanism for constructing 16-bit results that can be loaded into the GPPs or the SP. Additionally, there is the Status Register (SR)which stores the following CPU flags:

1. Zero (`Z`)
2. Carry (`C`)
3. Negative (`N`)
4. Overflow (`V`)
5. Interrupt Inhibit (`I`)

The first four of these are primarily set by the result of a recent ALU calculation. The final is used to enable or disable maskable interrupt requests (IRQ), and is managed directly by the user via `SEI` and `CLI`.

# Addressing Modes

- *Inherent*: There is no relevant operand source, or the source is implied directly by the mnemonic.

- *Immediate*: The operand source is the instruction stream; the operand appears as the byte following the opcode if the destination is 8-bits wide, or the two bytes following the opcode if the destination is 16-bits wide.

- *Absolute*: The operand source is given in the instruction stream. The opcode is followed by two bytes which gives an absolute address that is the operand source.

- *Direct Page*: The operand source is given in the instruction stream. The opcode is followed by one byte which gives a direct page address that is the operand source.

- *Indirect*: The operand source is specified in a pointer register. The pointer register is implied in the opcode.

- *Indexed Indirect*: The operand source is specified by the address that is computed by adding a signed 8-bit index to a pointer register's value. Both the pointer register and the index source are implied in the opcode.

- *Relative*: The operand source is specified by the address that is computed by adding a signed 8-bit offset to the Program Counter's value. The offset's source is byte immediately after the opcode in the instruction stream.

# Instruction Details

## `NOP` - No Operation

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

Does nothing, and then continues.

## `BRK` - Break Clock

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | 4
Mode   | Inherent

The clock module which provides the CPU's clock input has three modes: Run, Demo, and Step. The final of which single steps the CPU. This opcode forces the clock mode into Step, and so it acts similarly to a `HLT` instruction.

## `EXT` - Extended Mode

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

`EXT` switches the current CPU mode from `NRM` to `EXT`, and then finishes execution. This allows for the next fetched instruction to be interpretted uniquely.

## `CLC` - Clear Carry

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  0  |  -  |  -  |  -

Sets the SR's `C` flag to 0.

## `CLI` - Enable Interrupts

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  -  |  0

Sets the SR's `I` flag to 0.

## `CLV` - Clear Overflow

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  0  |  -

Sets the SR's `V` flag to 0.

## `SEC` - Set Carry Flag

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  1  |  -  |  -  |  -

Sets the SR's `C` flag to 1.

## `SEI` - Disable Interrupts

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  -  |  1

Sets the SR's `I` flag to 1.

## `MOV` - Move Register

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Inherent

The `MOV` instruction has both 8-bit and 16-bit versions. These versions have separate sets of allowed destinations and sources. The format of the `MOV` instruction is: `mov dst src`. It is illegal for `dst` to match `src`.

### 8-bit `MOV`

Source: `a`, `b`, `c`, `d`
Destination: `a`, `b`, `c`, `d`

Extraneous pairs:
    `mov a dp`
    `mov dp a`

### 16-bit `MOV`

Source: `x`, `y`, `e`
Destination: `x`, `y`, `e`

Extraneous pairs:
    `mov e sp`
    `mov sp e`

## `LOAD` - Load Register

Field  | Value
------ | ---
Type   | `NRM`
Size   | varies
Cycles | varies
Mode   | varies

The `LOAD` instruction has varying specifications for the 8-bit and 16-bit versions.

### 8-bit `LOAD`

Destinations: GPRs
Addressing Modes:

**Immediate**
    Size: 2
    Cycles: TBD

**Absolute**
    Size: 3
    Cycles: TBD

**Direct Page**
    Size: 2
    Cycles: TBD

**Indirect**
    Indirection Sources: GPPs or `sp`
    Size: 1
    Cycles: TBD

**Indexed Indirect**
    Indirection Sources: GPPs or `sp`
    Index Sources: GPRs
    Size: 1
    Cycles: TBD

### 16-bit `LOAD`

Destinations: GPPs
Addressing Modes:

**Immediate**
    Size: 3
    Cycles: TBD

**Absolute**
    Size: 3
    Cycles: TBD

**Direct Page**
    Size: 2
    Cycles: TBD

**Indirect**
    Indirection Sources: GPPs or `sp`
    Size: 1
    Cycles: TBD

## `LEA` - Load Effective Address

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | TBD
Mode   | Indexed Indirect

Destinations: GPPs
Indirection Sources: GPPs or `sp`
Index Sources: GPRs

The `LEA` instructions perform the same address calculation that occurs with Indexed Indirect loads and stores, but don't actually perform the memory operation.

## `ADC` - Add with Carry

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  +  |  -

`ADC` instructions follow the rules of Binary Math Operations.

## `SBB` - Subtract with Borrow

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  +  |  -

`SBB` instructions follow the rules of Binary Math Operations.

## `AND` - Bitwise AND

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  -  |  +  |  -  |  -

`AND` instructions follow the rules of Binary Math Operations.

## `OR` - Bitwise OR

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  -  |  +  |  -  |  -

`OR` instructions follow the rules of Binary Math Operations.

## `XOR` - Bitwise XOR

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  -  |  +  |  -  |  -

`XOR` instructions follow the rules of Binary Math Operations.

## `NOT` - Bitwise Inversion

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  -  |  +  |  -  |  -

`NOT` instructions follow the rules of Unary Math Operations.

## `NEG` - 2s Complement Negation

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  -  |  -

`NEG` instructions follow the rules of Unary Math Operations.

## `LSR` - Logical Shift Right

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

`LSR` instructions follow the rules of Unary Math Operations.

*TODO*: To be consistent with the lack of `ADD` and `SUB` instructions, this instruction should be removed in favor of the `LRC` instruction. Will allow for `CMP` with Immediate instrutions to be added. This change will probably allow for some reductions in ALU hardware.

## `LRC` - Logical Shift Right with Carry

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

`LRC` instructions follow the rules of Unary Math Operations.

## `ASR` - Arithmetic Shift Right

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

`ASR` instructions follow the rules of Unary Math Operations.

## `INC` - Increment

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

Addressing Modes:

**Inherent**
    Size: 2
    Cycles: TBD

Inherent `INC` instructions have a source which is either a GPR or a GPP.

**Direct Page**
    Size: 3
    Cycles: TBD

Direct Page `INC` instructions operate on 8-byte values only.

### Flag Modification
If the source is a GPP, then no flags are modified. Otherwise, the following is true:

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

## `DEC` - Decrement

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

Addressing Modes:

**Inherent**
    Size: 2
    Cycles: TBD

Inherent `DEC` instructions have a source which is either a GPR or a GPP.

**Direct Page**
    Size: 3
    Cycles: TBD

Direct Page `DEC` instructions operate on 8-byte values only.

### Flag Modification
If the source is a GPP, then no flags are modified. Otherwise, the following is true:

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

## `PUSH` - Push to Stack

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | varies
Mode   | Inherent

Sources: GPRs, GPPs, Status Register (SR)

## `POP` - Pop from Stack

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | varies
Mode   | Inherent

Sources: GPRs, GPPs, Status Register (SR)

## `CMP` - Compare

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  +  |  -

`CMP` instructions perform a subtract without borrow but discard the result. The purpose of this instruction is to set the SR flags appropriately, and is commonly used before performing a conditional jump. They closely follow the Binary Math Operations rules, with the exception that immediates are not a supported right hand operand.

*TODO*: Compare with Immediates are very useful. Add these in once `LSR` instructions have been removed.

## `TST` - Bit Test

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  -  |  +  |  -  |  -

`TST` instructions perform a Bitwise `AND` operation of the operand with itself, but then discards the result. The purpose of this instruction is to set the SR flags appropriately, and is commonly used before performing a conditional jump. They closed follow the Unary Math Operations rules.

## `WAI` - Wait for Interrupt

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | varies
Mode   | Inherent

The `WAI` instruction causes execution to suspend until an IRQ is received. This instruction has two distinct behaviors, depending on the state of the SR's `I` flag prior to it beginning execution.

- `I = 0`: When an IRQ is received, a context shift to the appropriate ISR occurs. When the routine returns, execution resumes after the `WAI` instruction.

- `I = 1`: When an IRQ is recieved, no context shift occurs and execution continues after the `WAI` instruction. This can be used to process interrupts "in-line".

## `SWI` - Software Interrupt

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | TBD
Mode   | Indirect

`SWI` instructions perform the same IRQ interrupt routine - that is, pushing the Program Counter, pushing the Status Register, disabling interrupts, and reading from the interrupt vector - with the exception that instead of using the CPU's hardware interrupt vector, the vector is provided in a GPP.

## `RTI` - Return from Interrupt

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | TBD
Mode   | Inherent

The `RTI` instruction performs a context switch away from an ISR to the previously executing code by restoring the Program Counter, the Status Register, and the Interrupt Inhibit flag.

## `JSR` - Jump to Subroutine

Field  | Value
------ | ---
Type   | varies
Size   | varies
Cycles | varies
Mode   | varies

`JSR` instructions execute a function call by saving the Program Counter to the stack and loading the source to the Program Counter to execute a jump. The size and type of the opcode varies based on its Addressing Mode.

Addressing Modes:

**Absolute**
    Type: `NRM`
    Size: 3
    Cycles: TBD

**Relative**
    Type: `NRM`
    Size: 2
    Cycles: TBD

**Indirect**
    Indirection Sources: GPPs
    Type: `EXT`
    Size: 2
    Cycles: TBD

## `RTS` - Return from Subroutine

Field  | Value
------ | ---
Type   | NRM
Size   | 1
Cycles | TBD
Mode   | Inherent

The `RTS` instruction shifts execution from a called subroutine to the previously executing code by reading the new Program Counter value from the stack.

## `JMP` - Unconditional Jump

`JMP` instructions perform an unconditional jump. They follow the specifications described in Jump Operations.

## `JO` - Jump if Overflow

`JO` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `V = 1`
Signedness: -

## `JNO` - Jump if not Overflow

`JNO` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `V = 0`
Signedness: -

## `JS` - Jump if Sign

`JS` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `N = 1`
Signedness: -

## `JNS` - Jump if not Sign

`JNS` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `N = 0`
Signedness: -

## `JE` - Jump if Equal

`JE` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `Z = 1`
Signedness: -

## `JNE` - Jump if not Equal

`JNE` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `Z = 0`
Signedness: -

## `JC` - Jump if Carry

`JC` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `C = 1`
Signedness: unsigned

## `JNC` - Jump if not Carry

`JNC` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `C = 0`
Signedness: unsigned

## `JBE` - Jump if Below or Equal

`JBE` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `C = 1` or `Z = 1`
Signedness: unsigned

## `JA` - Jump if Above

`JA` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `C = 0` and `Z = 0`
Signedness: unsigned

## `JL` - Jump if Less

`JL` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `N != V`
Signedness: signed

## `JGE` - Jump if Greater or Equal

`JGE` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `N = V`
Signedness: signed

## `JLE` - Jump if Less or Equal

`JLE` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `Z = 1` or `N != V`
Signedness: signed

## `JG` - Jump if Greater

`JG` instructions perform a conditional jump. They follow the specifications described in Jump Operations.

Flag Condition: `Z = 0` and `N = V`
Signedness: signed

# Binary Math Operations

Binary Math Instructions are Arithmetic or Logical instructions which have two operands. In the BW8 ISA, these include the following:

1. `ADC`
2. `SBB`
3. `AND`
4. `OR`
5. `XOR`

These instructions have left and right hand side operands. The left hand operand also serves as the destination of the result. The left hand side operand is referred to as the destination, and the right hand side operand is referred to as the source: `bin_op dst src`.

Destinations: GPRs or Direct Page location
Sources: GPRs, Direct Page location, or immediate value

When `dst` and `src` are both GPRs, they are allowed to be identical. Left shifts are supported via this mechanism. When the `dst` and `src` are both specified as Direct Page locations, they are specified uniquely in the instruction stream. For this reason, they can refer to the same or unique locations.

Binary Math Instructions which are 3 bytes in size - this occurs when `dst` and `src` are both Direct Page locations, or when `dst` is a Direct Page location and `src` is an immediate value - are of the `NRM` type. Otherwise, they are of the `EXT` type.

# Unary Math Operations

Unary Math Operations are Arithmetic and Logical instructions which have one operand. In the BW8 ISA, these include the following:

1. `NOT`
2. `NEG`
3. `LSR`
4. `LRC`
5. `ASR`

These instructions have a single operand, which is used as both the source and the destination: `uny_op src`. The source is either a GPR, or a Direct Page location.

Addressing Modes:

**Inherent**
    Size: 2
    Cycles: TBD

**Direct Page**
    Size: 3
    Cycles: TBD

All Unary Math Operations are of the `EXT` type.

# Jump Operations

Field | Value
--- | ---
Type | varies
Size | varies
Cycles | varies
Mode | varies

Jump instructions shift the execution path by moving the source into the Program Counter. This jump may be performed conditionally, based on the value of specific flags in the Status Register, or unconditionally. The source of the new execution point comes from the Addressing Mode. All jumps in the BW8 ISA support the same Addressing Modes. The mode also informs the type and size of the instruction.

Addressing Modes:

**Absolute**
    Type: `NRM`
    Size: 3
    Cycles: TBD

**Relative**
    Type: `NRM`
    Size: 2
    Cycles: TBD

*NOTE*: Relative Jumps are of type `NRM` for unconditional jumps, and for conditional jumps. *Unless* the conditional jump is for *signed comparisons*, in which case they are of type `EXT`.

**Indirect**
    Indirection Sources: GPPs
    Type: `EXT`
    Size: 2
    Cycles: TBD
