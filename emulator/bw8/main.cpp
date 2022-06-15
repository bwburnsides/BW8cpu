#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include "bw8cpu.h"
#include "bw8bus.h"


int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: bw8.exe <rom_path>");
        exit(-1);
    }

    uint8_t* memory = BW8::bus::init(argv[1]);
    BW8::cpu::BW8cpu* cpu = BW8::cpu::cpu_malloc(BW8::bus::read, BW8::bus::write, memory);
    BW8::cpu::reset(cpu, true);
    BW8::cpu::reset(cpu, false);

    while (true) {
        BW8::cpu::clock(cpu);
    }

    BW8::cpu::cpu_free(cpu);
}
