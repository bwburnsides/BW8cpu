class Ctrl:
    # Ctrl Fields
    DBUS_ASSERT = 0
    DBUS_LOAD = 4
    ALU_OP = 8
    XFER_ASSERT = 13
    XFER_LOAD = 18
    ADDR_ASSERT = 21
    COUNT = 24

    # DBUS device addresses
    NULL_DBUS = 0
    IR_DBUS = 1
    A_DBUS = 2
    B_DBUS = 3
    C_DBUS = 4
    D_DBUS = 5
    DP_DBUS = 6
    SR_DBUS = 7
    T1_DBUS = 8
    T2_DBUS = 9
    MEM_DBUS = 10
    DPI_DBUS = 11
    ALU_DBUS = 12

    # XFER device addresses
    RST_XFER   = 0
    SP_XFER    = 1
    PC_XFER    = 2
    X_XFER     = 3
    Y_XFER     = 4
    T_XFER     = 5
    E_XFER     = 6
    ISR_XFER   = 7
    SPI_XFER   = 8
    _XFER_BASE = 9

    # ADDR device addresses
    ACK_ADDR = 0
    PC_ADDR = 1
    SP_ADDR = 2
    X_ADDR = 3
    Y_ADDR = 4
    E_ADDR = 5
    DP_ADDR = 6
    T_ADDR = 7

    # 4 bits for DBUS Assert
    DBUS_ASSERT_NULL = NULL_DBUS << DBUS_ASSERT
    DBUS_ASSERT_A = A_DBUS << DBUS_ASSERT
    DBUS_ASSERT_B = B_DBUS << DBUS_ASSERT
    DBUS_ASSERT_C = C_DBUS << DBUS_ASSERT
    DBUS_ASSERT_D = D_DBUS << DBUS_ASSERT
    DBUS_ASSERT_DP = DP_DBUS << DBUS_ASSERT
    DBUS_ASSERT_SR = SR_DBUS << DBUS_ASSERT
    DBUS_ASSERT_T1 = T1_DBUS << DBUS_ASSERT
    DBUS_ASSERT_T2 = T2_DBUS << DBUS_ASSERT
    DBUS_ASSERT_MEM = MEM_DBUS << DBUS_ASSERT
    DBUS_ASSERT_DPI = DPI_DBUS << DBUS_ASSERT
    DBUS_ASSERT_ALU = ALU_DBUS << DBUS_ASSERT
    # Room for 5 more DBUS Asserts

    # 4 bits for DBUS Load
    DBUS_LOAD_NULL = NULL_DBUS << DBUS_LOAD
    DBUS_LOAD_A = A_DBUS << DBUS_LOAD
    DBUS_LOAD_B = B_DBUS << DBUS_LOAD
    DBUS_LOAD_C = C_DBUS << DBUS_LOAD
    DBUS_LOAD_D = D_DBUS << DBUS_LOAD
    DBUS_LOAD_SR = SR_DBUS << DBUS_LOAD
    DBUS_LOAD_DP = DP_DBUS << DBUS_LOAD
    DBUS_LOAD_T1 = T1_DBUS << DBUS_LOAD
    DBUS_LOAD_T2 = T2_DBUS << DBUS_LOAD
    DBUS_LOAD_MEM = MEM_DBUS << DBUS_LOAD
    DBUS_LOAD_IR = IR_DBUS << DBUS_LOAD

    # 5 bits for ALU OP
    ALU_NOP = 0 << ALU_OP
    ALU_ZERO = 1 << ALU_OP
    ALU_LHS = 2 << ALU_OP
    ALU_RHS = 3 << ALU_OP
    ALU_LHS_C = 4 << ALU_OP
    ALU_RHS_C = 5 << ALU_OP

    ALU_MSB = ALU_LHS
    ALU_LSB = ALU_RHS
    ALU_MSB_C = ALU_LHS_C
    ALU_LSB_C = ALU_RHS_C

    ALU_ADD = 6 << ALU_OP
    ALU_ADC = 7 << ALU_OP
    ALU_SUB = 8 << ALU_OP
    ALU_SBB = 9 << ALU_OP
    ALU_NEG = 10 << ALU_OP
    ALU_INC = 11 << ALU_OP
    ALU_DEC = 12 << ALU_OP

    ALU_AND = 13 << ALU_OP
    ALU_OR = 14 << ALU_OP
    ALU_XOR = 15 << ALU_OP
    ALU_NOT = 16 << ALU_OP

    ALU_LSR = 17 << ALU_OP
    ALU_LRC = 18 << ALU_OP
    ALU_ASR = 19 << ALU_OP

    ALU_SEI = 20 << ALU_OP
    ALU_CLI = 21 << ALU_OP
    ALU_SEC = 22 << ALU_OP
    ALU_CLC = 23 << ALU_OP
    ALU_SEV = 24 << ALU_OP
    ALU_CLV = 25 << ALU_OP
    ALU_SEZ = 26 << ALU_OP
    ALU_CLZ = 27 << ALU_OP
    ALU_SEN = 28 << ALU_OP
    ALU_CLN = 29 << ALU_OP

    # 5 bits for XFER Assert
    XFER_ASSERT_RST = RST_XFER << XFER_ASSERT
    XFER_ASSERT_SP = SP_XFER << XFER_ASSERT
    XFER_ASSERT_PC = PC_XFER << XFER_ASSERT
    XFER_ASSERT_X = X_XFER << XFER_ASSERT
    XFER_ASSERT_Y = Y_XFER << XFER_ASSERT
    XFER_ASSERT_T = T_XFER << XFER_ASSERT
    XFER_ASSERT_E = E_XFER << XFER_ASSERT
    XFER_ASSERT_ISR = ISR_XFER << XFER_ASSERT
    XFER_ASSERT_SPI = SPI_XFER << XFER_ASSERT

    XFER_ASSERT_T2_D = (_XFER_BASE + 0) << XFER_ASSERT

    XFER_ASSERT_A_A = (_XFER_BASE + 1) << XFER_ASSERT
    # XFER_ASSERT_A_B  = E_XFER            << XFER_ASSERT
    XFER_ASSERT_A_C = (_XFER_BASE + 2) << XFER_ASSERT
    XFER_ASSERT_A_D = (_XFER_BASE + 3) << XFER_ASSERT
    XFER_ASSERT_A_T1 = (_XFER_BASE + 4) << XFER_ASSERT

    XFER_ASSERT_B_A = (_XFER_BASE + 5) << XFER_ASSERT
    XFER_ASSERT_B_B = (_XFER_BASE + 6) << XFER_ASSERT
    XFER_ASSERT_B_C = (_XFER_BASE + 7) << XFER_ASSERT
    XFER_ASSERT_B_D = (_XFER_BASE + 8) << XFER_ASSERT
    XFER_ASSERT_B_T1 = (_XFER_BASE + 9) << XFER_ASSERT

    XFER_ASSERT_C_A = (_XFER_BASE + 10) << XFER_ASSERT
    XFER_ASSERT_C_B = (_XFER_BASE + 11) << XFER_ASSERT
    XFER_ASSERT_C_C = (_XFER_BASE + 12) << XFER_ASSERT
    XFER_ASSERT_C_D = (_XFER_BASE + 13) << XFER_ASSERT
    XFER_ASSERT_C_T1 = (_XFER_BASE + 14) << XFER_ASSERT

    XFER_ASSERT_D_A = (_XFER_BASE + 15) << XFER_ASSERT
    XFER_ASSERT_D_B = (_XFER_BASE + 16) << XFER_ASSERT
    XFER_ASSERT_D_C = (_XFER_BASE + 17) << XFER_ASSERT
    XFER_ASSERT_D_D = (_XFER_BASE + 18) << XFER_ASSERT
    XFER_ASSERT_D_T1 = (_XFER_BASE + 19) << XFER_ASSERT

    XFER_ASSERT_T2_A = (_XFER_BASE + 20) << XFER_ASSERT
    XFER_ASSERT_T2_B = (_XFER_BASE + 21) << XFER_ASSERT
    XFER_ASSERT_T2_C = (_XFER_BASE + 22) << XFER_ASSERT

    # 3 bits for XFER Load
    XFER_LOAD_PC = PC_XFER << XFER_LOAD
    XFER_LOAD_SP = SP_XFER << XFER_LOAD
    XFER_LOAD_E = E_XFER << XFER_LOAD
    XFER_LOAD_X = X_XFER << XFER_LOAD
    XFER_LOAD_Y = Y_XFER << XFER_LOAD
    # Room for 2 more XFER Load

    # 3 bits for ADDR Assert
    ADDR_ASSERT_ACK = ACK_ADDR << ADDR_ASSERT
    ADDR_ASSERT_PC = PC_ADDR << ADDR_ASSERT
    ADDR_ASSERT_SP = SP_ADDR << ADDR_ASSERT
    ADDR_ASSERT_X = X_ADDR << ADDR_ASSERT
    ADDR_ASSERT_Y = Y_ADDR << ADDR_ASSERT
    ADDR_ASSERT_E = E_ADDR << ADDR_ASSERT
    ADDR_ASSERT_DP = DP_ADDR << ADDR_ASSERT
    ADDR_ASSERT_T = T_ADDR << ADDR_ASSERT

    # 3 bits for Counter Inc/Decs
    COUNT_NULL = 0 << COUNT
    COUNT_INC_SP = SP_XFER << COUNT
    COUNT_INC_PC = PC_XFER << COUNT
    COUNT_INC_X = X_XFER << COUNT
    COUNT_INC_Y = Y_XFER << COUNT
    COUNT_INC_T = T_XFER << COUNT

    COUNT_DEC_X = 6 << COUNT
    COUNT_DEC_Y = 7 << COUNT

    COUNT_DEC_SP = 1 << 27

    # 4 bits for CPU CTRL
    RST_USEQ = 1 << 28
    TOG_EXT1 = 1 << 29
    TOG_EXT2 = 1 << 30
    BRK_CLK = 1 << 31


