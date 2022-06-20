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
        if (tx_write >= 4) {
            bus->interrupt(0, true);
        } else {
            bus->interrupt(0, false);
        }
    }

    void UART::falling() {

    }


    void UART::enqueue_tx(uint8_t data) {
        tx_buffer[tx_write++] = data;
    }

    void UART::print(FILE* stream) {
        fprintf(stream, "tx read ptr: %d\n", tx_read);
        fprintf(stream, "tx write ptr: %d\n", tx_write);
        fprintf(stream, "rx read ptr: %d\n", rx_read);
        fprintf(stream, "rx write ptr: %d\n", rx_write);

        fprintf(stream, "tx buf\trx_buff\n");
        for (int i = 0; i < 8; i++) {
            fprintf(stream, "%d\t%d\n", tx_buffer[i], rx_buffer[i]);
        }
    }
};