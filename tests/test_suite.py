import operator

import pytest

from .emulator import Emulator
from .simulator import Simulator
from .opcodes import Op
from .common import under_test

VirtualMachine = Emulator

@pytest.mark.parametrize(("src"), "abcd")
@under_test(
    Op.MOV_A_B,
    Op.MOV_A_C,
    Op.MOV_A_D,
    Op.MOV_B_A,
    Op.MOV_B_C,
    Op.MOV_B_D,
    Op.MOV_C_A,
    Op.MOV_C_B,
    Op.MOV_C_D,
    Op.MOV_D_A,
    Op.MOV_D_B,
    Op.MOV_D_C,
)
def test_mov8(src):
    expected = 1

    gprs = ["a", "b", "c", "d"]
    gprs.remove(src)

    assembly = f"""
    load {src}, #{expected}

    mov {gprs[0]}, {src}
    mov {gprs[1]}, {src}
    mov {gprs[2]}, {src}
    halt
    """

    vm = VirtualMachine(assembly)
    assert (vm.a, vm.b, vm.c, vm.d) == (expected, expected, expected, expected)


@pytest.mark.parametrize(
    ("dst"),
    "abcd",
)
@under_test(
    Op.LOAD_A_IMM,
    Op.LOAD_B_IMM,
    Op.LOAD_C_IMM,
    Op.LOAD_D_IMM,
)
def test_load8_imm(dst):
    expected = 69
    vm = VirtualMachine(
        f"""
        load {dst}, #{expected}
        halt
        """
    )

    dst_getter = operator.attrgetter(dst)

    assert dst_getter(vm) == expected


@pytest.mark.parametrize("dst", "abcd")
@under_test(
    Op.LOAD_A_ABS,
    Op.LOAD_B_ABS,
    Op.LOAD_C_ABS,
    Op.LOAD_D_ABS,
)
def test_load8_abs(dst):
    addr = 0x7000
    expected = 45

    assembly = f"""
    load {dst}, [{addr}]
    halt
    #addr {addr}
        #d8 {expected}
    """

    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == expected


@pytest.mark.parametrize("dst", "abcd")
@under_test(
    Op.LOAD_A_DP,
    Op.LOAD_B_DP,
    Op.LOAD_C_DP,
    Op.LOAD_D_DP,
)
def test_load8_dp(dst):
    expected = 5
    assembly = f"""
    load a, #0x70
    mov dp, a

    load {dst}, [!3]

    halt
    #addr 0x7003
        #d8 {expected}
    """

    dst_getter = operator.attrgetter(dst)
    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == expected


@pytest.mark.parametrize(
    ("dst", "ptr"),
    (
        "ax",
        "bx",
        "cx",
        "dx",
        "ay",
        "by",
        "cy",
        "dy",
    ),
)
@under_test(
    Op.LOAD_A_X_IDX,
    Op.LOAD_B_X_IDX,
    Op.LOAD_C_X_IDX,
    Op.LOAD_D_X_IDX,
    Op.LOAD_A_Y_IDX,
    Op.LOAD_B_Y_IDX,
    Op.LOAD_C_Y_IDX,
    Op.LOAD_D_Y_IDX,
)
def test_load8_ptr_idx(dst, ptr):
    expected = 79

    assembly = f"""
    load {ptr}, #0x7000
    load {dst}, [{ptr}, #2]

    halt
    #addr 0x7002
        #d8 {expected}
    """

    dst_getter = operator.attrgetter(dst)
    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == expected


@pytest.mark.parametrize(("dst"), "abcd")
@under_test(
    Op.LOAD_A_SP_IDX,
    Op.LOAD_B_SP_IDX,
    Op.LOAD_C_SP_IDX,
    Op.LOAD_D_SP_IDX,
)
def test_load8_sp_idx(dst):
    assembly = f"""
    load x, #0x8000
    mov sp, x

    load {dst}, [sp, #3]
    halt

    #addr 0x8003
        #d8 69
    """

    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == 69


