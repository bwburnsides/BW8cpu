import sys
from typing import Final
from pathlib import Path
import subprocess
import textwrap

timeout: Final[int] = 5
ASSEMBLER_PATH: Final[Path] = Path(
    "C:/Users/brady/projects/BW8cpu/assembler"
)


def eprint(msg: str, code: int):
    print(msg)
    exit(code)


def main(argv: list[str]) -> None:
    if len(argv) > 2:
        eprint("usage: python test_case_gen.py <asm_path>", -1)

    test_case = gen_test_case(argv[1])


def gen_test_case(asm_path: str) -> str:
    # Assemble the file
    out = subprocess.run(
        f"customasm.exe -f logisim8 -p -q {asm_path}",
        timeout=timeout,
        capture_output=True,
    )

    if out.stderr:
        eprint(f"An error has ocurred: {out.stderr}", -1)

    # Discard the header line
    stdout = out.stdout.decode("ascii")
    _, *lines = stdout.split("\n")
    mcode = []

    # Add 0x prefix
    for line in lines:
        mcode.extend([f"0x{byte}" for byte in line.split()])

    # Populate test case
    return textwrap.dedent(
        f"""
        step pass fail

        program({", ".join(mcode)})

        let i = 0;
        while(!(pass | fail | (i >= 100)))
            let i = i + 1;
            0 0 0
            1 x x
        end while
        0 1 0
        """
    )


if __name__ == "__main__":
    main(sys.argv)