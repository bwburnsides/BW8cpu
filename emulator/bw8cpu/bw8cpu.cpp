#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "bw8cpu.h"


#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)
#define randbool() (bool)(rand() % 2)

namespace BW8cpu {
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
        cpu->BR = 0x0;	// 4b register not 8b

        cpu->ALU = 0x00;  // TODO: base off of ctrl
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
            false,
            false,
            false,
            false,
            false,
        };

        cpu->ctrl_flags = {
            false,
            false,
            false,
            false,
        };

        cpu->bus_flags = {
            true,
            true,
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
        cpu->state |= ((int)(cpu->ctrl_flags.ext)) << 15;
        cpu->state |= (((int)(cpu->mode)) & 0b11) << 16;

        // Next, set the control word via the microcode
        for (int i = 0; i < 4; i++) {
            cpu->ctrl[i] = cpu->ucode[i][cpu->state];
        }

        CtrlLines lines = decode_ctrl(cpu);
        if (lines.tog_ext) {
            cpu->ctrl_flags.ext = true;
        }

        // Finally, perform the bus assertions
        assert_addr(cpu);
        assert_xfer(cpu);
        assert_dbus(cpu);
    }

    void falling(BW8cpu* cpu) {
        cpu->tstate++;
        cpu->tstate %= 8;
        cpu->clocks++;

        CtrlLines lines = decode_ctrl(cpu);

        if (lines.rst_useq) {
            cpu->tstate = 0;
        }

        if (cpu->tstate == 0) {
            cpu->ctrl_flags.ext = false;
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
                break;
            case DbusLoad::MEM:
                cpu->write(
                    cpu->BR,
                    cpu->addr_out,
                    cpu->dbus,
                    cpu->bus_flags.mem_io,
                    cpu->bus_flags.super_user,
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
            case DbusLoad::SET_UBR:
                break;
            case DbusLoad::CLR_UBR:
                break;
            case DbusLoad::SET_SUP:
                break;
            case DbusLoad::CLR_SUP:
                break;
            case DbusLoad::SET_NMI:
                break;
            case DbusLoad::CLR_NMI:
                break;
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

    BW8cpu* cpu_malloc(BusRead read, BusWrite write) {
        BW8cpu* cpu = (BW8cpu*)malloc(sizeof(BW8cpu));

        if (cpu == NULL) {
            fprintf(
                stderr,
                "Error BW8cpu *create_cpu: Could not allocate memory for CPU.\n"
            );
            exit(-1);
        }

        for (int i = 0; i < 4; i++) {
            cpu->ucode[i] = (uint8_t*)calloc(256 * 1024, sizeof(uint8_t));

            if (cpu->ucode[i] == NULL) {
                fprintf(
                    stderr,
                    "Error BW8cpu *create_cpu: Could not allocate memory for CPU.\n"
                );
                exit(-1);
            }
        }

        cpu->read = read;
        cpu->write = write;
        cpu->clocks = 0;

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

        cpu->ctrl_flags = {
            randbool(),
            randbool(),
            randbool(),
            randbool(),
        };
        cpu->bus_flags = {
            randbool(),
            randbool(),
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
            bool_colored(cpu->ctrl_flags.sup),
            bool_colored(cpu->ctrl_flags.ubr),
            bool_colored(cpu->interrupts.rst),
            bool_colored(cpu->interrupts.req),
            bool_colored(cpu->interrupts.nmi),
            bool_colored(cpu->interrupts.irq),
            "FETCH",
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

		lines.dbus_assert	    = DbusAssert((cpu->ctrl[0] >> 0) & 0b1111);
		// lines.alu_op         = AluOp((cpu->ctrl[0] >> 4) & 0b1111);

		lines.dbus_load 	    = DbusLoad((cpu->ctrl[1] >> 0) & 0b11111);
		lines.addr_assert 	    = AddrAssert((cpu->ctrl[1] >> 5) & 0b111);

		lines.xfer_assert	    = XferAssert((cpu->ctrl[2] >> 0) & 0b11111);
		lines.xfer_load 	    = XferLoad((cpu->ctrl[2] >> 5) & 0b111);

		lines.count 		    = Count((cpu->ctrl[3] >> 0) & 0b111);
		lines.dec_sp 		    = (bool)((cpu->ctrl[3] >> 3) & 0b1);
		lines.rst_useq 		    = (bool)((cpu->ctrl[3] >> 4) & 0b1);
		lines.tog_ext 		    = (bool)((cpu->ctrl[3] >> 5) & 0b1);
		lines.offset 		    = (bool)((cpu->ctrl[3] >> 6) & 0b1);
		lines.unused 		    = (bool)((cpu->ctrl[3] >> 7) & 0b1);

		return lines;
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
        if (lines.offset) {
            cpu->addr_out += sign_ex_offset;
            if (lines.count == Count::ADDR_INC) {
                cpu->addr_out += 1;
            }
        }
    }

    void assert_xfer(BW8cpu* cpu) {
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
            case XferAssert::NMI:
                cpu->xfer = NMI_ADDR;
                break;
        }
    }

    void assert_dbus(BW8cpu* cpu) {
        CtrlLines lines = decode_ctrl(cpu);

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
                    cpu->BR,
                    cpu->addr_out,
                    cpu->bus_flags.mem_io,
                    cpu->bus_flags.super_user,
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

    void clock(BW8cpu* cpu) {
        rising(cpu);
        falling(cpu);
    }

    const char* bool_colored(bool flag) {
        return flag ? GREEN_TEXT : RED_TEXT;
    }
}