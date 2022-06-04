from pprint import pprint

adcs = """
SBC_A_A
SBC_A_B
SBC_A_C
SBC_A_D
SBC_A_IMM
SBC_A_DP

SBC_B_A
SBC_B_B
SBC_B_C
SBC_B_D
SBC_B_IMM
SBC_B_DP

SBC_C_A
SBC_C_B
SBC_C_C
SBC_C_D
SBC_C_IMM
SBC_C_DP

SBC_D_A
SBC_D_B
SBC_D_C
SBC_D_D
SBC_D_IMM
SBC_D_DP

SBC_DP_A
SBC_DP_B
SBC_DP_C
SBC_DP_D
SBC_DP_IMM"""


template = """
sub {lhs_arg}, {rhs_arg} => asm{lbrace}
    sec
    sbc {lhs}, {rhs}
{rbrace}"""

braces = {"lbrace": "{", "rbrace": "}"}
# print(template.format(lhs="foo", rhs="foo", **braces))

gprs = {"a", "b", "c", "d"}
subs = []
for line in adcs.split():
    _, left, right = line.lower().split("_")

    lhs_arg = lhs = left
    rhs_arg = rhs = right

    if left not in gprs:
        lhs_arg = "[!{dp: u8}]"
        lhs = "[!dp]"

    if right not in gprs:
        if right == "imm":
            rhs_arg = "#{imm: i8}"
            rhs = "#imm"
        else:
            rhs_arg = "[!{dp: u8}]"
            rhs = "[!dp]"

    sub = template.format(lhs=lhs, lhs_arg=lhs_arg, rhs=rhs, rhs_arg=rhs_arg, **braces)
    subs.append(sub)


print("".join(subs))
