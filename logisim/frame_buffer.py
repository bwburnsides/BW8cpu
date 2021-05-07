with open("frame_rom.bin", "w") as rom_file:
    rom_file.write("v2.0 raw\n")
    rom_file.write("00\n01\n02\n00")

    for _ in range((2 ** 13) - 4):
        rom_file.write("\nff")
