import json
from dataclasses import dataclass
import itertools as it

from new_control_lines import Ctrl

c_mask = 0b10000
z_mask = 0b01000
v_mask = 0b00100 
n_mask = 0b00010
i_mask = 0b00001

fetch = Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_IR | Ctrl.COUNT_INC_PC

base = [fetch, 0, 0, 0, 0, 0, 0, Ctrl.RESET_USTEP]

rst_uops = [
    Ctrl.XFER_ASSERT_RST | Ctrl.XFER_LOAD_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TEMP | Ctrl.COUNT_INC_PC,
    Ctrl.XFER_ASSERT_CONST_TEMP | Ctrl.XFER_LOAD_PC | Ctrl.CLEAR_RESET | Ctrl.RESET_USTEP,
    0,
    0,
    0,
    0,
]

irq_uops = [
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_SR | Ctrl.COUNT_INC_SP | Ctrl.ALU_SEI,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_ALU | Ctrl.XFER_ASSERT_PC | Ctrl.ALU_RHS | Ctrl.COUNT_INC_SP,
    Ctrl.ADDR_ASSERT_SP | Ctrl.DBUS_LOAD_MEM | Ctrl.DBUS_ASSERT_ALU | Ctrl.XFER_ASSERT_PC | Ctrl.ALU_LHS | Ctrl.COUNT_INC_SP,
    Ctrl.XFER_ASSERT_ISR | Ctrl.XFER_LOAD_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_CONST | Ctrl.COUNT_INC_PC,
    Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_TEMP | Ctrl.COUNT_INC_PC,
    Ctrl.XFER_ASSERT_CONST_TEMP | Ctrl.XFER_LOAD_PC | Ctrl.RESET_USTEP,
    0,
]

def compute_uops(reset: int, irq: int, opcode: int, flags: int) -> list[int]:
    word = base.copy()

    c = (flags & c_mask) >> 4  # Carry Flag
    z = (flags & z_mask) >> 3  # Zero Flag
    v = (flags & v_mask) >> 2  # Overflow Flag
    n = (flags & n_mask) >> 1  # Negative Flag
    i = (flags & i_mask) >> 0  # Interrupt Inhibit Flag

    if reset:   return rst_uops
    if irq and not i:   return irq_uops

    # CPU Config
    if opcode.name == "NOP":    word[1] |= Ctrl.RESET_USTEP
    if opcode.name == "BREAK":  word[1] |= Ctrl.BREAK | Ctrl.RESET_USTEP
    if opcode.name == "EXTEND": word[1] |= Ctrl.EXTENDED_OP_FLIP | Ctrl.RESET_USTEP

@dataclass
class Opcode:
    name: str
    desc: str
    length: int
    mode: str
    alu_op: str
    extended: bool = False

def build_opcodes(fname: str) -> list[Opcode]:
    with open(fname, "r") as f:
        inst = json.load(f)

    opcodes = []
    for mnemonic in inst:
        modes = inst[mnemonic].get("modes", dict())
        inst_alu_op = inst[mnemonic].get("alu_op", "alu_nop")

        for mode in modes:
            count = modes[mode].get("operand_ct", 0)
            length = modes[mode].get("bytes", 0)
            alu_op = modes[mode].get("alu_op", inst_alu_op)

            if count == 0:
                # mode may be:
                # absolute -> mnemonic_abs
                # implied -> mnemonic
                # zeropage -> mnemonic_zpg
                name = mnemonic.upper()
                if mode == "absolute":
                    name += "_ABS"
                elif mode == "zeropage":
                    name += "_ZPG"

                opcode = Opcode(
                    name=name,
                    desc=inst[mnemonic].get("desc", ""),
                    length=length,
                    mode=mode,
                    alu_op=alu_op,
                )
                opcodes.append(opcode)

            if count == 1:
                # mode may be:
                # implied-immediate -> mnemonic_op_imm
                # implied-absolute -> mnemonic_op_abs
                # implied-zeropage -> mnemonic_op_zpg
                # implied-stackrel -> mnemonic_op_rel
                # implied / implied_8 / implied_16 -> mnemonic_op
                # indirect -> mnemonic_op
                operands = modes[mode].get("operands", [[]])[0]

                for operand in operands:
                    name = f"{mnemonic}_{operand}".upper()

                    if mode == "implied-immediate":
                        name += "_IMM"
                    elif mode == "implied-absolute":
                        name += "_ABS"
                    elif mode == "implied-zeropage":
                        name += "_ZPG"
                    elif mode == "implied-stackrel":
                        name += "_SPREL"

                    opcode = Opcode(
                        name=name,
                        desc=inst[mnemonic].get("desc", ""),
                        length=length,
                        mode=mode,
                        alu_op=alu_op,
                    )
                    opcodes.append(opcode)

            if count == 2:
                # mode may be:
                # implied-implied8 -> mnemonic_op1_op2
                # implied-implied16 -> mnemonic_op1_op2
                # implied-indirect -> mnemonic_op1_op2
                # implied-implied -> mnemonic_op1_op2
                operands = modes[mode].get("operands", [[], []])
                repeat = modes[mode].get("repeat_operands", True)

                for lhs, rhs in it.product(*operands):
                    if lhs == rhs and not repeat:
                        continue

                    name = f"{mnemonic}_{lhs}_{rhs}".upper()

                    opcode = Opcode(
                        name=name,
                        desc=inst[mnemonic].get("desc", ""),
                        length=length,
                        mode=mode,
                        alu_op=alu_op,
                    )
                    opcodes.append(opcode)

    return opcodes

def build_ucode(opcodes: list[Opcode]):
    ucode = []
    for addr in range(2 ** 16):
        reset = (addr & 0b1000000000000000) >> 15
        irq = (addr & 0b0100000000000000) >> 14
        ext = (addr & 0b0010000000000000) >> 13
        mcode = (addr & 0b0001111111100000) >> 5
        flags = (addr & 0b0000000000011111) >> 0

        ucode = []
        try:
            opcode = opcodes[mcode]
        except IndexError:
            opcode = opcodes[0]

        opcode = opcode | (ext << 8)
        uops = compute_uops(reset, irq, opcode, flags)
        ucode.extend(uops)

    return ucode


if __name__ == "__main__":
    opcodes = build_opcodes("instructions.json")
    ucode = build_ucode(opcodes)
