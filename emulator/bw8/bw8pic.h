#pragma once

#include "bw8cpu.h"

namespace BW8 {
    namespace pic {
        typedef struct BW8pic {
            bool interrupts[8];
        } BW8pic;

        void set_interrupt(BW8pic* pic, uint8_t idx, bool state);
    }
}