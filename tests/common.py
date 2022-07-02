import dataclasses
import contextlib
import functools

from . import opcodes

@dataclasses.dataclass
class CoreDump:
    pc: int
    sp: int
    x: int
    y: int
    a: int
    b: int
    c: int
    d: int
    nmi_f: bool
    ubr_f: bool
    us_f: bool
    c_f: bool
    z_f: bool
    v_f: bool
    n_f: bool
    i_f: bool

NoneDump = CoreDump(*(None for _ in range(16)))
OPCODES = list(opcodes.Op)


def under_test(*opcodes):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)

            with contextlib.suppress(ValueError):
                for opcode in opcodes:
                    OPCODES.remove(opcode)

            return result

        return wrapper

    return decorator