#pragma once
#include <inttypes.h>
#include <thread>
#include <mutex>

#include "bw8bus.h"

namespace BW8{
    class Bus;

    class UART {
        public:
            UART(Bus* sys_bus);
            void enqueue_tx(uint8_t data);
            uint8_t dequeue_tx();
            void enqueue_rx(uint8_t data);
            uint8_t dequeue_rx();
            void dump(FILE* stream);

            void rst(bool state);
            void rising();
            void falling();

            uint8_t tx_count();
            uint8_t rx_count();

            uint8_t port(uint8_t reg, uint8_t data_in, bool read_write, bool super_user);

            enum class Port {
                RX,
                TX,
                CTRL,
            };

        private:
            Bus* bus;
            std::mutex mut;

            bool rst_flag;
            uint8_t watchdog;

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