#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "bw8cpu.h"

#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)

namespace BW8cpu {

	BW8cpu* malloc_cpu() {
		BW8cpu* cpu = (BW8cpu*)malloc(sizeof(BW8cpu) * 1);

		if (cpu == NULL) {
			fprintf(stderr, "Error BW8cpu *create_cpu: Could not allocate memory for CPU.\n");
			exit(-1);
		}

		for (int i = 0; i < 4; i++) {
			cpu->ucode[i] = (uint8_t*)calloc(256 * 1024, sizeof(uint8_t));

			if (cpu->ucode[i] == NULL) {
				fprintf(stderr, "Error BW8cpu *create_cpu: Could not allocate memory for CPU.\n");
				exit(-1);
			}
		}

		cpu->clocks = 0;

		srand(time(NULL));

		cpu->A = randrange(0, 0xff);
		cpu->B = randrange(0, 0xff);
		cpu->A = randrange(0, 0xff);
		cpu->A = randrange(0, 0xff);

		cpu->DP = randrange(0, 0xff);
		cpu->DA = randrange(0, 0xff);
		cpu->TH = randrange(0, 0xff);
		cpu->TL = randrange(0, 0xff);
		cpu->IR = randrange(0, 0xff);
		cpu->OF = randrange(0, 0xff);
		cpu->BR = randrange(0, 0xf);	// 4b register not 8b

		cpu->ALU = randrange(0, 0xff);	// TODO: is this accurate?

		cpu->PC = randrange(0, 0xffff);
		cpu->SP = randrange(0, 0xffff);
		cpu->X = randrange(0, 0xffff);
		cpu->Y = randrange(0, 0xffff);

		cpu->carry_flag = rand() % 2;
		cpu->zero_flag = rand() % 2;
		cpu->overflow_flag = rand() % 2;
		cpu->negative_flag = rand() % 2;
		cpu->interrupt_enable = rand() % 2;

		cpu->interrupt_request = rand() % 2;
		cpu->nonmaskable_interrupt = rand() % 2;
		cpu->bus_request = rand() % 2;
		cpu->reset = rand() % 2;

		read_ucode(cpu);
		cpu->sequencer = randrange(0, 7);

		for (int i = 0; i < 4; i++) {
			cpu->ctrl_latch[i] = randrange(0, 0xff);
		}

		cpu->extended = rand() % 2;
		cpu->supervisor_mode = rand() % 2;
		cpu->use_bank_reg = rand() % 2;
		cpu->nmi_enable = rand() % 2;

		// TODO: these should take their values based on the random control bus values
		cpu->dbus = randrange(0, 0xff);
		cpu->xfer = randrange(0, 0xffff);
		cpu->addr = randrange(0, 0xffff);
		cpu->addr_out = randrange(0, 0xffff);

		return cpu;
	}

	void free_cpu(BW8cpu* cpu) {
		free(cpu->ucode);
		free(cpu);
	}

	void reset(BW8cpu* cpu, bool state) {
		cpu->reset = state;

		if (!cpu->reset) {
			return;
		}

		cpu->A = 0x00;
		cpu->B = 0x00;
		cpu->C = 0x00;
		cpu->D = 0x00;

		cpu->DP = 0x00;
		cpu->DA = 0x00;
		cpu->TH = 0x00;
		cpu->TL = 0x00;
		cpu->IR = 0x00;
		cpu->OF = 0x00;
		cpu->BR = 0x0;		// 4b register not 8b

		cpu->ALU = 0x00;	// TODO: is this accurate?

		cpu->PC = 0x0000;
		cpu->SP = 0x0000;
		cpu->X = 0x0000;
		cpu->Y = 0x0000;

		cpu->carry_flag = false;
		cpu->zero_flag = false;
		cpu->overflow_flag = false;
		cpu->negative_flag = false;
		cpu->interrupt_enable = false;

		cpu->interrupt_request = false;
		cpu->nonmaskable_interrupt = false;
		cpu->bus_request = false;

		cpu->sequencer = 0;

		cpu->extended = false;
		cpu->supervisor_mode = true;
		cpu->use_bank_reg = false;
		cpu->nmi_enable = true;

		// TODO: these should take their values based on the random control bus values
		cpu->dbus = 0x00;
		cpu->xfer = 0x0000;
		cpu->addr = 0x0000;
		cpu->addr_out = 0x0000;
	}

