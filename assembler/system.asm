; contains bank definitions for the reference computer

#bankdef mmio {
    #addr 0x0000
    #size 256
    #outp 0x0000 * 8
    #fill
}

#bankdef rom {
    #addr 0x0100
    #size (32 * 1024) - 256
    #outp 0x0100 * 8
    #fill
}

IO_PIC = 0x00
IO_MMU = 0x01
IO_UART = 0x02
IO_SPI = 0x03
IO_VDP = 0x04
IO_PSG = 0x05
IO_DMA = 0x07
IO_KEY = 0x08
IO_DEV10 = 0x09
IO_DEV11 = 0x0A
IO_DEV12 = 0x0B
IO_DEV13 = 0x0C
IO_DEV14 = 0x0D
IO_DEV15 = 0x0E
IO_DEV16 = 0x0F