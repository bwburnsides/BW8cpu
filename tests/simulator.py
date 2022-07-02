from pathlib import Path
from typing import Final
import os
from contextlib import contextmanager
import subprocess
import textwrap

from .common import CoreDump


PROJECT_ROOT = Path("C:/Users/brady/projects/BW8cpu")

DIGITAL_PATH: Final[Path] = Path("C:/Users/brady/Digital")
ASSEMBLER_PATH: Final[Path] = PROJECT_ROOT / "assembler"
TEST_CASE_PATH: Final[Path] = PROJECT_ROOT / "tests/testsuite.dig"
CPU_SIM_PATH: Final[Path] = PROJECT_ROOT / "simulator/BW8cpu.dig"

@contextmanager
def working_directory(path: os.PathLike):
    cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def assemble(assembly: str) -> str:
    assembly = "#include \"bw8cpu.asm\"\n" + assembly
    assembly_path = Path("TEMP_ASSEMBLY_FILE.ASM")

    # Dump the assembly to a file and then assemble it
    with working_directory(ASSEMBLER_PATH):
        with open(assembly_path, "w") as f:
            f.write(assembly)

        out = subprocess.run(
            f"customasm.exe -f logisim8 -p -q {assembly_path}",
            timeout=5000,
            capture_output=True,
        )

        assembly_path.unlink()

    if out.stderr:
        print(out.stderr.decode("ascii"))
        exit(-1)

    # Discard header line and divide lines
    stdout = out.stdout.decode("ascii")
    _, *lines = stdout.split("\n")
    machine_code = []

    # Flatten lines into single array of 0x prefixed bytes
    for line in lines:
        machine_code.extend([f"0x{byte}" for byte in line.split()])

    return machine_code


def Simulator(assembly: str) -> CoreDump:
    machine_code = assemble(assembly)
    test_dump = simulate(machine_code)
    return parse(test_dump)

def parse(test_dump: str) -> CoreDump:
    _, _, pc, sp, x, y, a, b, c, d, nmi_f, ubr_f, us_f, c_f, z_f, v_f, n_f, i_f, *_ = test_dump.splitlines()[2:-2][-1].split()
    regs = [pc, sp, x, y, a, b, c, d, nmi_f, ubr_f, us_f, c_f, z_f, v_f, n_f, i_f]
    int_regs = []
    for reg in regs:
        if reg.startswith("0x"):
            int_regs.append(int(reg, 16))
        elif reg.startswith("0b"):
            int_regs.append(int(reg, 2))
        else:
            if any(any(char.lower() == hex for hex in "abcdef")for char in reg):
                int_regs.append(int(reg, 16))
            else:
                int_regs.append(int(reg))

    return CoreDump(*int_regs)

def simulate(machine_code: list[str]) -> str:
    test_case = textwrap.dedent(
        f"""
        step halt PC SP X Y A B C D NMIIf UBRf USf Cf Zf Vf Nf If IR assert

        program({", ".join(machine_code)})

        let i = 0;
        while(!(halt | (i >= 100)))
            let i = i + 1;
            0 0 x x x x x x x x x x x x x x x x x x
            1 x x x x x x x x x x x x x x x x x x x
        end while
        x x x x x x x x x x x x x x x x x x x 0
        """
    )

    element = textwrap.dedent(
        f"""
        <visualElement>
            <elementName>Testcase</elementName>
            <elementAttributes>
                <entry>
                <string>Testdata</string>
                <testData>
                    <dataString>{test_case}</dataString>
                </testData>
                </entry>
            </elementAttributes>
            <pos x="0" y="0"/>
        </visualElement>
        """
    )

    # Copy the test case template into the Digital directory
    key = "</visualElement>"
    file_text = TEST_CASE_PATH.read_text()
    filled = file_text.replace("__TEST_CASE_ELEMENT__", element)

    (DIGITAL_PATH / "TEST_CASE.DIG").write_text(filled)

    with working_directory(DIGITAL_PATH):
        out = subprocess.run(
            f"java -cp Digital.jar CLI test -verbose {CPU_SIM_PATH.absolute()} -tests {DIGITAL_PATH / 'TEST_CASE.DIG'}",
            timeout=5000,
            capture_output=True,
        )
        (DIGITAL_PATH / "TEST_CASE.DIG").unlink()

    return out.stdout.decode("ascii")

if __name__ == "__main__":
    print(
        Simulator(
        """
            load a, #69
            mov b, a
            mov c, b
            mov d, c
            load x, #6502
            load y, #6809
            halt
        """
        )
    )
