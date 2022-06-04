from bw8emupy import BW8cpu


def main():
    cpu = BW8cpu(
        ucode_path="C:\\Users\\brady\projects\\BW8cpu\\control",
    )

    cpu.reset(True)
    cpu.reset(False)
    while True:
        print(cpu.dump())
        input()
        cpu.clock()


if __name__ == "__main__":
    main()
