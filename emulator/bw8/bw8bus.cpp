#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include "bw8bus.h"

namespace BW8 {
    Bus::Bus(const char* rom_path) {
        FILE* fp;
        size_t num_bytes;

        fp = fopen(rom_path, "rb");
        if (fp == NULL) {
            fprintf(stderr, "Error BW8::Bus constructor: Could not read ROM for CPU.\n");
            exit(-1);
        }

        memory = (uint8_t*)calloc(ADDR_SPACE_SIZE, sizeof(uint8_t));
        if (memory == NULL) {
            fprintf(stderr, "Error BW8::Bus constructor: Could not initiaize memory.\n");
        }

        num_bytes = fread(memory, sizeof(uint8_t), ROM_SIZE, fp);
        fclose(fp);

        for (int i = 0; i < 8; i++) {
            irq_sources[i] = false;
        }

        cpu = NULL;
    }

    Bus::~Bus() {
        free(memory);
    }

    void Bus::attach(CPU* cpu) {
        this->cpu = cpu;
    };

    uint8_t Bus::read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        return memory[addr];
    }

    void Bus::write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        uint8_t port = addr & 0xff;

        if (mem_io) {
            memory[addr] = data;
        } else {
            io_in(addr & 0xff, super_user);
        }
    }

    uint8_t Bus::io_in(uint8_t port, bool super_user) {
        return 0;
    }

    void Bus::io_out(uint8_t port, uint8_t data, bool super_user) {

    }
}