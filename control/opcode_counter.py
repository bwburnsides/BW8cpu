from pprint import pprint

lines = []
with open("bw8_instruction_set.txt") as f:
    for line in f:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)

print("Total: ", len(lines))
print("Unique: ", len(set(lines)))

movs_loads_stores = [op for op in lines if any(op.startswith(pre) for pre in ["MOV", "LOAD", "STORE"])]
loads = [op for op in lines if any(op.startswith(pre) for pre in ["LOAD"])]
stores = [op for op in lines if any(op.startswith(pre) for pre in ["STORE"])]
adds_subs = [op for op in lines if any(op.startswith(pre) for pre in ["ADD", "SUB", "ADC", "SBB", "SBC"])]
jumps = [op for op in lines if any(op.startswith(pre) for pre in ["J"])]

abss = [op for op in lines if "ABS" in op]
marked = [op for op in lines if op[-1] == "*"]

print()
print("MOVs, LOADs, STOREs: ", len(movs_loads_stores))
print("LOADs: ", len(loads))
print("STOREs: ", len(stores))
print("ADDs, SUBs: ", len(adds_subs))
print("Jumps: ", len(jumps))

print()
print("ABSs: ", len(abss))
print("Marked: ", len(marked))

print()
print("ABS or MOVs/LOADs/STOREs: ", len(set(movs_loads_stores) | set(abss)))
prefixes = [line.split("_")[0] for line in lines]

insts = []
for inst in prefixes:
    if inst not in insts:
        insts.append(inst)

print()
print("Instruction Count: ", len(insts))

# pprint(set(movs_loads_stores) | set(abss))
