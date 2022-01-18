; NOTE: take caution when modifying any orderings in this file. the simulator's control unit
; and bus decoder has been configured to use these exact values.

; Ctrl Fields
DBUS_ASSERT = 0
DBUS_LOAD   = 4
ALU_OP      = 8
XFER_ASSERT = 13
XFER_LOAD   = 18
ADDR_ASSERT = 21
COUNT       = 24

; DBUS device addresses
NULL_DBUS = 0
ALU_DBUS  = 0
IR_DBUS   = 1
A_DBUS    = 2
B_DBUS    = 3
C_DBUS    = 4
D_DBUS    = 5
DP_DBUS   = 6
SR_DBUS   = 7
T1_DBUS   = 8
T2_DBUS   = 9
MEM_DBUS  = 10
DPI_DBUS  = 11

; XFER device addresses
ALU_XFER   = 0
SP_XFER    = 1
PC_XFER    = 2
X_XFER     = 3
Y_XFER     = 4
T_XFER     = 5
E_XFER     = 6
ISR_XFER   = 7
RST_XFER   = 8
SPI_XFER   = 9
_XFER_BASE = 10

; ADDR device addresses
SP_ADDR = SP_XFER
PC_ADDR = PC_XFER
X_ADDR = X_XFER
Y_ADDR = Y_XFER
T_ADDR = T_XFER
E_ADDR = E_XFER
DP_ADDR = 7

; 4 bits for DBUS Assert
DBUS_ASSERT_ALU = ALU_DBUS << DBUS_ASSERT
DBUS_ASSERT_A   = A_DBUS   << DBUS_ASSERT
DBUS_ASSERT_B   = B_DBUS   << DBUS_ASSERT
DBUS_ASSERT_C   = C_DBUS   << DBUS_ASSERT
DBUS_ASSERT_D   = D_DBUS   << DBUS_ASSERT
DBUS_ASSERT_DP  = DP_DBUS  << DBUS_ASSERT
DBUS_ASSERT_SR  = SR_DBUS  << DBUS_ASSERT
DBUS_ASSERT_T1  = T1_DBUS  << DBUS_ASSERT
DBUS_ASSERT_T2  = T2_DBUS  << DBUS_ASSERT
DBUS_ASSERT_MEM = MEM_DBUS << DBUS_ASSERT
DBUS_ASSERT_DPI = DPI_DBUS << DBUS_ASSERT
; Room for 5 more DBUS Asserts

; 4 bits for DBUS Load
DBUS_LOAD_NULL = NULL_DBUS << DBUS_LOAD
DBUS_LOAD_A    = A_DBUS    << DBUS_LOAD
DBUS_LOAD_B    = B_DBUS    << DBUS_LOAD
DBUS_LOAD_C    = C_DBUS    << DBUS_LOAD
DBUS_LOAD_D    = D_DBUS    << DBUS_LOAD
DBUS_LOAD_SR   = SR_DBUS   << DBUS_LOAD
DBUS_LOAD_DP   = DP_DBUS   << DBUS_LOAD
DBUS_LOAD_T1   = T1_DBUS   << DBUS_LOAD
DBUS_LOAD_T2   = T2_DBUS   << DBUS_LOAD
DBUS_LOAD_MEM  = MEM_DBUS  << DBUS_LOAD
DBUS_LOAD_IR   = IR_DBUS   << DBUS_LOAD

DBUS_LOAD_PCL  = 12 << DBUS_LOAD
DBUS_LOAD_PCH  = 13 << DBUS_LOAD
; Room for 3 more DBUS Loads

; 5 bits for ALU OP
ALU_NOP   = 0  << ALU_OP
ALU_ZERO  = 1  << ALU_OP
ALU_LHS   = 2  << ALU_OP
ALU_RHS   = 3  << ALU_OP
ALU_LHS_C = 4  << ALU_OP
ALU_RHS_C = 5  << ALU_OP

ALU_MSB = ALU_LHS
ALU_LSB = ALU_RHS
ALU_MSB_C = ALU_LHS_C
ALU_LSB_C = ALU_RHS_C

ALU_ADD   = 6  << ALU_OP
ALU_ADC   = 7  << ALU_OP
ALU_SUB   = 8  << ALU_OP
ALU_SBB   = 9  << ALU_OP
ALU_NEG   = 10 << ALU_OP
ALU_INC   = 11 << ALU_OP
ALU_DEC   = 12 << ALU_OP

ALU_AND   = 13 << ALU_OP
ALU_OR    = 14 << ALU_OP
ALU_XOR   = 15 << ALU_OP
ALU_NOT   = 16 << ALU_OP

ALU_LSR   = 17 << ALU_OP
ALU_LRC   = 18 << ALU_OP
ALU_ASR   = 19 << ALU_OP

ALU_SEI   = 20 << ALU_OP
ALU_CLI   = 21 << ALU_OP
ALU_SEC   = 22 << ALU_OP
ALU_CLC   = 23 << ALU_OP
ALU_SEV   = 24 << ALU_OP
ALU_CLV   = 25 << ALU_OP
ALU_SEZ   = 26 << ALU_OP
ALU_CLZ   = 27 << ALU_OP
ALU_SEN   = 28 << ALU_OP
ALU_CLN   = 29 << ALU_OP

