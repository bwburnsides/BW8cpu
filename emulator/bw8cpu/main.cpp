#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include "bw8cpu.h"

#define ADDR_SPACE_SIZE 1024 * 1024
#define ROM_SIZE 64 * 1024
static uint8_t memory[ADDR_SPACE_SIZE];

void initialize_memory(const char* rom_path);

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
    if (argc < 2) {
        fprintf(stderr, "usage: bw8emu.exe <rom_path>");
        exit(-1);
    }

    char *fname = argv[1];
    initialize_memory(fname);
    BW8cpu::BW8cpu* cpu = BW8cpu::cpu_malloc(bus_read, bus_write);
    BW8cpu::reset(cpu, true);
    BW8cpu::reset(cpu, false);

    while (true) {
        BW8cpu::cpu_dump(cpu, stdout);
        BW8cpu::clock(cpu);
        Sleep(1000);
    }

    BW8cpu::cpu_free(cpu);
}

void initialize_memory(const char* rom_path) {
	FILE* fp;
	size_t num_bytes;

	fp = fopen(rom_path, "rb");
	if (fp == NULL) {
		fprintf(stderr, "Error initialize_memory: Could not read ROM for CPU.\n");
		exit(-1);
	}

	num_bytes = fread(memory, sizeof(uint8_t), ROM_SIZE, fp);
	fclose(fp);

	for (int i = num_bytes; i < ADDR_SPACE_SIZE; i++)
		memory[i] = 0x00;
}

uint8_t bus_read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
	uint32_t addr = ((bank & 0xf) << 16) | ptr;
	return memory[addr];
}

void bus_write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
	uint32_t addr = ((bank & 0xf) << 16) | ptr;
	memory[addr] = data;
}