	void rising(BW8cpu* cpu) {
		uint32_t state = 0;
		uint8_t flags = 0;

		if (cpu->sequencer == 0) {
			update_mode(cpu);
		}

		flags |= (
			(int)cpu->carry_flag << 0 |
			(int)cpu->zero_flag << 1 |
			(int)cpu->overflow_flag << 2 |
			(int)cpu->negative_flag << 3|
			(int)cpu-> interrupt_enable << 4
		) & 0b00011111;

		state |= (
			(int)cpu->mode << 16 |
			(int)cpu->extended << 15 |
			cpu->IR << 7 |
			flags << 3 |
			(cpu->sequencer & 0b111)
		);

		for (int i = 0; i < 4; i++) {
			cpu->ctrl_latch[i] = cpu->ucode[i][state];
		}

		addr_assert(cpu);
		xfer_assert(cpu);


	}

	void falling(BW8cpu* cpu) {
		cpu->sequencer++;
		cpu->sequencer %= 8;

		cpu->clocks += 1;
	}

	void dump(BW8cpu *cpu, FILE* fout) {
		fprintf(
			fout,
			STATE_FMT,
			cpu->clocks,
			cpu->sequencer,
			cpu->carry_flag ? GREEN_TXT : RED_TXT,
			cpu->zero_flag ? GREEN_TXT : RED_TXT,
			cpu->overflow_flag ? GREEN_TXT : RED_TXT,
			cpu->negative_flag ? GREEN_TXT : RED_TXT,
			cpu->interrupt_enable ? GREEN_TXT : RED_TXT,
			cpu->supervisor_mode ? GREEN_TXT : RED_TXT,
			cpu->use_bank_reg ? GREEN_TXT : RED_TXT,
			cpu->reset ? GREEN_TXT : RED_TXT,
			cpu->bus_request ? GREEN_TXT : RED_TXT,
			cpu->nonmaskable_interrupt ? GREEN_TXT : RED_TXT,
			cpu->interrupt_request ? GREEN_TXT : RED_TXT,
			"TODO",
			cpu->PC,
			cpu->SP,
			cpu->X,
			cpu->Y,
			cpu->A,
			cpu->DP,
			cpu->IR,
			cpu->B,
			cpu->DA,
			cpu->OF,
			cpu->C,
			cpu->TH,
			cpu->BR,
			cpu->D,
			cpu->TL
		);
	}

	void addr_assert(BW8cpu* cpu) {
		uint8_t addr_assert = (cpu->ctrl_latch[1] >> 5) & 0b111;
		uint8_t offset_en = (cpu->ctrl_latch[3] >> 6) & 0b1;
		uint8_t offset_inc = (cpu->ctrl_latch[3] >> 0) & 0b111;
		uint16_t offset;
		uint8_t offset_hi;

		if ((Count)offset_inc == Count::OFFSET_INC) {
			offset_inc = 1;
		}
		else {
			offset_inc = 0;
		}

		switch (AddrAssert(addr_assert)) {
			case AddrAssert::ACK:
				cpu->addr = 0x0000;
				break;
			case AddrAssert::PC:
				cpu->addr = cpu->PC;
				break;
			case AddrAssert::SP:
				cpu->addr = cpu->SP;
				break;
			case AddrAssert::X:
				cpu->addr = cpu->X;
				break;
			case AddrAssert::Y:
				cpu->addr = cpu->Y;
				break;
			case AddrAssert::DP:
				cpu->addr = (cpu->DP << 8) | cpu->DA;
				break;
			case AddrAssert::T:
				cpu->addr = (cpu->TH << 8) | cpu->TL;
				break;
			case AddrAssert::IO:
				cpu->addr = (cpu->TH << 8) | cpu->TL;
				break;
		}

		// Calculate the offset-applied address, if applicable
		if (!offset_en) {
			cpu->addr_out = cpu->addr;
		}
		else {
			if (cpu->OF & 0b10000000) {
				offset_hi = 0xff;
			}
			else {
				offset_hi = 0x00;
			}

			offset = (offset_hi << 8) | cpu->OF;

			cpu->addr_out = cpu->addr + offset + offset_inc;
		}
	}

