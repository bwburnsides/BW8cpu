lines = []
with open("bwb_opcodes.txt") as f:
    for line in f:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)

opcodes = [[], [], []]
ext_page = 1

for inst in lines:
    if inst.endswith("*"):
        opcodes[0].append(inst[:-1])
        if len(opcodes[0]) > 256:
            raise RuntimeError("too many instruction zero page opcodes")
        continue

    opcodes[ext_page].append(inst)
    if len(opcodes[ext_page]) == 256:
        ext_page += 1
        if ext_page > 2:
            raise RuntimeError("too many opcodes")


print(sum(len(page) for page in opcodes))
print(len(opcodes[0]))
print(len(opcodes[1]))
print(len(opcodes[2]))

with open("_opcodes.asm", "w") as f:
    for page in opcodes:
        for i, opcode in enumerate(page):
            f.write(f"{opcode} = 0x{i:02x}\n")
        f.write("\n")