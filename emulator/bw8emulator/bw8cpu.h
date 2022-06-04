#pragma once
#include <stdint.h>
#include <array>
#include <string>
#include <vector>

enum GeneralPurposeReg {A, B, C, D};
enum AddressReg {PC, SP, X, Y};
enum InternalReg {DP, DA, TH, TL, IR, SR, OF};
enum Flags {Cf, Zf, Vf, Nf, If, Ef, Kf, Uf};
enum Mode {FETCH, STALL, IRQ, NMI};

class BW8cpu {
public:
	BW8cpu();
	void reset();
	void interrupt_request();
	void nonmaskable_interrupt();
	void memory_request();
	void rising();
	void falling();

private:
	static uint16_t irq_vector;
	static uint16_t nmi_vector;

	std::vector<uint32_t> microcode;
	std::array<uint8_t, 4> general_purpose_reg;
	std::array<uint16_t, 4> address_reg;
	std::array<uint8_t, 7> internal_reg;

	uint8_t sequencer;

	bool irq;
	bool nmi;
 	bool req;
	bool rw;
	bool mi;
	bool ext;

	uint8_t dbus;
	uint16_t xfer;
	uint16_t addr;

	Mode get_mode(); 
	void read_microcode();
};