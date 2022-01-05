from pathlib import Path
from collections import namedtuple

Inst = namedtuple("Inst", ["name", "opcode"])

parent = Path(__file__).absolute().parent
opcodes_path = (parent / ".." / "instructions" / "opcodes.asm").resolve()
output_fname = "_AUTOGEN_microcode.asm"
output_path = parent / output_fname

output_lines = [
    "#include \"ctrl_state.asm\"",
    "#include \"ctrl_defin.asm\"",
    "\n#bits 32",
    "#labelalign 8 * 32",
]

with open(opcodes_path, "r") as f:
    input_lines = f.readlines()

pages = [[], [], []]
page_idx = 0

for line in input_lines:
    stripped = line.lower().strip()

    if not stripped:
        page_idx += 1
        continue

    name, _, opcode = stripped.split(" ")
    inst = Inst(name, int(opcode, base=16))

    pages[page_idx].append(inst)


output_lines.append("\n#bank mode00  ; NRM Mode")
for inst in pages[0]:
    output_lines.append(f"{inst.name}:  ; Opcode 0x{inst.opcode:02X}")

output_lines.append("\n#bank mode01  ; EX1 Mode")
for inst in pages[1]:
    output_lines.append(f"{inst.name}:  ; Opcode 0x{inst.opcode:02x}")

output_lines.append("\n#bank mode10  ; RST Mode")
output_lines.append("; insert reset sequence here")

output_lines.append("\n#bank mode11  ; EX2 Mode")
for inst in pages[2]:
    output_lines.append(f"{inst.name}:  ; Opcode 0x{inst.opcode:02x}")

output_text = "\n".join(output_lines)
with open(output_path, "w") as f:
    f.write(output_text)
