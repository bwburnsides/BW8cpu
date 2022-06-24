#pragma once
#include <stdint.h>
#include <stdio.h>

#include "bw8bus.h"

namespace BW8 {
    class Bus;

    class CPU {
        static const uint16_t IRQ_ADDR = 0x0003;
        static const uint16_t NMI_ADDR = 0x0006;
        static const uint32_t DIODE_MATRIX[16];

        public:
            CPU(BW8::Bus* bus);
            ~CPU();

            void dump(FILE* stream);
            void clock();
            void coredump();

            void rst(bool status);
            void req(bool status);
            void nmi(bool status);
            void irq(bool status);

            bool ack();
            bool hlt();

            void rising();
            void falling();

        private:
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

            typedef struct StatusFlags {
                bool Cf;    // Carry/Not Borrow
                bool Zf;    // Zero
                bool Vf;    // Overflow
                bool Nf;    // Negaitve (sign)
                bool If;    // IRQ Enable
                bool ext;	// Extended Opcode flag
                bool sup;   // Supervisor Mode flag
                bool ubr;   // Use Bank Register flag
                bool nmi;   // Non Maskable Interrupt mask
            } StatusFlags;

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
                NONE,
                PC,
                SP,
                X,
                Y,
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
                ADDR,
                INT,
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

            enum class CtrlGroup {
                NONE,
                RST_USEQ,
                SET_EXT,
                SET_UBR,
                CLR_UBR,
                SET_SUP,
                SET_NMI_INHIB,
                PLACEHOLDER7,
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
                bool offset;
                CtrlGroup ctrl_group;
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

            uint64_t clocks;
            uint8_t* memory;

            Bus* bus;

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
            StatusFlags status_flags;
            BusFlags bus_flags;

            // Interrupts
            Interrupts interrupts;
            Mode mode;

            // Stateful Control Logic
            uint8_t* ucode[4];		// 256 KB * 4 = 1 MB of microcode
            uint8_t tstate;
            uint32_t state;
            CtrlLines lines;

            // Internal buses
            uint8_t dbus;
            uint16_t xfer;
            uint16_t addr;
            uint16_t addr_out;

            uint8_t pack_state_flags();
            CtrlLines decode_ctrl(uint32_t state);
            AluCtrlLines decode_alu_ctrl();
            void assert_addr();
            void assert_xfer();
            void calculate_alu();
            void assert_dbus();
            void read_ucode();
            const char* mode_repr(Mode mode);
            const char* bool_colored(bool flag);
    };  // class cpu
};  // namespace BW8