ALU_SSR   = 30 << ALU_OP  ; set SR to RHS
; Room for 1 more ALU OPs

; 5 bits for XFER Assert
XFER_ASSERT_SP  = SP_XFER            << XFER_ASSERT
XFER_ASSERT_PC  = PC_XFER            << XFER_ASSERT
XFER_ASSERT_X   = X_XFER             << XFER_ASSERT
XFER_ASSERT_Y   = Y_XFER             << XFER_ASSERT
XFER_ASSERT_T   = T_XFER             << XFER_ASSERT
XFER_ASSERT_E   = E_XFER             << XFER_ASSERT
XFER_ASSERT_ISR = ISR_XFER           << XFER_ASSERT
XFER_ASSERT_RST = RST_XFER           << XFER_ASSERT
XFER_ASSERT_SPI = SPI_XFER           << XFER_ASSERT

XFER_ASSERT_A_A  = (_XFER_BASE + 0)  << XFER_ASSERT
; XFER_ASSERT_A_B  = E_XFER            << XFER_ASSERT
XFER_ASSERT_A_C  = (_XFER_BASE + 1)  << XFER_ASSERT
XFER_ASSERT_A_D  = (_XFER_BASE + 2)  << XFER_ASSERT
XFER_ASSERT_A_T1 = (_XFER_BASE + 3)  << XFER_ASSERT

XFER_ASSERT_B_A  = (_XFER_BASE + 4)  << XFER_ASSERT
XFER_ASSERT_B_B  = (_XFER_BASE + 5)  << XFER_ASSERT
XFER_ASSERT_B_C  = (_XFER_BASE + 6)  << XFER_ASSERT
XFER_ASSERT_B_D  = (_XFER_BASE + 7)  << XFER_ASSERT
XFER_ASSERT_B_T1 = (_XFER_BASE + 8)  << XFER_ASSERT

XFER_ASSERT_C_A  = (_XFER_BASE + 9) << XFER_ASSERT
XFER_ASSERT_C_B  = (_XFER_BASE + 10) << XFER_ASSERT
XFER_ASSERT_C_C  = (_XFER_BASE + 11) << XFER_ASSERT
XFER_ASSERT_C_D  = (_XFER_BASE + 12) << XFER_ASSERT
XFER_ASSERT_C_T1 = (_XFER_BASE + 13) << XFER_ASSERT

XFER_ASSERT_D_A  = (_XFER_BASE + 14) << XFER_ASSERT
XFER_ASSERT_D_B  = (_XFER_BASE + 15) << XFER_ASSERT
XFER_ASSERT_D_C  = (_XFER_BASE + 16) << XFER_ASSERT
XFER_ASSERT_D_D  = (_XFER_BASE + 17) << XFER_ASSERT
XFER_ASSERT_D_T1 = (_XFER_BASE + 18) << XFER_ASSERT

XFER_ASSERT_T2_A = (_XFER_BASE + 19) << XFER_ASSERT
XFER_ASSERT_T2_B = (_XFER_BASE + 20) << XFER_ASSERT
XFER_ASSERT_T2_C = (_XFER_BASE + 21) << XFER_ASSERT
XFER_ASSERT_T2_D = (_XFER_BASE + 22) << XFER_ASSERT

; 3 bits for XFER Load
XFER_LOAD_ALU = ALU_XFER << XFER_LOAD
XFER_LOAD_PC  = PC_XFER  << XFER_LOAD
XFER_LOAD_SP  = SP_XFER  << XFER_LOAD
XFER_LOAD_E   = E_XFER   << XFER_LOAD
XFER_LOAD_X   = X_XFER   << XFER_LOAD
XFER_LOAD_Y   = Y_XFER   << XFER_LOAD
; Room for 2 more XFER Load

; 3 bits for ADDR Assert
ADDR_ASSERT_PC = PC_ADDR << ADDR_ASSERT
ADDR_ASSERT_SP = SP_ADDR << ADDR_ASSERT
ADDR_ASSERT_X  = X_ADDR  << ADDR_ASSERT
ADDR_ASSERT_Y  = Y_ADDR  << ADDR_ASSERT
ADDR_ASSERT_E  = E_ADDR  << ADDR_ASSERT
ADDR_ASSERT_DP = DP_ADDR << ADDR_ASSERT
ADDR_ASSERT_T  = T_ADDR  << ADDR_ASSERT
; Room for 1 more ADDR Assert

; 3 bits for Counter Inc/Decs
COUNT_NULL   = 0       << COUNT
COUNT_INC_SP = SP_XFER << COUNT
COUNT_INC_PC = PC_XFER << COUNT
COUNT_INC_X  = X_XFER  << COUNT
COUNT_INC_Y  = Y_XFER  << COUNT
COUNT_INC_T  = T_XFER  << COUNT

COUNT_DEC_X  = 6       << COUNT
COUNT_DEC_Y  = 7       << COUNT

; 4 bits for CPU CTRL
RST_USEQ = 1 << 27
TOG_EXT1 = 1 << 28
TOG_EXT2 = 1 << 29
BRK_CLK  = 1 << 30

COUNT_DEC_SP = SP_XFER << 31
