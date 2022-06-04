import bw8emu


def main():
    bus = bw8emu.SystemBus("C:\\Users\\brady\projects\\BW8cpu\\assembler\\test.bin")
    cpu = bw8emu.BW8cpu(
        ucode_path="C:\\Users\\brady\projects\\BW8cpu\\control",
        system_bus=bus
    )

    computer = bw8emu.Computer(cpu, bus)
    cpu.reset(True)
    computer.clock()
    cpu.reset(False)
    while True:
        print(cpu.dump())
        input()
        computer.clock()


if __name__ == "__main__":
    main()