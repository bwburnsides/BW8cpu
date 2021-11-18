from typing import List
from control_lines import Ctrl
from opcodes import Opcode

# Louis: The opcodes are read from the opcodes.txt file, this is the same file I've
# shared with the Discord server. This Opcode class just reads those in and makes
# them class members so that they're easier to access. The actual implementation
# of how thats done in the Opcode class is not very pretty. The rest of this file
# is not very pretty, either.
Opcode.build_opcode_list()
print(f"Number of opcodes: {Opcode.count()}")

# These are ordering of the flags
# Carry, Zero, Overflow, Negative, Interrupt Inhibit
# The masks help with bitwise operations.
c_mask = 0b10000
z_mask = 0b01000
v_mask = 0b00100 
n_mask = 0b00010
i_mask = 0b00001

# This is my fetch sequence, should be pretty recognizable
fetch = Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_IR | Ctrl.COUNT_INC_PC

# This is the base of all instructions, which are 8 cycles at most. Think of this
# as an instruction template. They all start with fetch. The RESET_USTEP resets the
# ucode Tstate sequencer to 0 to start the next fetch. Its not strictly
# necessary to include it as the last step here since the sequencer will overflow after
# if anyhow. You'll see in the instruction implementations that for any instruction
# less than 8 cycles long, the last working step will include a RESET_USTEP in order
# to immediately start the next fetch instead of waiting out the rest of the 8 clocks.
base = [fetch, 0, 0, 0, 0, 0, 0, Ctrl.RESET_USTEP]

# This is my reset sequence. When the CPU is powered on, or the hardware reset button
# is pressed, this sequence will run. It loads the reset vector into the PC,
# reads that data, and the next location's data, and moves this address to the PC.
# The programmer puts whatever address they want to be the entry point of their program
# into reset vector lo and hi. This sequence does the work of reading that value and
# moving execution to there.
# TODO: There needs to be probably some hardware considerations to ensure that this
# sequence always starts at T0
rst_uops = [
    Ctrl.RESET_USTEP,
    Ctrl.XFER_ASSERT_RST | Ctrl.XFER_LOAD_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC,
    Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.CLEAR_RESET | Ctrl.RESET_USTEP,
    0,
    0,
    0,
]

# This is the interrupt sequence, these steps run in-place of a normal instruction
# cycle whenever the IRQ is active.
# This pushes the flags and PC to the stack, and reads from the ISR vector (similar
# to reset vector, except for interrupts) to see where to jump to. The value at that
# address is indirectly managed by the programmer, but ultimately its a memory-mapped
# programmable interrupt controller sitting at the ISR vector location.
irq_uops = [
    Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_Z | Ctrl.DBUS_ASSERT_SR | Ctrl.DBUS_LOAD_MEM | Ctrl.ADDR_ASSERT_SP | Ctrl.COUNT_INC_SP,
    Ctrl.XFER_ASSERT_PC | Ctrl.XFER_LOAD_TX | Ctrl.FLAG_I_SET,
    Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.ADDR_ASSERT_SP | Ctrl.COUNT_INC_SP,
    Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.ADDR_ASSERT_SP | Ctrl.COUNT_INC_SP | Ctrl.XFER_ASSERT_ISR | Ctrl.XFER_LOAD_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC,
    Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC,
    Ctrl.XFER_ASSERT_Z | Ctrl.XFER_LOAD_TX | Ctrl.RESET_USTEP,
]

need_implementation_count = 0

# Below is a massive function that returns the instruction sequence for a given
# state input. Its hundreds of lines long and not "clean" code, but should be
# really easy to follow. The code that calls this function is below the function,
# so might want to skip down there first before getting lost in here...

# Function takes in:
# reset - whether the CPU is in reset mode
# irq - whether the interrupt request line is active
# opcode - the current opcode
# flags - the current flag state
# Returns:
# a list of 8 control words for each step in that instruction.

