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

    char* rom_fname = argv[1];
    BW8::Bus bus = BW8::Bus(rom_fname);
    BW8::CPU cpu = BW8::CPU(&bus);
    BW8::UART uart = BW8::UART(&bus);

    cpu.rst(true);
    cpu.rst(false);

    while (true) {
        cpu.rising();
        cpu.falling();
        bus.dump(stdout);
        if (cpu.hlt()) {
            cpu.coredump();
        }
    }
}
