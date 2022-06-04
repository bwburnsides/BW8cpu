#include "bw8cpu.h"


int main() {
	BW8cpu::BW8cpu* cpu = BW8cpu::malloc_cpu();
	BW8cpu::reset(cpu, true);
	BW8cpu::dump(cpu, stdout);
}