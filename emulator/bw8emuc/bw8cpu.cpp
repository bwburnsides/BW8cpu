#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "bw8cpu.h"

#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)

namespace BW8cpu {

	BW8cpu* malloc_cpu(BusRead read, BusWrite write) {
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

		cpu->read = read;
		cpu->write = write;
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

		cpu->ALU = randrange(0, 0xff);  // TODO: base off of ctrl_latch
		cpu->ALU_FLAGS = randrange(0, 0xff);  // TODO: base off of ctrl_latch

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

		cpu->ALU = 0x00;	// TODO: base off of ctrl_latch
		cpu->ALU_FLAGS = 0x00;  // TODO: base off of ctrl_latch

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

		if (cpu->reset) {
			return;
		}

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
			(((int)cpu->mode << 16) & 0b11) |
			(((int)cpu->extended << 15) & 0b1) |
			cpu->IR << 7 |
			flags << 3 |
			(cpu->sequencer & 0b111)
		);

		for (int i = 0; i < 4; i++) {
			cpu->ctrl_latch[i] = cpu->ucode[i][state];
		}

		addr_assert(cpu);
		xfer_assert(cpu);
		alu_calculate(cpu);
		dbus_assert(cpu);
	}

	void falling(BW8cpu* cpu) {
		CtrlLines lines = decode_ctrl(cpu);

		cpu->clocks += 1;

		if (cpu->reset) {
			return;
		}

		cpu->sequencer++;
		cpu->sequencer %= 8;

		if (lines.rst_useq) {
			cpu->sequencer = 0;
		}

		if (cpu->sequencer == 0) {
			cpu->extended = false;
		}

		cpu->extended = lines.tog_ext;

		bool mem_io = true;
		bool data_code = true;

		uint8_t flags = cpu->ALU_FLAGS;

		switch (lines.count) {
			case Count::NONE:
				break;
			case Count::INC_PC:
				cpu->PC++;
				break;
			case Count::INC_SP:
				cpu->SP++;
				break;
			case Count::INC_X:
				cpu->X++;
				break;
			case Count::INC_Y:
				cpu->Y++;
				break;
			case Count::OFFSET_INC:
				break;
			case Count::DEC_X:
				cpu->X--;
				break;
			case Count::DEC_Y:
				cpu->Y--;
				break;
		}

		switch (lines.dbus_load) {
			case DbusLoad::A:
				cpu->A = cpu->dbus;
				break;
			case DbusLoad::B:
				cpu->B = cpu->dbus;
				break;
			case DbusLoad::C:
				cpu->C = cpu->dbus;
				break;
			case DbusLoad::D:
				cpu->D = cpu->dbus;
				break;
			case DbusLoad::DP:
				cpu->DP = cpu->dbus;
				break;
			case DbusLoad::DA:
				cpu->DA = cpu->dbus;
				break;
			case DbusLoad::TH:
				cpu->TH = cpu->dbus;
				break;
			case DbusLoad::TL:
				cpu->TL = cpu->dbus;
				break;
			case DbusLoad::SR:
				flags |= (
					(cpu->dbus & 0b1) >> 0,
					(cpu->dbus & 0b1) >> 1,
					(cpu->dbus & 0b1) >> 2,
					(cpu->dbus & 0b1) >> 3,
					(cpu->dbus & 0b1) >> 4
				);
				break;
			case DbusLoad::MEM:
				if (lines.addr_assert == AddrAssert::IO) {
					mem_io = false;
				}

				if (lines.addr_assert == AddrAssert::PC) {
					data_code = false;
				}

				cpu->write(cpu->BR, cpu->addr_out, cpu->dbus, mem_io, cpu->supervisor_mode, data_code);

				break;
			case DbusLoad::IR:
				cpu->IR = cpu->dbus;
				break;
			case DbusLoad::OFF:
				cpu->OF = cpu->dbus;
				break;
			case DbusLoad::PCH:
				cpu->PC = (cpu->dbus << 8) | (cpu->PC & 0xff);
				break;
			case DbusLoad::PCL:
				cpu->PC = (cpu->PC & (0xff << 8)) | cpu->dbus;
				break;
			case DbusLoad::SPH:
				cpu->SP = (cpu->dbus << 8) | (cpu->SP & 0xff);
				break;
			case DbusLoad::SPL:
				cpu->SP = (cpu->SP & (0xff << 8)) | cpu->dbus;
				break;
			case DbusLoad::XH:
				cpu->X = (cpu->dbus << 8) | (cpu->X & 0xff);
				break;
			case DbusLoad::XL:
				cpu->X = (cpu->X & (0xff << 8)) | cpu->dbus;
				break;
			case DbusLoad::YH:
				cpu->Y = (cpu->dbus << 8) | (cpu->Y & 0xff);
				break;
			case DbusLoad::YL:
				cpu->Y = (cpu->Y & (0xff << 8)) | cpu->dbus;
				break;
			case DbusLoad::BR:
				cpu->BR = cpu->dbus & 0xf;
				break;
			default:
				break;
		}

		decode_flags(cpu, flags);

		switch (lines.xfer_load) {
			case XferLoad::PC:
				cpu->PC = cpu->xfer;
				break;
			case XferLoad::SP:
				cpu->SP = cpu->xfer;
				break;
			case XferLoad::X:
				cpu->X = cpu->xfer;
				break;
			case XferLoad::Y:
				cpu->Y = cpu->xfer;
				break;
			case XferLoad::AB:
				cpu->A = cpu->xfer >> 8;
				cpu->B = cpu->xfer & 0xff;
				break;
			case XferLoad::CD:
				cpu->C = cpu->xfer >> 8;
				cpu->D = cpu->xfer & 0xff;
				break;
			default:
				break;
		}
	}

	void addr_assert(BW8cpu* cpu) {
		CtrlLines lines = decode_ctrl(cpu);

		uint8_t offset_inc;
		uint16_t offset;
		uint8_t offset_hi;

		if (lines.count == Count::OFFSET_INC) {
			offset_inc = 1;
		}
		else {
			offset_inc = 0;
		}

		switch (lines.addr_assert) {
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
		if (!lines.offset) {
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
		CtrlLines lines = decode_ctrl(cpu);

		switch (lines.xfer_assert) {
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
				break;
		}
	}

	void alu_calculate(BW8cpu* cpu) {
		uint8_t alu_op = (uint8_t)(decode_ctrl(cpu).alu_op);

		uint8_t sum_func	= (alu_op >> 0) & 0b11;
		uint8_t shift_func	= (alu_op >> 2) & 0b11;
		uint8_t logic_func	= (alu_op >> 4) & 0b1111;
		uint8_t cf_func		= (alu_op >> 8) & 0b111;
		uint8_t zf_func		= (alu_op >> 11) & 0b11;
		uint8_t vf_func		= (alu_op >> 13) & 0b11;
		uint8_t nf_func		= (alu_op >> 15) & 0b11;
		uint8_t if_func		= (alu_op >> 17) & 0b11;

		uint8_t lhs = cpu->xfer >> 8;
		uint8_t rhs = cpu->xfer & 0xff;

		uint8_t left = 0;
		uint8_t right = 0;
		uint16_t sum = 0;
		uint8_t result = 0;
		uint8_t flags_result = 0;

		bool c_shift = false;
		bool c_sum = false;
		bool c_new = false;
		bool z_new = false;
		bool v_new = false;
		bool n_new = false;
		bool i_new = false;

		// 1. Compute both Shift and Logic stage outputs
		// 2. Compute Sum stage outputs
		// 3. Compute flags
		// 4. Select and pack flags

		switch (ShiftFunc(shift_func)) {
			case ShiftFunc::LHS:
				left = lhs;
				break;
			case ShiftFunc::SRC:
				left = lhs >> 1;
				if (cpu->carry_flag) {
					left & 0b10000000;
				}
				break;
			case ShiftFunc::ASR:
				left = (uint8_t)(((int8_t)lhs) >> 1);
				break;
			case ShiftFunc::ZERO:
				left = 0;
				break;
		}

		if (lhs & 0b00000001) {
			c_shift = true;
		}

		switch (LogicFunc(logic_func)) {
			case LogicFunc::ZERO:
				right = 0;
				break;
			case LogicFunc::MAX:
				right = 0xff;
				break;
			case LogicFunc::LHS:
				right = lhs;
				break;
			case LogicFunc::RHS:
				right = rhs;
				break;
			case LogicFunc::notLHS:
				right = ~lhs;
				break;
			case LogicFunc::notRHS:
				right = ~rhs;
				break;
			case LogicFunc::OR:
				right = lhs | rhs;
				break;
			case LogicFunc::AND:
				right = lhs & rhs;
				break;
			case LogicFunc::XOR:
				right = lhs ^ rhs;
				break;
		}

		switch (SumFunc(sum_func)) {
			case SumFunc::ZERO:
				sum = left + right + 0;
				break;
			case SumFunc::CF:
				sum = left + right + (uint8_t)cpu->carry_flag;
				break;
			case SumFunc::ONE:
				sum = left + right + 1;
				break;
		}

		if (sum > 0xff) {
			c_sum = true;
		}

		result = (uint8_t)(sum & 0xff);

		if (result == 0) {
			z_new = true;
		}

		if (
			((left & 0b10000000) == (right & 0b10000000))
			&& ((result & 0b10000000) != (left & 0b10000000))
		) {
			v_new = true;
		}

		if (result & 0b10000000) {
			n_new = true;
		}

		switch (CfFunc(cf_func)) {
			case CfFunc::ONE:
				c_new = true;
				break;
			case CfFunc::C_SHIFT:
				c_new = c_shift;
				break;
			case CfFunc::C_SUM:
				c_new = c_sum;
				break;
			case CfFunc::ZERO:
				c_new = false;
				break;
			case CfFunc::NO_CHANGE:
				c_new = cpu->carry_flag;
				break;
		}

		switch (ZfFunc(zf_func)) {
			case ZfFunc::ONE:
				z_new = true;
				break;
			case ZfFunc::NEW:
				break;
			case ZfFunc::ZERO:
				z_new = false;
				break;
			case ZfFunc::NO_CHANGE:
				z_new = cpu->zero_flag;
				break;
		}

		switch (VfFunc(vf_func)) {
			case VfFunc::ONE:
				v_new = true;
				break;
			case VfFunc::NEW:
				break;
			case VfFunc::ZERO:
				v_new = false;
				break;
			case VfFunc::NO_CHANGE:
				v_new = cpu->zero_flag;
				break;
		}

		switch (NfFunc(nf_func)) {
			case NfFunc::ONE:
				n_new = true;
				break;
			case NfFunc::NEW:
				break;
			case NfFunc::ZERO:
				n_new = false;
				break;
			case NfFunc::NO_CHANGE:
				n_new = cpu->zero_flag;
				break;
		}

		switch (IfFunc(if_func)) {
		case IfFunc::ONE:
			i_new = true;
			break;
		case IfFunc::ZERO:
			i_new = false;
			break;
		case IfFunc::NO_CHANGE:
			i_new = cpu->interrupt_enable;
			break;
		}

		flags_result |= (
			(i_new & 0b1) >> 0,
			(n_new & 0b1) >> 1,
			(v_new & 0b1) >> 2,
			(z_new & 0b1) >> 3,
			(c_new & 0b1) >> 4
		);

		cpu->ALU = result;
		cpu->ALU_FLAGS = flags_result;
	}

	void dbus_assert(BW8cpu* cpu) {
		CtrlLines lines = decode_ctrl(cpu);

		bool mem_io = true;
		bool data_code = true;

		switch (lines.dbus_assert) {
			case DbusAssert::ALU:
				cpu->dbus = cpu->ALU;
				break;
			case DbusAssert::A:
				cpu->dbus = cpu->A;
				break;
			case DbusAssert::B:
				cpu->dbus = cpu->B;
				break;
			case DbusAssert::C:
				cpu->dbus = cpu->C;
				break;
			case DbusAssert::D:
				cpu->dbus = cpu->D;
				break;
			case DbusAssert::DP:
				cpu->dbus = cpu->DP;
				break;
			case DbusAssert::DA:
				cpu->dbus = cpu->DA;
				break;
			case DbusAssert::TH:
				cpu->dbus = cpu->TH;
				break;
			case DbusAssert::TL:
				cpu->dbus = cpu->TL;
				break;
			case DbusAssert::SR:
				cpu->dbus = (
					(cpu->interrupt_enable & 0b1) >> 0,
					(cpu->negative_flag & 0b1) >> 1,
					(cpu->overflow_flag & 0b1) >> 2,
					(cpu->zero_flag & 0b1) >> 3,
					(cpu->carry_flag & 0b1) >> 4
				);
				break;
			case DbusAssert::MEM:
				if (lines.addr_assert == AddrAssert::IO) {
					mem_io = false;
				}
				if (lines.addr_assert == AddrAssert::PC) {
					data_code = false;
				}

				cpu->dbus = cpu->read(cpu->BR, cpu->addr_out, mem_io, cpu->supervisor_mode, data_code);
				break;
			case DbusAssert::MSB:
				cpu->dbus = cpu->xfer >> 8;
				break;
			case DbusAssert::LSB:
				cpu->dbus = cpu->xfer & 0xff;
				break;
			case DbusAssert::BR:
				cpu->dbus = cpu->BR & 0b1111;
				break;
			default:
				cpu->dbus = 0;
		}
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
			cpu->addr,
			cpu->B,
			cpu->DA,
			cpu->OF,
			cpu->xfer,
			cpu->C,
			cpu->TH,
			cpu->BR,
			cpu->dbus,
			cpu->D,
			cpu->TL
		);
	}

	void dump_ctrl(BW8cpu *cpu, FILE* fout) {
		CtrlLines lines = decode_ctrl(cpu);
		fprintf(
			fout,
			CTRL_FMT,
			lines.dbus_assert,
			lines.alu_op,
			lines.dbus_load,
			lines.addr_assert,
			lines.xfer_assert,
			lines.xfer_load,
			lines.count,
			lines.dec_sp,
			lines.rst_useq,
			lines.tog_ext,
			lines.offset,
			lines.unused
		);
	}

	CtrlLines decode_ctrl(BW8cpu* cpu) {
		CtrlLines lines;

		lines.dbus_assert	= DbusAssert((cpu->ctrl_latch[0] >> 0) & 0b1111);
		lines.alu_op 		= AluOp((cpu->ctrl_latch[0] >> 4) & 0b1111);
		lines.dbus_load 	= DbusLoad((cpu->ctrl_latch[1] >> 0) & 0b11111);
		lines.addr_assert 	= AddrAssert((cpu->ctrl_latch[1] >> 5) & 0b111);
		lines.xfer_assert	= XferAssert((cpu->ctrl_latch[2] >> 0) & 0b11111);
		lines.xfer_load 	= XferLoad((cpu->ctrl_latch[2] >> 5) & 0b111);
		lines.count 		= Count((cpu->ctrl_latch[3] >> 0) & 0b111);
		lines.dec_sp 		= (bool)((cpu->ctrl_latch[3] >> 3) & 0b1);
		lines.rst_useq 		= (bool)((cpu->ctrl_latch[3] >> 4) & 0b1);
		lines.tog_ext 		= (bool)((cpu->ctrl_latch[3] >> 5) & 0b1);
		lines.offset 		= (bool)((cpu->ctrl_latch[3] >> 6) & 0b1);
		lines.unused 		= (bool)((cpu->ctrl_latch[3] >> 7) & 0b1);

		return lines;
	}

	void dump_state(BW8cpu* cpu, FILE* fout) {
		// state.mode		=;
		// state.extended	=;
		// state.opcode	=;
		// state.flags		=;
		// state.step		=;
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

	void decode_flags(BW8cpu* cpu, uint8_t flags) {
		cpu->interrupt_enable = (bool) ((flags >> 0) & 0b1);
		cpu->negative_flag = (bool) ((flags >> 1) & 0b1);
		cpu->overflow_flag = (bool) ((flags >> 2) & 0b1);
		cpu->zero_flag = (bool) ((flags >> 3) & 0b1);
		cpu->carry_flag = (bool) ((flags >> 4) & 0b1);
	}
}