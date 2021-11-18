from enum import IntFlag

# TODO: On arch diagram, include a TEMP reg on DBUS and RHS
# TODO: On arch diagram, include CONST + TEMP ADDR ASSERT
class Ctrl(IntFlag):
    # 4 bits to specify DBUS Assertions = 16 devices
    DBUS_ASSERT_00 = 0 << 0
    DBUS_ASSERT_01 = 1 << 0
    DBUS_ASSERT_02 = 2 << 0
    DBUS_ASSERT_03 = 3 << 0
    DBUS_ASSERT_04 = 4 << 0
    DBUS_ASSERT_05 = 5 << 0
    DBUS_ASSERT_06 = 6 << 0
    DBUS_ASSERT_07 = 7 << 0
    DBUS_ASSERT_08 = 8 << 0
    DBUS_ASSERT_09 = 9 << 0
    DBUS_ASSERT_10 = 10 << 0
    DBUS_ASSERT_11 = 11 << 0
    DBUS_ASSERT_12 = 12 << 0
    DBUS_ASSERT_13 = 13 << 0
    DBUS_ASSERT_14 = 14 << 0
    DBUS_ASSERT_15 = 15 << 0

    # DBUS ASSERT ALIASES
    ###################################
    DBUS_ASSERT_MEM = DBUS_ASSERT_00
    DBUS_ASSERT_A = DBUS_ASSERT_01
    DBUS_ASSERT_B = DBUS_ASSERT_02
    DBUS_ASSERT_C = DBUS_ASSERT_03
    DBUS_ASSERT_D = DBUS_ASSERT_04
    DBUS_ASSERT_ALU = DBUS_ASSERT_05
    DBUS_ASSERT_SR = DBUS_ASSERT_06
    DBUS_ASSERT_SP = DBUS_ASSERT_07
    DBUS_ASSERT_CONST = DBUS_ASSERT_08
    DBUS_ASSERT_XL = DBUS_ASSERT_09
    DBUS_ASSERT_XH = DBUS_ASSERT_10
    DBUS_ASSERT_YL = DBUS_ASSERT_11
    DBUS_ASSERT_YH = DBUS_ASSERT_12
    DBUS_ASSERT_PCL = DBUS_ASSERT_13
    DBUS_ASSERT_PCH = DBUS_ASSERT_14
    ###################################

    # 4 bits to specify DBUS Loads = 16 devices
    DBUS_LOAD_00 = 0 << 4
    DBUS_LOAD_01 = 1 << 4
    DBUS_LOAD_02 = 2 << 4
    DBUS_LOAD_03 = 3 << 4
    DBUS_LOAD_04 = 4 << 4
    DBUS_LOAD_05 = 5 << 4
    DBUS_LOAD_06 = 6 << 4
    DBUS_LOAD_07 = 7 << 4
    DBUS_LOAD_08 = 8 << 4
    DBUS_LOAD_09 = 9 << 4
    DBUS_LOAD_10 = 10 << 4
    DBUS_LOAD_11 = 11 << 4
    DBUS_LOAD_12 = 12 << 4
    DBUS_LOAD_13 = 13 << 4
    DBUS_LOAD_14 = 14 << 4
    DBUS_LOAD_15 = 15 << 4

    # DBUS LOAD ALIASES
    ###############################
    DBUS_LOAD_NULL = DBUS_LOAD_00
    DBUS_LOAD_A = DBUS_LOAD_01
    DBUS_LOAD_B = DBUS_LOAD_02
    DBUS_LOAD_C = DBUS_LOAD_03
    DBUS_LOAD_D = DBUS_LOAD_04
    DBUS_LOAD_SR = DBUS_LOAD_05
    DBUS_LOAD_MEM = DBUS_LOAD_06
    DBUS_LOAD_CONST = DBUS_LOAD_07
    DBUS_LOAD_IR = DBUS_LOAD_08
    DBUS_LOAD_SP = DBUS_LOAD_09
    DBUS_LOAD_TEMP = DBUS_LOAD_10
    ################################

    # 5 bits to specify ALU Operation = 32 operations
    ALU_OP_00 = 0 << 8
    ALU_OP_01 = 1 << 8
    ALU_OP_02 = 2 << 8
    ALU_OP_03 = 3 << 8
    ALU_OP_04 = 4 << 8
    ALU_OP_05 = 5 << 8
    ALU_OP_06 = 6 << 8
    ALU_OP_07 = 7 << 8
    ALU_OP_08 = 8 << 8
    ALU_OP_09 = 9 << 8
    ALU_OP_10 = 10 << 8
    ALU_OP_11 = 11 << 8
    ALU_OP_12 = 12 << 8
    ALU_OP_13 = 13 << 8
    ALU_OP_14 = 14 << 8
    ALU_OP_15 = 15 << 8
    ALU_OP_16 = 16 << 8
    ALU_OP_17 = 17 << 8
    ALU_OP_18 = 18 << 8
    ALU_OP_19 = 19 << 8
    ALU_OP_20 = 20 << 8
    ALU_OP_21 = 21 << 8
    ALU_OP_22 = 22 << 8
    ALU_OP_23 = 23 << 8
    ALU_OP_24 = 24 << 8
    ALU_OP_25 = 25 << 8
    ALU_OP_26 = 26 << 8
    ALU_OP_27 = 27 << 8
    ALU_OP_28 = 28 << 8
    ALU_OP_29 = 29 << 8
    ALU_OP_30 = 30 << 8
    ALU_OP_31 = 31 << 8

    # ALU Operation Aliases
    #######################
    ALU_NOP = ALU_OP_00  # ALU NOP
    ALU_ADD = ALU_OP_01  # Add without carry
    ALU_ADC = ALU_OP_02  # Add with carry
    ALU_SUB = ALU_OP_03  # Sub without borrow
    ALU_SBB = ALU_OP_04  # Sub with borrow
    ALU_AND = ALU_OP_05  # Bitwise AND
    ALU_OR = ALU_OP_06  # Bitwise OR
    ALU_XOR = ALU_OP_07  # Bitwise XOR
    ALU_NOT = ALU_OP_08  # Bitwise NOT
    ALU_NEG = ALU_OP_09  # Negation (perform 2s complement)
    ALU_LSR = ALU_OP_10  # Logical Right Shift
    ALU_LRC = ALU_OP_11  # Logical Right Shift with Carry
    ALU_ASR = ALU_OP_12  # Arithmetic Right Shift
    ALU_INC = ALU_OP_13  # Increment
    ALU_DEC = ALU_OP_14  # Decrement
    ALU_LHS = ALU_OP_15  # Pass LHS through to DBUS
    ALU_RHS = ALU_OP_16  # Pass RHS through to DBUS
    ALU_SEI = ALU_OP_17  # Set the I Flag
    ALU_CLI = ALU_OP_18  # Clear the I Flag
    ALU_SEC = ALU_OP_19  # Set the C Flag
    ALU_CLC = ALU_OP_20  # Clear the C Flag
    ALU_SEV = ALU_OP_21  # Set the V Flag
    ALU_CLV = ALU_OP_22  # Clear the V Flag
    ALU_SEZ = ALU_OP_23  # Set the Z Flag
    ALU_CLZ = ALU_OP_24  # Clear the Z Flag
    ALU_SEN = ALU_OP_25  # Set the N Flag
    ALU_CLN = ALU_OP_26  # Clear the N Flag

    ALU_LHS_C = ALU_OP_27  # Result is LHS + C
    ALU_RHS_C = ALU_OP_28  # Result is RHS + C
    #######################

    # 5 bits to specify Transfer Bus Assertions = 32 devices
    XFER_ASSERT_00 = 0 << 13
    XFER_ASSERT_01 = 1 << 13
    XFER_ASSERT_02 = 2 << 13
    XFER_ASSERT_03 = 3 << 13
    XFER_ASSERT_04 = 4 << 13
    XFER_ASSERT_05 = 5 << 13
    XFER_ASSERT_06 = 6 << 13
    XFER_ASSERT_07 = 7 << 13
    XFER_ASSERT_08 = 8 << 13
    XFER_ASSERT_09 = 9 << 13
    XFER_ASSERT_10 = 10 << 13
    XFER_ASSERT_11 = 11 << 13
    XFER_ASSERT_12 = 12 << 13
    XFER_ASSERT_13 = 13 << 13
    XFER_ASSERT_14 = 14 << 13
    XFER_ASSERT_15 = 15 << 13
    XFER_ASSERT_16 = 16 << 13
    XFER_ASSERT_17 = 17 << 13
    XFER_ASSERT_18 = 18 << 13
    XFER_ASSERT_19 = 19 << 13
    XFER_ASSERT_20 = 20 << 13
    XFER_ASSERT_21 = 21 << 13
    XFER_ASSERT_22 = 22 << 13
    XFER_ASSERT_23 = 23 << 13
    XFER_ASSERT_24 = 24 << 13
    XFER_ASSERT_25 = 25 << 13
    XFER_ASSERT_26 = 26 << 13
    XFER_ASSERT_27 = 27 << 13
    XFER_ASSERT_28 = 28 << 13
    XFER_ASSERT_29 = 29 << 13
    XFER_ASSERT_30 = 30 << 13
    XFER_ASSERT_31 = 31 << 13

    # XFER Assert Aliases
    ###################################
    XFER_ASSERT_A_A = XFER_ASSERT_00
    XFER_ASSERT_A_B = XFER_ASSERT_01
    XFER_ASSERT_A_C = XFER_ASSERT_02
    XFER_ASSERT_A_D = XFER_ASSERT_03
    XFER_ASSERT_A_SPL = XFER_ASSERT_04
    XFER_ASSERT_A_CONST = XFER_ASSERT_05
    XFER_ASSERT_B_A = XFER_ASSERT_06
    XFER_ASSERT_B_B = XFER_ASSERT_07
    XFER_ASSERT_B_C = XFER_ASSERT_08
    XFER_ASSERT_B_D = XFER_ASSERT_09
    XFER_ASSERT_B_SPL = XFER_ASSERT_10
    XFER_ASSERT_B_CONST = XFER_ASSERT_11
    XFER_ASSERT_C_A = XFER_ASSERT_12
    XFER_ASSERT_C_B = XFER_ASSERT_13
    XFER_ASSERT_C_C = XFER_ASSERT_14
    XFER_ASSERT_C_D = XFER_ASSERT_15
    XFER_ASSERT_C_SPL = XFER_ASSERT_16
    XFER_ASSERT_C_CONST = XFER_ASSERT_17
    XFER_ASSERT_D_A = XFER_ASSERT_18
    XFER_ASSERT_D_B = XFER_ASSERT_19
    XFER_ASSERT_D_C = XFER_ASSERT_20
    XFER_ASSERT_D_D = XFER_ASSERT_21
    XFER_ASSERT_D_SPL = XFER_ASSERT_22
    XFER_ASSERT_D_CONST = XFER_ASSERT_23
    XFER_ASSERT_CONST_TEMP = XFER_ASSERT_24
    XFER_ASSERT_SP = XFER_ASSERT_25
    XFER_ASSERT_ISR = XFER_ASSERT_26
    XFER_ASSERT_RST = XFER_ASSERT_27
    XFER_ASSERT_Y = XFER_ASSERT_28
    XFER_ASSERT_X = XFER_ASSERT_29
    XFER_ASSERT_PC = XFER_ASSERT_30
    ###################################

    # 2 bits to specify Transfer Bus Loads = 4 devices
    XFER_LOAD_00 = 0 << 18
    XFER_LOAD_01 = 1 << 18
    XFER_LOAD_02 = 2 << 18
    XFER_LOAD_03 = 3 << 18

    # XFER Load Aliases
    #########################
    XFER_LOAD_ALU = XFER_LOAD_00
    XFER_LOAD_PC = XFER_LOAD_01
    XFER_LOAD_X = XFER_LOAD_02
    XFER_LOAD_Y = XFER_LOAD_03
    #########################

    # 3 bits to specify Addr Bus Assertions = 8 devices
    ADDR_ASSERT_00 = 0 << 20
    ADDR_ASSERT_01 = 1 << 20
    ADDR_ASSERT_02 = 2 << 20
    ADDR_ASSERT_03 = 3 << 20
    ADDR_ASSERT_04 = 4 << 20
    ADDR_ASSERT_05 = 5 << 20
    ADDR_ASSERT_06 = 6 << 20
    ADDR_ASSERT_07 = 7 << 20

    # Addr Assert Aliases
    #########################
    ADDR_ASSERT_PC = ADDR_ASSERT_00
    ADDR_ASSERT_X = ADDR_ASSERT_01
    ADDR_ASSERT_Y = ADDR_ASSERT_02
    ADDR_ASSERT_SP = ADDR_ASSERT_03
    ADDR_ASSERT_ZPG = ADDR_ASSERT_04
    ADDR_ASSERT_CONST_TEMP = ADDR_ASSERT_05
    #########################

    # 3 bits to specify Counter Increments = 8 devices
    COUNT_INC_00 = 0 << 23
    COUNT_INC_01 = 1 << 23
    COUNT_INC_02 = 2 << 23
    COUNT_INC_03 = 3 << 23
    COUNT_INC_04 = 4 << 23
    COUNT_INC_05 = 5 << 23
    COUNT_INC_06 = 6 << 23
    COUNT_INC_07 = 7 << 23

    # Counter Inc Aliases
    ########################
    COUNT_INC_NULL = COUNT_INC_00
    COUNT_INC_PC = COUNT_INC_01
    COUNT_INC_SP = COUNT_INC_02
    COUNT_INC_X = COUNT_INC_03
    COUNT_INC_Y = COUNT_INC_04
    ########################

    # 2 bits to specify Counter Decrements = 4 devices
    COUNT_DEC_00 = 0 << 26
    COUNT_DEC_01 = 1 << 26
    COUNT_DEC_02 = 2 << 26
    COUNT_DEC_03 = 3 << 26

    # Counter Dec Aliases
    ##############################
    COUNT_DEC_NULL = COUNT_DEC_00
    COUNT_DEC_SP = COUNT_DEC_01
    COUNT_DEC_X = COUNT_DEC_02
    COUNT_DEC_Y = COUNT_DEC_03
    ##############################

    # Single bit control lines
    EXTENDED_OP_FLIP = 1 << 28
    RESET_USTEP = 1 << 29
    CLEAR_RESET = 1 << 30
    BREAK = 1 << 31
