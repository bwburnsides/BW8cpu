import pytest

from emulator import emulator

def test_load8_imm():
    expected = 1, 2, 3, 4

    assembly = f"""
    load a, #{expected[0]}
    load b, #{expected[1]}
    load c, #{expected[2]}
    load d, #{expected[3]}
    """

    emu = emulator(assembly)

    assert (emu.a, emu.b, emu.c, emu.d) == expected

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

    emu = emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d) == expected

def test_load8_ptr_idx():
    expected = (255, 254, 253, 252)

    # Basic positive offsets
    assembly = f"""
    load x, #0x8000
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

    emu = emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d) == expected

    # Negative offsets
    assembly = f"""
    load x, #0x8004
    load a, [x, #-4]
    load b, [x, #-3]
    load c, [x, #-2]
    load d, [x, #-1]
    halt
    #addr 0x8000
        #d8 {expected[0]}
        #d8 {expected[1]}
        #d8 {expected[2]}
        #d8 {expected[3]}
    """

    emu = emulator(assembly)
    assert (emu.a, emu.b, emu.c, emu.d) == expected

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

    emu = emulator(assembly)
    assert emu.a == left + right
    assert emu.b == (left + right) + right

# def test_sbc():
#     left, right = 40, 30

#     assembly = f"""
#     load a, #{left}
#     load b, #{right}
#     sec
#     sbc a, b
#     """

#     emu = emulator(assembly)
#     assert emu.a == 10
