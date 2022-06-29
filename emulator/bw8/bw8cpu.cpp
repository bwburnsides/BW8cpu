#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "bw8cpu.h"

#define randrange(a, b) rand() % ((b) + 1 - (a)) + (a)
#define randbool() (bool)(rand() % 2)

namespace BW8 {
    const uint32_t CPU::DIODE_MATRIX[16] = {
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

    CPU::CPU(Bus* sys_bus) {
        for (int i = 0; i < 4; i++) {
            ucode[i] = (uint8_t*)calloc(256 * 1024, sizeof(uint8_t));

            if (ucode[i] == NULL) {
                fprintf(
                    stderr,
                    "Error BW8::CPU Constructor: Could not allocate memory for CPU.\n"
                );
                exit(-1);
            }
        }

        bus = sys_bus;
        clocks = 0;

        srand((unsigned int)time(NULL));

        A = randrange(0, 0xff);
        B = randrange(0, 0xff);
        C = randrange(0, 0xff);
        D = randrange(0, 0xff);

        DP = randrange(0, 0xff);
        DA = randrange(0, 0xff);
        TH = randrange(0, 0xff);
        TL = randrange(0, 0xff);
        IR = randrange(0, 0xff);
        OF = randrange(0, 0xff);
        BR = randrange(0, 0xf);	// 4b register not 8b

        ALU = randrange(0, 0xff);
        ALU_FLAGS = {
            randbool(),  // Cf
            randbool(),  // Zf
            randbool(),  // Vf
            randbool(),  // Nf
            randbool(),  // If
        };

        PC = randrange(0, 0xffff);
        SP = randrange(0, 0xffff);
        X = randrange(0, 0xffff);
        Y = randrange(0, 0xffff);

        status_flags = {
            randbool(),  // Cf
            randbool(),  // Zf
            randbool(),  // Vf
            randbool(),  // Nf
            randbool(),  // If
            randbool(),  // ext
            randbool(),  // sup
            randbool(),  // ubr
            randbool(),  // nmi
        };

        bus_flags = {
            randbool(),  // mem_io
            randbool(),  // data_code
        };

        interrupts = {
            randbool(),  // rst
            randbool(),  // req
            randbool(),  // nmi
            randbool(),  // irq
        };

        read_ucode();
        mode = Mode(randrange(0, 3));
        tstate = randrange(0, 7);
        state = randrange(0, 0xffff);  // todo this is wrong

        lines = decode_ctrl(state);

        // TODO: these should take their values based on the random control bus values
        dbus = randrange(0, 0xff);
        xfer = randrange(0, 0xffff);
        addr = randrange(0, 0xffff);
        addr_out = randrange(0, 0xffff);
    }

    CPU::~CPU() {
        for (int i = 0; i < 4; i++) {
            free(ucode[i]);
        }
    }

    void CPU::rst(bool status) {
        interrupts.rst = status;

        if (!interrupts.rst) {
            return;
        }

        A = 0x00;
        B = 0x00;
        C = 0x00;
        D = 0x00;

        DP = 0x00;
        DA = 0x00;
        TH = 0x00;
        TL = 0x00;
        IR = 0x00;
        OF = 0x00;
        BR = 0x0;      // 4b register not 8b

        ALU = 0x00;    // TODO: base off of ctrl
        ALU_FLAGS = {
            false,
            false,
            false,
            false,
            false
        };  // TODO: base off of ctrl

        PC = 0x0000;
        SP = 0x0000;
        X = 0x0000;
        Y = 0x0000;

        status_flags = {
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

        bus_flags = {
            true,
            true,
        };

        interrupts = {
            false,
            false,
            false,
            false,
        };

        mode = Mode::FETCH;
        tstate = 0;
        state = 0;
        lines = decode_ctrl(state);

        dbus = 0x00;
        xfer = 0x0000;
        addr = 0x0000;
        addr_out = 0x0000;
    }

    void CPU::req(bool status) {
        interrupts.req = status;
    }

    void CPU::nmi(bool status) {
        interrupts.nmi = status;
    }

    void CPU::irq(bool status) {
        interrupts.irq = status;
    }

    bool CPU::ack() {
        return lines.addr_assert == AddrAssert::ACK && lines.xfer_assert == XferAssert::ADDR;
    }

    bool CPU::hlt() {
        return IR == 0xFC && status_flags.ext;
    }

    void CPU::rising() {       
        if (interrupts.rst) {
            return;
        }

        state = encode_state(tstate, status_flags, IR, mode);
        lines = decode_ctrl(state);
 
        bus_flags.data_code = true;
        bus_flags.mem_io = true;

        switch (lines.ctrl_group) {
            case CtrlGroup::NONE:
                break;
            case CtrlGroup::RST_USEQ:
                break;
            case CtrlGroup::SET_EXT:
                status_flags.ext = true;
                break;
            case CtrlGroup::SET_UBR:
                status_flags.ubr = true;
                break;
            case CtrlGroup::CLR_UBR:
                status_flags.ubr = false;
                break;
            case CtrlGroup::SET_SUP:
                status_flags.sup = true;
                break;
            case CtrlGroup::SET_NMI_INHIB:
                status_flags.nmi = true;
                break;
        }

        // Finally, perform the bus assertions
        assert_addr();
        assert_xfer();
        calculate_alu();
        assert_dbus();
    }

    void CPU::assert_addr() {
        switch (lines.addr_assert) {
            case AddrAssert::ACK:
                addr = 0x0000;
                break;
            case AddrAssert::PC:
                addr = PC;
                bus_flags.data_code = false;
                break;
            case AddrAssert::SP:
                addr = SP;
                break;
            case AddrAssert::X:
                addr = X;
                break;
            case AddrAssert::Y:
                addr = Y;
                break;
            case AddrAssert::DP:
                addr = (DP << 8) | (DA << 0);
                break;
            case AddrAssert::T:
                addr = (TH << 8) | (TL << 0);
                break;
            case AddrAssert::IO:
                addr = (TH << 8) | (TL << 0);
                bus_flags.mem_io = false;
                break;
        }

        int16_t sign_ex_offset = (int16_t)((int8_t)(OF));
        addr_out = addr;

        if (lines.count == Count::ADDR_INC) {
            addr_out += 1;
        }

        if (lines.offset) {
            addr_out += sign_ex_offset;
        }
    }

    void CPU::assert_xfer() {
        switch (lines.xfer_assert) {
            case XferAssert::NONE:
                break;
            case XferAssert::PC:
                xfer = PC;
                break;
            case XferAssert::SP:
                xfer = SP;
                break;
            case XferAssert::X:
                xfer = X;
                break;
            case XferAssert::Y:
                xfer = Y;
                break;
            case XferAssert::A_A:
                xfer = (A << 8) | (A << 0);
                break;
            case XferAssert::A_B:
                xfer = (A << 8) | (B << 0);
                break;
            case XferAssert::A_C:
                xfer = (A << 8) | (C << 0);
                break;
            case XferAssert::A_D:
                xfer = (A << 8) | (D << 0);
                break;
            case XferAssert::A_TL:
                xfer = (A << 8) | (TL << 0);
                break;
            case XferAssert::B_A:
                xfer = (B << 8) | (A << 0);
                break;
            case XferAssert::B_B:
                xfer = (B << 8) | (B << 0);
                break;
            case XferAssert::B_C:
                xfer = (B << 8) | (C << 0);
                break;
            case XferAssert::B_D:
                xfer = (B << 8) | (D << 0);
                break;
            case XferAssert::B_TL:
                xfer = (B << 8) | (TL << 0);
                break;
            case XferAssert::C_A:
                xfer = (C << 8) | (A << 0);
                break;
            case XferAssert::C_B:
                xfer = (C << 8) | (B << 0);
                break;
            case XferAssert::C_C:
                xfer = (C << 8) | (C << 0);
                break;
            case XferAssert::C_D:
                xfer = (C << 8) | (D << 0);
                break;
            case XferAssert::C_TL:
                xfer = (C << 8) | (TL << 0);
                break;
            case XferAssert::D_A:
                xfer = (D << 8) | (A << 0);
                break;
            case XferAssert::D_B:
                xfer = (D << 8) | (B << 0);
                break;
            case XferAssert::D_C:
                xfer = (D << 8) | (C << 0);
                break;
            case XferAssert::D_D:
                xfer = (D << 8) | (D << 0);
                break;
            case XferAssert::D_TL:
                xfer = (D << 8) | (TL << 0);
                break;
            case XferAssert::TH_A:
                xfer = (TH << 8) | (A << 0);
                break;
            case XferAssert::TH_B:
                xfer = (TH << 8) | (B << 0);
                break;
            case XferAssert::TH_C:
                xfer = (TH << 8) | (C << 0);
                break;
            case XferAssert::TH_D:
                xfer = (TH << 8) | (D << 0);
                break;
            case XferAssert::T:
                xfer = (TH << 8) | (TL << 0);
                break;
            case XferAssert::INT:
                xfer = mode == Mode::NMI ? NMI_ADDR : IRQ_ADDR;
                break;
            case XferAssert::ADDR:
                xfer = addr_out;
                break;
        }
    }

    void CPU::calculate_alu() {
        uint8_t alu_op = (uint8_t)(lines.alu_op);

        AluCtrlLines lines = decode_alu_ctrl();

        uint8_t lhs = xfer >> 8;
        uint8_t rhs = xfer & 0xff;

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
                if (status_flags.Cf) {
                    left &= 0b10000000;
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
                sum = left + right + (uint8_t)status_flags.Cf;
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
                c_new = status_flags.Cf;
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
                z_new = status_flags.Zf;
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
                v_new = status_flags.Vf;
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
                n_new = status_flags.Nf;
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
            i_new = status_flags.If;
            break;
        }

        ALU = result;
        ALU_FLAGS.Cf = c_new;
        ALU_FLAGS.Zf = z_new;
        ALU_FLAGS.Vf = v_new;
        ALU_FLAGS.Nf = n_new;
        ALU_FLAGS.If = i_new;
    }

    void CPU::assert_dbus() {
        uint8_t bank = BR;

        if (status_flags.sup) {
            bank = 0x0;
        }
        if (bus_flags.data_code) {
            bank = BR;
        }

        switch (lines.dbus_assert) {
            case DbusAssert::ALU:
                dbus = ALU;
                break;
            case DbusAssert::A:
                dbus = A;
                break;
            case DbusAssert::B:
                dbus = B;
                break;
            case DbusAssert::C:
                dbus = C;
                break;
            case DbusAssert::D:
                dbus = D;
                break;
            case DbusAssert::DP:
                dbus = DP;
                break;
            case DbusAssert::DA:
                dbus = DA;
                break;
            case DbusAssert::TH:
                dbus = TH;
                break;
            case DbusAssert::TL:
                dbus = TL;
                break;
            case DbusAssert::SR:
                // TODO - flag unpacking
                break;
            case DbusAssert::MEM:
                dbus = bus->read(
                    bank,
                    addr_out,
                    bus_flags.mem_io,
                    status_flags.sup,
                    bus_flags.data_code
                );
                break;
            case DbusAssert::MSB:
                dbus = xfer >> 8;
                break;
            case DbusAssert::LSB:
                dbus = xfer & 0xff;
                break;
            case DbusAssert::BR:
                dbus = BR;
                break;
        }
    }

    void CPU::falling() {
        if (interrupts.rst) {
            return;
        }

        tstate++;
        tstate %= 8;
        clocks++;

        if (lines.ctrl_group == CtrlGroup::RST_USEQ) {
            tstate = 0;
        }

        if (tstate == 0) {
            status_flags.ext = false;

            if (interrupts.req) {
                mode = Mode::STALL;
            } else if (interrupts.nmi && !status_flags.nmi) {
                mode = Mode::NMI;
            } else if (interrupts.irq && status_flags.If) {
                mode = Mode::IRQ;
            } else {
                mode = Mode::FETCH;
            }
        }

        switch (lines.dbus_load) {
            case DbusLoad::NONE:
                break;
            case DbusLoad::A:
                A = dbus;
                break;
            case DbusLoad::B:
                B = dbus;
                break;
            case DbusLoad::C:
                C = dbus;
                break;
            case DbusLoad::D:
                D = dbus;
                break;
            case DbusLoad::DP:
                DP = dbus;
                break;
            case DbusLoad::DA:
                DA = dbus;
                break;
            case DbusLoad::TH:
                TH = dbus;
                break;
            case DbusLoad::TL:
                TL = dbus;
                break;
            case DbusLoad::SR:
                // SR is loaded below to accomodate
                // loading the flags via the ALU
                // if they are not being loaded via DBUS
                break;
            case DbusLoad::MEM:
                bus->write(
                    BR,
                    addr_out,
                    dbus,
                    bus_flags.mem_io,
                    status_flags.sup,
                    bus_flags.data_code
                );
                break;
            case DbusLoad::IR:
                IR = dbus;
                break;
            case DbusLoad::OFF:
                OF = dbus;
                break;
            case DbusLoad::PCH:
                PC = (dbus << 8) | (PC & 0xFF);
                break;
            case DbusLoad::PCL:
                PC = (PC & 0xFF00) | (dbus);
                break;
            case DbusLoad::SPH:
                SP = (dbus << 8) | (SP & 0xFF);
                break;
            case DbusLoad::SPL:
                SP = (SP & 0xFF00) | (dbus);
                break;
            case DbusLoad::XH:
                X = (dbus << 8) | (X & 0xFF);
                break;
            case DbusLoad::XL:
                X = (X & 0xFF00) | (dbus);
                break;
            case DbusLoad::YH:
                Y = (dbus << 8) | (Y & 0xFF);
                break;
            case DbusLoad::YL:
                Y = (Y & 0xFF00) | (dbus);
                break;
            case DbusLoad::BR:
                BR = dbus;
                break;
        }

        if (lines.dbus_load == DbusLoad::SR) {
            status_flags.Cf = (bool)((dbus >> 4) & 0b11111);
            status_flags.Zf = (bool)((dbus >> 3) & 0b11111);
            status_flags.Vf = (bool)((dbus >> 2) & 0b11111);
            status_flags.Nf = (bool)((dbus >> 1) & 0b11111);
            status_flags.If = (bool)((dbus >> 0) & 0b11111);
        } else {
            status_flags.Cf = ALU_FLAGS.Cf;
            status_flags.Zf = ALU_FLAGS.Zf;
            status_flags.Vf = ALU_FLAGS.Vf;
            status_flags.Nf = ALU_FLAGS.Nf;
            status_flags.If = ALU_FLAGS.If;
        }

        switch (lines.count) {
            case Count::NONE:
                break;
            case Count::PC_INC:
                PC++;
                break;
            case Count::SP_INC:
                SP++;
                break;
            case Count::X_INC:
                X++;
                break;
            case Count::Y_INC:
                Y++;
                break;
            case Count::ADDR_INC:
                break;
            case Count::X_DEC:
                X--;
                break;
            case Count::Y_DEC:
                Y--;
                break;
        }

        if (lines.dec_sp) {
            SP--;
        }

        switch (lines.xfer_load) {
            case XferLoad::NONE:
                break;
            case XferLoad::PC:
                PC = xfer;
                break;
            case XferLoad::SP:
                SP = xfer;
                break;
            case XferLoad::X:
                X = xfer;
                break;
            case XferLoad::Y:
                Y = xfer;
                break;
            case XferLoad::AB:
                A = xfer >> 8;
                B = xfer & 0xFF;
                break;
            case XferLoad::CD:
                C = xfer >> 8;
                D = xfer & 0xFF;
                break;
        }
    }

    uint32_t CPU::encode_state(uint8_t tstate, StatusFlags flags, uint8_t ir, Mode mode) {
        // First, compute the state input
        // 18b -> Mode (2), EXT (1), Opcode (8), Flags (4), tstate (3)

        uint8_t packed = 0;
        uint32_t state = 0;

        packed |= (((int)(flags.Nf)) & 0b1) << 0;
        packed |= (((int)(flags.Vf)) & 0b1) << 1;
        packed |= (((int)(flags.Zf)) & 0b1) << 2;
        packed |= (((int)(flags.Cf)) & 0b1) << 3;

        state |= (tstate & 0b111) << 0;
        state |= ((packed & 0b1111)) << 3;
        state |= (ir) << 7;
        state |= ((int)(flags.ext)) << 15;
        state |= (((int)(mode)) & 0b11) << 16;
        return state;
    }

    CPU::CtrlLines CPU::decode_ctrl(uint32_t state) {
        CtrlLines lines;
        uint8_t ctrl[4];

        for (int i = 0; i < 4; i++) {
            ctrl[i] = ucode[i][state];
        }

        lines.dbus_assert   = DbusAssert((ctrl[0] >> 0) & 0b1111);
        lines.alu_op        = AluOp((ctrl[0] >> 4) & 0b1111);

        lines.dbus_load     = DbusLoad((ctrl[1] >> 0) & 0b11111);
        lines.addr_assert   = AddrAssert((ctrl[1] >> 5) & 0b111);

        lines.xfer_assert   = XferAssert((ctrl[2] >> 0) & 0b11111);
        lines.xfer_load     = XferLoad((ctrl[2] >> 5) & 0b111);

        lines.count 	    = Count((ctrl[3] >> 0) & 0b111);
        lines.dec_sp 	    = (bool)((ctrl[3] >> 3) & 0b1);
        lines.offset 	    = (bool)((ctrl[3] >> 4) & 0b1);
        lines.ctrl_group    = CtrlGroup((ctrl[3] >> 5) & 0b111);

        return lines;
    }

    CPU::AluCtrlLines CPU::decode_alu_ctrl() {
        AluCtrlLines alu_lines;

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

    void CPU::read_ucode() {
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
            fread(ucode[i], sizeof(uint8_t), 256 * 1024, fp);
            fclose(fp);
        }
    }

    void CPU::coredump() {
        FILE* fp;
        fp = fopen("CORE_DUMP.BIN", "w");

        uint16_t reg16[] = {
            PC,
            SP,
            X,
            Y
        };
        fwrite(reg16, sizeof(uint16_t), 4, fp);

        uint8_t reg8[] = {
            A,  B,  C,  D,
        };
        fwrite(reg8, sizeof(uint8_t), 4, fp);


        bool flags[] = {
            status_flags.nmi, status_flags.ubr, status_flags.sup,
            status_flags.Cf, status_flags.Zf, status_flags.Vf, status_flags.Nf, status_flags.If
        };
        fwrite(flags, sizeof(bool), 8, fp);

        fwrite(bus->memory, sizeof(uint8_t), ADDR_SPACE_SIZE, fp);

        fclose(fp);

        exit(0);
    }
}  // namespace BW8