#define _CRT_SECURE_NO_WARNINGS

#include "bw8cpu.h"
#include <time.h>
#include <fstream>
#include <cassert>
#include <stdio.h>

uint8_t BW8cpu::dp_initial = 0x01;
uint16_t BW8cpu::sp_initial = 0xFFFF;
uint16_t BW8cpu::rst_vec_hi = 0x0100;
uint16_t BW8cpu::irq_vec_hi = 0x0000;

BW8cpu::BW8cpu(const char* microcode_path) {
    read_microcode(microcode_path);

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
    rst = (bool)(rand() % 1);
    irq = (bool)(rand() % 1);

    dbus = 0;
    xfer = 0;
    addr = 0;
}

void BW8cpu::reset() {
    general_purpose_reg = { 0 };
    address_reg = { 0 };
    internal_reg = { 0 };

    rst = true;
    irq = false;
    sequencer = 0;
}

void BW8cpu::rising() {

}

void BW8cpu::falling() {

}

void BW8cpu::read_microcode(const char* microcode_path) {
    FILE *fp = std::fopen(microcode_path, "rb");
    std::fread(&microcode[0], sizeof(microcode[0]), microcode.size(), fp)
}