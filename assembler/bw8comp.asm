; contains bank definitions for the reference computer

#bankdef shadow_rom {
    #addr 0x0000
    #size 8 * 1024
    #outp 0x0000 * 8
    #fill
}

#bankdef mmio {
    #addr 0x2000
    #size 256
}

RST_VECTOR = 0x1FFE
PIC_ISR_VECTOR = 0x2000
PIC_IRQ_MASK_ADDR = 0x2002
PIC_ISR_0_ADDR = 0x2003
PIC_ISR_1_ADDR = 0x2005
PIC_ISR_2_ADDR = 0x2006
PIC_ISR_3_ADDR = 0x2008