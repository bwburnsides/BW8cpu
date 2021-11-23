from pprint import pprint

with open("bwb_opcodes.txt") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines if line.strip()]
lines = [line for line in lines if not line.startswith("#")]
print("Total: ", len(lines))
print("Unique: ", len(set(lines)))
print("MOVs, LOADs, STOREs: ", len([op for op in lines if any(op.startswith(pre) for pre in ["MOV", "LOAD", "STORE"])]))
print("ADDs, SUBs: ", len([op for op in lines if any(op.startswith(pre) for pre in ["ADD", "SUB"])]))
print("Jumps: ", len([op for op in lines if any(op.startswith(pre) for pre in ["J"])]))

prefixes = [line.split("_")[0] for line in lines]

insts = []
for inst in prefixes:
    if inst not in insts:
        insts.append(inst)

print("Instruction Count: ", len(insts))