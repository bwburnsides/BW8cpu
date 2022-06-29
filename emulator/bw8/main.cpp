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
    bool dump = false;

    if (argc < 2) {
        fprintf(stderr, "usage: bw8.exe <rom_path>");
        exit(-1);
    }

    BW8::Bus bus = BW8::Bus(argv[1]);

    bus.rst(true);
    bus.rst(false);

    while (true) {
        bus.clock();
        bus.dump(stdout);
        if (bus.hlt()) {
            bus.coredump();
        }
    }
}
