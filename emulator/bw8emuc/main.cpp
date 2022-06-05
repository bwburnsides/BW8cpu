#include "bw8cpu.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

uint8_t bus_read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code);
void bus_write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code);

int main() {
	BW8cpu::BW8cpu* cpu = BW8cpu::malloc_cpu(bus_read, bus_write);
	BW8cpu::reset(cpu, true);
	BW8cpu::dump(cpu, stdout);

	while (true) {
		Sleep(2);
		BW8cpu::rising(cpu);
		BW8cpu::falling(cpu);
		BW8cpu::dump(cpu, stdout);
		Sleep(1000);
	}
}

uint8_t bus_read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
	return 0x06;
}

void bus_write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
	return;
}