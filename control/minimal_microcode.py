import microcode as uc
from minimal_opcodes import Op


Ctrl = uc.Ctrl

def get_uops(flags: uc.Flags, op: int, mode: uc.Op) -> list[int]:
    uops = uc.BASE.copy()

    if op == Op.NOP:
        uops[1] |= Ctrl.RST_USEQ
    elif op == Op.BRK:
        uops[1] |= Ctrl.BRK_CLK
        uops[2] |= Ctrl.RST_USEQ

    elif op == Op.CLC:
        uops[1] |= Ctrl.ALU_CLC | Ctrl.RST_USEQ

    elif op == Op.MOV_A_B:
        return uc.mov8(uc.GPR.A, uc.GPR.B)
    elif op == Op.MOV_A_C:
        return uc.mov8(uc.GPR.A, uc.GPR.C)
    elif op == Op.MOV_A_D:
        return uc.mov8(uc.GPR.A, uc.GPR.D)
    elif op == Op.MOV_B_A:
        return uc.mov8(uc.GPR.B, uc.GPR.A)
    elif op == Op.MOV_B_C:
        return uc.mov8(uc.GPR.B, uc.GPR.C)
    elif op == Op.MOV_B_D:
        return uc.mov8(uc.GPR.B, uc.GPR.D)
    elif op == Op.MOV_C_A:
        return uc.mov8(uc.GPR.C, uc.GPR.A)
    elif op == Op.MOV_C_B:
        return uc.mov8(uc.GPR.C, uc.GPR.B)
    elif op == Op.MOV_C_D:
        return uc.mov8(uc.GPR.C, uc.GPR.D)
    elif op == Op.MOV_D_A:
        return uc.mov8(uc.GPR.D, uc.GPR.A)
    elif op == Op.MOV_D_B:
        return uc.mov8(uc.GPR.D, uc.GPR.B)
    elif op == Op.MOV_D_C:
        return uc.mov8(uc.GPR.D, uc.GPR.C)

    elif op == Op.MOV_A_DP:
        uops[1] |= Ctrl.DBUS_ASSERT_DP | Ctrl.DBUS_LOAD_A | Ctrl.RST_USEQ
    elif op == Op.MOV_DP_A:
        uops[1] |= Ctrl.DBUS_ASSERT_A | Ctrl.DBUS_LOAD_DP | Ctrl.RST_USEQ

    elif op == Op.LOAD_A_IMM:
        return uc.load8_imm(uc.GPR.A)
    elif op == Op.LOAD_B_IMM:
        return uc.load8_imm(uc.GPR.B)
    elif op == Op.LOAD_C_IMM:
        return uc.load8_imm(uc.GPR.C)
    elif op == Op.LOAD_D_IMM:
        return uc.load8_imm(uc.GPR.D)

    elif op == Op.ADC_A_B:
        return uc.binop_gpr_gpr(uc.BinOp.ADC, uc.GPR.A, uc.GPR.B)

    elif op == Op.AND_A_B:
        return uc.binop_gpr_gpr(uc.BinOp.AND, uc.GPR.A, uc.GPR.B)

    else:
        return [-1]

    return uops



def main() -> None:
    # 18b of state input:
    # 2b MODE, 1b EXT, 8b OP, 4b flags, 3b t-state

    ucode = []
    for addr in range(2**15):
        flags_packed = (addr >> 0) & 0b1111
        OP = (addr >> 4) & 0b1111_1111
        EXT = (addr >> 12) & 0b1
        MODE = (addr >> 13) & 0b11

        Nf = bool((flags_packed >> 3) & 8)
        Vf = bool((flags_packed >> 2) & 4)
        Zf = bool((flags_packed >> 1) & 2)
        Cf = bool((flags_packed >> 0) & 1)

        flags = uc.Flags(Nf, Vf, Zf, Cf)
        mode = uc.Mode.FETCH
        opcode = OP

        uops = get_uops(flags, opcode, mode)

        if uops[0] == -1:
            uops = uc.get_uops(flags, Op.NOP, mode)

        ucode.extend(uops)

    uc.write_ucode(ucode, "minimal_microcode{}.bin")


if __name__ == "__main__":
    main()
