"""
This script reads opcodes enumerated in an input file, and produces an output file
which maps the opcodes to actual hex values in valid customasm syntax. Though all
opcodes are 1 byte in size, there are two opcodes which may be used as prefix bytes to
other instructions in order to modify the meaning of the subseqeuent opcode. This enables
the system to support 2 * 256 opcodes. In the produced asm file, all opcodes have two
bytes - the MSB byte signifies whether a prefix byte needs to be included before the LSB
opcode byte in the instruction stream.

Prefix Bytes:
00 - No prefix required. Inject only the LSB byte in the instruction stream.
01 - EXT prefix byte should be injected prior to LSB in the instruction stream.

Rules for Input File:
- Blank lines and lines beginning with # are ignored.
- Trailing comments not supported.
- Trailing * signifies zero-page instruction. File should not contain more than
256 of these, or error will be raised.
- Error will be raised if more than 512 opcodes in file

TODO: allow trailing comments in input 
"""
import argparse
from pathlib import Path

EXT = "EXT"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Produce canonical opcode assignments for instruction set."
    )
    parser.add_argument(
        "input_fname", help="file which contains list of instructions in set"
    )
    parser.add_argument(
        "output_fname", help="file root to write assigned opcodes to, no suffix"
    )
    args = parser.parse_args()

    in_path = Path(args.input_fname)
    out = Path(args.output_fname)

    out_paths = (out.with_suffix(".asm"), out.with_suffix(".py"))

    if not in_path.exists():
        print(f"The input file named '{in_path.name}' does not exist. Exiting...")
        exit()

    if any(path.exists() for path in out_paths):
        print(f"One of the output files exists. Exiting for safety...")
        exit()

    return in_path, out_paths


def read_input(in_path):
    # Read in input lines. Discard comment lines and strip whitespace.
    lines = []
    with open(in_path) as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                lines.append(stripped)

    if not len(lines) == len(set(lines)):
        print("There are duplicate instructions. Exiting for safety...")
        exit()

    return lines


def write_output(out_paths, opcodes):
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
            extra_lines.extend(("import enum", "class Op(enum.IntEnum):"))
        else:
            raise ValueError(f"{path} has unexpected suffix.")

        header = [
            f"{comment_token} NOTE: This file was autogenerated by {Path(__file__).name}",
            f"{comment_token} Total opcode count: {sum(len(page) for page in opcodes)}",
            f"{comment_token} Zeropage opcodes: {len(opcodes[0])}",
            f"{comment_token} Extended opcodes: {len(opcodes[1])}",
        ]

        header.extend(extra_lines)
        header = "\n".join(header)

        # Write opcodes to output
        with open(path, "w") as f:

            f.write(header)
            f.write("\n")

            for pre, page in enumerate(opcodes):
                for i, opcode in enumerate(page):
                    f.write(f"{padding}{opcode} = 0x{pre:02x}{i:02x}\n")
                f.write("\n")


def main():
    in_path, out_path = parse_args()
    instructions = read_input(in_path)

    # Split opcodes into 2 pages - normal, extended
    opcodes = ([], [])
    ext_page = 1

    for inst in instructions:
        # if ends with *, then try to add to zero page
        if inst.endswith("*"):
            inst_stripped = inst[:-1]
            opcodes[0].append(inst_stripped)
            if len(opcodes[0]) > 256:
                raise RuntimeError("too many instruction zero page opcodes")
            continue

        # otherwise, add to ext page
        opcodes[ext_page].append(inst)
        if len(opcodes[ext_page]) > 256:
            print("too many opcodes")
            exit()

    if EXT not in opcodes[0]:
        print(f"{EXT} must be present in the instruction zeropage. Exiting...")
        exit()

    write_output(out_path, opcodes)


if __name__ == "__main__":
    main()
