import pytest

from emulator import Emulator, under_test, OPCODES
from opcodes import Op


@pytest.fixture(scope='session', autouse=True)
def opcode_reporter():
    yield
    print(len(OPCODES))

@under_test(
    Op.MOV_B_A,
    Op.MOV_C_A,
    Op.MOV_D_A,
)
def test_mov8_from_a():
    expected_bcd = 1

    assembly = f"""
    load a, #{expected_bcd}

    mov b, a
    mov c, a
    mov d, a
    """

    emu = Emulator(assembly)
    assert (emu.b, emu.c, emu.d) == (expected_bcd, expected_bcd, expected_bcd)

@under_test(
    Op.MOV_A_B,
    Op.MOV_C_B,
    Op.MOV_D_B,
)
def test_mov8_from_b():
    expected_acd = 1

    assembly = f"""
    load b, #{expected_acd}

    mov a, b
    mov c, b
    mov d, b
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.c, emu.d) == (expected_acd, expected_acd, expected_acd)

@under_test(
    Op.MOV_A_C,
    Op.MOV_B_C,
    Op.MOV_D_C,
)
def test_mov8_from_c():
    expected_abd = 1

    assembly = f"""
    load c, #{expected_abd}

    mov a, c
    mov b, c
    mov d, c
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.d) == (expected_abd, expected_abd, expected_abd)

@under_test(
    Op.MOV_A_D,
    Op.MOV_B_D,
    Op.MOV_C_D,
)
def test_mov8_from_d():
    expected = 1

    assembly = f"""
    load d, #{expected}

    mov a, d
    mov b, d
    mov c, d
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.c) == (expected, expected, expected)

@under_test(
    Op.LOAD_A_IMM,
    Op.LOAD_B_IMM,
    Op.LOAD_C_IMM,
    Op.LOAD_D_IMM,
)
def test_load8_imm():
    expected = (69, 70, 71, 72)

    assembly = f"""
    load a, #{expected[0]}
    load b, #{expected[1]}
    load c, #{expected[2]}
    load d, #{expected[3]}
    """

    emu = Emulator(assembly)

    assert (emu.a, emu.b, emu.c, emu.d) == expected

@under_test(
    Op.LOAD_A_ABS,
    Op.LOAD_B_ABS,
    Op.LOAD_C_ABS,
    Op.LOAD_D_ABS,
)
def test_load8_abs():
    expected = (255, 254, 253, 252)

    assembly = f"""
    load a, [0x8000]
    load b, [0x8001]
    load c, [0x8002]
    load d, [0x8003]
    halt
    #addr 0x8000
        #d8 {expected[0]}
        #d8 {expected[1]}
        #d8 {expected[2]}
        #d8 {expected[3]}
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d) == expected

@under_test(
    Op.LOAD_A_DP,
    Op.LOAD_B_DP,
    Op.LOAD_C_DP,
    Op.LOAD_D_DP,
)
def test_load8_dp():
    expected = (2, 3, 4, 5)

    assembly = f"""
    load a, #0x80
    mov dp, a

    load a, [!0]
    load b, [!1]
    load c, [!2]
    load d, [!3]

    halt
    #addr 0x8000
        #d8 {expected[0]}
        #d8 {expected[1]}
        #d8 {expected[2]}
        #d8 {expected[3]}
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d) == expected

@under_test(
    Op.LOAD_A_X_IDX,
    Op.LOAD_B_X_IDX,
    Op.LOAD_C_X_IDX,
    Op.LOAD_D_X_IDX,
)
def test_load8_ptr_x_idx():
    expected = (255, 254, 253, 252, 0x8000)

    assembly = f"""
    load x, #{expected[4]}
    load a, [x, #0]
    load b, [x, #1]
    load c, [x, #2]
    load d, [x, #3]
    halt
    #addr 0x8000
        #d8 {expected[0]}
        #d8 {expected[1]}
        #d8 {expected[2]}
        #d8 {expected[3]}
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d, emu.x) == expected

@under_test(
    Op.LOAD_A_Y_IDX,
    Op.LOAD_B_Y_IDX,
    Op.LOAD_C_Y_IDX,
    Op.LOAD_D_Y_IDX,
)
def test_load8_ptr_y_idx():
    expected = (255, 254, 253, 252, 0x8000)

    assembly = f"""
    load y, #{expected[4]}
    load a, [y, #0]
    load b, [y, #1]
    load c, [y, #2]
    load d, [y, #3]
    halt
    #addr 0x8000
        #d8 {expected[0]}
        #d8 {expected[1]}
        #d8 {expected[2]}
        #d8 {expected[3]}
    """

    emu = Emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d, emu.y) == expected

@under_test(
    Op.LOAD_A_X_IDX,
    Op.LOAD_B_X_IDX,
    Op.LOAD_C_X_IDX,
    Op.LOAD_D_X_IDX,
)
def test_load8_ptr_x_gpr_a():
    value = 69
    expected = (0x8000, value, value, value, value)
    offset = 3
    assembly = f"""
    load x, #{expected[0]}
    load a, #{offset}

    load b, [x, a]
    load c, [x, a]
    load d, [x, a]
    load a, [x, a]

    halt
    #addr {expected[0]}
        #d8 0
        #d8 0
        #d8 0
        #d8 {value}
    """

    emu = Emulator(assembly)
    assert (emu.x, emu.a, emu.b, emu.c, emu.d) == expected

@under_test(
    Op.ADC_A_B,
)
def test_adc():
    left, right = 30, 40

    assembly = f"""
    load a, #{left}
    load b, #{right}
    clc
    adc a, b
    clc
    adc b, a
    """

    emu = Emulator(assembly)
    assert emu.a == left + right
    assert emu.b == (left + right) + right
