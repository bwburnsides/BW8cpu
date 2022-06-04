#pragma once
#include <stdint.h>
#include <stdio.h>

#define RED_TXT "\033[0;31m"
#define GREEN_TXT "\033[0;32m"
#define RESET_TXT "\033[0m"
#define STATE_FMT "\033[1;1H"\
"+----------------------------------------------------+\n"\
"| BW8cpu Emulator                          June 2022 |\n"\
"| Clock Cycles: %-20lld       Tstate: %1d |\n"\
"+----------------------------------------------------+\n"\
"| Status: %sC %sZ %sV %sN %sI %sK %sU    %sRST %sREQ %sNMI %sIRQ\033[0m    %6s |\n"\
"| PC:  $%04X     SP: $%04X     X: $%04X     Y: $%04X |\n"\
"| A:   $%02X       DP: $%02X       IR: $%02X               |\n"\
"| B:   $%02X       DA: $%02X       OF: $%02X               |\n"\
"| C:   $%02X       TH: $%02X       BR: $%02X               |\n"\
"| D:   $%02X       TL: $%02X                             |\n"\
"+----------------------------------------------------+\n"\

namespace BW8cpu {
	enum class AddrAssert {
		ACK,
		PC,
		SP,
		X,
		Y,
		DP,
		T,
		IO,
	};

	enum class XferAssert {
		PC,
		SP,
		X,
		Y,
		IRQ,
		ADDR,
		A_A,
		A_B,
		A_C,
		A_D,
		A_TL,
		B_A,
		B_B,
		B_C,
		B_D,
		B_TL,
		C_A,
		C_B,
		C_C,
		C_D,
		C_TL,
		D_A,
		D_B,
		D_C,
		D_D,
		D_TL,
		TH_A,
		TH_B,
		TH_C,
		TH_D,
		T,
		NMI,
	};

	enum class Count {
		NONE,
		INC_PC,
		INC_SP,
		INC_X,
		INC_Y,
		OFFSET_INC,
		DEC_X,
		DEC_Y,
	};

	enum class Mode {
		FETCH,
		NMI,
		IRQ,
		STALL,
	};

	static uint16_t IRQ_ADDR = 0x0003;
	static uint16_t NMI_ADDR = 0x0006;

	typedef struct BW8cpu {
		uint64_t clocks;

		// General Purpose Registers
		uint8_t A;
		uint8_t B;
		uint8_t C;
		uint8_t D;

		// Special Purpose Registers
		uint8_t DP;
		uint8_t DA;
		uint8_t TH;
		uint8_t TL;
		uint8_t IR;
		uint8_t OF;
		uint8_t BR;

		uint8_t ALU;

		// Address Registers
		uint16_t PC;
		uint16_t SP;
		uint16_t X;
		uint16_t Y;

		// Status Register Flags
		bool carry_flag;
		bool zero_flag;
		bool overflow_flag;
		bool negative_flag;
		bool interrupt_enable;

		// Interrupts
		bool interrupt_request;
		bool nonmaskable_interrupt;
		bool bus_request;
		bool reset;
		Mode mode;

		// Stateful Control Logic
		uint8_t* ucode[4];		// 256 KB * 4 = 1 MB of microcode
		uint8_t sequencer;
		uint8_t ctrl_latch[4];
		bool extended;			// Extended Opcode flag
		bool supervisor_mode;	// Supervisor Mode flag
		bool use_bank_reg;		// Use Bank Register flag
		bool nmi_enable;		// Non Maskable Interrupt mask

		// Internal buses
		uint8_t dbus;
		uint16_t xfer;
		uint16_t addr;
		uint16_t addr_out;
	} BW8cpu;


	// Public functions
	BW8cpu* malloc_cpu();
	void free_cpu(BW8cpu* cpu);
	void reset(BW8cpu* cpu, bool state);
	void rising(BW8cpu* cpu);
	void falling(BW8cpu* cpu);

	void dump(BW8cpu* cpu, FILE* fout);

	// Private functions
	void read_ucode(BW8cpu* cpu);
	void update_mode(BW8cpu* cpu);
	void addr_assert(BW8cpu* cpu);
	void xfer_assert(BW8cpu* cpu);
	void alu_calculate(BW8cpu* cpu);

	uint16_t concatenate_bytes(uint8_t left, uint8_t right);
} // namespace BW8cpu