names = ["Fixed ROM", "Banked ROM", "Banked RAM", "Fixed RAM", "IO"]
sizes = [8, 8, 8, 39, 1]
mem_groups = [[] for _ in sizes]

curr_group = 0
for addr in range(2 ** 16):
    if len(mem_groups[curr_group]) == (sizes[curr_group] * 1024):
        curr_group += 1
    mem_groups[curr_group].append(addr)

print(
    "{:<13}   {:<}   {:<}   {:<}               {:<}".format(
        "Name", "Hex Low", "Hex High", "Bin Low", "Bin High"
    )
)
for name, mem in zip(names, mem_groups):
    print(
        "{name:<13}   ${low:04x}     ${high:04x}      #{lowb:016b}     #{highb:016b}".format(
            name=name, low=mem[0], high=mem[-1], lowb=mem[0], highb=mem[-1]
        )
    )

fbl = int("1000000000000000", base=2)
fbh = int("1011111111111111", base=2)

print()
print(
    "{name:<13}   ${low:04x}     ${high:04x}      #{lowb:016b}     #{highb:016b}".format(
        name="Frame Buffer", low=fbl, high=fbh, lowb=fbl, highb=fbh
    )
)