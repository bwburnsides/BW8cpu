"""
This script reads opcodes enumerated in an input file, and produces output files
which maps the opcodes to actual hex values. Though all opcodes are 1 byte in size,
there is one opcode which may be used as a prefix byte to other instructions in order
to modify the meaning of the subseqeuent opcode. This enables the system to support
2 * 256 opcodes. In the produced files, all opcodes have two bytes - the MSB byte signifies
whether a prefix byte needs to be included before the LSB opcode byte in the instruction stream.

Prefix Bytes:
00 - No prefix required. Inject only the LSB byte in the instruction stream.
01 - EXT prefix byte should be injected prior to LSB in the instruction stream.

Rules for Input File:
- Blank lines and lines beginning with # are ignored.
- Trailing comments not supported.
- Trailing * signifies prioritized instruction. File should not contain more than
256 of these, or error will be raised.
- Error will be raised if more than 512 opcodes in file
- Lines should contain no spaces and be in all caps
"""
import argparse
from pathlib import Path
from os import PathLike
from sys import stderr

EXT = "EXT"


def parse_args() -> tuple[Path, tuple[Path, Path]]:
    parser = argparse.ArgumentParser(
        description="Produce canonical opcode assignments for instruction set."
    )
    parser.add_argument(
        "input_fname", help="file which contains list of instructions in set"
    )
    parser.add_argument(
        "output_fname", help="file root to write assigned opcodes to, no suffix"
    )
    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="overwrite existing output files",
    )
    args = parser.parse_args()

    in_path = Path(args.input_fname)
    out = Path(args.output_fname)

    out_paths = (out.with_suffix(".asm"), out.with_suffix(".py"))

    if not in_path.exists():
        print(
            f"The input file named '{in_path.name}' does not exist. Exiting...",
            file=stderr,
        )
        exit(-1)

    if not args.force and any(path.exists() for path in out_paths):
        print(
            f"One of the output files exists. Exiting for safety...",
            file=stderr,
        )
        exit(-1)

    return in_path, out_paths


def read_input(in_path: PathLike) -> list[str]:
    with open(in_path) as f:
        lines = [
            stripped
            for line in f.readlines()
            if (stripped := line.strip()) and not stripped.startswith("#")
        ]

    if not len(lines) == len(set(lines)):
        print("There are duplicate instructions. Exiting for safety...", file=stderr)
        exit(-1)

    return lines


def write_output(
    out_paths: tuple[Path, Path], opcodes: tuple[list[str], list[str]]
) -> None:

    for path in out_paths:
        extra_lines = []
        padding = ""

        if path.suffix == ".asm":
            comment_token = ";"
            padding = "OP_"
            extra_lines.append("#once")
        elif path.suffix == ".py":
            comment_token = "#"
            padding = "    "
            extra_lines.append("import enum")
            extra_lines.append("class Op(enum.IntEnum):")
        else:
            raise ValueError(f"{path} has unexpected suffix.")

        header = [
            f"{comment_token} NOTE: This file was autogenerated by {Path(__file__).name}",
            f"{comment_token} Total opcode count: {sum(len(page) for page in opcodes)}",
            f"{comment_token} Zeropage opcodes: {len(opcodes[0])}",
            f"{comment_token} Extended opcodes: {len(opcodes[1])}",
        ]

        header.extend(extra_lines)
        header_joined = "\n".join(header)

        # Write opcodes to output
        with open(path, "w") as f:
            f.write(header_joined)
            f.write("\n")

            for pre, page in enumerate(opcodes):
                for i, opcode in enumerate(page):
                    f.write(f"{padding}{opcode} = 0x{pre:02x}{i:02x}\n")
                f.write("\n")

        print(f"Generated {path} file....")


def display_stats(groups):
    total = groups[0] + groups[1]

    print(f"Total opcodes: {len(set(total))}")

    movs = [op for op in total if op.startswith("MOV")]
    loads = [op for op in total if op.startswith("LOAD")]
    stores = [op for op in total if op.startswith("STORE")]
    adds = [op for op in total if op.startswith("ADC")]
    subs = [op for op in total if op.startswith("SBC")]
    jumps = [op for op in total if op.startswith("J")]

    abs = [op for op in total if "ABS" in op]
    dp = [op for op in total if "DP" in op]

    print(f"mov: {len(movs)}")
    print(f"ld: {len(loads)}")
    print(f"st: {len(stores)}")
    print(f"add: {len(adds)}")
    print(f"sub: {len(subs)}")
    print(f"jump: {len(jumps)}")
    print()
    print(f"absolute: {len(abs)}")
    print(f"direct page: {len(dp)}")
    print()

    insts = []
    for inst in (line.split("_")[0] for line in total):
        if inst not in insts:
            insts.append(inst)

    print(f"Instruction Count: {len(insts)}")
    print()


def main():
    in_path, out_path = parse_args()
    opcodes = read_input(in_path)

    # Split opcodes into 2 pages - normal, extended
    groups = ([], [])

    for op in opcodes:
        # if ends with *, then try to add to zero page
        if op.endswith("*"):
            op_stripped = op[:-1]
            groups[0].append(op_stripped)
            continue

        groups[1].append(op)

    if (ct := len(groups[0])) > 256:
        print(
            f"Max of 256 normal opcodes, got {ct}. Exiting...",
            file=stderr,
        )
        exit(-1)

    if (ct := len(groups[1])) > 256:
        print(
            f"Max of 256 extended opcodes, got {ct}. Exiting...",
            file=stderr,
        )

    if EXT not in groups[0]:
        print(
            f"{EXT} must be present normal opcodes. Exiting...",
            file=stderr,
        )
        exit(-1)

    display_stats(groups)
    write_output(out_path, groups)


if __name__ == "__main__":
    main()