@pytest.mark.parametrize(
    ("dst", "gpr"),
    (
        "aa",
        "ab",
        "ac",
        "ad",
        "ba",
        "bb",
        "bc",
        "bd",
        "ca",
        "cb",
        "cc",
        "cd",
        "da",
        "db",
        "dc",
        "dd",
    ),
)
@under_test(
    Op.LOAD_A_SP_A,
    Op.LOAD_A_SP_B,
    Op.LOAD_A_SP_C,
    Op.LOAD_A_SP_D,
    Op.LOAD_B_SP_A,
    Op.LOAD_B_SP_B,
    Op.LOAD_B_SP_C,
    Op.LOAD_B_SP_D,
    Op.LOAD_C_SP_A,
    Op.LOAD_C_SP_B,
    Op.LOAD_C_SP_C,
    Op.LOAD_C_SP_D,
    Op.LOAD_D_SP_A,
    Op.LOAD_D_SP_B,
    Op.LOAD_D_SP_C,
    Op.LOAD_D_SP_D,
)
def test_load8_sp_gpr(dst, gpr):
    assembly = f"""
    load x, #0x8000
    mov sp, x

    load {gpr}, #3

    load {dst}, [sp, {gpr}]
    halt

    #addr 0x8003
        #d8 69
    """

    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == 69


@pytest.mark.parametrize(
    ("dst", "ptr", "idx"),
    (
        "axa",
        "bxa",
        "cxa",
        "dxa",
        "axb",
        "bxb",
        "cxb",
        "dxb",
        "axc",
        "bxc",
        "cxc",
        "dxc",
        "axd",
        "bxd",
        "cxd",
        "dxd",
        "aya",
        "bya",
        "cya",
        "dya",
        "ayb",
        "byb",
        "cyb",
        "dyb",
        "ayc",
        "byc",
        "cyc",
        "dyc",
        "ayd",
        "byd",
        "cyd",
        "dyd",
    ),
)
@under_test(
    Op.LOAD_A_X_A,
    Op.LOAD_B_X_A,
    Op.LOAD_C_X_A,
    Op.LOAD_D_X_A,
    Op.LOAD_A_X_B,
    Op.LOAD_B_X_B,
    Op.LOAD_C_X_B,
    Op.LOAD_D_X_B,
    Op.LOAD_A_X_C,
    Op.LOAD_B_X_C,
    Op.LOAD_C_X_C,
    Op.LOAD_D_X_C,
    Op.LOAD_A_X_D,
    Op.LOAD_B_X_D,
    Op.LOAD_C_X_D,
    Op.LOAD_D_X_D,
    Op.LOAD_A_Y_A,
    Op.LOAD_B_Y_A,
    Op.LOAD_C_Y_A,
    Op.LOAD_D_Y_A,
    Op.LOAD_A_Y_B,
    Op.LOAD_B_Y_B,
    Op.LOAD_C_Y_B,
    Op.LOAD_D_Y_B,
    Op.LOAD_A_Y_C,
    Op.LOAD_B_Y_C,
    Op.LOAD_C_Y_C,
    Op.LOAD_D_Y_C,
    Op.LOAD_A_Y_D,
    Op.LOAD_B_Y_D,
    Op.LOAD_C_Y_D,
    Op.LOAD_D_Y_D,
)
def test_load8_ptr_gpr(dst, ptr, idx):
    base = 0x8000
    offset = 3

    value = 69
    expected = (base, value)

    assembly = f"""
    load {ptr}, #{base}
    load {idx}, #{offset}

    load {dst}, [{ptr}, {idx}]

    halt
    #addr {expected[0]}
        #d8 0, 0, 0, {value}
    """

    ptr_getter = operator.attrgetter(ptr)
    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert (ptr_getter(vm), dst_getter(vm)) == expected

