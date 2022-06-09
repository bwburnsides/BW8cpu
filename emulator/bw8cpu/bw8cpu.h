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
"| Status: %sC %sZ %sV %sN %sI %sS %sU    %sRST %sREQ %sNMI %sIRQ\033[0m   %6s  |\n"\
"| DBUS:  $%02X  ADDR: $%04X  XFER: $%04X  AOUT: $%04X  |\n"\
"| PC:  $%04X   SP:  $%04X    X:  $%04X    Y:  $%04X  |\n"\
"| A:     $%02x    B:    $%02X    C:    $%02X    D:    $%02X  |\n"\
"| DP:    $%02x   DA:    $%02X   TH:    $%02X   TL:    $%02X  |\n"\
"| BR:     $%01x   OF:    $%02X   IR:    $%02X               |\n"\
"+----------------------------------------------------+\n"

namespace BW8cpu {
    static uint16_t IRQ_ADDR = 0x0003;
    static uint16_t NMI_ADDR = 0x0006;

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
        bool read_write;
        bool mem_io;
        bool super_user;
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
        BR
    };

    // enum class AluOp {

    // };

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
        // AluOp alu_op;
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
    void reset(BW8cpu* cpu, bool status);
    void rising(BW8cpu* cpu);
    void falling(BW8cpu* cpu);

    // Utilities
    BW8cpu* cpu_malloc(BusRead read, BusWrite write);
    void cpu_free(BW8cpu* cpu);
    void cpu_dump(BW8cpu* cpu, FILE* stream);

    uint8_t pack_state_flags(BW8cpu* cpu);
    CtrlLines decode_ctrl(BW8cpu* cpu);
    void assert_addr(BW8cpu* cpu);
    void assert_xfer(BW8cpu* cpu);
    void assert_dbus(BW8cpu* cpu);
    void read_ucode(BW8cpu* cpu);
    void clock(BW8cpu* cpu);

    const char* bool_colored(bool flag);
}  // namespace BW8cpu