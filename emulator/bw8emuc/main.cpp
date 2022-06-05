#include "bw8cpu.h"

#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

int main() {
	BW8cpu::BW8cpu* cpu = BW8cpu::malloc_cpu();
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