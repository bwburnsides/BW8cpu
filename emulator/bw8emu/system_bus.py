import os
from abc import ABC, abstractmethod


class ISystemBus(ABC):
    @property
    @abstractmethod
    def read(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def write(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def memory(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def io(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def user(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def supervisor(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def code(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def rising(self):
        raise NotImplementedError

    @abstractmethod
    def falling(self):
        raise NotImplementedError


class SystemBus(ISystemBus):
    def __init__(self, rom_path: os.PathLike):
        self.ram = [0 for _ in range(1024 ** 2)]

        with open(rom_path, "rb") as f:
            idx = 0
            while (byte := f.read(1)):
                self.ram[idx] = int.from_bytes(byte, "big")
                idx += 1

        # Initialize bus values to reasonable defaults
        self.data_bus = 0x00
        self.addr_bus = 0x00000
        self.read = True
        self.memory = True
        self.supervisor = True
        self.code = True

    def rising(self):
        if self.read:
            if self.memory:
                self.memory_read()
            else:
                self.io_read()

    def falling(self):
        if self.write:
            if self.memory:
                self.memory_write()
            else:
                self.io_write()

    def memory_read(self):
        self.data_bus = self.ram[self.addr_bus]

    def memory_write(self):
        self.ram[self.addr_bus] = self.data_bus

    def io_read(self):
        pass

    def io_write(self):
        pass

    @property
    def read(self) -> bool:
        return self._read

    @read.setter
    def read(self, state: bool) -> None:
        self._read = state
        self._write = not state

    @property
    def write(self) -> bool:
        return self._write

    @write.setter
    def write(self, state: bool) -> None:
        self._write = state
        self._read = not state

    @property
    def memory(self) -> bool:
        return self._memory

    @memory.setter
    def memory(self, state: bool) -> None:
        self._memory = state
        self._io = not state

    @property
    def io(self) -> bool:
        return self._io

    @io.setter
    def io(self, state: bool) -> None:
        self._io = state
        self._memory = not state

    @property
    def user(self) -> bool:
        return self._user

    @user.setter
    def user(self, state: bool) -> None:
        self._user = state
        self._supervisor = not state

    @property
    def supervisor(self) -> bool:
        return self._supervisor

    @supervisor.setter
    def supervisor(self, state: bool) -> bool:
        self._supervisor = state
        self._user = not state

    @property
    def data(self) -> bool:
        return self._data

    @data.setter
    def data(self, state: bool) -> None:
        self._data = state
        self._code = not state

    @property
    def code(self) -> bool:
        return self._code

    @code.setter
    def code(self, state: bool) -> None:
        self._code = state
        self._data = not state


if __name__ == "__main__":
    sysbus = SystemBus()
