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
        uart = NULL;
    }

    Bus::~Bus() {
        free(memory);
    }

    void Bus::attach(CPU* cpu) {
        this->cpu = cpu;
    };

    void Bus::attach(UART* uart) {
        this->uart = uart;
    };

    void Bus::interrupt(uint8_t index, bool state){
        irq_sources[index % 8] = state;
        for (int i = 0; i < 8; i++) {
            if (irq_sources[i]) {
                cpu->irq(true);
                return;
            }
        }
        cpu->irq(false);
    };

    void Bus::dump(FILE *stream) {
        // fprintf(stream, "%s", "\033[0;0H");
        // cpu->dump(stream);
        // uart->dump(stream);
        for (int i = 0; i < uart->tx_count(); i++) {
            fprintf(stream, "%c", uart->dequeue_tx());
        }
    }

    uint8_t Bus::read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        uint8_t port = addr & 0xff;

        if (mem_io) {
            return memory[addr];
        } else {
            return io(port, 0x00, true, super_user);
        }
    }

    void Bus::write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        uint8_t port = addr & 0xff;

        if (mem_io) {
            memory[addr] = data;
        } else {
            io(port, data, false, super_user);
        }
    }

    uint8_t Bus::io(uint8_t port, uint8_t data_in, bool read_write, bool super_user) {
        uint8_t data_out;
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
            case Port::UART_RX:
                if (read_write) {
                    data_out = uart->dequeue_rx();
                    return data_out;
                }
            case Port::UART_TX:
                if (!read_write) {
                    uart->enqueue_tx(data_in);
                }
                break;
            case Port::UART_CTRL:
                break;
        }
    }
}