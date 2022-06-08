#pragma once
#include <stdint.h>
#include <stdio.h>

#define DUMP_TEMPLATE ""\
"BW8cpu Dump:\n"\
"PC: %d\tSP: %d\tX: %d\tY: %d\n"\
"A: %d\tB: %d\tC: %d\tD: %d\n"\
"IR: %d\tBR: %d\tOF: %d\n"\
"Tstate: %d\n"\
"State: %d\n"\
"ADDR: %d\n"\
"DBUS: %d\n"\
"XFER: %d\n"\
"DBUS_LOAD: %d\n"\
"DBUS_ASSERT: %d\n"

namespace BW8cpu {
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

    // enum class XferAssert {

    // };

    // enum class XferLoad {

    // };

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

    typedef struct CtrlLines {
        DbusAssert dbus_assert;
        // AluOp alu_op;
        DbusLoad dbus_load;
        AddrAssert addr_assert;
        // XferAssert xfer_assert;
        // XferLoad xfer_load;
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
}  // namespace BW8cpu