#define _CRT_SECURE_NO_WARNINGS

#include "bw8cpu.h"
#include <time.h>
#include <stdio.h>
#include <fstream>
#include <vector>



uint16_t BW8cpu::irq_vector = 0x0003;
uint16_t BW8cpu::nmi_vector = 0x0006;

BW8cpu::BW8cpu() {
    read_microcode();

    general_purpose_reg = { 0 };
    address_reg = { 0 };
    internal_reg = { 0 };

    for (int i = 0; i < 7; i++)
    {
        if (i < 4)
        {
            general_purpose_reg[i] = rand() % 0xFF;
            address_reg[i] = rand() % 0xFFFF;
        }
        internal_reg[i] = rand() % 0xFF;
    }

    srand((unsigned int) time(NULL));

    sequencer = rand() % 7;
    irq = (bool)(rand() % 1);
    rw = (bool)(rand() % 1);
    req = (bool)(rand() % 1);
    nmi = (bool)(rand() % 1);
    mi = (bool)(rand() % 1);
    ext = (bool)(rand() % 1);

    dbus = 0;
    xfer = 0;
    addr = 0;
}

void BW8cpu::reset() {
    general_purpose_reg = { 0 };
    address_reg = { 0 };
    internal_reg = { 0 };

    irq = false;
    rw = true;
    req = false;
    nmi = false;
    mi = true;
    ext = false;

    sequencer = 0;
}

void BW8cpu::interrupt_request() {

}

void BW8cpu::nonmaskable_interrupt() {

}

void BW8cpu::memory_request() {

}

void BW8cpu::rising() {
    // On a rising edge, we want to read from the microcode, decode the control word,
    // and begin bus asserts.

    uint32_t state = (get_mode() << 16)     |
                    (ext << 15)             |
                    (internal_reg[IR] << 7) |
                    (internal_reg[SR] << 3) |
                    sequencer;

    state = 0;
    printf("Addr: %d\n", state);

    uint32_t ctrl_word = microcode[state];

    uint8_t dbus_assert = (ctrl_word >> 0)  & (0b1111);
    uint8_t dbus_load   = (ctrl_word >> 4)  & (0b11111);
    uint8_t alu_op      = (ctrl_word >> 9)  & (0b1111);
    uint8_t xfer_assert = (ctrl_word >> 13) & (0b11111);
    uint8_t xfer_load   = (ctrl_word >> 18) & (0b111);
    uint8_t addr_assert = (ctrl_word >> 21) & (0b111);
    uint8_t count       = (ctrl_word >> 24) & (0b111);
    uint8_t dec_sp      = (ctrl_word >> 27) & (0b1);
    uint8_t rst_useq    = (ctrl_word >> 28) & (0b1);
    uint8_t tog_ext     = (ctrl_word >> 29) & (0b1);
    uint8_t offset      = (ctrl_word >> 30) & (0b1);
    uint8_t brk_clk     = (ctrl_word >> 31) & (0b1);

    printf("Ctrl Word: %d\n", ctrl_word);
    printf("Mode: %d\n", get_mode());
    printf("Dbus Assert: %d\n", dbus_assert);
    printf("Dbus Load: %d\n", dbus_load);
    printf("ALU Op: %d\n", alu_op);
    printf("Xfer Assert: %d\n", xfer_assert);
    printf("Xfer Load: %d\n", xfer_load);
    printf("Addr Assert: %d\n", addr_assert);
    printf("Count: %d\n", count);
    printf("dec sp: %d\n", dec_sp);
    printf("rst useq: %d\n", rst_useq);
    printf("tog ext: %d\n", tog_ext);
    printf("offset: %d\n", offset);
    printf("brk clk: %d\n", brk_clk);
}

void BW8cpu::falling() {

}

Mode BW8cpu::get_mode() {
    if (req) {
        return STALL;
    }
    else if (nmi) {
        return NMI;
    }
    else if (irq) {
        return IRQ;
    }
    return FETCH;
}

void BW8cpu::read_microcode() {
    std::ifstream input;
    uint8_t byte;

    std::array<std::string, 4> file_paths = {
        "C:\\Users\\brady\\projects\\BW8cpu\\control\\microcode0.bin",
        "C:\\Users\\brady\\projects\\BW8cpu\\control\\microcode1.bin",
        "C:\\Users\\brady\\projects\\BW8cpu\\control\\microcode2.bin",
        "C:\\Users\\brady\\projects\\BW8cpu\\control\\microcode3.bin",
    };

    for (int i = 0; i < (256 * 1024); i++) {
        microcode.push_back(0);
    }

    for (int i = 0; i < 4; i++) {
        input.open(file_paths[i].c_str(), std::ios::binary);

        if (input.fail()) {
            printf("Couldn't open %s\n", file_paths[i].c_str());
            exit(-1);
        }

        for (int j = 0; j < (256 * 1024); j++) {
            input >> byte;
            byte <<= 8 * i;
            microcode[j] |= byte;
        }
        input.close();
    }
}