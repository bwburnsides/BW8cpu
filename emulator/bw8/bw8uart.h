#pragma once
#include <inttypes.h>
#include <thread>

#include "bw8bus.h"

namespace BW8{
    class Bus;

    class UART {
        public:
            UART(Bus* sys_bus, FILE *istream, FILE *ostream);
            void enqueue_tx(uint8_t data);
            uint8_t dequeue_tx();
            void enqueue_rx(uint8_t data);
            uint8_t dequeue_rx();
            void dump(FILE* stream);

            uint8_t tx_count();
            uint8_t rx_count();

        private:
            Bus* bus;
            FILE *input;
            FILE *output;

            uint8_t tx_read;
            uint8_t tx_write;

            uint8_t rx_read;
            uint8_t rx_write;

            uint8_t tx_buffer[8];
            uint8_t rx_buffer[8];

            std::thread console_thread;
            void console_monitor();
    };
}