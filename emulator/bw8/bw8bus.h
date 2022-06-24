#pragma once

#include <inttypes.h>
#include "bw8cpu.h"
#include "bw8uart.h"

#define ADDR_SPACE_SIZE 1024 * 1024
#define ROM_SIZE 64 * 1024

namespace BW8 {
    class CPU;
    class UART;

    class Bus {
    public:
        uint8_t* memory;
        CPU* cpu;
        UART* uart;

        Bus(const char* rom_path);
        ~Bus();

        void attach(CPU* cpu);
        void attach(UART* uart);

        uint8_t read(
            uint8_t bank,
            uint16_t ptr,
            bool mem_io,
            bool super_user,
            bool data_code
        );

        void write(
            uint8_t bank,
            uint16_t ptr,
            uint8_t data,
            bool mem_io,
            bool super_user,
            bool data_code
        );

        void interrupt(uint8_t index, bool state);

        void dump(FILE *stream);

    private:
        bool irq_sources[8];

        enum class Port {
            CLK_MODE,
            IRQ_SRC,
            IRQ_MASK,
            DMA_DST_BR,
            DMA_DST_HI,
            DMA_DST_LO,
            DMA_SRC_BR,
            DMA_SRC_HI,
            DMA_SRC_LO,
            DMA_LEN_HI,
            DMA_LEN_LO,
            UART_RX,
            UART_TX,
            UART_CTRL,
        };

        uint8_t io(uint8_t port, uint8_t data, bool read_write, bool super_user);
    };  // class Bus
};  // namespace BW8