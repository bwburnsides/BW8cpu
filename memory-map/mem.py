mem_groups = [[], [], [], [], []]

sizes = [39.75, 0.25, 8, 8, 8]

curr_group = 0
for addr in range(2 ** 16):
    if len(mem_groups[curr_group]) == (sizes[curr_group] * 1024):
        curr_group += 1
    mem_groups[curr_group].append(addr)

low_ram, io, bank1, bank2, fixed_rom = mem_groups

print(bin(low_ram[0]))
print(bin(low_ram[-1]))
print()

print(bin(io[0]))
print(bin(io[-1]))
print()

print(bin(bank1[0]))
print(bin(bank1[-1]))
print()

print(bin(bank2[0]))
print(bin(bank2[-1]))
print()

print(bin(fixed_rom[0]))
print(bin(fixed_rom[-1]))
print()
print()

frame_buffer = []
for addr in reversed(low_ram):
    frame_buffer.append(addr)
    if len(frame_buffer) == (2 ** 14):
        break

print(len(low_ram) / 1024)
print(len(frame_buffer) / 1024)

frame_buffer = list(reversed(frame_buffer))
print(bin(frame_buffer[0]))
print(bin(frame_buffer[-1]))