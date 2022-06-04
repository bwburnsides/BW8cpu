#include "bw8cpu.asm"
#include "system.asm"

#bank rom

; This code is loaded into the ROM chip which is copied into RAM at system reset-time
; The full ROM image is 32KB. 12KB of that are graphics assets (8KB system bitmaps, 4KB palettes)
; And the remaining 20KB is afforded to code which implements a system monitor, and IO
; rountines required to load extra code and data from an external device.

; This is the bootloader entry point and the first code that the CPU will run upon startup.
boot:
    ; First, configure the memory map of the CPU. Going to allocate the second 32KB of RAM
    ; to the bootloader / kernel. Going to go ahead and map them in, though don't have a use
    ; at the moment.
    ; Pages 0 - 7 are fixed and owned by kernel
    ; Pages 8 - 15 are not fixed and are additionally owned by the kernel
    out <MMU_PAGE8>, #8
    out <MMU_PAGE9>, #9
    out <MMU_PAGE10>, #10
    out <MMU_PAGE11>, #11
    out <MMU_PAGE12>, #12
    out <MMU_PAGE13>, #13
    out <MMU_PAGE14>, #14
    out <MMU_PAGE15>, #15

    ; Kernel stack will live in Page 8, mapped into Frame 0. Stack grows downwards,
    ; so needs to be set to the high address of Frame 0.
    ; SP is special purpose so can't be loaded directly, load via X.
    load x, #(0x8000 + (4 * 1024))
    mov sp, x

    jsr init_vram

    brk


init_vram:
    jsr init_bitmap0
    jsr init_palettes
    jmp init_bitmap1_tilemap


init_bitmap0:
    load a, #vblob_bitmaps[15:8]
    load b, #vblob_bitmaps[7:0]

    out <DMA_SRC_HI>, #0x00
    out <DMA_SRC_MI>, a
    out <DMA_SRC_LO>, b

    out <DMA_LEN_HI>, #(8 * 1024)[23:16]
    out <DMA_LEN_MI>, #(8 * 1024)[15:8]
    out <DMA_LEN_LO>, #(8 * 1024)[7:0]

    out <DMA_DST_HI>, #VRAM_BITMAP0[23:16]
    out <DMA_DST_MI>, #VRAM_BITMAP0[15:8]
    out <DMA_DST_LO>, #VRAM_BITMAP0[7:0]

    rts


init_palettes:
    load a, #vblob_palettes[15:8]
    load b, #vblob_palettes[7:0]

    out <DMA_SRC_HI>, #0x00
    out <DMA_SRC_MI>, a
    out <DMA_SRC_LO>, b

    out <DMA_LEN_HI>, #(4 * 1024)[23:16]
    out <DMA_LEN_MI>, #(4 * 1024)[15:8]
    out <DMA_LEN_LO>, #(4 * 1024)[7:0]

    out <DMA_DST_HI>, #VRAM_PALETTE[23:16]
    out <DMA_DST_MI>, #VRAM_PALETTE[15:8]
    out <DMA_DST_LO>, #VRAM_PALETTE[7:0]

    rts


init_bitmap1_tilemap:
    ; This subroutine is a bit different than the previous two because instead of
    ; transferring a block of data from one place to another, it needs to zero out
    ; a large region of memory. This is basically a memset. We can do this quickly
    ; using the DMA controller too, by making the src and dst windows overlap. If
    ; we write a zero to src, then set src to it, and set dst to src + 1, then that
    ; zero will be written from src to src + len.

    in a, <MMU_PAGE8>
    out <MMU_PAGE8>, #250

    load b, #0x00
    store b, [0x8000]

    out <MMU_PAGE8>, a

    out <DMA_SRC_HI>, #VRAM_BITMAP1[23:16]
    out <DMA_SRC_MI>, #VRAM_BITMAP1[15:8]
    out <DMA_SRC_LO>, #VRAM_BITMAP1[7:0]

    out <DMA_DST_HI>, #(VRAM_BITMAP1 + 1)[23:16]
    out <DMA_DST_MI>, #(VRAM_BITMAP1 + 1)[15: 8]
    out <DMA_DST_LO>, #(VRAM_BITMAP1 + 1)[7:0]

    out <DMA_LEN_HI>, #0x00
    out <DMA_LEN_MI>, #0x40
    out <DMA_LEN_LO>, #0x00

    rts

vblob:
    #d8 incbin("vblob.bin")
vblob_bitmaps = vblob
vblob_palettes = vblob + (8 * 1024)

; Bitmaps 0 - 248, 249
; Bitmaps 1 - 250, 251
; Tile Map  - 252, 253
; Palettes  - 254
