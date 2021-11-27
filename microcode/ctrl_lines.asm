; NOTE: take caution when modifying any orderings in this file. the simulator's control unit
; and bus decoder has been configured to use these exact values.

; DBUS device addresses
ALU_DBUS = 0
A_DBUS   = 1
B_DBUS   = 2
C_DBUS   = 3
D_DBUS   = 4
SR_DBUS  = 5
DP_DBUS  = 6
T1_DBUS  = 7
T2_DBUS  = 8
MEM_DBUS = 9

; 4 bits for DBUS Assert
DBUS_ASSERT_ALU = 0 << 0
DBUS_ASSERT_A   = 1 << 0
DBUS_ASSERT_B   = 2 << 0
DBUS_ASSERT_C   = 3 << 0
DBUS_ASSERT_D   = 4 << 0
DBUS_ASSERT_SR  = 5 << 0
DBUS_ASSERT_DP  = 6 << 0
DBUS_ASSERT_T1  = 7 << 0
DBUS_ASSERT_T2  = 8 << 0
DBUS_ASSERT_MEM = 9 << 0
DBUS_ASSERT_DPI = 10 << 0
; Room for 5 more DBUS Asserts

; 4 bits for DBUS Load
DBUS_LOAD_NULL = 0 << 4
DBUS_LOAD_A    = 1 << 4
DBUS_LOAD_B    = 2 << 4
DBUS_LOAD_C    = 3 << 4
DBUS_LOAD_D    = 4 << 4
DBUS_LOAD_SR   = 5 << 4
DBUS_LOAD_DP   = 6 << 4
DBUS_LOAD_T1   = 7 << 4
DBUS_LOAD_T2   = 8 << 4
DBUS_LOAD_MEM  = 9 << 4
DBUS_LOAD_IR   = 10 << 4
; Room for 5 more DBUS Loads

; 5 bits for ALU OP
ALU_NOP   = 0 << 8
ALU_ZERO  = 1 << 8
ALU_LHS   = 2 << 8
ALU_RHS   = 3 << 8
ALU_LHS_C = 4 << 8
ALU_RHS_C = 5 << 8

ALU_ADD   = 6 << 8
ALU_ADC   = 7 << 8
ALU_SUB   = 8 << 8
ALU_SBB   = 9 << 8
ALU_NEG   = 10 << 8
ALU_INC   = 11 << 8
ALU_DEC   = 12 << 8

ALU_AND   = 13 << 8
ALU_OR    = 14 << 8
ALU_XOR   = 15 << 8
ALU_NOT   = 16 << 8

ALU_LSR   = 17 << 8
ALU_LRC   = 18 << 8
ALU_ASR   = 19 << 8

ALU_SEI   = 20 << 8
ALU_CLI   = 21 << 8
ALU_SEC   = 22 << 8
ALU_CLC   = 23 << 8
ALU_SEV   = 24 << 8
ALU_CLV   = 25 << 8
ALU_SEZ   = 26 << 8
ALU_CLZ   = 27 << 8
ALU_SEN   = 28 << 8
ALU_CLN   = 29 << 8
; Room for 2 more ALU OPs

; 5 bits for XFER Assert
XFER_ASSERT_A_A  = 0 << 13
XFER_ASSERT_A_B  = 1 << 13
XFER_ASSERT_A_C  = 2 << 13
XFER_ASSERT_A_D  = 3 << 13
XFER_ASSERT_A_T1 = 4 << 13
XFER_ASSERT_A_T2 = 5 << 13

XFER_ASSERT_B_A  = 6 << 13
XFER_ASSERT_B_B  = 7 << 13
XFER_ASSERT_B_C  = 8 << 13
XFER_ASSERT_B_D  = 9 << 13
XFER_ASSERT_B_T1 = 10 << 13
XFER_ASSERT_B_T2 = 11 << 13

XFER_ASSERT_C_A  = 12 << 13
XFER_ASSERT_C_B  = 13 << 13
XFER_ASSERT_C_C  = 14 << 13
XFER_ASSERT_C_D  = 15 << 13
XFER_ASSERT_C_T1 = 16 << 13
XFER_ASSERT_C_T2 = 17 << 13

XFER_ASSERT_D_A  = 18 << 13
XFER_ASSERT_D_B  = 19 << 13
XFER_ASSERT_D_C  = 20 << 13
XFER_ASSERT_D_D  = 21 << 13
XFER_ASSERT_D_T1 = 22 << 13
XFER_ASSERT_D_T2 = 23 << 13

XFER_ASSERT_PC   = 24 << 13
XFER_ASSERT_SP   = 25 << 13
XFER_ASSERT_X    = 26 << 13
XFER_ASSERT_Y    = 27 << 13
XFER_ASSERT_ISR  = 28 << 13
XFER_ASSERT_RST  = 29 << 13
XFER_ASSERT_SPI  = 30 << 13
; Room for 1 more XFER Assert

; 3 bits for XFER Load
XFER_LOAD_ALU = 0 << 18
XFER_LOAD_PC  = 1 << 18
XFER_LOAD_SP  = 2 << 18
XFER_LOAD_X   = 3 << 18
XFER_LOAD_Y   = 4 << 18
XFER_LOAD_E   = 5 << 18
; Room for 2 more XFER Load

; 3 bits for ADDR Assert
ADDR_ASSERT_PC = 0 << 21
ADDR_ASSERT_SP = 1 << 21
ADDR_ASSERT_X  = 2 << 21
ADDR_ASSERT_Y  = 3 << 21
ADDR_ASSERT_E  = 4 << 21
ADDR_ASSERT_DP = 5 << 21
; Room for 2 more ADDR Assert

; 3 bits for Counter Inc/Decs
COUNT_NULL   = 0 << 24
COUNT_INC_PC = 1 << 24
COUNT_INC_SP = 2 << 24
COUNT_INC_X  = 3 << 24
COUNT_INC_Y  = 4 << 24
COUNT_DEC_SP = 5 << 24
COUNT_DEC_X  = 6 << 24
COUNT_DEC_Y  = 7 << 24

; 5 bits for CPU CTRL
RST_USEQ = 1 << 27
TOG_EXT1 = 1 << 28
TOG_EXT2 = 1 << 29
BRK_CLK = 1 << 30
; 1 spare control line