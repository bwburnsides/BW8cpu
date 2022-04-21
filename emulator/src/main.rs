use rand::Rng;

#[derive(Debug)]
struct BW8cpu {
    // GPRs
    a: u8,
    b: u8,
    c: u8,
    d: u8,

    // GPPs
    x: u16,
    y: u16,

    // Special Purpose
    dp: u8,
    sp: u16,

    // Implementation
    pc: u16,
    ir: u8,
    t1: u8,
    t2: u8,
    sr: u8,

    // Buses
    dbus: u8,
    mbus: u8,
    xbus: u16,
    abus: u16,

    // Constants
    dp_init: u8,
    sp_init: u16,
    rst_vechi: u16,
    isr_vechi: u16,

    // State Management
    ctrl_latch: u32,
    tstate: u8,
    irq: bool,
    rst_latched: bool,
    ext: bool,
    rw: bool,

    clocks: u128,
}

impl BW8cpu {
    fn new<R: Rng>(rng: &mut R) -> BW8cpu {
        BW8cpu {
            a: rng.gen(),
            b: rng.gen(),
            c: rng.gen(),
            d: rng.gen(),
            x: rng.gen(),
            y: rng.gen(),
            dp: rng.gen(),
            sp: rng.gen(),
            pc: rng.gen(),
            ir: rng.gen(),
            t1: rng.gen(),
            t2: rng.gen(),
            sr: rng.gen(),

            dbus: 0,
            mbus: 0,
            xbus: 0,
            abus: 0,

            // Hardcoded constants
            dp_init: 0x00,
            sp_init: 0x00,
            rst_vechi: 0x1FFE,
            isr_vechi: 0x2000,

            ctrl_latch: rng.gen(),
            tstate: rng.gen(),
            irq: false,             // pull up resistor
            rst_latched: false,
            ext: rng.gen(),
            rw: true,               // pull up resistor
            clocks: 0,
        }
    }

    fn reset(&mut self) {
        self.a = 0;
        self.b = 0;
        self.c = 0;
        self.d = 0;
        self.x = 0;
        self.y = 0;
        self.dp = 0;
        self.sp = 0;
        self.pc = 0;
        self.ir = 0;
        self.t1 = 0;
        self.t2 = 0;
        self.sr = 0;

        self.ctrl_latch = 0;
        self.tstate = 0;
        self.rst_latched = true;
        self.ext = false;
    }

    fn rising(&mut self) {

    }

    fn falling(&mut self) {

    }
}

fn main() {
    let mut cpu = BW8cpu::new(&mut rand::thread_rng());
    cpu.reset();
    cpu.rising();
    cpu.falling();
    println!("{:#?}", cpu);
}
