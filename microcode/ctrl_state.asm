#once

T_0 = 1 << 0
T_1 = 1 << 1
T_3 = 1 << 2

I_F = 1 << 3
N_F = 1 << 4
V_F = 1 << 5
Z_V = 1 << 6
C_F = 1 << 7

OP_7 = 1 << 8
OP_6 = 1 << 9
OP_5 = 1 << 10
OP_4 = 1 << 11
OP_3 = 1 << 12
OP_2 = 1 << 13
OP_1 = 1 << 14
OP_0 = 1 << 15

IRQ = 1 << 16

MODE_0 = 1 << 17
MODE_1 = 1 << 18

#bits 32

#bankdef ucode {   ; instruction zero page (normal mode)
    #addr     0x00000
    #outp 8 * 0x00000
    #addr_end 0x80000
    #fill
}
