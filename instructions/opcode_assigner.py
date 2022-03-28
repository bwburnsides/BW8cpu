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
    parser = argparse.ArgumentParser(description="Produce canonical opcode assignments for instruction set.")
    parser.add_argument("input_fname", help="file which contains list of instructions in set")
    parser.add_argument("output_fname", help="file to write assigned opcodes to")
    args = parser.parse_args()

    in_path = Path(args.input_fname)
    out_path = Path(args.output_fname)

    if not in_path.exists():
        print(f"The input file named '{in_path.name}' does not exist. Exiting...")
        exit()

    if out_path.exists():
        print(f"The output file named '{out_path.name}' exists. Exiting for safety...")
        exit()

    return in_path, out_path

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

def write_output(out_path, opcodes):
    # Write opcodes to output
    with open(out_path, "w") as f:

        f.write(f"; Total opcode count: {sum(len(page) for page in opcodes)}\n")
        f.write(f"; Zeropage opcodes: {len(opcodes[0])}\n")
        f.write(f"; Extended opcodes: {len(opcodes[1])}\n")

        for pre, page in enumerate(opcodes):
            for i, opcode in enumerate(page):
                f.write(f"{opcode} = 0x{pre:02x}{i:02x}\n")
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
                exit()
            continue

        # otherwise, add to ext page
        opcodes[ext_page].append(inst)
        if len(opcodes[ext_page]) == 256:
            print("too many opcodes")
            exit()

    if not EXT in opcodes[0]:
        print(f"{EXT} must be present in the instruction zeropage. Exiting...")

    write_output(out_path, opcodes)

if __name__ == "__main__":
    main()
