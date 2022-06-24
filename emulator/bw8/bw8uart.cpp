#include <stdio.h>
#include <thread>
#include <conio.h>

#include "bw8uart.h"

namespace BW8 {
    UART::UART(Bus* sys_bus, FILE *istream, FILE *ostream) {
        bus = sys_bus;
        bus->attach(this);

        input = istream;
        output = ostream;

        for (int i = 0; i < 8; i++) {
            tx_buffer[i] = 0;
            rx_buffer[i] = 0;
        }

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

    void UART::enqueue_tx(uint8_t data) {
        tx_buffer[tx_write++] = data;
        tx_write %= 8;
    }

    uint8_t UART::dequeue_tx() {
        uint8_t byte = tx_buffer[tx_read++];
        tx_read %= 8;
        return byte;
    }

    void UART::enqueue_rx(uint8_t data) {
        rx_buffer[rx_write++] = data;
        rx_write %= 8;
        bus->interrupt(0, rx_count() > 3 ? true : false);
    }

    uint8_t UART::dequeue_rx() {
        uint8_t byte = rx_buffer[rx_read++];
        rx_read %= 8;
        return byte;
    }

    void UART::dump(FILE* stream) {
        fprintf(stream, "\033[0;0H");
        fprintf(stream, "tx read ptr: %d\n", tx_read);
        fprintf(stream, "tx write ptr: %d\n", tx_write);
        fprintf(stream, "rx read ptr: %d\n", rx_read);
        fprintf(stream, "rx write ptr: %d\n", rx_write);
        fprintf(stream, "tx count: %d\n", tx_count());
        fprintf(stream, "rx count: %d\n", rx_count());

        fprintf(stream, "tx buf\trx_buff\n");
        for (int i = 0; i < 8; i++) {
            fprintf(stream, "%02X\t%02X\n", tx_buffer[i], rx_buffer[i]);
        }
    }

    uint8_t UART::tx_count() {
        return (tx_write - tx_read) % 8;
    }

    uint8_t UART::rx_count() {
        return (rx_write - rx_read) % 8;
    }
};