active_low_signals = [Ctrl.BRK_CLK]

fetch = 0 | Ctrl.ADDR_ASSERT_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_IR | Ctrl.COUNT_INC_PC | Ctrl.BRK_CLK

def build_uops(mode, irq, opcode, flags, t_state):
    uops = [Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK, Ctrl.BRK_CLK]

    # if opcode == 0x00:  # NOP
    #     uops[1] |= Ctrl.RST_USEQ

    # if opcode == 0x01:  # LOAD A IMM
    #     uops[1] |= Ctrl.ADDR_ASSERT_PC | Ctrl.COUNT_INC_PC | Ctrl.DBUS_ASSERT_MEM | Ctrl.DBUS_LOAD_A | Ctrl.RST_USEQ

    # if opcode == 0x02:  # BRK
    #     uops[1] = Ctrl.RST_USEQ

    return uops

ucode = []
for addr in range(2**19):
    mode = (addr & (0b11 << 17)) >> 17
    irq = (addr & (0b1 << 15)) >> 15
    opcode = (addr & (0b1111_1111 << 8)) >> 8
    flags = (addr & (0b11111 << 3)) >> 3
    t_state = (addr & (0b111 << 0)) >> 0

    # irq is an active-low signal
    irq = 1 if irq else 0
 
    uops = build_uops(mode, irq, opcode, flags, t_state)
    ucode.extend(uops)

print(len(ucode) / 1024)

val = bin(ucode[-1])[2:]
new = []
for char in val:
    new.append(char)
    new.append(" ")

print("".join(new))

roms = [[], [], [], []]
for word in ucode:
    byte0 = (word & (0b1111_1111 << 0)) >> 0
    byte1 = (word & (0b1111_1111 << 8)) >> 8
    byte2 = (word & (0b1111_1111 << 16)) >> 16
    byte3 = (word & (0b1111_1111 << 24)) >> 24

    roms[0].append(byte0)
    roms[1].append(byte1)
    roms[2].append(byte2)
    roms[3].append(byte3)

print(roms[0][0])
print(roms[1][0])
print(roms[2][0])
print(roms[3][0])
handles = [
    ("control_0.bin", roms[0]),
    ("control_1.bin", roms[1]),
    ("control_2.bin", roms[2]),
    ("control_3.bin", roms[3]),
]

for name, data in handles:
    with open(name, "wb") as f:
        for word in data:
            f.write(word.to_bytes(1, byteorder="big"))