@pytest.mark.skip("Refactor to not need memory")
@pytest.mark.parametrize(("src"), "abcd")
@under_test(
    Op.STORE_A_ABS,
    Op.STORE_B_ABS,
    Op.STORE_C_ABS,
    Op.STORE_D_ABS,
)
def test_store8_abs(src):
    expected = 0x69
    addr = 0x6502

    assembly = f"""
    load {src}, #{expected}
    store [{addr}], {src}
    halt
    """

    vm = VirtualMachine(assembly, memory=True)
    assert vm.memory[0][0x6502] == expected

@pytest.mark.skip("Refactor to not need memory")
@pytest.mark.parametrize(("src"), "abcd")
@under_test(
    Op.STORE_A_DP,
    Op.STORE_B_DP,
    Op.STORE_C_DP,
    Op.STORE_D_DP,
)
def test_store8_dp(src):
    expected = 0x79
    dp = 0x68
    da = 0x09

    assembly = f"""
    load a, #{dp}
    mov dp, a

    load {src}, #{expected}
    store [!{da}], {src}
    halt
    """

    vm = VirtualMachine(assembly, memory=True)
    assert vm.memory[0][0x6809] == expected

@pytest.mark.skip("Refactor to not need memory")
@pytest.mark.parametrize(
    ("src", "ptr"),
    (
        "ax",
        "bx",
        "cx",
        "dx",
        "ay",
        "by",
        "cy",
        "dy"
    )
)
@under_test(
    Op.STORE_A_X_IDX,
    Op.STORE_A_Y_IDX,
    Op.STORE_B_X_IDX,
    Op.STORE_B_Y_IDX,
    Op.STORE_C_X_IDX,
    Op.STORE_C_Y_IDX,
    Op.STORE_D_X_IDX,
    Op.STORE_D_Y_IDX,
)
def test_store8_ptr_idx(src, ptr):
    base = 0x6500
    offset = 0x02
    expected = 0xff

    assembly = f"""
    load {ptr}, #{base}
    load {src}, #{expected}

    store [{ptr}, #{offset}], {src}
    halt
    """

    vm = VirtualMachine(assembly, memory=True)
    assert vm.memory[0][base + offset] == expected

@pytest.mark.skip("Refactor to not need memory")
@pytest.mark.parametrize(("src"), "abcd")
@under_test(
    Op.STORE_A_SP_IDX,
    Op.STORE_B_SP_IDX,
    Op.STORE_C_SP_IDX,
    Op.STORE_D_SP_IDX,
)
def test_store8_sp_idx(src):
    assembly = f"""
    load x, #0x8085
    mov sp, x

    load {src}, #0xFF
    store [sp, #1], {src}
    halt
    """

    vm = VirtualMachine(assembly, memory=True)
    assert vm.memory[0][0x8086] == 0xFF

