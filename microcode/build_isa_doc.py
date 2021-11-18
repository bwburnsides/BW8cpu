""" This file builds a Markdown file that documents the Instruction Set Architecture
documented in 'instructions.json'.
"""

import json

fname = "AUTO_instruction_set_architecture.md"
intro_str = """
The instruction set for my homebrew 8-bit processor contains 48 instructions, most with multiple addressing modes and numerous corresponding opcodes. Within is a description of each instruction and the addressing modes that are available for them.

The CPU architecture is based a variant of James Sharman's Homebrew 8-bit Pipelined CPU. Some changes have been made:

- CPU is not pipelined
- LHS/RHS buses have been merged with the Transfer Bus
- Transfer Register has been removed
- Stack Pointer's top byte is fixed
- Zeropage address assertions
- Reset Vector inclusion
- ISR Vector inclusion

The result is something similar in interface to the MOS 6502, but with considerably larger instruction support and a greater number of registers.

The Control Unit uses 19 bits of state input to determine the 32 bit control state of the CPU. These 19 bits include a reset line, an IRQ line, 9 bits for opcode, 5 bits for flags, and 3 bits for t-state. The five flags are similar to the 6502's:

- Z: Zero Flag
- C: Carry Flag
- V: Overflow Flag
- N: Negative Flag
- I: Interrupt Inhibit Flag

Opcodes fetched from memory are only 8-bits in width. The 9th bit is provided by a T-flip-flop which is controlled via 1 bit from the control bus. One of the instructions, EXT, is meant to toggle this flip-flop to put the CPU into "extended" mode for the next instruction. At the conclusion of the instruction, this flip flop is toggled back into the offstate.

This system allows for 255 normal opcodes, the EXT opcode, and 256 extended opcodes. EXT is not meant to be used directly by the programmer. Rather, the Assembler will insert EXT immediately before mnemonic that is identified as belonging to an extended opcode.

As of yet, the extended opcodes have not been selected. I am open to feedback on which instructions should be put onto the extended page - of course, these should probably be the ones likely to have the lowest use-frequencies.
"""

with open(fname, "w") as f:
    f.write("# Instruction Set Architecture\n")
    f.write(intro_str)


table = ["| # | Mnemonic | Description |", "| - | -------- | ----------- |"]
instructions_blocks = []

with open("instructions.json") as f:
    instructions = json.load(f)


for i, (k, v) in enumerate(instructions.items()):
    desc = v.get("desc", "")
    k = k.upper()
    table.append(f"| {i} | {k} | {desc} |")

    instructions_blocks.append([])
    block = instructions_blocks[-1]

    block.append(f"### {k}")
    block.append("| Mode | Assembly | Opcode | Bytes | Cycles |")
    block.append("| ---- | -------- | ------ | ----- | ------ |")

    modes = v.get("modes", {})
    for mode in modes:
        info = modes[mode]
        asm_ex = info.get("asm-ex", "No ex given")
        length = info.get("bytes", "No bytes given")

        block.append(f"| {mode} | {asm_ex} | TBD | {length} | TBD |")

with open(fname, "a") as f:
    f.write("## Instruction Overview\n")
    f.write("\n".join(table))
    f.write("\n")

    f.write("## Instruction Details\n")

    for block in instructions_blocks:
        f.write("\n".join(block))
        f.write("\n")
