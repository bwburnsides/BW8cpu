""" The Logisim 7-segment display is laid out as shown below. I have assigned the
marked bit order to the 8 terminals denoted by asterisks:

0 1 2 3
* * * *
  __
 |__|
 |__|.
* * * *
7 6 5 4

The constants ZERO...NINE below represent the bit pattern representing each digits
in the standard 7-Segment manner with this bit order. The produced ROM maps 8 bit
addresses corresponding to the decimal values 0-255 to 24 bit values that represent
3 of the digit bit patterns. As such, three 7-segment display modules can be driven
via the output.

In order to simplify wiring, The 24 bit output will be split into 12 bit segments,
where the lower 12 bits drive the 0-3 inputs and the upper 12 bits drive the 4-7 inputs.
This is shown below, where a, b, c correspond to the ones, tens, and hundreds places
displays, respectively.

Output Bits: 11 10 09 08 | 07 06 05 04 | 03 02 01 00
Display Pin: 0c 1c 2c 3c | 0b 1b 2b 3b | 0a 1a 2a 3a

Output Bits: 23 22 21 20 | 19 18 17 16 | 15 14 13 12
Display Pin: 7c 6c 5c 4c | 7b 6b 5b 4b | 7a 6a 5a 4a

This gives the following bit order:

Hundreds 0-3 Reversed : Tens 0-3 Reversed : Ones 0-3 Reversed : Hundreds 4-7 : Tens 4-7 : Ones 4-7

This script produces a file, "segment_rom.bin" in the working dir that is a Logisim-compatible
ROM image file. As such, the expected usage is with a 8-bit address, 24-bit word ROM,
where the output is split and sent to three 7-segment display modules.
"""

NULL = "00000000"
ZERO = "01110111"
ONE = "01000001"
TWO = "00111011"
THREE = "01101011"
FOUR = "01001101"
FIVE = "01101110"
SIX = "01111110"
SEVEN = "01000011"
EIGHT = "01111111"
NINE = "01001111"

digits = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]

with open("segment_rom.bin", "w") as rom_file:
    rom_file.write("v2.0 raw\n")
    for value in range(256):
        ones = digits[(value // 1) % 10]
        tens = digits[(value // 10) % 10]
        hundreds = digits[(value // 100) % 10]

        if value < 100:
            hundreds = NULL
            if value < 10:
                tens = NULL

        bit_order = (
            f"{''.join(list(reversed(hundreds[:4])))}"
            f"{''.join(list(reversed(tens[:4])))}"
            f"{''.join(list(reversed(ones[:4])))}"
            f"{hundreds[4:]}{tens[4:]}{ones[4:]}"
        )

        rom_file.write(str(hex(int(bit_order, 2)))[2:])
        rom_file.write("\n")
