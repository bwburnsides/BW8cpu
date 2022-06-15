#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include "bw8bus.h"

namespace BW8 {
    namespace bus {
        uint8_t io_in(uint8_t port, bool super_user);
        void io_out(uint8_t port, bool super_user);

        uint8_t* init(const char* rom_path) {
            FILE* fp;
            size_t num_bytes;

            fp = fopen(rom_path, "rb");
            if (fp == NULL) {
                fprintf(stderr, "Error initialize_memory: Could not read ROM for CPU.\n");
                exit(-1);
            }

            num_bytes = fread(memory, sizeof(uint8_t), ROM_SIZE, fp);
            fclose(fp);

            for (int i = num_bytes; i < ADDR_SPACE_SIZE; i++) {
                memory[i] = 0x00;
            }

            for (int i = 0; i < 8; i++) {
                pic.interrupts[i] = false;
            }

            return memory;
        };

        uint8_t read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
            uint32_t addr = ((bank & 0xf) << 16) | ptr;
            return memory[addr];
        }

        void write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
            uint32_t addr = ((bank & 0xf) << 16) | ptr;
            uint8_t port = addr & 0xff;

            if (mem_io) {
                memory[addr] = data;
            } else {
                io_in(addr & 0xff, super_user);
            }
        }

        uint8_t io_in(uint8_t port, bool super_user) {
            switch (Port(port)) {
                case Port::CLK_MODE:
                    break;
                case Port::IRQ_SRC:
                    break;
                case Port::IRQ_MASK:
                    break;
                case Port::DMA_DST_BR:
                    break;
                case Port::DMA_DST_HI:
                    break;
                case Port::DMA_DST_LO:
                    break;
                case Port::DMA_SRC_BR:
                    break;
                case Port::DMA_SRC_HI:
                    break;
                case Port::DMA_SRC_LO:
                    break;
                case Port::DMA_LEN_HI:
                    break;
                case Port::DMA_LEN_LO:
                    break;
            }
        }
    }
}