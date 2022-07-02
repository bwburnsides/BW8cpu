#include "bw8cpu.asm"

#bankdef rom {
    #addr 0x0000
    #size 0x8000
    #outp 0
    #fill
}

#bankdef ram {
    #addr 0x8000
    #size 0x8000
}

#ruledef testing_opcodes {
    musteq a, #{imm: i8} => opcode(OP_MUSTEQ_A_IMM) @ imm
    musteq b, #{imm: i8} => opcode(OP_MUSTEQ_B_IMM) @ imm
    musteq c, #{imm: i8} => opcode(OP_MUSTEQ_C_IMM) @ imm
    musteq d, #{imm: i8} => opcode(OP_MUSTEQ_D_IMM) @ imm
}

#bank rom

jmp.abs rst
jmp.abs irq
jmp.abs nmi

nmi:
irq:
    rti

rst:
    load a, #0b00100001
    push a
    load x, #usr
    push x
    load a, #0
    load x, #0
    rti

usr:
    load a, #0
    load x, #data_rom
    load y, #data_ram

    .loop_ctrl:
        cmp a, #7
        jg .done

    .loop_body:
        load b, [x, a]
        store [y, a], b

        inc a
        jmp .loop_ctrl

    .done:

        load a, #7
        load x, #data_ram
        jsr bubble_sort
        ..spin:
            jmp ..spin

    data_rom:
        #d8 5, 8, 2, 1, 10, 4, 3

; Arguments
; A - number of elements in array
; X - pointer to array start
bubble_sort:
; void bubbleSort(int arr[], int n)
; {
;     int i, j;
;     for (i = 0; i < n - 1; i++)
 
;         for (j = 0; j < n - i - 1; j++)
;             if (arr[j] > arr[j + 1])
;                 swap(&arr[j], &arr[j + 1]);
; }
    push c
    push d
    ; A -> n - 1
    ; B -> i
    ; C -> n - 1 - i
    ; D -> j
    outer_loop_setup:
        dec a
        load b, #0
    outer_loop_ctrl:
        cmp b, a
        jl outer_loop_end
    outer_loop_body:
        inner_loop_setup:
            load d, #0
        inner_loop_ctrl:
            mov c, a
            sub c, #1
            cmp d, c
            jl inner_loop_end
        inner_loop_body:
            push a
            push b
            push c
            push d

            load a, [x, d]
            inc d
            load b, [x, d]
            cmp a, b
            jle no_swap
            store [x, d], a
            dec d
            store [x, d], b
            no_swap:
                pop d
                pop c
                pop b
                pop a

            inc d
            jmp inner_loop_ctrl
        inner_loop_end:
            inc b
            jmp outer_loop_ctrl
    outer_loop_end:
        pop d
        pop c
        rts


#bank ram
data_ram:
    #res 7
