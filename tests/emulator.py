from typing import Final
import subprocess
from pathlib import Path

from .common import CoreDump, NoneDump

timeout: Final[int] = 5
PROJ_ROOT: Final = Path("C:/Users/brady/projects/BW8cpu")

ASSEMBLER_PATH: Final = PROJ_ROOT / "assembler"
EMULATOR_PATH: Final = PROJ_ROOT / "emulator/bw8/x64/Release/bw8.exe"
CORE_DUMP_PATH: Final = PROJ_ROOT / "tests/CORE_DUMP.BIN"

BANK_DEF: str = """
#bankdef rom {
    #addr 0x0000
    #size 0xFFFF
    #outp 8 * 0x0000
    #fill
}
"""

def Emulator(assembly: str) -> CoreDump:
    fname = "TEMP_EMU_TESTING"
    asm_path = ASSEMBLER_PATH / f"{fname}.asm"

    # Write the assembly to a file
    with open(asm_path, "w") as f:
        f.write('#include "bw8cpu.asm"\n')
        f.write(BANK_DEF)
        f.write("\n")
        f.write(assembly)
        f.write("\nhalt\n")

    # Assemble the file
    try:
        subprocess.call(
            ["customasm.exe", str(asm_path)],
            timeout=timeout,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        print("TIMEOUT EXPIRES")
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
        for _ in range(4):
            regs.append(int.from_bytes(f.read(1), byteorder="little"))

        flags = []
        for _ in range(8):
            regs.append(bool(int.from_bytes(f.read(1), byteorder="little")))

        final = regs + flags

    core_dump = CoreDump(*final)
    CORE_DUMP_PATH.unlink()
    return core_dump
