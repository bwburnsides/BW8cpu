#include "bw8pic.h"

namespace BW8 {
    namespace pic {
        void set_interrupt(BW8pic* pic, uint8_t idx, bool state) {
            pic->interrupts[idx] = state;
        }
    }
}