# You might notice that Tstate is not an input. This is because whenever the function
# is called, its assumed that the Tstate is T0, so the 8 steps it returns are
# T0...T7. Look at the code calling this function to make more sense of this.
def compute_uops(reset: int, irq: int, opcode: int, flags: int) -> List[int]:    
    # Ultimately this word list is returned. The starting value of the instruction
    # sequence is just a copy of the instruction template "base" from above.
    word = base.copy()

    # The flags are passed in as a single value, this just splits them out into
    # separate variables using the masks from above.
    c = (flags & c_mask) >> 4  # Carry Flag
    z = (flags & z_mask) >> 3  # Zero Flag
    v = (flags & v_mask) >> 2  # Overflow Flag
    n = (flags & n_mask) >> 1  # Negative Flag
    i = (flags & i_mask) >> 0  # Interrupt Inhibit Flag

    # If the reset state is active, then nothing else matters: just return the
    # reset sequence from above
    if reset:   return rst_uops

    # If the interrupt inhibit flag is not set (ie instructions are enabled)
    # and the IRQ is active, then we want to service the interrupt, so just return
    # the instruction sequence. Recall that when this function is called, we are at T0.
    # So the only time these irq_uops are accessed is when Tstate is T0.
    if irq and not i:   return irq_uops

    # Below are all the cycle-wise implementations of my opcodes. Note that they
    # start with word[1], as word[0] is fetch, and thats already filled in via
    # the base template.

    # CPU Config
    if opcode == Opcode.NOP:    word[1] |= Ctrl.RESET_USTEP
    if opcode == Opcode.BREAK:  word[1] |= Ctrl.BREAK | Ctrl.RESET_USTEP
    if opcode == Opcode.EXTEND: word[1] |= Ctrl.EXTENDED_OP_FLIP | Ctrl.RESET_USTEP

    # The only exception to an opcode having fetch at T0 is WAI. The implementation
    # here is new and I'm not certain in its correct-ness yet. I'm suspect that its
    # not. I need more simulation and emulation!
    if opcode == Opcode.WAI:
        if not irq:
            word[0] = Ctrl.RESET_USTEP
            word[1] = Ctrl.RESET_USTEP
        elif irq and i: word[1] = fetch

    # Below, everything should be straightforward to understand but potentially
    # not that interesting. Note that I haven't gotten around to providing implementations
    # for all the opcodes in opcodes.txt just yet.

    # Flag Manipulation
    if opcode == Opcode.CLC:    word[1] |= Ctrl.FLAG_C_CLEAR | Ctrl.RESET_USTEP
    if opcode == Opcode.CLI:    word[1] |= Ctrl.FLAG_I_CLEAR | Ctrl.RESET_USTEP
    if opcode == Opcode.CLV:    word[1] |= Ctrl.FLAG_V_CLEAR | Ctrl.RESET_USTEP
    if opcode == Opcode.SEC:    word[1] |= Ctrl.FLAG_C_SET | Ctrl.RESET_USTEP
    if opcode == Opcode.SEI:    word[1] |= Ctrl.FLAG_I_SET | Ctrl.RESET_USTEP

    # Moves to A
    if opcode == Opcode.MOV_A_B:    word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_A_C:    word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_A_D:    word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_A_TL:   word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_A_TH:   word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_A_SP:   word[1] |= Ctrl.DBUS_LOAD_A | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to B
    if opcode == Opcode.MOV_B_A:    word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_B_C:    word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_B_D:    word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_B_TL:   word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_B_TH:   word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_B_SP:   word[1] |= Ctrl.DBUS_LOAD_B | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to C
    if opcode == Opcode.MOV_C_A:    word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_C_B:    word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_C_D:    word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_C_TL:   word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_C_TH:   word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_C_SP:   word[1] |= Ctrl.DBUS_LOAD_C | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to D
    if opcode == Opcode.MOV_D_A:    word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_D_B:    word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_D_C:    word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_D_TL:   word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_D_TH:   word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_D_SP:   word[1] |= Ctrl.DBUS_LOAD_D | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to TL
    if opcode == Opcode.MOV_TL_A:   word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TL_B:   word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TL_C:   word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TL_D:   word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TL_TH:  word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TL_SP:  word[1] |= Ctrl.DBUS_LOAD_TL | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to TH
    if opcode == Opcode.MOV_TH_A:   word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TH_B:   word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TH_C:   word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TH_D:   word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TH_TL:  word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TH_SP:  word[1] |= Ctrl.DBUS_LOAD_TH | Ctrl.DBUS_ASSERT_SP | Ctrl.RESET_USTEP

    # Moves to TX
    if opcode == Opcode.MOV_TX_Y:   word[1] |= Ctrl.XFER_LOAD_TX | Ctrl.XFER_ASSERT_Y | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TX_X:   word[1] |= Ctrl.XFER_LOAD_TX | Ctrl.XFER_ASSERT_X | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TX_PC:  word[1] |= Ctrl.XFER_LOAD_TX | Ctrl.XFER_ASSERT_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_TX_SPREL_IMM:
        word[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_TX | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_A | Ctrl.COUNT_INC_SP
        word[3] |= Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_A
        word[4] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_DEC_SP
        word[5] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # Moves to Y
    if opcode == Opcode.MOV_Y_TX:   word[1] |= Ctrl.XFER_LOAD_Y | Ctrl.XFER_ASSERT_TX | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_Y_X:    word[1] |= Ctrl.XFER_LOAD_Y | Ctrl.XFER_ASSERT_X | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_Y_PC:   word[1] |= Ctrl.XFER_LOAD_Y | Ctrl.XFER_ASSERT_PC | Ctrl.RESET_USTEP

    # Moves to X
    if opcode == Opcode.MOV_X_TX:   word[1] |= Ctrl.XFER_LOAD_X | Ctrl.XFER_ASSERT_TX | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_X_Y:    word[1] |= Ctrl.XFER_LOAD_X | Ctrl.XFER_ASSERT_Y | Ctrl.RESET_USTEP
    if opcode == Opcode.MOV_X_PC:   word[1] |= Ctrl.XFER_LOAD_X | Ctrl.XFER_ASSERT_PC | Ctrl.RESET_USTEP

    # Loads to A
    if opcode == Opcode.LOAD_A_X:   word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_Y:   word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_TX:  word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_IMM: word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_A_SPREL_IMM:
        word[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_TX | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_SP | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # if opcode == Opcode.LOAD_A_X_REL:
    #     word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
    #     word[2] |= Ctrl.XFER_ASSERT_X | Ctrl.ALU_RHS | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TEMP
    #     word[3] |= Ctrl.XFER_ASSERT_CONST_TEMP | Ctrl.ALU_ADD | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TEMP
    #     word[4] |= Ctrl.XFER_ASSERT_X | Ctrl.ALU_LHS_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_CONST
    #     word[5] |= Ctrl.ADDR_ASSERT_CONST_TEMP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # if opcode == Opcode.STORE_A_X_REL:
    #     word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
    #     word[2] |= Ctrl.XFER_ASSERT_X | Ctrl.ALU_RHS | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TEMP
    #     word[3] |= Ctrl.XFER_ASSERT_CONST_TEMP | Ctrl.ALU_ADD | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TEMP
    #     word[4] |= Ctrl.XFER_ASSERT_X | Ctrl.ALU_LHS_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_CONST
    #     word[5] |= Ctrl.ADDR_ASSERT_CONST_TEMP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP


    # Loads to B
    if opcode == Opcode.LOAD_B_X:   word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_Y:   word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_TX:  word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_IMM: word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_B_SPREL_IMM:
        word[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_TX | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_SP | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # Loads to C
    if opcode == Opcode.LOAD_C_X:   word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_Y:   word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_TX:  word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_IMM: word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_C_SPREL_IMM:
        word[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_TX | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_SP | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # Loads to D
    if opcode == Opcode.LOAD_D_X:   word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_Y:   word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_TX:  word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_IMM: word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_D_SPREL_IMM:
        word[1] |= Ctrl.XFER_ASSERT_SP | Ctrl.XFER_LOAD_TX | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_SP | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_TL
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # Loads to TL
    if opcode == Opcode.LOAD_TL_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TL_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TL_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TL_IMM:    word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TL_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TL_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP

    # Loads to TH
    if opcode == Opcode.LOAD_TH_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TH_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TH_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TH_IMM:    word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TH_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.LOAD_TH_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP

    # Stores from A
    if opcode == Opcode.STORE_A_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_A_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_A_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_A | Ctrl.RESET_USTEP

    # Stores from B
    if opcode == Opcode.STORE_B_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_B | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_B_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_B | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_B_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_B | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_B | Ctrl.RESET_USTEP

    # Stores from C
    if opcode == Opcode.STORE_C_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_C | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_C_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_C | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_C_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_C | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_C | Ctrl.RESET_USTEP

    # Stores from D
    if opcode == Opcode.STORE_D_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_D | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_D_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_D | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_D_TX: word[1] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_D | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_D | Ctrl.RESET_USTEP

    # Stores from TL
    if opcode == Opcode.STORE_TL_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TL_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TL_ABS:
        word[1] |= Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[4] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_CONST
        word[5] |= Ctrl.DBUS_ASSERT_CONST | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TL_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TL | Ctrl.RESET_USTEP

    # Stores from TH
    if opcode == Opcode.STORE_TH_X:  word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TH_Y:  word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TH_ABS:   # Store TH to abs address
        word[1] |= Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[4] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_CONST | Ctrl.RESET_USTEP
    if opcode == Opcode.STORE_TH_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TH | Ctrl.RESET_USTEP

    # Counter Reg Inc/Dec
    if opcode == Opcode.INC_X:  word[1] |= Ctrl.COUNT_INC_X | Ctrl.RESET_USTEP
    if opcode == Opcode.INC_Y:  word[1] |= Ctrl.COUNT_INC_Y | Ctrl.RESET_USTEP
    if opcode == Opcode.DEC_X:  word[1] |= Ctrl.COUNT_DEC_X | Ctrl.RESET_USTEP
    if opcode == Opcode.DEC_Y:  word[1] |= Ctrl.COUNT_DEC_Y | Ctrl.RESET_USTEP

    # Stack Pushes
    if opcode == Opcode.PUSH_A: word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_A | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_B: word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_B | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_C: word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_C | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_D: word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_D | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_TL:    word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TL | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_TH:    word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_TH | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP
    if opcode == Opcode.PUSH_SR:    word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_SR | Ctrl.COUNT_INC_SP | Ctrl.RESET_USTEP

    # Stack Pops
    if opcode == Opcode.POP_A:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_B:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_C:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_D:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_TL:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_TH:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.RESET_USTEP
    if opcode == Opcode.POP_SR:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_SR | Ctrl.RESET_USTEP

    # Jumps / Branches
    if opcode == Opcode.JMP_ABS:  # set PC to abs addr
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        word[3] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.JMP_TX: word[1] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.JMP_X:  word[1] |= Ctrl.XFER_ASSERT_X | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.JMP_Y:  word[1] |= Ctrl.XFER_ASSERT_Y | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP

    # NOTE: due to JSR_ABS, PC pushed to stack is PC - 1 for all JSR_xx
    if opcode == Opcode.JSR_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.XFER_ASSERT_PC | Ctrl.XFER_LOAD_TX
        word[3] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[4] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[5] |= Ctrl.DBUS_ASSERT_CONST | Ctrl.DBUS_LOAD_TL
        word[6] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[7] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC

    # NOTE: JSR_X and JSR_Y need to have dummy bytes injected immediately after their
    # opcodes in the instruction stream to ensure that the PC is off by 1 to match JSR_ABS.
    if opcode == Opcode.JSR_X:
        word[1] |= Ctrl.XFER_ASSERT_PC | Ctrl.XFER_LOAD_TX
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[3] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[4] |= Ctrl.XFER_ASSERT_X | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.JSR_Y:
        word[1] |= Ctrl.XFER_ASSERT_PC | Ctrl.XFER_LOAD_TX
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TL | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[3] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_TH | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[4] |= Ctrl.XFER_ASSERT_Y | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP

    # NOTE: due to JSR_ABS, PC pulled from stack is PC - 1
    if opcode == Opcode.RTS:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_DEC_SP
        word[3] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH
        word[4] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC
        word[5] |= Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP

    # Return from Interrupt - restore flags, PC, TX
    if opcode == Opcode.RTI:
        word[1] |= Ctrl.COUNT_DEC_SP
        word[2] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_DEC_SP
        word[3] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_DEC_SP
        word[4] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_SR
        word[5] |= Ctrl.XFER_ASSERT_Z | Ctrl.XFER_LOAD_TX | Ctrl.RESET_USTEP

    # Jump if Overflow (V = 1)
    if opcode == Opcode.JO_ABS:
        if v:
            word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
            word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
            word[3] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
        else:
            word[1] |= Ctrl.COUNT_INC_PC
            word[2] |= Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP
    if opcode == Opcode.JO_TX:
        if v:   word[1] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
        else:   word[1] |= Ctrl.RESET_USTEP
    if opcode == Opcode.JO_X:
        if v:   word[1] |= Ctrl.XFER_ASSERT_X | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
        else:   word[1] |= Ctrl.RESET_USTEP
    if opcode == Opcode.JO_Y:
        if v:   word[1] |= Ctrl.XFER_ASSERT_Y | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
        else:   word[1] |= Ctrl.RESET_USTEP

    # Jump If Greater / Jump If Not Less or Equal (Z = 0 and N = V)
    if opcode == Opcode.JG_ABS:
        if z == 0 and n == v:
            word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
            word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
            word[3] |= Ctrl.XFER_ASSERT_TX | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP
        else:
            word[1] |= Ctrl.COUNT_INC_PC
            word[2] |= Ctrl.COUNT_INC_PC | Ctrl.RESET_USTEP

    # Add without Carry with A and Store in A
    if opcode == Opcode.ADD_A_B: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_C: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_D: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # Add without Carry with B and Store in B
    if opcode == Opcode.ADD_B_A: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_C: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_D: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # Add without Carry with C and Store in C
    if opcode == Opcode.ADD_C_A: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_B: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_D: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # Add without Carry with D and Store in D
    if opcode == Opcode.ADD_D_A: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_B: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_C: word[1] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADD_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_ADD | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # Add with Carry into A
    if opcode == Opcode.ADC_A_B:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_A_C:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_A_D:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # Add with Carry into B
    if opcode == Opcode.ADC_B_A:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_B_C:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_B_D:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # Add with Carry into C
    if opcode == Opcode.ADC_C_A:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_C_B:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_C_D:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # Add with Carry into D
    if opcode == Opcode.ADC_D_A:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_D_B:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.ADC_D_C:    word[1] |= Ctrl.ALU_ADC | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # Sub without Borrow with A and Store in A
    if opcode == Opcode.SUB_A_B: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_C: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_D: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # Sub without Borrow with B and Store in B
    if opcode == Opcode.SUB_B_A: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_C: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_D: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # Sub without Borrow with C and Store in C
    if opcode == Opcode.SUB_C_A: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_B: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_D: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # Sub without Borrow with D and Store in D
    if opcode == Opcode.SUB_D_A: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_B: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_C: word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.SUB_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # GPR Increments
    if opcode == Opcode.INC_A:  word[1] |= Ctrl.ALU_INC | Ctrl.LHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.INC_B:  word[1] |= Ctrl.ALU_INC | Ctrl.LHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.INC_C:  word[1] |= Ctrl.ALU_INC | Ctrl.LHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.INC_D:  word[1] |= Ctrl.ALU_INC | Ctrl.LHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # GPR Decrements
    if opcode == Opcode.DEC_A:  word[1] |= Ctrl.ALU_DEC | Ctrl.LHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.DEC_B:  word[1] |= Ctrl.ALU_DEC | Ctrl.LHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.DEC_C:  word[1] |= Ctrl.ALU_DEC | Ctrl.LHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.DEC_D:  word[1] |= Ctrl.ALU_DEC | Ctrl.LHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # GPR Negations (2s complement)
    if opcode == Opcode.NEG_A:  word[1] |= Ctrl.ALU_NEG | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.NEG_B:  word[1] |= Ctrl.ALU_NEG | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.NEG_C:  word[1] |= Ctrl.ALU_NEG | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.NEG_D:  word[1] |= Ctrl.ALU_NEG | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # AND into A
    if opcode == Opcode.AND_A_B:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_C:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_D:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # AND into B
    if opcode == Opcode.AND_B_A:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_C:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_D:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # AND into C
    if opcode == Opcode.AND_C_A:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_B:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_D:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # AND into D
    if opcode == Opcode.AND_D_A:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_B:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_C:    word[1] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.AND_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # OR into A
    if opcode == Opcode.OR_A_B:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_C:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_D:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # OR into B
    if opcode == Opcode.OR_B_A:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_C:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_D:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_B_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # OR into C
    if opcode == Opcode.OR_C_A:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_B:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_D:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # OR into D
    if opcode == Opcode.OR_D_A:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_B:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_C:    word[1] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.OR_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_OR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # XOR into A
    if opcode == Opcode.XOR_A_A:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_A_B:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_A_C:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_A_D:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    # XOR into B
    if opcode == Opcode.XOR_B_A:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_B_B:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_B_C:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_B_D:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP

    # XOR into C
    if opcode == Opcode.XOR_C_A:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_B:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_D:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_C_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP

    # XOR into D
    if opcode == Opcode.XOR_D_A:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_B:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_C:    word[1] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP
    if opcode == Opcode.XOR_D_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_XOR | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_CONST | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # Logical NOTs
    if opcode == Opcode.NOT_A:  word[1] |= Ctrl.ALU_NOT | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.NOT_B:  word[1] |= Ctrl.ALU_NOT | Ctrl.LHS_ASSERT_B | Ctrl.RHS_ASSERT_B | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_B | Ctrl.RESET_USTEP
    if opcode == Opcode.NOT_C:  word[1] |= Ctrl.ALU_NOT | Ctrl.LHS_ASSERT_C | Ctrl.RHS_ASSERT_C | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_C | Ctrl.RESET_USTEP
    if opcode == Opcode.NOT_D:  word[1] |= Ctrl.ALU_NOT | Ctrl.LHS_ASSERT_D | Ctrl.RHS_ASSERT_D | Ctrl.DBUS_ASSERT_ALU | Ctrl.DBUS_LOAD_D | Ctrl.RESET_USTEP

    # Compare with A
    if opcode == Opcode.CMP_A_B:    word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_C:    word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_D:    word[1] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_IMM:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_X:
        word[1] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_Y:
        word[1] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.RESET_USTEP
    if opcode == Opcode.CMP_A_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ALU_SUB | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_CONST | Ctrl.RESET_USTEP

    if opcode == Opcode.TEST_A: word[1] |= Ctrl.ALU_AND | Ctrl.RHS_ASSERT_A | Ctrl.RHS_ASSERT_A | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_B: word[1] |= Ctrl.ALU_AND | Ctrl.RHS_ASSERT_B | Ctrl.RHS_ASSERT_B | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_C: word[1] |= Ctrl.ALU_AND | Ctrl.RHS_ASSERT_C | Ctrl.RHS_ASSERT_C | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_D: word[1] |= Ctrl.ALU_AND | Ctrl.RHS_ASSERT_D | Ctrl.RHS_ASSERT_D | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_ABS:
        word[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TL | Ctrl.COUNT_INC_PC
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TH | Ctrl.COUNT_INC_PC
        word[3] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_CONST
        word[4] |= Ctrl.ADDR_ASSERT_TX | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A
        word[5] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A
        word[6] |= Ctrl.DBUS_ASSERT_CONST | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_X:
        word[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ADDR_ASSERT_X | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A
        word[4] |= Ctrl.DBUS_ASSERT_CONST | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_Y:
        word[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_CONST
        word[2] |= Ctrl.ADDR_ASSERT_Y | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A
        word[3] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A
        word[4] |= Ctrl.DBUS_ASSERT_CONST | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP
    if opcode == Opcode.TEST_ZPG:
        word[1] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_MEM | Ctrl.COUNT_INC_SP
        word[2] |= Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST
        word[3] |= Ctrl.ADDR_ASSERT_ZPG | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A
        word[4] |= Ctrl.ALU_AND | Ctrl.LHS_ASSERT_A | Ctrl.RHS_ASSERT_A | Ctrl.COUNT_DEC_SP
        word[5] |= Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RESET_USTEP

    if word == base:
        global need_implementation_count
        need_implementation_count += 1

    return word

# This function is incomplete, but the idea is to ensure that the produced ucode
# for any instruction doesn't violate certain hardware rules in how my control system
# is built. It's also called by code below.
def check_rules(uop):
    # Cant increment and xfer load same counter reg at once
    xfer_load_enc = (uop >> 19) & 0b111
    cntr_inc_enc = (uop >> 25) & 0b111

    if xfer_load_enc in range(1, 4) and xfer_load_enc == cntr_inc_enc:
        return False

    # TODO: Cant load TX from multiple sources at once
    # TODO: Cant use RHS extended asserts while doing XFER LOAD
    # TODO: Cant clear RST state while incrementing counter reg
    # TODO: Cant break out of free run while incrementing counter reg
    # TODO: Last working step has RESET_USTEP
    # TODO: Dec or Inc when using SP
    # TODO: Inc when using PC
    return True


# Here is the MSB -> LSB ordering of the 19 state inputs to the control unit.
# RESET IRQ EX OPCODE FLAGS STEP
# 1     1   1  8      5     3

# Here we call the above monster function to build the ucode for all the possible
# contorl unit addresses.
# Note that there are 19 state inputs, but I only loop from 0 to 2^16. This is because
# the lowest 3 bits are the Tstate. That means each time this loop iterates, it can
# be thought of as the next T0 in the address range, which is every 8 clocks. So the
# opcode function above will produce the 8 values that need to be filled in-between.
ucode = []
for addr in range(2 ** 16):
    # From the address we use bit masking and shifting to extract the appropriate
    # values for each state input
    reset = (addr & 0b1000000000000000) >> 15
    irq = (addr & 0b0100000000000000) >> 14
    ext = (addr & 0b0010000000000000) >> 13
    mcode = (addr & 0b0001111111100000) >> 5
    flags = (addr & 0b0000000000011111) >> 0

    # Then we call the opcode function with them.
    uops = compute_uops(reset, irq, mcode | ext << 8, flags)

    # If the produced ucode passes all the rules, we extend the ucode list with them.
    # recall the check function doesn't currently do much.
    if all(check_rules(uop) for uop in uops):
        ucode.extend(uops)
    else:
        print(f"uop for {addr} did not pass rule checks.")
        for uop in uops:
            print(uop)

if len(ucode) > 2 ** 19:
    print("Too much ucode; probably the result of too many opcodes")

# I've commented out the code below, as it will write to your harddisk the produced
# opcode binaries. Feel free to experiment with it though...

# rom0_ucode = [(word & (255 << 0)) >> 0 for word in ucode]
# rom1_ucode = [(word & (255 << 1)) >> 1 for word in ucode]
# rom2_ucode = [(word & (255 << 2)) >> 2 for word in ucode]
# rom3_ucode = [(word & (255 << 3)) >> 3 for word in ucode]

# spi_ucode = []
# spi_ucode.extend(rom0_ucode)
# spi_ucode.extend(rom1_ucode)
# spi_ucode.extend(rom2_ucode)
# spi_ucode.extend(rom3_ucode)

# handles = [
#     ("control_0.bin", rom0_ucode, "big"),
#     ("control_1.bin", rom1_ucode, "big"),
#     ("control_2.bin", rom2_ucode, "big"),
#     ("control_3.bin", rom3_ucode, "big"),
#     ("control_spi.bin", spi_ucode, "little")
# ]

# for name, data, order in handles:
#     with open(name, "wb") as f:
#         for word in data:
#             f.write(word.to_bytes(1, byteorder=order))

# with open("control_wide.bin", "wb") as f:
#     for word in ucode:
#         f.write(word.to_bytes(4, byteorder="big"))

print(f"Need implementations for this many: {need_implementation_count}")