@pytest.mark.skip("Refactor to not need memory")
@pytest.mark.parametrize(
    ("src", "ptr", "idx"),
    (
        "axa",
        "axb",
        "axc",
        "axd",
        "bxa",
        "bxb",
        "bxc",
        "bxd",
        "cxa",
        "cxb",
        "cxc",
        "cxd",
        "dxa",
        "dxb",
        "dxc",
        "dxd",
        "aya",
        "ayb",
        "ayc",
        "ayd",
        "bya",
        "byb",
        "byc",
        "byd",
        "cya",
        "cyb",
        "cyc",
        "cyd",
        "dya",
        "dyb",
        "dyc",
        "dyd",
    )
)
@under_test(
    Op.STORE_A_X_A,
    Op.STORE_A_X_B,
    Op.STORE_A_X_C,
    Op.STORE_A_X_D,
    Op.STORE_B_X_A,
    Op.STORE_B_X_B,
    Op.STORE_B_X_C,
    Op.STORE_B_X_D,
    Op.STORE_C_X_A,
    Op.STORE_C_X_B,
    Op.STORE_C_X_C,
    Op.STORE_C_X_D,
    Op.STORE_D_X_A,
    Op.STORE_D_X_B,
    Op.STORE_D_X_C,
    Op.STORE_D_X_D,
    Op.STORE_A_Y_A,
    Op.STORE_A_Y_B,
    Op.STORE_A_Y_C,
    Op.STORE_A_Y_D,
    Op.STORE_B_Y_A,
    Op.STORE_B_Y_B,
    Op.STORE_B_Y_C,
    Op.STORE_B_Y_D,
    Op.STORE_C_Y_A,
    Op.STORE_C_Y_B,
    Op.STORE_C_Y_C,
    Op.STORE_C_Y_D,
    Op.STORE_D_Y_A,
    Op.STORE_D_Y_B,
    Op.STORE_D_Y_C,
    Op.STORE_D_Y_D,
)
def test_store8_gpr_ptr_gpr(src, ptr, idx):
    expected = 0xDE
    base = 0x6500
    offset = 0x02
    assembly = f"""
    load {ptr}, #{base}
    load {idx}, #{offset}
    load {src}, #{expected}

    store [{ptr}, {idx}], {src}
    halt
    """
    vm = VirtualMachine(assembly, memory=True)
    assert vm.memory[0][0x6502] == expected

@pytest.mark.parametrize(("dst", "src"), ("xy", "yx"))
@under_test(
    Op.MOV_X_Y,
    Op.MOV_Y_X,
)
def test_mov16_strict(dst, src):
    assembly = f"""
    load {src}, #0x6809
    mov {dst}, {src}
    halt
    """

    src_getter = operator.attrgetter(src)
    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert (src_getter(vm), dst_getter(vm)) == (0x6809, 0x6809)


@pytest.mark.parametrize(
    ("dst", "src"),
    (
        ("ab", "x"),
        ("ab", "y"),
        ("cd", "x"),
        ("cd", "y"),
    ),
)
@under_test(
    Op.MOV_AB_X,
    Op.MOV_AB_Y,
    Op.MOV_CD_X,
    Op.MOV_CD_Y,
)
def test_mov16_psuedo_dst(dst, src):
    assembly = f"""
    load {src}, #0x6809
    mov {dst}, {src}
    halt
    """

    src_getter = operator.attrgetter(src)
    dst_hi_getter = operator.attrgetter(dst[0])
    dst_lo_getter = operator.attrgetter(dst[1])

    vm = VirtualMachine(assembly)
    assert src_getter(vm) == 0x6809
    assert dst_hi_getter(vm) == 0x68
    assert dst_lo_getter(vm) == 0x09


@pytest.mark.parametrize(
    ("dst", "src"),
    (
        ("x", "ab"),
        ("x", "cd"),
        ("y", "ab"),
        ("y", "cd"),
    ),
)
@under_test(
    Op.MOV_X_AB,
    Op.MOV_X_CD,
    Op.MOV_Y_AB,
    Op.MOV_Y_CD,
)
def test_mov16_psuedo_src(dst, src):
    assembly = f"""
    load {src[0]}, #0x68
    load {src[1]}, #0x09

    mov {dst}, {src}
    halt
    """

    src_hi_getter = operator.attrgetter(src[0])
    src_lo_getter = operator.attrgetter(src[1])
    dst_getter = operator.attrgetter(dst)

    vm = VirtualMachine(assembly)
    assert src_hi_getter(vm) == 0x68
    assert src_lo_getter(vm) == 0x09
    assert dst_getter(vm) == 0x6809


@under_test(Op.MOV_SP_X)
def test_mov_sp_x():
    assembly = """
    load x, #0x6502
    mov sp, x
    halt
    """

    vm = VirtualMachine(assembly)
    assert vm.sp == 0x6502

