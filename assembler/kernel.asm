#include "system.asm"

KERNEL_STACK_BASE = 0xBFFF
CTX_PAGE = 0xCF
CTX_ACTIVE = 0
CTX_A = 1
CTX_B = 2
CTX_C = 3
CTX_D = 4
CTX_X = 5
CTX_Y = 7
CTX_SP = 9
KERNEL_CTX = 0

SWAP_A = 0
SWAP_B = 1
SWAP_C = 2
SWAP_D = 3
SWAP_X = 4
SWAP_Y = 6

vector_table:
    jmp rst_handler
    jmp irq_handler
    jmp nmi_handler

rst_handler:
    
nmi_handler:
    rti

irq_handler:
    ; write the original register values to the Direct Page for safe keeping
    store [!SWAP_A], a
    store [!SWAP_B], b
    store [!SWAP_X], x

    ; compute pointer to userspace’s context struct
    mov a, br
    mov b, a
    load a, #CTX_PAGE
    mov x, ab

    ; store unmolested values to Ctx struct
    store [x, #CTX_Y], y
    store [x, #CTX_C], c
    store [x, #CTX_D], d

    ; retrieve unmolested values and then write to Ctx struct
    load a, [!SWAP_A]
    load b, [!SWAP_B]
    load y, [!SWAP_X]

    store [x, #CTX_A], a
    store [x, #CTX_B], b
    store [x, #CTX_X], y

    mov y, x
    mov x, sp

    ; finally save user stack pointer
    store [y, #CTX_SP], x

    load b, #KERNEL_CTX
    load a, #CTX_PAGE
    mov y, ab

    ; only after this point can the kernel start using the stack
    load x, [y, #CTX_SP]
    mov sp, x

    in a, <IRQ_SOURCE>
    clc

    src a
    jc swi_handler
    src a
    jc vsync_handler
    src a
    jc scanline_handler
    src a
    jc uart_handler
    src a
    jc spi_handler
    src a
    jc ps2_handler
    src a
    jc timer_handler
    src a
    jc port_handler

    pop a
    rti

vsync_handler:
scanline_handler:
uart_handler:
spi_handler:
ps2_handler:
timer_handler:
port_handler:
    brk

swi_handler:
    ; Pre state: register values irrelevant
    ; Post State: all registers are equivalent to returning context
    ;             except for `A` which contains the return value

    ; `A` contains the syscall number, so load the vector into `X`
    cmp a, #(syscall_table_end - syscall_table)
    jg .invalid_syscall

    load x, #syscall_table
    lea x, a

    ; Perform the syscall
    jsr x
    ; State: `A` contains the return value. All other registers equivalent
    ; to state at call time
    ; this is irrelevant because they'll be loaded from stack now.

    .invalid_syscall:
        jsr restore_context
        rti

syscall_table:
    #d16 sys_yield
    #d16 sys_exit
    #d16 sys_kill
    #d16 sys_fork
    #d16 sys_exec
    #d16 sys_open
    #d16 sys_close
    #d16 sys_read
    #d16 sys_write
syscall_table_end:

sys_yield:
sys_exit:
sys_kill:
sys_fork:
    ; fork requires two main things to happen
    ; 1. a context duplication
    ;   - starting from 0, loop to 15 to find a free context
    ; 2. an addr space copy

    load a, #CTX_PAGE
    load b, #0

    .loop_body:
        mov x, ab
        load c, [x, #CTX_ACTIVE]

        ; if the context is not active, then we have found our target
        cmp c, #FALSE
        jne .found_context

        ; otherwise, increment the pointer and try again
        inc b
        cmp b, #0   ; if b is zero, then we've exhausted all options
        jne .loop_body

    .none_avail:
        ; if this happens, then the fork request needs to be added to a queue and serviced
        ; next time there is an available context slot. the calling process also has be suspended
        ; until the request is fulfilled.
        brk

    .found_context:
        ; now that context is found, copy from the parent context to this
        ; new child just going to use DMA controller to prevent lots of register
        ; spilling.

        mov a, br

        out <DMA_SRC_BR>, a
        out <DMA_SRC_HI>, #CTX_PAGE
        out <DMA_SRC_LO>, a

        out <DMA_DST_BR>, b
        out <DMA_DST_HI>, #CTX_PAGE
        out <DMA_DST_LO>, b

        out <DMA_LEN_HI>, #0x0
        out <DMA_LEN_LO>, #0xF

        ; next, the address space needs to be copied. going to do this with the
        ; DMA controller again.
        out <DMA_SRC_BR>, a
        out <DMA_SRC_HI>, #0x00
        out <DMA_SRC_LO>, #0x00

        out <DMA_DST_BR>, b
        out <DMA_DST_HI>, #0x00
        out <DMA_DST_LO>, #0x00

        out <DMA_LEN_HI>, #0xFF
        out <DMA_LEN_LO>, #0xFF

sys_exec:
sys_open:
sys_close:
sys_read:
sys_write:
    brk

restore_context:
    mov a, br
    mov b, a
    load a, #CTX_PAGE
    mov y, ab

    load a, [y, #CTX_A]
    load b, [y, #CTX_B]
    load c, [y, #CTX_C]
    load d, [y, #CTX_D]

    load x, [y, #CTX_SP]
    mov sp, x

    load x, [y, #CTX_X]
    load y, [y, #CTX_Y]

    rts
