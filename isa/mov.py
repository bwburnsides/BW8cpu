from dataclasses import dataclass
import functools as ft
import itertools as it
from typing import Iterable, Sequence
from shared import Opcode, Units


from pprint import pprint


def mov_8bit():
    codes = []

    gprs = Units.AREG, Units.BREG, Units.CREG

    for src, dest in it.permutations(gprs, r=2):
        codes.append(Opcode(f"MOV {src.name} {dest.name}"))

    one_ways = Units.ACC, Units.SP, Units.SR
    for src in one_ways:
        for dest in gprs:
            codes.append(Opcode(f"MOV {src.name} {src.name}"))

    return codes


def mov_16bit():
    codes = []

    gprs = Units.XREG, Units.YREG, Units.PC

    for src, dest in it.permutations(gprs, r=2):
        codes.append(Opcode(f"MOV {src.name} {dest.name}"))

    for dest in gprs:
        codes.append(Opcode(f"MOV {Units.SP.name} {dest.name}"))

    return codes


def mov_8to16():
    srcs = Units.AREG, Units.BREG, Units.CREG, Units.ACC, Units.IMM, Units.SR
    dests = Units.PCL, Units.PCH, Units.XLREG, Units.XHREG, Units.YLREG, Units.YHREG

    codes = []
    for src in srcs:
        for dest in dests:
            codes.append(Opcode(f"MOV {src.name} {dest.name}"))

    return codes


def mov_16to8():
    srcs = Units.PCL, Units.PCH, Units.XLREG, Units.XHREG, Units.YLREG, Units.YHREG
    dests = Units.AREG, Units.BREG, Units.CREG

    codes = []
    for src in srcs:
        for dest in dests:
            codes.append(Opcode(f"MOV {src.name} {dest.name}"))

    return codes


def mov_mixedbit():
    return (
        *mov_8to16(),
        *mov_16to8(),
    )


def mov_opcodes():
    return (
        *mov_8bit(),
        *mov_16bit(),
        *mov_mixedbit(),
    )
