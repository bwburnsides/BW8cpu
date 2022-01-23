"""
This script reads opcodes enumerated in bwb_opcodes.txt, and produces a new .asm file
which maps the opcodes to actual hex values. Though all opcodes are 1 byte in size, there
are two opcodes which may be used as pre fix bytes to other instructions in order to
modify the meaning of the subseqeuent opcode. This enables the system to support 3 * 256
opcodes. In the produces asm file, all opcodes have two bytes - the MSB byte signifies
whether a prefix byte needs to be included before the LSB opcode byte in the instruction
stream.

Prefix Bytes:
00 - No prefix required. Inject only the LSB byte in the instruction stream.
01 - EX1 prefix byte should be injected prior to LSB in the instruction stream.
02 - EX2 prefix byte should be injected prior to the LSB in the instruction stream.

Rules for Input File:
- Blank lines and lines beginning with # are ignored.
- Trailing comments not supported.
- Trailing * signifies zero-page instruction. File should not contain more than
256 of these, or error will be raised.
- Error will be raised if more than 768 opcodes in file

TODO: allow trailing comments in input 
"""
import argparse
from pathlib import Path

EX1 = "EX1"
EX2 = "EX2"

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
        f.write(f"; Extended 1 opcodes: {len(opcodes[1])}\n")
        f.write(f"; Extended 2 opcodes: {len(opcodes[2])}\n\n")

        for pre, page in enumerate(opcodes):
            for i, opcode in enumerate(page):
                f.write(f"{opcode} = 0x{pre:02x}{i:02x}\n")
            f.write("\n")

def main():
    in_path, out_path = parse_args()
    instructions = read_input(in_path)

    # Split opcodes into 3 pages - normal, extended 1, extended 2
    opcodes = ([], [], [])
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

        # otherwise, add to current ext page, and then advance ptr if full
        opcodes[ext_page].append(inst)
        if len(opcodes[ext_page]) == 256:
            ext_page += 1
            if ext_page > 2:
                print("too many opcodes")
                exit()

    if not EX1 in opcodes[0] or EX2 in opcodes[1]:
        print(f"{EX1} and {EX2} must be present in the instruction zeropage. Exiting...")

    write_output(out_path, opcodes)

if __name__ == "__main__":
    main()
