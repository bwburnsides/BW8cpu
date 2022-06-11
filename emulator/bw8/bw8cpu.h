#pragma once
#include <stdint.h>
#include <stdio.h>

#define RED_TEXT "\033[0;31m"
#define GREEN_TEXT "\033[0;32m"
#define RESET_TEXT "\033[0m"
#define STATE_FORMAT "\033[0;0H"\
"+----------------------------------------------------+\n"\
"| BW8cpu Emulator                          June 2022 |\n"\
"| Clock Cycles: %-20lld       Tstate: %1d |\n"\
"+----------------------------------------------------+\n"\
"| Status: %sC %sZ %sV %sN %sI %sS %sU %sE  %sRST %sREQ %sNMI %sIRQ\033[0m   %6s  |\n"\
"| DBUS:  $%02X  ADDR: $%04X  XFER: $%04X  AOUT: $%04X  |\n"\
"| PC:  $%04X   SP:  $%04X    X:  $%04X    Y:  $%04X  |\n"\
"| A:     $%02X    B:    $%02X    C:    $%02X    D:    $%02X  |\n"\
"| DP:    $%02X   DA:    $%02X   TH:    $%02X   TL:    $%02X  |\n"\
"| BR:     $%01X   OF:    $%02X   IR:    $%02X               |\n"\
"+----------------------------------------------------+\n"

namespace BW8cpu {
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

	typedef uint8_t (* BusRead)(
        uint8_t bank,
        uint16_t ptr,
        bool mem_io,
        bool super_user,
        bool data_code
    );

	typedef void (* BusWrite)(
        uint8_t bank,
        uint16_t ptr,
        uint8_t data,
        bool mem_io,
        bool super_user,
        bool data_code
    );

	enum class Mode {
		FETCH,
		NMI,
		IRQ,
		STALL,
	};

    typedef struct AluFlags {
        bool Cf;    // Carry/Not Borrow
        bool Zf;    // Zero
        bool Vf;    // Overflow
        bool Nf;    // Negaitve (sign)
        bool If;    // IRQ Enable
    } AluFlags;

    typedef struct CtrlFlags {
		bool ext;	// Extended Opcode flag
		bool sup;   // Supervisor Mode flag
		bool ubr;   // Use Bank Register flag
		bool nmi;   // Non Maskable Interrupt mask
    } CtrlFlags;

    typedef struct BusFlags {
        bool mem_io;
        bool data_code;
    } BusFlags;

    typedef struct Interrupts {
        bool rst;
        bool req;
        bool nmi;
        bool irq;
    } Interrupts;

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
        PLACEHOLDER1,
        PLACEHOLDER2,
		notRHS,
        PLACEHOLDER4,
		notLHS,
		XOR,
        PLACEHOLDER7,
		AND,
        PLACEHOLDER9,
        LHS,
        PLACEHOLDER11,
		RHS,
        PLACEHOLDER13,
		OR,
		MAX,
	};

	enum class CfFunc {
		ONE,
		C_SHIFT,
		C_SUM,
		ZERO,
		NO_CHANGE,
		PLACEHOLDER5,
		PLACEHOLDER6,
		PLACEHOLDER7,
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
        PLACEHOLDER_2,
		NO_CHANGE,
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
        SET_UBR,
        CLR_UBR,
        SET_SUP,
        CLR_SUP,
        SET_NMI,
        CLR_NMI
    };

    enum class AddrAssert {
        ACK,
        PC,
        SP,
        X,
        Y,
        DP,
        T,
        IO
    };

    enum class Count {
        NONE,
        PC_INC,
        SP_INC,
        X_INC,
        Y_INC,
        ADDR_INC,
        X_DEC,
        Y_DEC
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

    typedef struct AluCtrlLines {
        SumFunc sum_func;
        ShiftFunc shift_func;
        LogicFunc logic_func;
        CfFunc cf_func;
        ZfFunc zf_func;
        VfFunc vf_func;
        NfFunc nf_func;
        IfFunc if_func;
    } AluCtrlLines;

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
		AluFlags ALU_FLAGS;

		// Address Registers
		uint16_t PC;
		uint16_t SP;
		uint16_t X;
		uint16_t Y;

        // Flags
        AluFlags status_flags;
        CtrlFlags ctrl_flags;
        BusFlags bus_flags;

		// Interrupts
        Interrupts interrupts;
		Mode mode;

		// Stateful Control Logic
		uint8_t* ucode[4];		// 256 KB * 4 = 1 MB of microcode
		uint8_t tstate;
        uint32_t state;
		uint8_t ctrl[4];

		// Internal buses
		uint8_t dbus;
		uint16_t xfer;
		uint16_t addr;
		uint16_t addr_out;
    } BW8cpu;

    // Interface
    BW8cpu* cpu_malloc(BusRead read, BusWrite write);
    void cpu_free(BW8cpu* cpu);
    void cpu_dump(BW8cpu* cpu, FILE* stream);
    void clock(BW8cpu* cpu);
    void cpu_coredump(BW8cpu* cpu);

    void reset(BW8cpu* cpu, bool status);
    void rising(BW8cpu* cpu);
    void falling(BW8cpu* cpu);
}  // namespace BW8cpu