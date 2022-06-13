import typing
import dataclasses
import subprocess
from pathlib import Path
import contextlib
import functools

import opcodes

timeout: typing.Final[int] = 5

ASSEMBLER_PATH: typing.Final[Path] = Path("C:/Users/brady/projects/BW8cpu/assembler")
EMULATOR_PATH: typing.Final[Path] = Path(
    "C:/Users/brady/projects/BW8cpu/emulator/bw8/x64/Debug/cpu.exe"
)
CORE_DUMP_PATH: typing.Final[Path] = Path(
    "C:/Users/brady/projects/BW8cpu/emulator/test_emu/CORE_DUMP.BIN"
)

BANK_DEF: str = """
#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}

#ruledef emulator {
    halt => opcode(OP_EXT) @ 0xFC
}
"""


@dataclasses.dataclass
class CoreDump:
    pc: int
    sp: int
    x: int
    y: int
    a: int
    b: int
    c: int
    d: int
    dp: int
    da: int
    th: int
    tl: int
    br: int
    ir: int
    of: int

    c_f: bool
    z_f: bool
    v_f: bool
    n_f: bool
    i_f: bool

    ext_f: bool
    nmi_f: bool
    sup_f: bool
    ubr_f: bool

    memory: list[list[int]] | None = None


NoneDump = CoreDump(*(None for _ in range(25)))


def Emulator(assembly: str, memory=False) -> CoreDump:
    fname = "TEMP_EMU_TESTING"
    asm_path = ASSEMBLER_PATH / f"{fname}.asm"

    # Write the assembly to a file
    with open(asm_path, "w") as f:
        f.write('#include "bw8cpu.asm"\n')
        f.write(BANK_DEF)
        f.write("\n")
        f.write(assembly)
        f.write("\n halt")

    # Assemble the file
    try:
        subprocess.call(
            ["customasm.exe", str(asm_path)],
            timeout=timeout,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return NoneDump
    finally:
        asm_path.unlink()

    # Run the emulator
    bin_path = ASSEMBLER_PATH / f"{fname}.bin"
    try:
        subprocess.call(
            [str(EMULATOR_PATH), str(bin_path)],
            timeout=timeout,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        return NoneDump
    finally:
        bin_path.unlink()

    # Read the core dump
    with open(CORE_DUMP_PATH, "rb") as f:
        regs = []
        for _ in range(4):
            regs.append(int.from_bytes(f.read(2), byteorder="little"))
        for _ in range(11):
            regs.append(int.from_bytes(f.read(1), byteorder="little"))

        flags = []
        for _ in range(9):
            regs.append(bool(int.from_bytes(f.read(1), byteorder="little")))

        final = regs + flags

        if memory:
            memory = []
            for br in range(16):
                memory.append([])
                data = f.read(1024 * 1024)                
                for byte in data:
                    memory[br].append(byte)

            final += [memory]

    core_dump = CoreDump(*final)
    CORE_DUMP_PATH.unlink()
    return core_dump


OPCODES = list(opcodes.Op)


def under_test(*opcodes):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)

            with contextlib.suppress(ValueError):
                for opcode in opcodes:
                    OPCODES.remove(opcode)

            return result

        return wrapper

    return decorator
