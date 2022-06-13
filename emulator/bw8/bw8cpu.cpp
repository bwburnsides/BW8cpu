#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "bw8cpu.h"


#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)
#define randbool() (bool)(rand() % 2)

namespace BW8cpu {
    uint8_t pack_state_flags(BW8cpu* cpu);
    CtrlLines decode_ctrl(BW8cpu* cpu);
    AluCtrlLines decode_alu_ctrl(BW8cpu *cpu);
    void assert_addr(BW8cpu* cpu);
    void assert_xfer(BW8cpu* cpu);
    void calculate_alu(BW8cpu* cpu);
    void assert_dbus(BW8cpu* cpu);
    void read_ucode(BW8cpu* cpu);
    const char* mode_repr(Mode mode);
    const char* bool_colored(bool flag);

    void reset(BW8cpu* cpu, bool status) {
        cpu->interrupts.rst = status;

        if (!cpu->interrupts.rst) {
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
        cpu->BR = 0x0;      // 4b register not 8b

        cpu->ALU = 0x00;    // TODO: base off of ctrl
        cpu->ALU_FLAGS = {
            false,
            false,
            false,
            false,
            false
        };  // TODO: base off of ctrl

        cpu->PC = 0x0000;
        cpu->SP = 0x0000;
        cpu->X = 0x0000;
        cpu->Y = 0x0000;

        cpu->status_flags = {
            false,  // Cf
            false,  // Zf
            false,  // Vf
            false,  // Nf
            false,  // If
            false,  // EXT
            true,   // ~SUP
            false,  // UBR
            true,   // ~(NMI Enable)
        };

        cpu->bus_flags = {
            true,
            true,
        };

        cpu->interrupts = {
            false,
            false,
            false,
            false,
        };

        cpu->mode = Mode::FETCH;
        cpu->tstate = 0;
        cpu->state = 0;
        for (int i = 0; i < 4; i++) {
            cpu->ctrl[i] = 0x00;
        }

        cpu->dbus = 0x00;
        cpu->xfer = 0x0000;
        cpu->addr = 0x0000;
        cpu->addr_out = 0x0000;
    }

    void rising(BW8cpu* cpu) {        
        // First, compute the state input
        // 18b -> Mode (2), EXT (1), Opcode (8), Flags (4), tstate (3)
        cpu->state = 0;
        cpu->state |= (cpu->tstate & 0b111) << 0;
        cpu->state |= ((pack_state_flags(cpu) & 0b1111)) << 3;
        cpu->state |= (cpu->IR) << 7;
        cpu->state |= ((int)(cpu->status_flags.ext)) << 15;
        cpu->state |= (((int)(cpu->mode)) & 0b11) << 16;

        // Next, set the control word via the microcode
        for (int i = 0; i < 4; i++) {
            cpu->ctrl[i] = cpu->ucode[i][cpu->state];
        }

        CtrlLines lines = decode_ctrl(cpu);

        cpu->bus_flags.data_code = true;
        cpu->bus_flags.mem_io = true;

        switch (lines.ctrl_group) {
            case CtrlGroup::NONE:
                break;
            case CtrlGroup::RST_USEQ:
                break;
            case CtrlGroup::SET_EXT:
                cpu->status_flags.ext = true;
                break;
            case CtrlGroup::SET_UBR:
                cpu->status_flags.ubr = true;
                break;
            case CtrlGroup::CLR_UBR:
                cpu->status_flags.ubr = false;
                break;
            case CtrlGroup::SET_SUP:
                cpu->status_flags.sup = true;
                break;
            case CtrlGroup::SET_NMI_INHIB:
                cpu->status_flags.nmi = true;
                break;
        }

        // Finally, perform the bus assertions
        assert_addr(cpu);
        assert_xfer(cpu);
        calculate_alu(cpu);
        assert_dbus(cpu);
    }

    void assert_addr(BW8cpu* cpu) {
        CtrlLines lines = decode_ctrl(cpu);

        switch (lines.addr_assert) {
            case AddrAssert::ACK:
                cpu->addr = 0x0000;
                break;
            case AddrAssert::PC:
                cpu->addr = cpu->PC;
                cpu->bus_flags.data_code = false;
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
                cpu->addr = (cpu->DP << 8) | (cpu->DA << 0);
                break;
            case AddrAssert::T:
                cpu->addr = (cpu->TH << 8) | (cpu->TL << 0);
                break;
            case AddrAssert::IO:
                cpu->addr = (cpu->TH << 8) | (cpu->TL << 0);
                cpu->bus_flags.mem_io = false;
                break;
        }

        int16_t sign_ex_offset = (int16_t)((int8_t)(cpu->OF));
        cpu->addr_out = cpu->addr;

        if (lines.count == Count::ADDR_INC) {
            cpu->addr_out += 1;
        }

        if (lines.offset) {
            cpu->addr_out += sign_ex_offset;
        }
    }

    void assert_xfer(BW8cpu* cpu) {
        CtrlLines lines = decode_ctrl(cpu);

        switch (lines.xfer_assert) {
            case XferAssert::NONE:
                break;
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
            case XferAssert::A_A:
                cpu->xfer = (cpu->A << 8) | (cpu->A << 0);
                break;
            case XferAssert::A_B:
                cpu->xfer = (cpu->A << 8) | (cpu->B << 0);
                break;
            case XferAssert::A_C:
                cpu->xfer = (cpu->A << 8) | (cpu->C << 0);
                break;
            case XferAssert::A_D:
                cpu->xfer = (cpu->A << 8) | (cpu->D << 0);
                break;
            case XferAssert::A_TL:
                cpu->xfer = (cpu->A << 8) | (cpu->TL << 0);
                break;
            case XferAssert::B_A:
                cpu->xfer = (cpu->B << 8) | (cpu->A << 0);
                break;
            case XferAssert::B_B:
                cpu->xfer = (cpu->B << 8) | (cpu->B << 0);
                break;
            case XferAssert::B_C:
                cpu->xfer = (cpu->B << 8) | (cpu->C << 0);
                break;
            case XferAssert::B_D:
                cpu->xfer = (cpu->B << 8) | (cpu->D << 0);
                break;
            case XferAssert::B_TL:
                cpu->xfer = (cpu->B << 8) | (cpu->TL << 0);
                break;
            case XferAssert::C_A:
                cpu->xfer = (cpu->C << 8) | (cpu->A << 0);
                break;
            case XferAssert::C_B:
                cpu->xfer = (cpu->C << 8) | (cpu->B << 0);
                break;
            case XferAssert::C_C:
                cpu->xfer = (cpu->C << 8) | (cpu->C << 0);
                break;
            case XferAssert::C_D:
                cpu->xfer = (cpu->C << 8) | (cpu->D << 0);
                break;
            case XferAssert::C_TL:
                cpu->xfer = (cpu->C << 8) | (cpu->TL << 0);
                break;
            case XferAssert::D_A:
                cpu->xfer = (cpu->D << 8) | (cpu->A << 0);
                break;
            case XferAssert::D_B:
                cpu->xfer = (cpu->D << 8) | (cpu->B << 0);
                break;
            case XferAssert::D_C:
                cpu->xfer = (cpu->D << 8) | (cpu->C << 0);
                break;
            case XferAssert::D_D:
                cpu->xfer = (cpu->D << 8) | (cpu->D << 0);
                break;
            case XferAssert::D_TL:
                cpu->xfer = (cpu->D << 8) | (cpu->TL << 0);
                break;
            case XferAssert::TH_A:
                cpu->xfer = (cpu->TH << 8) | (cpu->A << 0);
                break;
            case XferAssert::TH_B:
                cpu->xfer = (cpu->TH << 8) | (cpu->B << 0);
                break;
            case XferAssert::TH_C:
                cpu->xfer = (cpu->TH << 8) | (cpu->C << 0);
                break;
            case XferAssert::TH_D:
                cpu->xfer = (cpu->TH << 8) | (cpu->D << 0);
                break;
            case XferAssert::T:
                cpu->xfer = (cpu->TH << 8) | (cpu->TL << 0);
                break;
            case XferAssert::INT:
                cpu->xfer = cpu->mode == Mode::NMI ? NMI_ADDR : IRQ_ADDR;
                break;
            case XferAssert::ADDR:
                cpu->xfer = cpu->addr_out;
                break;
        }
    }

    void calculate_alu(BW8cpu* cpu) {
        CtrlLines ctrl_lines = decode_ctrl(cpu);
		uint8_t alu_op = (uint8_t)(ctrl_lines.alu_op);

        AluCtrlLines lines = decode_alu_ctrl(cpu);

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

		switch (lines.shift_func) {
			case ShiftFunc::LHS:
				left = lhs;
				break;
			case ShiftFunc::SRC:
				left = lhs >> 1;
				if (cpu->status_flags.Cf) {
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

		switch (lines.logic_func) {
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
            default:
                break;
		}

		switch (lines.sum_func) {
			case SumFunc::ZERO:
				sum = left + right + 0;
				break;
			case SumFunc::CF:
				sum = left + right + (uint8_t)cpu->status_flags.Cf;
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

		switch (lines.cf_func) {
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
            default:
				c_new = cpu->status_flags.Cf;
				break;
		}

		switch (lines.zf_func) {
			case ZfFunc::ONE:
				z_new = true;
				break;
			case ZfFunc::NEW:
				break;
			case ZfFunc::ZERO:
				z_new = false;
				break;
			case ZfFunc::NO_CHANGE:
				z_new = cpu->status_flags.Zf;
				break;
		}

		switch (lines.vf_func) {
			case VfFunc::ONE:
				v_new = true;
				break;
			case VfFunc::NEW:
				break;
			case VfFunc::ZERO:
				v_new = false;
				break;
			case VfFunc::NO_CHANGE:
				v_new = cpu->status_flags.Vf;
				break;
		}

		switch (lines.nf_func) {
			case NfFunc::ONE:
				n_new = true;
				break;
			case NfFunc::NEW:
				break;
			case NfFunc::ZERO:
				n_new = false;
				break;
			case NfFunc::NO_CHANGE:
				n_new = cpu->status_flags.Nf;
				break;
		}

		switch (lines.if_func) {
		case IfFunc::ONE:
			i_new = true;
			break;
		case IfFunc::ZERO:
			i_new = false;
			break;
		case IfFunc::NO_CHANGE:
			i_new = cpu->status_flags.If;
			break;
		}

		cpu->ALU = result;
		cpu->ALU_FLAGS.Cf = c_new;
		cpu->ALU_FLAGS.Zf = z_new;
		cpu->ALU_FLAGS.Vf = v_new;
		cpu->ALU_FLAGS.Nf = n_new;
		cpu->ALU_FLAGS.If = i_new;
    }

    void assert_dbus(BW8cpu* cpu) {
        CtrlLines lines = decode_ctrl(cpu);
        uint8_t bank = cpu->BR;

        if (cpu->status_flags.sup) {
            bank = 0x0;
        }
        if (cpu->bus_flags.data_code) {
            bank = cpu->BR;
        }

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
                // TODO - flag unpacking
                break;
            case DbusAssert::MEM:
                cpu->dbus = cpu->read(
                    bank,
                    cpu->addr_out,
                    cpu->bus_flags.mem_io,
                    cpu->status_flags.sup,
                    cpu->bus_flags.data_code
                );
                break;
            case DbusAssert::MSB:
                cpu->dbus = cpu->xfer >> 8;
                break;
            case DbusAssert::LSB:
                cpu->dbus = cpu->xfer & 0xff;
                break;
            case DbusAssert::BR:
                cpu->dbus = cpu->BR;
                break;
        }
    }

    void falling(BW8cpu* cpu) {
        cpu->tstate++;
        cpu->tstate %= 8;
        cpu->clocks++;

        CtrlLines lines = decode_ctrl(cpu);

        if (lines.ctrl_group == CtrlGroup::RST_USEQ) {
            cpu->tstate = 0;
        }

        if (cpu->tstate == 0) {
            cpu->status_flags.ext = false;

            if (cpu->interrupts.req) {
                cpu->mode = Mode::STALL;
            } else if (cpu->interrupts.nmi) {
                cpu->mode = Mode::NMI;
            } else if (cpu->interrupts.irq) {
                cpu->mode = Mode::IRQ;
            } else {
                cpu->mode = Mode::FETCH;
            }
        }

        switch (lines.dbus_load) {
            case DbusLoad::NONE:
                break;
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
                // SR is loaded below to accomodate
                // loading the flags via the ALU
                // if they are not being loaded via DBUS
                break;
            case DbusLoad::MEM:
                cpu->write(
                    cpu->BR,
                    cpu->addr_out,
                    cpu->dbus,
                    cpu->bus_flags.mem_io,
                    cpu->status_flags.sup,
                    cpu->bus_flags.data_code
                );
                break;
            case DbusLoad::IR:
                cpu->IR = cpu->dbus;
                break;
            case DbusLoad::OFF:
                cpu->OF = cpu->dbus;
                break;
            case DbusLoad::PCH:
                cpu->PC = (cpu->dbus << 8) | (cpu->PC & 0xFF);
                break;
            case DbusLoad::PCL:
                cpu->PC = (cpu->PC & 0xFF00) | (cpu->dbus);
                break;
            case DbusLoad::SPH:
                cpu->SP = (cpu->dbus << 8) | (cpu->SP & 0xFF);
                break;
            case DbusLoad::SPL:
                cpu->SP = (cpu->SP & 0xFF00) | (cpu->dbus);
                break;
            case DbusLoad::XH:
                cpu->X = (cpu->dbus << 8) | (cpu->X & 0xFF);
                break;
            case DbusLoad::XL:
                cpu->X = (cpu->X & 0xFF00) | (cpu->dbus);
                break;
            case DbusLoad::YH:
                cpu->Y = (cpu->dbus << 8) | (cpu->Y & 0xFF);
                break;
            case DbusLoad::YL:
                cpu->Y = (cpu->Y & 0xFF00) | (cpu->dbus);
                break;
            case DbusLoad::BR:
                cpu->BR = cpu->dbus;
                break;
        }

        if (lines.dbus_load == DbusLoad::SR) {
            cpu->status_flags.Cf = (bool)((cpu->dbus >> 4) & 0b11111);
            cpu->status_flags.Zf = (bool)((cpu->dbus >> 3) & 0b11111);
            cpu->status_flags.Vf = (bool)((cpu->dbus >> 2) & 0b11111);
            cpu->status_flags.Nf = (bool)((cpu->dbus >> 1) & 0b11111);
            cpu->status_flags.If = (bool)((cpu->dbus >> 0) & 0b11111);
        } else {
            cpu->status_flags.Cf = cpu->ALU_FLAGS.Cf;
            cpu->status_flags.Zf = cpu->ALU_FLAGS.Zf;
            cpu->status_flags.Vf = cpu->ALU_FLAGS.Vf;
            cpu->status_flags.Nf = cpu->ALU_FLAGS.Nf;
            cpu->status_flags.If = cpu->ALU_FLAGS.If;
        }

        if (cpu->IR == 0xFC && cpu->status_flags.ext) {
            cpu_coredump(cpu);
        }

        switch (lines.count) {
            case Count::NONE:
                break;
            case Count::PC_INC:
                cpu->PC++;
                break;
            case Count::SP_INC:
                cpu->SP++;
                break;
            case Count::X_INC:
                cpu->X++;
                break;
            case Count::Y_INC:
                cpu->Y++;
                break;
            case Count::ADDR_INC:
                break;
            case Count::X_DEC:
                cpu->X--;
                break;
            case Count::Y_DEC:
                cpu->Y--;
                break;
        }

        if (lines.dec_sp) {
            cpu->SP--;
        }

        switch (lines.xfer_load) {
            case XferLoad::NONE:
                break;
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
                cpu->B = cpu->xfer & 0xFF;
                break;
            case XferLoad::CD:
                cpu->C = cpu->xfer >> 8;
                cpu->D = cpu->xfer & 0xFF;
                break;
        }
    }

    BW8cpu* cpu_malloc(BusRead read, BusWrite write, uint8_t *memory) {
        BW8cpu* cpu = (BW8cpu*)malloc(sizeof(BW8cpu));

        if (cpu == NULL) {
            fprintf(
                stderr,
                "Error BW8cpu *cpu_malloc: Could not allocate memory for CPU.\n"
            );
            exit(-1);
        }

        for (int i = 0; i < 4; i++) {
            cpu->ucode[i] = (uint8_t*)calloc(256 * 1024, sizeof(uint8_t));

            if (cpu->ucode[i] == NULL) {
                fprintf(
                    stderr,
                    "Error BW8cpu *cpu_malloc: Could not allocate memory for CPU.\n"
                );
                exit(-1);
            }
        }

        cpu->read = read;
        cpu->write = write;
        cpu->clocks = 0;
        cpu->memory = memory;

        srand(time(NULL));

        cpu->A = randrange(0, 0xff);
        cpu->B = randrange(0, 0xff);
        cpu->C = randrange(0, 0xff);
        cpu->D = randrange(0, 0xff);

        cpu->DP = randrange(0, 0xff);
        cpu->DA = randrange(0, 0xff);
        cpu->TH = randrange(0, 0xff);
        cpu->TL = randrange(0, 0xff);
        cpu->IR = randrange(0, 0xff);
        cpu->OF = randrange(0, 0xff);
        cpu->BR = randrange(0, 0xf);	// 4b register not 8b

        cpu->ALU = randrange(0, 0xff);  // TODO: base off of ctrl
        cpu->ALU_FLAGS = {
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
        };  // TODO: base off of ctrl

        cpu->PC = randrange(0, 0xffff);
        cpu->SP = randrange(0, 0xffff);
        cpu->X = randrange(0, 0xffff);
        cpu->Y = randrange(0, 0xffff);

        cpu->status_flags = {
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
        };

        cpu->status_flags = {
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
            randbool(),
        };
        cpu->bus_flags = {
            randbool(),
            randbool(),
        };

        cpu->interrupts = {
            randbool(),
            randbool(),
            randbool(),
            randbool(),
        };

        read_ucode(cpu);
        cpu->mode = Mode(randrange(0, 3));
        cpu->tstate = randrange(0, 7);
        cpu->state = randrange(0, 0xffff);  // todo this is wrong

        for (int i = 0; i < 4; i++) {
            cpu->ctrl[i] = randrange(0, 0xff);
        }

        // TODO: these should take their values based on the random control bus values
        cpu->dbus = randrange(0, 0xff);
        cpu->xfer = randrange(0, 0xffff);
        cpu->addr = randrange(0, 0xffff);
        cpu->addr_out = randrange(0, 0xffff);

        return cpu;
    }

    void cpu_free(BW8cpu* cpu) {
        for (int i = 0; i < 4; i++) {
            free(cpu->ucode[i]);
        }
        free(cpu);
    }

    void cpu_dump(BW8cpu* cpu, FILE* stream) {
        CtrlLines lines = decode_ctrl(cpu);
        fprintf(
            stream,
            STATE_FORMAT,
            cpu->clocks,
            cpu->tstate,
            bool_colored(cpu->status_flags.Cf),
            bool_colored(cpu->status_flags.Zf),
            bool_colored(cpu->status_flags.Vf),
            bool_colored(cpu->status_flags.Nf),
            bool_colored(cpu->status_flags.If),
            bool_colored(cpu->status_flags.sup),
            bool_colored(cpu->status_flags.ubr),
            bool_colored(cpu->status_flags.ext),
            bool_colored(cpu->interrupts.rst),
            bool_colored(cpu->interrupts.req),
            bool_colored(cpu->interrupts.nmi),
            bool_colored(cpu->interrupts.irq),
            mode_repr(cpu->mode),
            cpu->dbus, cpu->addr, cpu->xfer, cpu->addr_out,
            cpu->PC, cpu->SP, cpu->X, cpu->Y,
            cpu->A, cpu->B, cpu->C, cpu->D,
            cpu->DP, cpu->DA, cpu->TH, cpu->TL,
            cpu->BR, cpu->OF, cpu->IR
        );
    }

    uint8_t pack_state_flags(BW8cpu* cpu) {
        uint8_t flags = 0;
        flags |= (((int)(cpu->status_flags.Nf)) & 0b1) << 0;
        flags |= (((int)(cpu->status_flags.Vf)) & 0b1) << 1;
        flags |= (((int)(cpu->status_flags.Zf)) & 0b1) << 2;
        flags |= (((int)(cpu->status_flags.Cf)) & 0b1) << 3;
        return flags;
    }

    CtrlLines decode_ctrl(BW8cpu* cpu) {
		CtrlLines lines;

		lines.dbus_assert   = DbusAssert((cpu->ctrl[0] >> 0) & 0b1111);
		lines.alu_op        = AluOp((cpu->ctrl[0] >> 4) & 0b1111);

		lines.dbus_load     = DbusLoad((cpu->ctrl[1] >> 0) & 0b11111);
		lines.addr_assert   = AddrAssert((cpu->ctrl[1] >> 5) & 0b111);

		lines.xfer_assert   = XferAssert((cpu->ctrl[2] >> 0) & 0b11111);
		lines.xfer_load     = XferLoad((cpu->ctrl[2] >> 5) & 0b111);

		lines.count 	    = Count((cpu->ctrl[3] >> 0) & 0b111);
		lines.dec_sp 	    = (bool)((cpu->ctrl[3] >> 3) & 0b1);

		lines.offset 	    = (bool)((cpu->ctrl[3] >> 4) & 0b1);

        lines.ctrl_group    = CtrlGroup((cpu->ctrl[3] >> 5) & 0b111);

		return lines;
    }

    AluCtrlLines decode_alu_ctrl(BW8cpu *cpu) {
        AluCtrlLines alu_lines;
        CtrlLines lines = decode_ctrl(cpu);

        uint8_t alu_op = (uint8_t)(lines.alu_op);
        uint32_t row = DIODE_MATRIX[alu_op];

		alu_lines.sum_func	    = SumFunc((row >> 0) & 0b11);
		alu_lines.shift_func    = ShiftFunc((row >> 2) & 0b11);
		alu_lines.logic_func    = LogicFunc((row >> 4) & 0b1111);
		alu_lines.cf_func	    = CfFunc((row >> 8) & 0b111);
		alu_lines.zf_func	    = ZfFunc((row >> 11) & 0b11);
		alu_lines.vf_func	    = VfFunc((row >> 13) & 0b11);
		alu_lines.nf_func	    = NfFunc((row >> 15) & 0b11);
		alu_lines.if_func	    = IfFunc((row >> 17) & 0b11);

        return alu_lines;
    }

    void read_ucode(BW8cpu* cpu) {
        const char* fname[4] = {
			"C:/Users/brady/projects/BW8cpu/control/bin/microcode0.bin",
			"C:/Users/brady/projects/BW8cpu/control/bin/microcode1.bin",
			"C:/Users/brady/projects/BW8cpu/control/bin/microcode2.bin",
			"C:/Users/brady/projects/BW8cpu/control/bin/microcode3.bin",
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

    void clock(BW8cpu* cpu) {
        rising(cpu);
        falling(cpu);
    }

    void cpu_coredump(BW8cpu* cpu) {
        FILE* fp;
        fp = fopen("CORE_DUMP.BIN", "w");

        uint16_t reg16[] = {
            cpu->PC,
            cpu->SP,
            cpu->X,
            cpu->Y
        };
        fwrite(reg16, sizeof(uint16_t), 4, fp);

        uint8_t reg8[] = {
            cpu->A,  cpu->B,  cpu->C,  cpu->D,
            cpu->DP, cpu->DA, cpu->TH, cpu->TL,
            cpu->IR, cpu->OF, cpu->BR,
        };
        fwrite(reg8, sizeof(uint8_t), 11, fp);

        bool flags[] = {
            cpu->status_flags.Cf, cpu->status_flags.Zf, cpu->status_flags.Vf, cpu->status_flags.Nf, cpu->status_flags.If,
            cpu->status_flags.ext, cpu->status_flags.nmi, cpu->status_flags.sup, cpu->status_flags.ubr,
        };
        fwrite(flags, sizeof(bool), 9, fp);

        fwrite(cpu->memory, sizeof(uint8_t), 1024 * 1024, fp);

        fclose(fp);
        exit(0);
    }

    const char* mode_repr(Mode mode) {
        switch (mode) {
            case Mode::STALL:
                return "MEMREQ";
            case Mode::IRQ:
                return "IRQACK";
            case Mode::NMI:
                return "NMIACK";
            case Mode::FETCH:
                return "NORMAL";
        }
    }

    const char* bool_colored(bool flag) {
        return flag ? GREEN_TEXT : RED_TEXT;
    }
}