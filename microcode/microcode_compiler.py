from pathlib import Path
from collections import namedtuple
import argparse
import sys
from typing import Sequence, Optional
import datetime

Inst = namedtuple("Inst", ["name", "opcode"])

"""
Support two modes:
    1. Produce a microcode source template file
        - Include all standard customasm cargo
        - place labels / "inst" directives using opcodes.asm
    2. Compile a microcode source file
        - expand instructions 32x to satisfy status region of control space
        - fill in conditional uop sequences via custom "cond" directive
        - compile file with customasm
        - split into 4x binaries for physical ROMs
"""

def _config_template_output_path(output_name: Optional[str]) -> Optional[Path]:
    if output_name is None:
        timestamp = datetime.datetime.now()
        default_name = "_AUTOGEN_{time:%Y-%m-%d-%H-%M-%S}_microcode.asm".format(time=timestamp)
        output_path = Path.cwd() / default_name
    else:
        output_path = Path(output_name)

    if output_path.exists():
        print(
            f"The output path '{str(output_path)}' already exists. Are you sure you "
            "want to write the template file to this location?\n"
        )

        while True:
            response = input("(y/N) >>> ").strip().lower()
            response = "n" if not response else response

            if response in ("n", "no"):
                print("Aborting.\n")
                return
            elif response not in ("y", "yes"):
                print("Response not recognized.\n")
            else:
                break

    print(f"Will output microcode source template file to '{str(output_path)}'.")
    return output_path

def _config_template_opcodes_path(opcodes_name: Optional[str]) -> Optional[Path]:
    if opcodes_name is None:
        parent = Path(__file__).absolute().parent
        opcodes_path = (parent / ".." / "instructions" / "opcodes.asm").resolve()
    else:
        opcodes_path = Path(opcodes_name)
        print(
            f"The opcodes file at '{str(opcodes_path)}' must be well formed. The template "
            "generator has not been tested with malformed opcodes file.\n"
        )
        input("Press enter to continue.")

    if not opcodes_path.exists():
        print(f"The opcodes path '{str(opcodes_path)}' does not exist. Aborting.\n")
        return

    print(f"Will read opcodes from '{str(opcodes_path)}'.")
    return opcodes_path

def _parse_opcodes_file(
    opcodes_path: Path
) -> tuple[list[Inst], list[Inst], list[Inst]]:
    with open(opcodes_path, "r") as f:
        input_lines = f.readlines()

    pages: tuple[list[Inst]] = ([], [], [])
    page_idx = 0

    for line in input_lines:
        stripped = line.lower().strip()

        if not stripped:
            page_idx += 1
            continue

        name, _, opcode = stripped.split(" ")
        inst = Inst(name, int(opcode, base=16))

        pages[page_idx].append(inst)

    return pages

def _build_microcode_template_file(
    pages: tuple[list[Inst], list[Inst], list[Inst]],
    output_path: Path,
    definition_file: Optional[str],
) -> None:
    output_lines = [] if definition_file is None else [f"#include \"{definition_file}\""]
    output_lines.extend([
        "#bits 32",
        "#labelalign 8 * 32",
    ])

    opcode_fmt_str = "#opcode {name} ; 0x{value:02x}"

    output_lines.append("\n#bank mode00  ; NRM Mode")
    for inst in pages[0]:
        output_lines.append(opcode_fmt_str.format(name=inst.name, value=inst.opcode))

    output_lines.append("\n#bank mode01  ; EX1 Mode")
    for inst in pages[1]:
        output_lines.append(opcode_fmt_str.format(name=inst.name, value=inst.opcode))

    output_lines.append("\n#bank mode10  ; RST Mode")
    output_lines.append("; insert reset sequence here")

    output_lines.append("\n#bank mode11  ; EX2 Mode")
    for inst in pages[2]:
        output_lines.append(opcode_fmt_str.format(name=inst.name, value=inst.opcode))

    output_text = "\n".join(output_lines)
    with open(output_path, "w") as f:
        f.write(output_text)

    print(f"Wrote microcode source template file to '{str(output_path)}'")

def produce_template(
    output_name: Optional[str],
    opcodes_name: Optional[str],
    definition_file: Optional[str],
) -> None:
    """
    Produce a microcode source file template, which can then be populated with custom
    micro-instructions and compiled using this compiler. The template includes customasm
    directives to align all labels on 8-word boundaries so as to ensure that all
    instructions start at the beginning of their t-state in the control address space.
    Labels are placed in order and within their proper mode-banks based on the contents of
    :opcodes_names:. A helper file can be automatically included at the top of the
    template file via :definition_file:.

    :output_name: - the location to output the template file
        default value is based on the current timestamp
    :opcodes_name: - the location to read opcode definitions from
        default value is bw8/instructions/opcodes.asm
    :definition_file: - the name of the file to #include in template file
        default behavior is to not include anything
    """

    output_path = _config_template_output_path(output_name)
    if output_path is None:
        return

    opcodes_path = _config_template_opcodes_path(opcodes_name)
    if opcodes_path is None:
        return

    pages = _parse_opcodes_file(opcodes_path)

    _build_microcode_template_file(pages, output_path, definition_file)


def compile_microcode(
    source_file: Optional[str],
    output_file: Optional[str],
    write_split: bool,
    write_wide: bool
) -> None:
    ...


def main(argv: Sequence[str]) -> None:
    parser = argparse.ArgumentParser(description="Produce microcode binaries for use in simulation, emulation, and hardware.")
    subparsers = parser.add_subparsers(help="available compiler modes", dest="command")
    template_subparser = subparsers.add_parser("template", help="produce microcode source template")
    compiler_subparser = subparsers.add_parser("compile", help="compile microcode binaries from source")

    template_subparser.add_argument("--output_name", nargs="?", help="produce microcode source template with optional output name")
    template_subparser.add_argument("--opcodes_name", help="use opcoding mapping from non-default file")
    template_subparser.add_argument("--definition_file", help="nn assembly file to include in the microcode template")

    compiler_subparser.add_argument("source_file", help="source file to compile")
    compiler_subparser.add_argument("output_file", help="compiled output file names base")
    compiler_subparser.add_argument("--write_split", action="store_true", default=False, help="split microcode into byte-wide files")
    compiler_subparser.add_argument("--write_wide", action="store_true", default=True, help="output 32-bit wide output")

    argv = ["--help"] if len(argv) < 2 else argv[1:]
    args = parser.parse_args(argv)

    if args.command == "template":
        produce_template(args.output_name, args.opcodes_name, args.definition_file)
    elif args.command == "compile":
        compile_microcode(args.source_file, args.output_file, args.write_split, args.write_wide)
    else:
        raise RuntimeError(f"Invalid subcommand '{args.command}', must be 'template' or 'compile'.")

if __name__ == "__main__":
    main(sys.argv)
