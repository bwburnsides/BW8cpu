#include <stdio.h>

#include "bw8uart.h"

namespace BW8 {
    UART::UART(Bus* sys_bus) {
        bus = sys_bus;
        bus->attach(this);

        for (int i = 0; i < 8; i++) {
            tx_buffer[i] = 0;
            rx_buffer[i] = 0;
        }
    }

    void UART::rising() {
        if (rx_write >= 4) {
            bus->interrupt(0, true);
        } else {
            bus->interrupt(0, false);
        }
    }

    void UART::falling() {

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

    uint8_t UART::dequeue_rx() {
        uint8_t byte = rx_buffer[rx_read++];
        rx_read %= 8;
        return byte;
    }

    void UART::dump(FILE* stream) {
        fprintf(stream, "tx read ptr: %d\n", tx_read);
        fprintf(stream, "tx write ptr: %d\n", tx_write);
        fprintf(stream, "rx read ptr: %d\n", rx_read);
        fprintf(stream, "rx write ptr: %d\n", rx_write);

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