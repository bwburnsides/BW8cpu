#pragma once

#include <inttypes.h>
#include "bw8pic.h"

#define ADDR_SPACE_SIZE 1024 * 1024
#define ROM_SIZE 64 * 1024

namespace BW8 {
    namespace bus {
        static uint8_t memory[ADDR_SPACE_SIZE];
        static pic::BW8pic pic;

        uint8_t* init(const char* rom_path);

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
        };
    }
}