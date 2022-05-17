; This code is loaded into the ROM chip which is copied into RAM at system reset-time
; The full ROM image is 32KB. 12KB of that are graphics assets (8KB system bitmaps, 4KB palettes)
; And the remaining 20KB is afforded to code which implements a system monitor, and file IO
; rountines required to load extra code and data from an external device.

; Initialize VRAM by copying in the binary data included in the boot image
vram_init:
    .NLOCALS = 0
    push c
    push d
    push x
    mov x, sp
    lea sp, #-.NLOCALS

    load a, #vblob_start[15:8]
    load b, #vblob_start[7:0]

    store a, [DMA_SRC_HI]
    store b, [DMA_SRC_LO]

    vblob_length = (vblob_start - vblob_end)`16
    load a, #vblob_length[15:8]
    load b, #vblob_length[7:0]

    mov sp, x
    pop x
    pop d
    pop c
    rts

; Perform a block memory copy via the DMA controller.
; Memory map must be preconfigured to necessary state.
; Arguments:
;   - AB: Pointer to the destination block
;   - Y: Pointer to the source block
;   - FP-1:  
;   - FP-2:
; Returns:
;   None
dma_copy:
    store a, [DMA_LEN_HI]
    store b, [DMA_LEN_LO]
    store y, [DMA_SRC_HI]
    rts
