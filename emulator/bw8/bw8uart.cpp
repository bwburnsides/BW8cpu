#include <stdio.h>
#include <thread>
#include <conio.h>

#include "bw8uart.h"

#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)
#define randbool() (bool)(rand() % 2)

#define WATCHDOG_INITIAL 100

namespace BW8 {
    UART::UART(Bus* sys_bus) {
        bus = sys_bus;

        rst_flag = randbool();

        for (int i = 0; i < 8; i++) {
            tx_buffer[i] = randrange(0, 0xff);
            rx_buffer[i] = randrange(0, 0xff);
        }

        watchdog = WATCHDOG_INITIAL;

        tx_read = randrange(0, 0xff);
        tx_write = randrange(0, 0xff);

        rx_read = randrange(0, 0xff);
        rx_write = randrange(0, 0xff);

        std::thread console_thread(&UART::console_monitor, this);
        console_thread.detach();
    }

    void UART::console_monitor() {
        char new_char;
        while (true) {
            new_char = _getch();
            enqueue_rx(new_char);
        }
    }

    void UART::rising() {
        mut.lock();
        watchdog--;
        if (watchdog == 0 && rx_count() != 0) {
            bus->interrupt(0, true);
            watchdog = WATCHDOG_INITIAL;
        }
        mut.unlock();
    }

    void UART::falling() {

    }

    void UART::enqueue_tx(uint8_t data) {
        if (rst_flag) {
            return;
        }
        mut.lock();
        tx_buffer[tx_write++] = data;
        tx_write &= 15;
        mut.unlock();
    }

    uint8_t UART::dequeue_tx() {
        if (rst_flag) {
            return 0x00;
        }
        mut.lock();
        uint8_t byte = tx_buffer[tx_read++];
        tx_read &= 15;
        mut.unlock();
        return byte;
    }

    void UART::enqueue_rx(uint8_t data) {
        if (rst_flag) {
            return;
        }
        mut.lock();
        rx_buffer[rx_write++] = data;
        rx_write &= 15;
        watchdog = WATCHDOG_INITIAL;
        bus->interrupt(0, rx_count() > 3);
        mut.unlock();
    }

    uint8_t UART::dequeue_rx() {
        if (rst_flag) {
            return 0x00;
        }
        mut.lock();
        uint8_t byte = rx_buffer[rx_read++];
        rx_read &= 15;
        bus->interrupt(0, rx_count() > 3);
        mut.unlock();
        return byte;
    }

    void UART::rst(bool state) {
        rst_flag = state;

        if (rst_flag) {
            tx_read = 0;
            tx_write = 0;
            rx_read = 0;
            rx_write = 0;

            for (int i = 0; i < 8; i++) {
                tx_buffer[i] = 0;
                rx_buffer[i] = 0;
            }
        }
    }

    uint8_t UART::tx_count() {
        return (tx_write - tx_read) & 15;
    }

    uint8_t UART::rx_count() {
        return (rx_write - rx_read) & 15;
    }

    uint8_t UART::port(uint8_t reg, uint8_t data_in, bool read_write, bool super_user)
    {
        switch (Port(reg & 0xF)) {
            case Port::CTRL:
                if (read_write) {
                    return (tx_count() << 4) | (rx_count() << 0);
                }
                break;
            case Port::RX:
                if (read_write) {
                    return dequeue_rx();
                }
                break;
            case Port::TX:
                if (!read_write) {
                    enqueue_tx(data_in);
                }
                break;
        }
    }
};