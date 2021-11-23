from enum import Enum, auto

class Inst(Enum):
    NOP = "nop"
    BRK = "brk"
    WAI = "wai"
    EX1 = "ex1"
    EX2 = "ex2"
    CLC = "clc"
    CLI = "cli"
    CLV = "clv"
    SEC = "sec"
    SEI = "sei"
    MOV = "mov"
    LOAD = "load"
    STORE = "store"
    INC = "inc"
    DEC = "dec"
    ADD = "add"
    ADC = "adc"
    SUB = "sub"
    SBB = "sbb"
    AND = "and"
    OR = "or"
    XOR = "xor"
    NOT = "not"
    NEG = "neg"
    ASR = "asr"
    SHRC = "shrc"
    SHR = "shr"
    SHLC = "shlc"
    SHL = "shl"
    CMP = "cmp"
    TST = "tst"
    PUSH = "push"
    POP = "pop"
    JMP = "jmp"
    JSR = "jsr"
    RTS = "rts"
    RTI = "rti"
    JO = "jo"
    JNO = "jno"
    JN = "jn"
    JP = "jp"
    JZ = "jz"
    JNZ = "jnz"
    JC = "jc"
    JNC = "jnc"
    JA = "ja"
    JNA = "jna"
    JL = "jl"
    JGE = "jge"
    JG = "jg"
    JLE = "jle"


def main():
    with open("bwb_opcodes.txt") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    opcodes = [line for line in lines if not line.startswith("#")]

    print(len(opcodes))
    # ucode = gen_ucode(opcodes)

if __name__ == "__main__":
    main()
