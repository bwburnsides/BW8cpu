#once

; 4 bits for DBUS Assert
DBUS_ASSERT_ALU  = 0  << 0
DBUS_ASSERT_A    = 1  << 0
DBUS_ASSERT_B    = 2  << 0
DBUS_ASSERT_C    = 3  << 0
DBUS_ASSERT_D    = 4  << 0
DBUS_ASSERT_DP   = 5  << 0
DBUS_ASSERT_DA   = 6  << 0
DBUS_ASSERT_TH   = 7  << 0
DBUS_ASSERT_TL   = 8  << 0
DBUS_ASSERT_SR   = 9  << 0
DBUS_ASSERT_MEM  = 10 << 0
DBUS_ASSERT_DPI  = 11 << 0
DBUS_ASSERT_SPIH = 12 << 0
DBUS_ASSERT_SPIL = 13 << 0
DBUS_ASSERT_MSB  = 14 << 0
DBUS_ASSERT_LSB  = 15 << 0

; 5 bits for DBUS Load
DBUS_LOAD_NULL = 0  << 4
DBUS_LOAD_A    = 1  << 4
DBUS_LOAD_B    = 2  << 4
DBUS_LOAD_C    = 3  << 4
DBUS_LOAD_D    = 4  << 4
DBUS_LOAD_DP   = 5  << 4
DBUS_LOAD_DA   = 6  << 4
DBUS_LOAD_TH   = 7  << 4
DBUS_LOAD_TL   = 8  << 4
DBUS_LOAD_SR   = 9  << 4
DBUS_LOAD_MEM  = 10 << 4
DBUS_LOAD_IR   = 11 << 4
DBUS_LOAD_OFF  = 12 << 4
DBUS_LOAD_PCH  = 13 << 4
DBUS_LOAD_PCL  = 14 << 4
DBUS_LOAD_SPH  = 15 << 4
DBUS_LOAD_SPL  = 16 << 4
DBUS_LOAD_XH   = 17 << 4
DBUS_LOAD_XL   = 18 << 4
DBUS_LOAD_YH   = 19 << 4
DBUS_LOAD_YL   = 20 << 4

; 4 bits for ALU OP
ALU_NOP = 0  << 9
ALU_ADC = 1  << 9
ALU_SBC = 2  << 9
ALU_INC = 3  << 9
ALU_DEC = 4  << 9
ALU_AND = 5  << 9
ALU_OR  = 6  << 9
ALU_XOR = 7  << 9
ALU_NOT = 8  << 9
ALU_SRC = 9  << 9
ALU_ASR = 10 << 9
ALU_SEI = 11 << 9
ALU_CLI = 12 << 9
ALU_SEC = 13 << 9
ALU_CLC = 14 << 9
ALU_CLV = 15 << 9

; 5 bits for XFER Assert
XFER_ASSERT_PC    = 0  << 13
XFER_ASSERT_SP    = 1  << 13
XFER_ASSERT_X     = 2  << 13
XFER_ASSERT_Y     = 3  << 13
XFER_ASSERT_RST   = 4  << 13
XFER_ASSERT_ISR   = 5  << 13
XFER_ASSERT_ADDR  = 6  << 13
XFER_ASSERT_A_A   = 7  << 13
XFER_ASSERT_A_B   = 8  << 13
XFER_ASSERT_A_C   = 9  << 13
XFER_ASSERT_A_D   = 10 << 13
XFER_ASSERT_A_T1  = 11 << 13
XFER_ASSERT_B_A   = 12 << 13
XFER_ASSERT_B_B   = 13 << 13
XFER_ASSERT_B_C   = 14 << 13
XFER_ASSERT_B_D   = 15 << 13
XFER_ASSERT_B_T1  = 16 << 13
XFER_ASSERT_C_A   = 17 << 13
XFER_ASSERT_C_B   = 18 << 13
XFER_ASSERT_C_C   = 19 << 13
XFER_ASSERT_C_D   = 20 << 13
XFER_ASSERT_C_T1  = 21 << 13
XFER_ASSERT_D_A   = 22 << 13
XFER_ASSERT_D_B   = 23 << 13
XFER_ASSERT_D_C   = 24 << 13
XFER_ASSERT_D_D   = 25 << 13
XFER_ASSERT_D_T1  = 26 << 13
XFER_ASSERT_T2_A  = 27 << 13
XFER_ASSERT_T2_B  = 28 << 13
XFER_ASSERT_T2_C  = 29 << 13
XFER_ASSERT_T2_D  = 30 << 13
XFER_ASSERT_T2_T1 = 31 << 13

; 3 bits for XFER Load
XFER_LOAD_NULL = 0 << 18
XFER_LOAD_PC   = 1 << 18
XFER_LOAD_SP   = 2 << 18
XFER_LOAD_X    = 3 << 18
XFER_LOAD_Y    = 4 << 18
XFER_LOAD_AB   = 5 << 18
XFER_LOAD_CD   = 6 << 18

; 3 bits for ADDR Assert
ADDR_ASSERT_ACK = 0 << 21
ADDR_ASSERT_PC  = 1 << 21
ADDR_ASSERT_SP  = 2 << 21
ADDR_ASSERT_X   = 3 << 21
ADDR_ASSERT_Y   = 4 << 21
ADDR_ASSERT_DP  = 5 << 21
ADDR_ASSERT_T   = 6 << 21

; 3 bits for Counter Inc/Decs
COUNT_NULL     = 0 << 24
COUNT_INC_PC   = 1 << 24
COUNT_INC_SP   = 2 << 24
COUNT_INC_X    = 3 << 24
COUNT_INC_Y    = 4 << 24
COUNT_INC_ADDR = 5 << 24
COUNT_DEC_X    = 6 << 24
COUNT_DEC_Y    = 7 << 24

; 1 bit for SP Dec
; (Allows SP to be prepped for push while operand is being fetched)
COUNT_DEC_SP = 1 << 27

; 4 bit fields for CPU CTRL
RST_USEQ = 1 << 28
TOG_EXT  = 1 << 29
OFFSET   = 1 << 30
BRK_CLK  = 1 << 31
