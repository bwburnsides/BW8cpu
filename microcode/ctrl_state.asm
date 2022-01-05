#bankdef mode00 {   ; instruction zero page (normal mode)
    #addr     0x00000
    #outp 8 * 0x00000
    #addr_end 0x10000
    #fill
}

#bankdef mode01 {   ; extended page 1
    #addr     0x10000
    #outp 8 * 0x10000
    #addr_end 0x20000
    #fill
}

#bankdef mode10 {   ; reset mode
    #addr     0x20000
    #outp 8 * 0x20000
    #addr_end 0x30000
    #fill
}

#bankdef mode11 {   ; extended page 2
    #addr     0x30000
    #outp 8 * 0x30000
    #addr_end 0x40000
    #fill
}

#bankdef irq {
    #addr     0x40000
    #outp 8 * 0x40000
    #addr_end 0x7FFFF
    #fill
}

T_0 = 1 << 0
T_1 = 1 << 1
T_3 = 1 << 2

OP_7 = 1 << 3
OP_6 = 1 << 4
OP_5 = 1 << 5
OP_4 = 1 << 6
OP_3 = 1 << 7
OP_2 = 1 << 8
OP_1 = 1 << 9
OP_0 = 1 << 10

I_F = 1 << 11
N_F = 1 << 12
V_F = 1 << 13
Z_V = 1 << 14
C_F = 1 << 15

IRQ = 1 << 16

MODE_0 = 1 << 17
MODE_1 = 1 << 18
