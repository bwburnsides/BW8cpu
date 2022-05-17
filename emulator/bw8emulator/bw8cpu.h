#pragma once
#include <stdint.h>
#include <array>
#include <string>
#include <vector>

enum GeneralPurposeReg {A, B, C, D};
enum AddressReg {PC, SP, X, Y};
enum InternalReg {DP, DA, TH, TL, IR, SR, OF};

class BW8cpu {
public:
	BW8cpu(const char* microcode_path);
	void reset();
	void rising();
	void falling();

private:
	static uint8_t dp_initial;
	static uint16_t sp_initial;
	static uint16_t rst_vec_hi;
	static uint16_t irq_vec_hi;

	std::vector<uint32_t> microcode(512 * 1024);
	std::array<uint8_t, 4> general_purpose_reg;
	std::array<uint16_t, 4> address_reg;
	std::array<uint8_t, 7> internal_reg;

	bool rst;
	bool irq;
	uint8_t sequencer;

	bool req;
	bool rw;
	bool mi;

	uint8_t dbus;
	uint16_t xfer;
	uint16_t addr;

	void read_microcode(const char* microcode_path);
};