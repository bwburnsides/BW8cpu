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

        void clock();

        void rst(bool state);
        bool hlt();
        void coredump();

        void interrupt(uint8_t index, bool state);

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

        void dump(FILE *stream);

    private:
        bool irq_sources[8];

        char terminal[15][51];
        struct Cursor {
            uint8_t row;
            uint8_t col;
        } cursor;

        enum class Device {
            CLK,
            IRQ,
            DMA,
            UART,
        };

        uint8_t io(uint8_t port, uint8_t data, bool read_write, bool super_user);
    };  // class Bus
};  // namespace BW8