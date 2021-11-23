A_DBUS   = 1
B_DBUS   = 2
C_DBUS   = 3
D_DBUS   = 4
SR_DBUS  = 5
DP_DBUS  = 6
T1_DBUS  = 7
T2_DBUS  = 8
MEM_DBUS = 9
ALU_DBUS = 0

; 4 bits for DBUS Assert
DBUS_ASSERT_ALU   = 0 << 0
DBUS_ASSERT_A     = 1 << 0
DBUS_ASSERT_B     = 2 << 0
DBUS_ASSERT_C     = 3 << 0
DBUS_ASSERT_D     = 4 << 0
DBUS_ASSERT_SR    = 5 << 0
DBUS_ASSERT_DP    = 6 << 0
DBUS_ASSERT_T1    = 7 << 0
DBUS_ASSERT_T2    = 8 << 0
DBUS_ASSERT_MEM   = 9 << 0
; Room for 6 more DBUS Asserts

; 4 bits for DBUS Load
DBUS_LOAD_NULL  = 0 << 4
DBUS_LOAD_A     = 1 << 4
DBUS_LOAD_B     = 2 << 4
DBUS_LOAD_C     = 3 << 4
DBUS_LOAD_D     = 4 << 4
DBUS_LOAD_SR    = 5 << 4
DBUS_LOAD_DP    = 6 << 4
DBUS_LOAD_T1    = 7 << 4
DBUS_LOAD_T2    = 8 << 4
DBUS_LOAD_MEM   = 9 << 4
DBUS_LOAD_IR    = 10 << 4
; Room for 5 more DBUS Loads

; 5 bits for ALU OP
ALU_NOP   = 0 << 8
ALU_ADD   = 1 << 8
ALU_ADC   = 2 << 8
ALU_SUB   = 3 << 8
ALU_SBB   = 4 << 8
ALU_AND   = 5 << 8
ALU_OR    = 6 << 8
ALU_XOR   = 7 << 8
ALU_NOT   = 8 << 8
ALU_NEG   = 9 << 8
ALU_LSR   = 10 << 8
ALU_LRC   = 11 << 8
ALU_ASR   = 12 << 8
ALU_INC   = 13 << 8
ALU_DEC   = 14 << 8
ALU_SEI   = 15 << 8
ALU_CLI   = 16 << 8
ALU_SEC   = 17 << 8
ALU_CLC   = 18 << 8
ALU_SEV   = 19 << 8
ALU_CLV   = 20 << 8
ALU_SEZ   = 21 << 8
ALU_CLZ   = 22 << 8
ALU_SEN   = 23 << 8
ALU_CLN   = 24 << 8
ALU_LHS   = 25 << 8
ALU_RHS   = 26 << 8
ALU_LHS_C = 27 << 8
ALU_RHS_C = 28 << 8
ALU_ZERO  = 29 << 8
; Room for 2 more ALU OPs

; 5 bits for XFER Assert
XFER_ASSERT_A_A     = 0 << 13
XFER_ASSERT_A_B     = 1 << 13
XFER_ASSERT_A_C     = 2 << 13
XFER_ASSERT_A_D     = 3 << 13
XFER_ASSERT_A_T1    = 4 << 13
XFER_ASSERT_A_T2    = 5 << 13
XFER_ASSERT_B_A     = 6 << 13
XFER_ASSERT_B_B     = 7 << 13
XFER_ASSERT_B_C     = 8 << 13
XFER_ASSERT_B_D     = 9 << 13
XFER_ASSERT_B_T1    = 10 << 13
XFER_ASSERT_B_T2    = 11 << 13
XFER_ASSERT_C_A     = 12 << 13
XFER_ASSERT_C_B     = 13 << 13
XFER_ASSERT_C_C     = 14 << 13
XFER_ASSERT_C_D     = 15 << 13
XFER_ASSERT_C_T1    = 16 << 13
XFER_ASSERT_C_T2    = 17 << 13
XFER_ASSERT_D_A     = 18 << 13
XFER_ASSERT_D_B     = 19 << 13
XFER_ASSERT_D_C     = 20 << 13
XFER_ASSERT_D_D     = 21 << 13
XFER_ASSERT_D_T1    = 22 << 13
XFER_ASSERT_D_T2    = 23 << 13
XFER_ASSERT_E       = 24 << 13
XFER_ASSERT_SP      = 25 << 13
XFER_ASSERT_ISR     = 26 << 13
XFER_ASSERT_RST     = 27 << 13
XFER_ASSERT_Y       = 28 << 13
XFER_ASSERT_X       = 29 << 13
XFER_ASSERT_PC      = 30 << 13
; Room for 1 more XFER Assert

; 3 bits for XFER Load
XFER_LOAD_ALU = 0 << 18
XFER_LOAD_PC  = 1 << 18
XFER_LOAD_X   = 2 << 18
XFER_LOAD_Y   = 3 << 18
XFER_LOAD_SP  = 4 << 18
XFER_LOAD_E   = 5 << 18
; Room for 2 more XFER Load

; 3 bits for ADDR Assert
ADDR_ASSERT_PC = 0 << 21
ADDR_ASSERT_X  = 1 << 21
ADDR_ASSERT_Y  = 2 << 21
ADDR_ASSERT_SP = 3 << 21
ADDR_ASSERT_DP = 4 << 21
ADDR_ASSERT_E  = 5 << 21
; Room for 2 more ADDR Assert

; 3 bits for Counter Increments
COUNT_INC_NULL = 0 << 24
COUNT_INC_PC   = 1 << 24
COUNT_INC_SP   = 2 << 24
COUNT_INC_X    = 3 << 24
COUNT_INC_Y    = 4 << 24
; Room for 3 more Counter Incs

; 2 bits for Counter Decrements
COUNT_DEC_NULL = 0 << 27 
COUNT_DEC_SP   = 1 << 27
COUNT_DEC_X    = 2 << 27
COUNT_DEC_Y    = 3 << 27

; 3 bits for CPU CTRL
; TODO: determine
RST_USEQ      = 0 << 29
RST_USEQ_EXT1 = 1 << 29
RST_USEQ_EXT2 = 2 << 29
BRK_CLK       = 3 << 29
RST_BRK_CLK   = 4 << 29