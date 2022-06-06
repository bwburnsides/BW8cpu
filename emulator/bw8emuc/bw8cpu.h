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
"| A:   $%02X       DP: $%02X       IR: $%02X   ADDR: $%04X |\n"\
"| B:   $%02X       DA: $%02X       OF: $%02X   XFER: $%04X |\n"\
"| C:   $%02X       TH: $%02X       BR: $%02X   DBUS: $%02X   |\n"\
"| D:   $%02X       TL: $%02X                             |\n"\
"+----------------------------------------------------+\n"\

#define CTRL_FMT ""\
"DBUS_ASSERT: %d\n"\
"ALU_OP: %d\n"\
"DBUS_LOAD: %d\n"\
"ADDR_ASSERT: %d\n"\
"XFER_ASSERT: %d\n"\
"XFER_LOAD: %d\n"\
"COUNT: %d\n"\
"DEC_SP: %d\n"\
"RST_USEQ: %d\n"\
"TOG_EXT: %d\n"\
"OFFSET: %d\n"\
"UNUSED: %d\n"\

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

	enum class XferLoad {
		NONE,
		PC,
		SP,
		X,
		Y,
		AB,
		CD,
	};

	enum class DbusAssert {
		ALU,
		A,
		B,
		C,
		D,
		DP,
		DA,
		TH,
		TL,
		SR,
		MEM,
		MSB,
		LSB,
		BR,
		PLACEHOLDER14,
		PLACEHOLDER15,
	};

	enum class DbusLoad {
		NONE,
		A,
		B,
		C,
		D,
		DP,
		DA,
		TH,
		TL,
		SR,
		MEM,
		IR,
		OFF,
		PCH,
		PCL,
		SPH,
		SPL,
		XH,
		XL,
		YH,
		YL,
		BR,

		SET_USE_BR,
		CLR_USE_BR,
		SET_SUPER_MODE,
		CLR_SUPER_MODE,
		SET_NMI_MASK,
		CLR_NMI_MASK,
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

	enum class AluOp {
		NOP,
		ADC,
		SBC,
		INC,
		DEC,
		AND,
		OR,
		XOR,
		NOT,
		SRC,
		ASR,
		SEI,
		CLI,
		SEC,
		CLC,
		CLV,
	};

	enum class SumFunc {
		ZERO,
		CF,
		ONE,
	};

	enum class ShiftFunc {
		LHS,
		SRC,
		ASR,
		ZERO,
	};

	enum class LogicFunc {
		ZERO,
		MAX,
		LHS,
		RHS,
		notLHS,
		notRHS,
		OR,
		AND,
		XOR,
	};

	enum class CfFunc {
		ONE,
		C_SHIFT,
		C_SUM,
		ZERO,
		NO_CHANGE,
	};

	enum class ZfFunc {
		ONE,
		NEW,
		ZERO,
		NO_CHANGE,
	};

	typedef ZfFunc VfFunc;
	typedef ZfFunc NfFunc;

	enum class IfFunc {
		ONE,
		ZERO,
		NO_CHANGE,
	};

	enum class CtrlField {
		DBUS_ASSERT,
		ALU_OP,
		DBUS_LOAD,
		ADDR_ASSERT,
		XFER_ASSERT,
		XFER_LOAD,
		COUNT,
		DEC_SP,
		RST_USEQ,
		TOG_EXT,
		OFFSET,
		UNUSED,
	};

	typedef struct CtrlLines {
		DbusAssert dbus_assert;
		AluOp alu_op;
		DbusLoad dbus_load;
		AddrAssert addr_assert;
		XferAssert xfer_assert;
		XferLoad xfer_load;
		Count count;
		bool dec_sp;
		bool rst_useq;
		bool tog_ext;
		bool offset;
		bool unused;

	} CtrlLines;

	typedef uint8_t (* BusRead)(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code);
	typedef void (* BusWrite)(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code);

	static uint16_t IRQ_ADDR = 0x0003;
	static uint16_t NMI_ADDR = 0x0006;
	static uint32_t DIODE_MATRIX[16] = {
		0b1111111111100001100,
		0b1101010101011000001,
		0b1101010101000110001,
		0b1101110101011001111,
		0b1101110101011110000,
		0b1101110111110001100,
		0b1101110111111101100,
		0b1101110111101101100,
		0b1101110111100111100,
		0b1101110100100001100,
		0b1101110100100000000,
		0b0011111111111111111,
		0b0111111111111111111,
		0b1111111100011111111,
		0b1111111101111111111,
		0b1111101111111111111,
	};

	typedef struct BW8cpu {
		uint64_t clocks;

		// Function pointers for doing bus operations
		BusRead read;
		BusWrite write;

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
		uint8_t ALU_FLAGS;

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
	BW8cpu* malloc_cpu(BusRead read, BusWrite write);
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
	void dbus_assert(BW8cpu* cpu);
	CtrlLines decode_ctrl(BW8cpu* cpu);

	// Private (utils)
	uint16_t concatenate_bytes(uint8_t left, uint8_t right);
	void dump_ctrl(BW8cpu *cpu, FILE* fout);
} // namespace BW8cpu