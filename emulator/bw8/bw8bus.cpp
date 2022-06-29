#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include "bw8bus.h"

#define RED_TEXT "\033[0;31m"
#define GREEN_TEXT "\033[0;32m"
#define RESET_TEXT "\033[0m"
#define STATE_FORMAT "\033[0;0H"\
"+----------------------------------------------------+\n"\
"| BW8cpu Emulator                          June 2022 |\n"\
"| Clock Cycles: %-20lld       Tstate: %1d |\n"\
"+----------------------------------------------------+\n"\
"| Status: %sC %sZ %sV %sN %sI %sS %sU %sE  %sRST %sREQ %sNMI %sIRQ\033[0m   %6s  |\n"\
"| DBUS:  $%02X  ADDR: $%04X  XFER: $%04X  AOUT: $%04X  |\n"\
"| PC:  $%04X   SP:  $%04X    X:  $%04X    Y:  $%04X  |\n"\
"| A:     $%02X    B:    $%02X    C:    $%02X    D:    $%02X  |\n"\
"| DP:    $%02X   DA:    $%02X   TH:    $%02X   TL:    $%02X  |\n"\
"| BR:     $%01X   OF:    $%02X   IR:    $%02X               |\n"\
"+----------------------------------------------------+\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"| %-50s |\n"\
"+----------------------------------------------------+\n"

namespace BW8 {

    const char* _bool_colored(bool flag);
    const char* _mode_repr(CPU::Mode mode);

    Bus::Bus(const char* rom_path) {
        FILE* fp;
        size_t num_bytes;

        fp = fopen(rom_path, "rb");
        if (fp == NULL) {
            fprintf(stderr, "Error BW8::Bus constructor: Could not read ROM for CPU.\n");
            exit(-1);
        }

        memory = (uint8_t*)calloc(ADDR_SPACE_SIZE, sizeof(uint8_t));
        if (memory == NULL) {
            fprintf(stderr, "Error BW8::Bus constructor: Could not initiaize memory.\n");
        }

        num_bytes = fread(memory, sizeof(uint8_t), ROM_SIZE, fp);
        fclose(fp);

        for (int i = 0; i < 8; i++) {
            irq_sources[i] = false;
        }

        cpu = new CPU(this);
        uart = new UART(this);

        for (int i = 0; i < 15; i++) {
            for (int j = 0; j < 51; j++) {
                terminal[i][j] = '\0';
            }
        }

        cursor = {
            0, 0
        };
    }

    Bus::~Bus() {
        free(memory);
        delete cpu;
        delete uart;
    }

    void Bus::clock() {
        cpu->rising();
        uart->rising();

        cpu->falling();
        uart->falling();

        uint8_t data;
        for (int i = 0; i < uart->tx_count(); i++) {
            data = uart->dequeue_tx();
            if (data != '\n') {
                terminal[cursor.row % 17][cursor.col % 50] = data;
                cursor.col++;
                if (cursor.col > 49) {
                    cursor.col = 0;
                    cursor.row++;
                    cursor.row %= 17;
                }
            }
            if (data == '\n') {
                cursor.row++;
                cursor.col = 0;
            }

            cursor.row %= 17;
            cursor.col %= 50;
        }
    }

    void Bus::rst(bool state) {
        cpu->rst(state);
        uart->rst(state);
    }

    bool Bus::hlt() {
        return cpu->hlt();
    }

    void Bus::coredump() {
        cpu->coredump();
    }

    void Bus::interrupt(uint8_t index, bool state){
        irq_sources[index % 8] = state;
        for (int i = 0; i < 8; i++) {
            if (irq_sources[i]) {
                cpu->irq(true);
                return;
            }
        }
        cpu->irq(false);
    };

    void Bus::dump(FILE *stream) {
        fprintf(
            stream,
            STATE_FORMAT,
            cpu->clocks,
            cpu->tstate,
            _bool_colored(cpu->status_flags.Cf),
            _bool_colored(cpu->status_flags.Zf),
            _bool_colored(cpu->status_flags.Vf),
            _bool_colored(cpu->status_flags.Nf),
            _bool_colored(cpu->status_flags.If),
            _bool_colored(cpu->status_flags.sup),
            _bool_colored(cpu->status_flags.ubr),
            _bool_colored(cpu->status_flags.ext),
            _bool_colored(cpu->interrupts.rst),
            _bool_colored(cpu->interrupts.req),
            _bool_colored(cpu->interrupts.nmi),
            _bool_colored(cpu->interrupts.irq),
            _mode_repr(cpu->mode),
            cpu->dbus, cpu->addr, cpu->xfer, cpu->addr_out,
            cpu->PC, cpu->SP, cpu->X, cpu->Y,
            cpu->A, cpu->B, cpu->C, cpu->D,
            cpu->DP, cpu->DA, cpu->TH, cpu->TL,
            cpu->BR, cpu->OF, cpu->IR,
            terminal[0],
            terminal[1],
            terminal[2],
            terminal[3],
            terminal[4],
            terminal[5],
            terminal[6],
            terminal[7],
            terminal[8],
            terminal[9],
            terminal[10],
            terminal[11],
            terminal[12],
            terminal[13],
            terminal[14]
        );
    }

    uint8_t Bus::read(uint8_t bank, uint16_t ptr, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        uint8_t port = addr & 0xff;

        if (mem_io) {
            return memory[addr];
        } else {
            return io(port, 0x00, true, super_user);
        }
    }

    void Bus::write(uint8_t bank, uint16_t ptr, uint8_t data, bool mem_io, bool super_user, bool data_code) {
        uint32_t addr = ((bank & 0xf) << 16) | ptr;
        uint8_t port = addr & 0xff;

        if (mem_io) {
            memory[addr] = data;
        } else {
            io(port, data, false, super_user);
        }
    }

    uint8_t Bus::io(uint8_t port, uint8_t data_in, bool read_write, bool super_user) {
        uint8_t data_out = 0x00;
        uint8_t dev = (port >> 4) & 0xF;
        switch (Device(dev)) {
            case Device::CLK:
                break;
            case Device::IRQ:
                break;
            case Device::DMA:
                break;
            case Device::UART:
                return uart->port(port, data_in, read_write, super_user);
            default:
                break;
        }
        return data_out;
    }

    const char* _bool_colored(bool flag) {
        return flag ? GREEN_TEXT : RED_TEXT;
    }

    const char* _mode_repr(CPU::Mode mode) {
        switch (mode) {
            case CPU::Mode::STALL:
                return "MEMREQ";
            case CPU::Mode::IRQ:
                return "IRQACK";
            case CPU::Mode::NMI:
                return "NMIACK";
            case CPU::Mode::FETCH:
                return "NORMAL";
        }
    }
}