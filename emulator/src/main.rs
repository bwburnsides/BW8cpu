use std::cell::RefCell;
use std::rc::Rc;

struct Memory;
type MemoryRef = Rc<RefCell<Memory>>;

const MICROCODE: &[u8] = include_bytes!("main.rs");

#[derive(Debug)]
struct BW8cpu {
    // General Purpose Registers
    a: u8,
    b: u8,
    c: u8,
    d: u8,

    // Implementation
    dp: u8,
    t1: u8,
    t2: u8,

    // Constants
    dp_init: u8,
    sp_init: u16,
    rst_veclo: u16,
    isr_veclo: u16,

    // Indexes
    x: u16,
    y: u16,

    // Special Purpose
    sp: u16,
    pc: u16,
    ir: u8,
    sr: u8,

    ctrl_latch: u32,
    tstate: u8,  // uses only 3 bits
    irq: bool,   // uses only 1 bit
    mode: u8,    // uses only 2 bits
    rw: bool,    // uses only 1 bit

    clocks: u128,
}

impl BW8cpu {
    fn new() -> BW8cpu {
        BW8cpu {
            a: 0,
            b: 0,
            c: 0,
            d: 0,

            dp: 0,
            temp1: 0,
            temp2: 0,

            rst_veclo: 0x1FFE,
            isr_veclo: 0x2000,

            x: 0,
            y: 0,
            pc: 0,
            sp: 0,

            ir: 0,
            sr: 0,

            ctrl_latch: 0,
            tstate: 0,
            irq: false,
            mode: 0,
            rw: false,

            clocks: 0,
        }
    }

    fn clock(&self) {
    }
}

fn main() {
    let cpu = BW8cpu::new();
    println!("Hello, world!");
}