	void xfer_assert(BW8cpu* cpu) {
		uint8_t xfer_assert = (cpu->ctrl_latch[1] >> 0) & 0b11111;
		switch (XferAssert(xfer_assert)) {
			case XferAssert::PC:
				cpu->xfer = cpu->PC;
				break;
			case XferAssert::SP:
				cpu->xfer = cpu->SP;
				break;
			case XferAssert::X:
				cpu->xfer = cpu->X;
				break;
			case XferAssert::Y:
				cpu->xfer = cpu->Y;
				break;
			case XferAssert::IRQ:
				cpu->xfer = IRQ_ADDR;
				break;
			case XferAssert::ADDR:
				cpu->xfer = cpu->addr_out;
				break;
			case XferAssert::A_A:
				cpu->xfer = concatenate_bytes(cpu->A, cpu->A);
				break;
			case XferAssert::A_B:
				cpu->xfer = concatenate_bytes(cpu->A, cpu->B);
				break;
			case XferAssert::A_C:
				cpu->xfer = concatenate_bytes(cpu->A, cpu->C);
				break;
			case XferAssert::A_D:
				cpu->xfer = concatenate_bytes(cpu->A, cpu->D);
				break;
			case XferAssert::A_TL:
				cpu->xfer = concatenate_bytes(cpu->A, cpu->TL);
				break;
			case XferAssert::B_A:
				cpu->xfer = concatenate_bytes(cpu->B, cpu->A);
				break;
			case XferAssert::B_B:
				cpu->xfer = concatenate_bytes(cpu->B, cpu->B);
				break;
			case XferAssert::B_C:
				cpu->xfer = concatenate_bytes(cpu->B, cpu->C);
				break;
			case XferAssert::B_D:
				cpu->xfer = concatenate_bytes(cpu->B, cpu->D);
				break;
			case XferAssert::B_TL:
				cpu->xfer = concatenate_bytes(cpu->B, cpu->TL);
				break;
			case XferAssert::C_A:
				cpu->xfer = concatenate_bytes(cpu->C, cpu->A);
				break;
			case XferAssert::C_B:
				cpu->xfer = concatenate_bytes(cpu->C, cpu->B);
				break;
			case XferAssert::C_C:
				cpu->xfer = concatenate_bytes(cpu->C, cpu->C);
				break;
			case XferAssert::C_D:
				cpu->xfer = concatenate_bytes(cpu->C, cpu->D);
				break;
			case XferAssert::C_TL:
				cpu->xfer = concatenate_bytes(cpu->C, cpu->TL);
				break;
			case XferAssert::D_A:
				cpu->xfer = concatenate_bytes(cpu->D, cpu->A);
				break;
			case XferAssert::D_B:
				cpu->xfer = concatenate_bytes(cpu->D, cpu->B);
				break;
			case XferAssert::D_C:
				cpu->xfer = concatenate_bytes(cpu->D, cpu->C);
				break;
			case XferAssert::D_D:
				cpu->xfer = concatenate_bytes(cpu->D, cpu->D);
				break;
			case XferAssert::D_TL:
				cpu->xfer = concatenate_bytes(cpu->D, cpu->TL);
				break;
			case XferAssert::TH_A:
				cpu->xfer = concatenate_bytes(cpu->TH, cpu->A);
				break;
			case XferAssert::TH_B:
				cpu->xfer = concatenate_bytes(cpu->TH, cpu->B);
				break;
			case XferAssert::TH_C:
				cpu->xfer = concatenate_bytes(cpu->TH, cpu->C);
				break;
			case XferAssert::TH_D:
				cpu->xfer = concatenate_bytes(cpu->TH, cpu->D);
				break;
			case XferAssert::T:
				cpu->xfer = concatenate_bytes(cpu->TH, cpu->TL);
				break;
			case XferAssert::NMI:
				cpu->xfer = NMI_ADDR;
		}
	}

	void alu_calculate(BW8cpu* cpu) {

	}

	void update_mode(BW8cpu* cpu) {
		if (cpu->bus_request) {
			cpu->mode = Mode::STALL;
		}
		else if (cpu->nonmaskable_interrupt) {
			cpu->mode = Mode::NMI;
		}
		else if (cpu->interrupt_request) {
			cpu->mode = Mode::IRQ;
		}
		else {
			cpu->mode = Mode::FETCH;
		}
	}

	uint16_t concatenate_bytes(uint8_t left, uint8_t right) {
		return (left << 8) | right;
	}

	void read_ucode(BW8cpu* cpu) {
		const char* fname[4] = {
			"C:/Users/brady/projects/BW8cpu/control/microcode0.bin",
			"C:/Users/brady/projects/BW8cpu/control/microcode1.bin",
			"C:/Users/brady/projects/BW8cpu/control/microcode2.bin",
			"C:/Users/brady/projects/BW8cpu/control/microcode3.bin",
		};
		FILE* fp;


		for (int i = 0; i < 4; i++) {
			fp = fopen(fname[i], "rb");

			if (fp == NULL) {
				fprintf(stderr, "Error void read_ucode: Unable to open file \"%s\"\n", fname[i]);
			}
			fread(cpu->ucode[i], sizeof(uint8_t), 256 * 1024, fp);
			fclose(fp);
		}
	}
}