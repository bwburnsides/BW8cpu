from contextlib import contextmanager
from typing import Generator, Final
from dataclasses import dataclass
import subprocess
from pathlib import Path

from numpy import byte

ASSEMBLER_PATH: Final[Path] = Path("C:/Users/brady/projects/BW8cpu/assembler")
EMULATOR_PATH: Final[Path] = Path(
    "C:/Users/brady/projects/BW8cpu/emulator/bw8cpu/Debug/bw8cpu.exe"
)
CORE_DUMP_PATH: Final[Path] = Path(
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


@dataclass
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


def emulator(assembly: str) -> CoreDump:
    fname = "TEMP_EMU_TESTING"
    asm_path = ASSEMBLER_PATH / f"{fname}.asm"

    # Write the assembly to a file
    with open(asm_path, "w") as f:
        f.write("#include \"bw8cpu.asm\"\n")
        f.write(BANK_DEF)
        f.write("\n")
        f.write(assembly)
        f.write("\n halt")

    # Assemble the file
    subprocess.call(["customasm.exe", str(asm_path)])

    asm_path.unlink()

    # Run the emulator
    bin_path = ASSEMBLER_PATH / f"{fname}.bin"
    subprocess.call([str(EMULATOR_PATH), str(bin_path)])

    bin_path.unlink()

    # Read the core dump
    with open(CORE_DUMP_PATH, "rb") as f:
        regs = []
        for _ in range(4):
            regs.append(int.from_bytes(f.read(2), byteorder="little"))
        for _ in range(11):
            regs.append(int.from_bytes(f.read(1), byteorder="little"))

        core_dump = CoreDump(*regs)

    CORE_DUMP_PATH.unlink()

    return core_dump
