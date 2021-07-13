# Instructions

## NOP

No Operation, takes no operands. Does nothing and then continues. No flag changes.

## HLT

Halt, takes no operands. Stops the system clock. No flag changes.

## MOV

Move, takes 2 operands. Moves the value located at first location to second location. No flag changes.


# Binary Arithmetic Instructions

## ADD

Add, takes 2 operands. Performs addition on the values and stores the result in the Accumulator. May modify C, Z, V, N flags.

## ADC

Add With Carry, takes 2 operands. Performs addition on the values, including the value of the carry bit, and stores the result in the Accumulator. May modify C, Z, V, N flags.

## SUB

Subtract, takes 2 operands. Performs subtraction on the values and stores the result in the Accumulator. May modify C, Z, V, N flags.

## SBB

Subtract With Borrow, takes 2 operands. Sutracts the values, including the value of the carry bit, and stores the result in the Accumulator. May modify C, Z, V, N flags.


# Unary Arithmetic Instructions

## INC

Increment, takes 1 operand. Adds 1 to the value, and stores the result in the Accumulator. May modify C, Z, V, N flags.

## DEC

Decrement, takes 1 operand. Takes 1 from the value, and stores the result in the Accumulator. May modify C, Z, V, N flags.

## ASR

Arithmetic Shift Right, takes 1 operand. Performs a 1-bit arithmetic right shift on the value, and stores the result in the Accumulator. May modify Z, N flags.


# Binary Logical Instructions

## AND

AND, takes 2 operands. Performs logical ANDing on the values and stores the result in the Accumulator. May modify Z, N flags.

## OR

OR, takes 2 operands. Performs logical ORing on the values and stores the result in the Accumulator. May modify Z, N flags.

## XOR

Exclusive OR, takes 2 operands. Performs logical XORing on the values and stores the result in the Accumulator. May modify Z, N flags.


# Unary Logical Instructions

## NOT

NOT, takes 1 operand. Performs logical NOTing on the value and stores the result in the Accumulator. May modify Z, N flags.

## LSL

Logical Shift Left, takes 1 operand. Perfoms a logical 1-bit left shift on the value and stores the result in the Accumulator. May modify Z, N, L flags.

## LSR

Logical Shift Right, takes 1 operand. Perfoms a logical 1-bit right shift on the value and stores the result in the Accumulator. May modify Z, N, L flags.

## ROL

Rotation Left, takes 1 operand. Performs a 1-bit left rotation on the value and stores the result in the Accumulator. May modify Z, N flags.

## ROR

Rotation Right, takes 1 operand. Performs a 1-bit right rotation on the value and stores the result in the Accumulator. May modify Z, N flags.


# Flag Setting Instructions

## SEZ

Set Zero Flag, takes no operands, sets the Z flag to true.

## SEC

Set Carry Flag, takes no operands, sets the C flag to true.

## SEN

Set Negative Flag, takes no operands, sets the N flag to true.

## SEV

Set Overflow Flag, takes no operands, sets the V flag to true.

## SEL

Set Logical Carry Flag, takes no operands, sets the L flag to true.

## SEI

Set Interrupt Inhibit Flag, takes no operands, sets the I flag to true.

## CLZ

Clear Zero Flag, takes no operands, sets the Z flag to false.

## CLC

Clear Carry Flag, takes no operands, sets the C flag to false.

## CLN

Clear Negative Flag, takes no operands, sets the N flag to false.

## CLV

Clear Overflow Flag, takes no operands, sets the V flag to false.

## CLL

Clear Logical Carry Flag, takes no operands, sets the L flag to false.

## CLI

Clear Interrupt Inhibit Flag, takes no operands, sets the I flag to false.


# Jump Instructions

## JMP

Jump, takes 1 operand, unconditionally jumps to the address.

## JSR

Jump to Subroutine, takes 1 operand, unconditionally jumps to the subroutine at address.

## RTS

Return from Subroutine, takes no operands, returns from the current subroutine.

## RTI

Return from Interrupt, takes no operands, returns from the current service routine.

## JZC

Jump if Zero Clear, takes 1 operand, conditionally jumps to the address if Z = 0.

## JZS

Jump if Zero Set, takes 1 operand, conditionally jumps to the address if Z = 1.

## JCC

Jump if Carry Clear, takes 1 operand, conditionally jumps to the address if C = 0.

## JCS

Jump if Carry Set, takes 1 operand, conditionally jumps to the address if C = 1.

## JNC

Jump if Negative Clear, takes 1 operand, conditionally jumps to the address if N = 0.

## JNS

Jump if Negative Set, takes 1 operand, conditionally jumps to the address if N = 1.

## JVC

Jump if Overflow Clear, takes 1 operand, conditionally jumps to the address if V = 0.

## JVS

Jump if Overflow Set, takes 1 operand, conditionally jumps to the address if V = 1.

## JLC

Jump if Logical Carry Clear, takes 1 operand, conditionally jumps to the address if L = 0.

## JLS

Jump if Logical Carry Set, takes 1 operand, conditionally jumps to the address if L = 1.


# Load and Store Instructions

## LDA

Load A, takes 1 operand. Puts the specified value in the A register.

## LDB

Load B, takes 1 operand. Puts the specified value in the B register.

## LDC

Load C, takes 1 operand. Puts the specified value in the C register.

## STA

Store A, takes 1 operand. Stores the value in the A register at the specified address.

## STB

Store B, takes 1 operand. Stores the value in the B register at the specified address.

## STC

Store C, takes 1 operand. Stores the value in the C register at the specified address.

## STE

Store Accumulator, takes 1 operand. Stores the value in the accumulator at the specified address.

# Stack Instructions

## PSH

Push, takes 1 operand. Stores the value on the stack.

## PUL

Pull, takes 1 operand. Load the stack into the location.
