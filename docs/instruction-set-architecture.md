# 🔧 BW8 Instruction Set Architecture Specification

The BW8cpu instruction set contains the following instructions. Each instruction has several opcodes that implement various combinations of operands and addressing mode variations on their base behavior. These will be discussed below.

Mnemonic                                       | Name                           
---------------------------------------------- | ------------------------------
[`NOP`](#nop---no-operation)                   | No Operation                   
[`BRK`](#brk---break-clock)                    | Break Clock                    
[`CLC`](#clc---clear-carry)                    | Clear Carry                    
[`CLI`](#cli---enable-interrupts)              | Disable Interrupts
[`CLV`](#clv---clear-overflow)                 | Clear Overflow                 
[`SEC`](#sec---set-carry-flag)                 | Set Carry                      
[`SEI`](#sei---disable-interrupts)             | Enable Interrupts             
[`IN`](#in---read-io-port)                     | IO Input
[`OUT`](#out---write-io-port)                  | IO Output             
[`MOV`](#mov---move-register)                  | Move Register                  
[`LOAD`](#load---load-register)                | Load Register                  
[`STORE`](#store---store-register)             | Store Register                 
[`LEA`](#lea---load-effective-address)         | Load Effective Address         
[`ADC`](#adc---add-with-carry)                 | Add with Carry                 
[`SBB`](#sbb---subtract-with-borrow)           | Subtract with Borrow           
[`AND`](#and---bitwise-and)                    | Bitwise AND                    
[`OR`](#or---bitwise-or)                       | Bitwise OR                     
[`XOR`](#xor---bitwise-xor)                    | Bitwise XOR                    
[`NOT`](#not---bitwise-inversion)              | Bitwise NOT                    
[`NEG`](#neg---2s-complement-negation)         | 2s Complement Negation         
[`SRC`](#shr---logical-shift-right-with-carry) | Logical Shift Right with Carry 
[`ASR`](#asr---arithmetic-shift-right)         | Arithmetic Shift Right         
[`INC`](#inc---increment)                      | Increment                      
[`DEC`](#dec---decrement)                      | Decrement                      
[`PUSH`](#push---push-to-stack)                | Push to Stack                  
[`POP`](#pop---pop-from-stack)                 | Pop from Stack                 
[`CMP`](#cmp---compare)                        | Compare                       
[`TST`](#tst---bit-test)                       | Bit Test                       
[`RTI`](#rti---return-from-interrupt)          | Return from Interrupt          
[`JSR`](#jsr---jump-to-subroutine)             | Jump to Subroutine             
[`RTS`](#rts---return-from-subroutine)         | Return from Subroutine   
[`JMP`](#jmp---unconditional-jump)             | Jump                           
[`JO`](#jo---jump-if-overflow)                 | Jump if Overflow               
[`JNO`](#jno---jump-if-not-overflow)           | Jump if not Overflow           
[`JS`](#js---jump-if-sign)                     | Jump if Sign                   
[`JNS`](#jns---jump-if-not-sign)               | Jump if not Sign               
[`JE`](#je---jump-if-equal)                    | Jump if Equal                  
[`JNE`](#jne---jump-if-not-equal)              | Jump if not Equal              
[`JC`](#jc---jump-if-carry)                    | Jump if Carry                  
[`JNC`](#jnc---jump-if-not-carry)              | Jump if not Carry              
[`JBE`](#jbe---jump-if-below-or-equal)         | Jump if Below or Equal         
[`JA`](#ja---jump-if-above)                    | Jump if Above                  
[`JL`](#jl---jump-if-less)                     | Jump if Less                   
[`JGE`](#jge---jump-if-greater-or-equal)       | Jump if Greater or Equal       
[`JLE`](#jle---jump-if-less-or-equal)          | Jump if Less or Equal          
[`JG`](#jg---jump-if-greater)                  | Jump if Greater                

The BW8 has an 8-bit Instruction Register, so there is some trickery involved to support up to 512 opcodes, rather than just 256. This is done with the `EXT` instruction. This is a 1 byte, 1 cycle instruction which transitions the CPU from normal "`NRM`" mode to extended "`EXT`" mode, and then fetches the next instruction. This next instruction is interpretted differently due to the system being in `EXT` Mode. At the conclusion of these instructions, they return the CPU to `NRM` Mode. Through this mechanism, the CPU can ascribe two different meanings to each 8-bit opcode value, yielding a total of 512 opcodes.

The `NRM` Mode instructions are those which are commonly used, have long cycle counts, or have larger operand counts. The idea is to limit the cycle penalty incurred by `EXT` Mode opcodes to those which already execute quickly, or are not commonly used. In addition, by making sure that large operand count instructions exist in NRM Mode, we limit the maximum instruction size to 3 bytes, thereby keeping the program size penalty down.

# Programming Model

The CPU programming model includes four 8-bit General Purpose Registers (GPRs): `a`, `b`, `c`, `d`, and two 16-bit General Purpose Pointers (GPPs): `x`, `y`. There are four special purpose programmer facing registers:

1. `dp` - 8-bit, the location of the Direct Page
2. `ab` - 16-bit, a pseudo register constructed with `a` in the high byte and `b` in the low byte
3. `cd` - 16-bit, a psuedo register constructed with `c` in the high byte and `d` in the low byte
3. `sp` - 16-bit, the system Stack Pointer

These three registers have limited direct support, and are generally interacted with via `MOV`s. The `ab` and `cd` registers provide a mechanism for constructing 16-bit results that can be loaded into the GPPs or the SP. Additionally, there is the Status Register (`sr`) which stores the following CPU flags:

1. Zero (`Z`)
2. Carry (`C`)
3. Negative (`N`)
4. Overflow (`V`)
5. Interrupt Enable (`I`)

The first four of these are primarily set by the result of a recent ALU calculation. The final is used to enable or disable maskable interrupt requests (IRQ), and is managed directly by the programmer via `SEI` and `CLI`.

In the subsequent section, the size of an instruction is given as the total number of bytes required to execute the instruction. This includes the optional prefix `EXT` byte, and any operands following the opcode in the instruction stream.

# Addressing Modes

- *Implied*: There is no relevant operand source or destination, or they are implied directly by the opcode.

- *Register Direct*: There is no effective address; all operands are in registers which are implied by the opcode.

- *Immediate*: Their is no effective address; the operand is the one or two bytes following the opcode in the instruction stream, depending on the target of the instruction.

- *Absolute*: The effective address is given as a two-byte absolute address which follows the opcode in Big Endian order.

- *Direct*: The effective address is given as a one-byte direct page address which follows the opcode.

- *Register Indirect*: The effective address is the address in a pointer register implied by the opcode.

- *Indexed Indirect*: The effective address is computed by adding a signed 8-bit index to a pointer register's contents. Both the pointer register and the index source are implied in the opcode.

- *Relative*: The effective address is computed by adding a signed 8-bit offset to the Program Counter. The offset source is the byte following the opcode.

# Instruction Details

## `NOP` - No Operation

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

    nop

Does nothing, and then continues.


## `BRK` - Break Clock

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | 4
Mode   | Implied

    brk

The clock module which provides the CPU's clock input has three modes: Run, Demo, and Step. The final of which single steps the CPU. This opcode forces the clock mode into Step, and so it acts similarly to a `HLT` instruction, but is recoverable via the hardware clock control features. This instruction slightly breaks the encapsulation of the CPU's implementation details as it makes assumptions about hardware external to the CPU.

## `CLC` - Clear Carry

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  0  |  -  |  -  |  -

    clc

Sets the SR's `C` flag to 0.

## `CLI` - Disable Interrupts

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  -  |  0

    cli

Sets the SR's `I` flag to 0.

## `CLV` - Clear Overflow

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  0  |  -

    clv

Sets the SR's `V` flag to 0.

## `SEC` - Set Carry Flag

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  1  |  -  |  -  |  -

    sec

Sets the SR's `C` flag to 1.

## `SEI` - Enable Interrupts

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  -  |  -  |  -  |  -  |  1

    sei

Sets the SR's `I` flag to 1.

## `IN` - Read IO Port

Field | Value
----- | -----
Type  | `EXT`
Size  | varies
Cycles | varies
Mode | varies

    in {dst: gpr}, <{port: u8}>
    in [{dp: u8}], <{port: u8}>

## `OUT` -- Write IO Port

Field | Value
----- | -----
Type  | `EXT`
Size  | varies
Cycles | varies
Mode | varies

    out <{port: u8}>, {src: gpr}
    out <{port: u8}>, [{dp: u8}]
    out <{port: u8}>, #{imm: i8}

## `MOV` - Move Register

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | 2
Mode   | Implied

The `MOV` instruction has both 8-bit and 16-bit versions. These versions have separate sets of allowed destinations and sources. The format of the `MOV` instruction is: `mov dst src`. It is illegal for `dst` to match `src`.

### 8-bit `MOV`

Source: `a`, `b`, `c`, `d`
Destination: `a`, `b`, `c`, `d`

Extraneous pairs:
    `mov a dp`
    `mov dp a`

### 16-bit `MOV`

Source: `x`, `y`, `ab`, `cd`
Destination: `x`, `y`, `ab`, `cd`

Extraneous pairs:
    `mov x sp`
    `mov sp x`

Note:
    `ab` and `cd` being used as a `src`-`dst` (or `dst`-`src`) pair is illegal. The assembler should implement these instructions as pseudo instructions consisting of two 8-bit `MOV`s.

## `LOAD` - Load Register

Field  | Value
------ | ---
Type   | `NRM`
Size   | varies
Cycles | varies
Mode   | varies

The `LOAD` instruction has varying specifications for the 8-bit and 16-bit versions.

### 8-bit `LOAD`

    load {dst: gpr}, #{imm: i8}
    load {dst: gpr}, [{abs: u16}]
    load {dst: gpr}, [{dp: u8}]
    load {dst: gpr}, [{ptr: gpp | sp}, #{idx: s8}]
    load {dst: gpr}, [{ptr: gpp | sp}, {idx: gpr}]

Destinations: GPRs
Addressing Modes:


**Immediate**

    load {dst: gpr}, #{imm: i8}

Size: 2
Cycles: TBD

**Absolute**

Size: 3
Cycles: TBD

**Direct Page**

Size: 2
Cycles: TBD

**Indirect**

Indirection Sources: GPPs
Size: 1
Cycles: TBD

**Indexed Indirect**

Indirection Sources: GPPs or `sp`
Index Sources: GPRs (sometimes immediate)
Size: varies
Cycles: TBD

The *indexed indirect* 8-bit Load instructions allow for a GPR to be loaded with the value found at an address computed by adding an 8-bit value to a GPP or the SP. In all indirection sources, all 4 GPRs are valid index sources. When the indirection source is the `sp`, then an additional index source is allowed from the instruction stream, as an immediate offset.

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

## `STORE` - Store Register

`STORE` instructions write a register's contents to memory. They are the reciprocal to the [`LOAD`](#load---load-register) instructions. They have identical modes and restrictions as the `LOAD` instructions do, with the exceptions that the **Immediate** mode does not exist, as that doesn't make sense in the context of a memory write, and the cycle counts may be different. Those are currently TBD.

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

`ADC` instructions follow the rules of [Binary Math Operations](#binary-math-operations).

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

`SBB` instructions follow the rules of [Binary Math Operations](#binary-math-operations).

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

`AND` instructions follow the rules of [Binary Math Operations](#binary-math-operations).

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

`OR` instructions follow the rules of [Binary Math Operations](#binary-math-operations).

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

`XOR` instructions follow the rules of [Binary Math Operations](#binary-math-operations).

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

`NOT` instructions follow the rules of [Unary Math Operations](#unary-math-operations).

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

`NEG` instructions follow the rules of [Unary Math Operations](#unary-math-operations).

## `SRC` - Logical Shift Right with Carry

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

| `Z` | `C` | `N` | `V` | `I`
| --- | --- | --- | --- | ---
|  +  |  +  |  +  |  -  |  -

`SRC` instructions follow the rules of [Unary Math Operations](#unary-math-operations).

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

`ASR` instructions follow the rules of [Unary Math Operations](#unary-math-operations).

## `INC` - Increment

Field  | Value
------ | ---
Type   | `EXT`
Size   | varies
Cycles | varies
Mode   | varies

Addressing Modes:

**Implied**

Size: 2
Cycles: TBD

Implied `INC` instructions have a source which is either a GPR or a GPP.

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

**Implied**

Size: 2
Cycles: TBD

Implied `DEC` instructions have a source which is either a GPR or a GPP.

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
Mode   | Implied

Sources: GPRs, GPPs, Status Register (SR)

## `POP` - Pop from Stack

Field  | Value
------ | ---
Type   | `EXT`
Size   | 2
Cycles | varies
Mode   | Implied

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
Type   | `NRM`
Size   | 1
Cycles | varies
Mode   | Implied

The `WAI` instruction causes execution to suspend until an IRQ is received. This instruction has two distinct behaviors, depending on the state of the SR's `I` flag prior to it beginning execution.

- `I = 0`: When an IRQ is received, a context shift to the appropriate ISR occurs. When the routine returns, execution resumes after the `WAI` instruction.

- `I = 1`: When an IRQ is recieved, no context shift occurs and execution continues after the `WAI` instruction. This can be used to process interrupts "in-line".

## `RTI` - Return from Interrupt

Field  | Value
------ | ---
Type   | `NRM`
Size   | 1
Cycles | TBD
Mode   | Implied

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
Mode   | Implied

The `RTS` instruction shifts execution from a called subroutine to the previously executing code by reading the new Program Counter value from the stack.

## `JMP` - Unconditional Jump

`JMP` instructions perform an unconditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

## `JO` - Jump if Overflow

`JO` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `V = 1`
Signedness: -

## `JNO` - Jump if not Overflow

`JNO` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `V = 0`
Signedness: -

## `JS` - Jump if Sign

`JS` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `N = 1`
Signedness: -

## `JNS` - Jump if not Sign

`JNS` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `N = 0`
Signedness: -

## `JE` - Jump if Equal

`JE` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `Z = 1`
Signedness: -

## `JNE` - Jump if not Equal

`JNE` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `Z = 0`
Signedness: -

## `JC` - Jump if Carry

`JC` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `C = 1`
Signedness: unsigned

## `JNC` - Jump if not Carry

`JNC` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `C = 0`
Signedness: unsigned

## `JBE` - Jump if Below or Equal

`JBE` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `C = 1` or `Z = 1`
Signedness: unsigned

## `JA` - Jump if Above

`JA` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `C = 0` and `Z = 0`
Signedness: unsigned

## `JL` - Jump if Less

`JL` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `N != V`
Signedness: signed

## `JGE` - Jump if Greater or Equal

`JGE` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `N = V`
Signedness: signed

## `JLE` - Jump if Less or Equal

`JLE` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

Flag Condition: `Z = 1` or `N != V`
Signedness: signed

## `JG` - Jump if Greater

`JG` instructions perform a conditional jump. They follow the specifications described in [Jump Operations](#jump-operations).

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

- When `dst` and `src` are both GPRs, they are allowed to be identical. Left shifts are supported via this mechanism.
- Both the `dst` and `src` may not be Direct Page locations.

Binary Math Instructions which are 3 bytes in size - this occurs when `dst` is a Direct Page location and `src` is an immediate value - are of the `NRM` type. Otherwise, they are of the `EXT` type.

# Unary Math Operations

Unary Math Operations are Arithmetic and Logical instructions which have one operand. In the BW8 ISA, these include the following:

1. `NOT`
2. `NEG`
3. `LSR`
4. `LRC`
5. `ASR`

These instructions have a single operand, which is used as both the source and the destination: `uny_op src`. The source is either a GPR, or a Direct Page location.

Addressing Modes:

**Implied**

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

**Indirect**

Indirection Sources: GPPs
Type: `EXT`
Size: 2
Cycles: TBD