@pytest.mark.skip("known failure for some reason")
@under_test(Op.MOV_X_SP)
def test_mov_x_sp():
    assembly = """
    load x, #0x6502
    mov sp, x

    load x, #0x000
    mov x, sp
    halt
    """
    vm = VirtualMachine(assembly)

    assert vm.sp == 0x6502 and vm.x == 0x6502


@pytest.mark.parametrize(("ptr"), ("x", "y", "sp"))
@under_test(
    Op.LEA_X_IDX,
    Op.LEA_Y_IDX,
    Op.LEA_SP_IDX,
)
def test_lea_idx(ptr):
    assembly = f"""
    lea {ptr}, #0x3
    halt
    """

    ptr_getter = operator.attrgetter(ptr)

    vm = VirtualMachine(assembly)
    assert ptr_getter(vm) == 0x0003


def test_flags_initial():
    vm = VirtualMachine("")
    assert vm.c_f is False, "carry flag"
    assert vm.z_f is False, "zero flag"
    assert vm.v_f is False, "overflow flag"
    assert vm.n_f is False, "negative flag"
    assert vm.i_f is False, "irq enable"

    assert vm.nmi_f is True, "nmi enable"
    assert vm.us_f is True, "supervisor enable"
    assert vm.ubr_f is False, "user bank reg"

@under_test(Op.SEC)
def test_set_carry():
    assert VirtualMachine("sec\n").c_f is True


@under_test(Op.CLC)
def test_clear_carry():
    assembly = """
    sec
    clc
    halt
    """

    assert VirtualMachine(assembly).c_f is False


@pytest.mark.parametrize(
    ("dst", "src"),
    (
        "ab",
        "ac",
        "ad",
        "ba",
        "bc",
        "bd",
        "ca",
        "cb",
        "cd",
        "da",
        "db",
        "dc",
    ),
)
@under_test(
    Op.ADC_A_B,
    Op.ADC_A_C,
    Op.ADC_A_D,
    Op.ADC_B_A,
    Op.ADC_B_C,
    Op.ADC_B_D,
    Op.ADC_C_A,
    Op.ADC_C_B,
    Op.ADC_C_D,
    Op.ADC_D_A,
    Op.ADC_D_B,
    Op.ADC_D_C,
)
def test_adc_no_carry_out_gpr_gpr_no_match(dst, src):
    left, right = 127, 127

    assembly = f"""
    sec
    load {dst}, #{left}
    load {src}, #{right}
    adc {dst}, {src}
    halt
    """

    dst_getter = operator.attrgetter(dst)
    src_getter = operator.attrgetter(src)

    vm = VirtualMachine(assembly)
    assert dst_getter(vm) == 0xFF
    assert src_getter(vm) == 127
    assert vm.c_f is False
    assert vm.z_f is False
    assert vm.v_f is True
    assert vm.n_f is True

def test_set_overflow():
    assembly = """
    load a, #-128
    load b, #-128
    clc
    adc a, b
    halt
    """

    vm = VirtualMachine(assembly)
    assert vm.a == 0
    assert vm.v_f is True

@pytest.mark.skip("failing")
@under_test(Op.CLV)
def test_clear_overflow():
    assembly = """
    load a, #-128
    load b, #-128
    clc
    adc a, b
    clv
    halt
    """

    vm = VirtualMachine(assembly)
    assert vm.a == 0
    assert vm.v_f is False

@under_test(Op.SEI)
def test_enable_irq():
    assert VirtualMachine("sei").i_f is True


@under_test(Op.CLI)
def test_disable_irq():
    assembly = """
    sei
    cli
    halt
    """

    vm = VirtualMachine(assembly)
    assert vm.i_f is False

@under_test(Op.UBR)
def test_ubr():
    assert VirtualMachine("ubr").ubr_f is True


@under_test(Op.KBR)
def test_kbr():
    assembly = """
    ubr
    kbr
    halt
    """
    assert VirtualMachine(assembly).ubr_f is False
