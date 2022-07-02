import pytest

from .emulator import Emulator
from .simulator import Simulator

# VirtualMachine = None

# def pytest_addoption(parser):
#     parser.addoption(
#         "--vm",
#         action="store",
#         # default="sim",
#         help="my option: sim or emu"
#     )


# @pytest.fixture(autouse=True, scope="module")
# def virtual_machine(request):
#     vm = request.config.getoption("--vm").strip()
#     print(vm)
#     if vm == "sim":
#         VirtualMachine = Simulator
#     elif vm == "emu":
#         VirtualMachine = Emulator
#     else:
#         assert False
