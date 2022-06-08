#include <stdio.h>

#include "bw8cpu.h"

uint8_t bus_read(
    uint8_t bank,
    uint16_t ptr,
    bool mem_io,
    bool super_user,
    bool data_code
);

void bus_write(
    uint8_t bank,
    uint16_t ptr,
    uint8_t data,
    bool mem_io,
    bool super_user,
    bool data_code
);

int main(int argc, char** argv) {
    printf("Hello, world!\n");
    BW8cpu::BW8cpu* cpu = BW8cpu::cpu_malloc(bus_read, bus_write);
    BW8cpu::reset(cpu, true);
    BW8cpu::reset(cpu, false);

    cpu->IR = 0x14;
    cpu->tstate = 1;

    cpu->PC = 0;

    cpu->A = 45;
    BW8cpu::cpu_dump(cpu, stdout);
    BW8cpu::rising(cpu);
    BW8cpu::falling(cpu);

    BW8cpu::cpu_dump(cpu, stdout);

    BW8cpu::cpu_free(cpu);
}

uint8_t bus_read(
    uint8_t bank,
    uint16_t ptr,
    bool mem_io,
    bool super_user,
    bool data_code
) {
    return -1;
}

void bus_write(
    uint8_t bank,
    uint16_t ptr,
    uint8_t data,
    bool mem_io,
    bool super_user,
    bool data_code
) {
    return;
}