from .cpu import BW8cpu
from .system_bus import SystemBus


class Computer:
    def __init__(self, cpu: BW8cpu, bus: SystemBus):
        self.cpu = cpu
        self.bus = bus

    def rising(self):
        self.bus.rising()
        self.cpu.rising()

    def falling(self):
        self.cpu.falling()
        self.bus.falling()

    def clock(self):
        self.rising()
        self.falling()