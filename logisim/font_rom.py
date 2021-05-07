with open("font_rom.bin", "w") as rom_file:
    rom_file.write("v2.0 raw\n")

    T = ["7e", "18", "18", "18", "18", "18", "18", "00"]
    E = ["7e", "60", "60", "78", "60", "60", "7e", "00"]
    S = ["3c", "66", "60", "3c", "06", "66", "3c", "00"]

    rom = T + E + S
    rom_file.write("\n".join(rom))