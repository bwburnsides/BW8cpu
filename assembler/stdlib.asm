#include "bw8cpu.asm"

; Calling Conventions:
; Caller Saved Registers: A, B, Y
; Callee Saved Registers: C, D, X

; X is used as Frame Pointer
; A, B, and Y are used for function arguments
; Excess arguments are on the stack, directly below
; the Return Address

; Return Values are in A or AB.


; Adds two unsigned 16-bit numbers
; Arguments:
;   AB: 16-bit unsigned number, operand1
;   Y:  16-bit unsigned number, operand2
; Returns:
;   AB: 16-bit unsigned number, operand1 + operand2
uadd16:
    ; Prolouge
    push c
    push d
    ; No need for FP or locals

    mov cd, y

    clc
    adc b, d
    adc a, c

    ; Epilouge
    pop d
    pop c
    rts

; Subtracts two unsigned 16-bit numbres
; Arguments:
;   AB: 16-bit unsigned number, operand1
;   Y:  16-bit unsigned number, operand2
; Returns:
;   AB: 16-bit unsigned number, operand1 - operand2
usub16:
    ; Prolouge
    push c
    push d

    mov cd, y

    sec
    sbc b, d
    sbc a, c

    ; Epilouge
    pop d
    pop c
    rts

; Convert an ASCII HEX character to its corresponding
; numerical value
; eg, "0" -> 0b00000000, "1" -> "0b00000001", "F" -> 0b00001111
; Arguments:
;   A: 8-bit ASCII code. Must be "0"-"9" or "A"-"F"
; Returns:
;   A: 8-bit numerical value, or -1 if ASCII value was not valid
atoi8:
    ; If value is less than "0", then can't be 0-9 or A-F, so arg is invalid
    load b, #"0"
    cmp a, b
    jl .invalid_arg

    ; If value is greater than "F", then can't be 0-9 or A-F, so arg is invalid
    load b, #"F"
    cmp a, b
    jg .invalid_arg

    ; offset the value by the position of "0" if the value was decimal, then this
    ; is the value otherwise, its either alphabetical or invalid.
    sec
    sbc a, #"0"
    cmp a, #("9" - "0")
    jg .is_alpha
    jmp .return

    .is_alpha:
        cmp a, #("A" - "0")
        jl .invalid_arg
        cmp a, #("F" - "0")
        jg .invalid_arg

        sec
        sbc a, #"A"

        ; Value is now 0-5, corresponding to "A" to "F"
        ; and needs to be mapped into 10-15
        ; so add the value to 10 and return it

        load b, #10
        clc
        adc a, b
        jmp .return

    .invalid_arg:
        load a, #-1

    .return:
        rts

; Convert two ASCII HEX characters to its corresponding
; numerical value
; Arguments:
;   A: 8-bit ASCII HEX character. The high byte.
;   B: 8-bit ASCII HEX character. The low byte.
; Returns:
;   A: 8-bit numerical value representative of the ASCII input.
;   B: denote error code. 0 denotes success.
atoi16:
    ; Prolouge
    push c

    ; Move lower byte into A and compute
    ; lower nibble, then check for success
    push a
    mov a, b
    jsr atoi8
    cmp a, #-1
    je .invalid_args

    ; Move low nibble to B, retrieve higher byte
    ; from stack, and backup B (caller-saved register)
    ; check for success
    mov b, a
    pop a
    push b
    jsr atoi8
    cmp a, #-1
    je .invalid_args

    ; Now, high nibble is in low 4 bits of A. So shift left 4 bits
    load b, #4
    jsr shl_n

    ; Retrieve low nibble from stack, combine
    ; the nibbles by ANDing, denote success
    ; then return
    pop b
    and a, b
    load b, #0
    jmp .return

    .invalid_args:
        ; atoi8 put -1 in A for us, so just move
        ; that to B
        mov b, a

    .return:
        ; Epilouge
        pop c
        rts

; Given a byte, returns 2 ASCII characters that represent it
; in hexadecimal notation.
; Arguments:
;   A: the byte to convert.
; Returns:
;   A: the ASCII char representing the high nibble.
;   B: the ASCII char representing the low nibble.
itoa8:
    ; Prolouge
    push c
    push x

    ; backup input argument in B
    mov b, a

    ; clear out high 4 bits from the arg
    and a, #0b0000_1111

    ; Read the Ath element from the array into C. This is the high byte.
    load x, #.hex_array
    load c, [x, a]

    ; Restore argument from b, logically shift it right 4 bits
    mov a, b
    load b, #4
    jsr shr_n

    ; Read Ath element from array in B. This is the low byte.
    ; Also return high byte from C to A.
    load b, [x, a]
    mov a, c

    ; Epilouge
    pop x
    pop c
    rts

    .hex_array:
        #d "0123456789ABCDEF"


; Perform a left shift of the specified number of bits.
; Arguments:
;   A: the value to shift.
;   B: the number of bits to shift.
; Returns:
;   A: the shifted value.
shl_n:
    .loop_control:
        cmp b, #-1
        jg .loop_body
        jmp .loop_exit

    .loop_body:
        clc
        adc a, a

        dec b
        jmp .loop_control

    .loop_exit:
        rts

; Perform a logical right shift without carry of the specified number of bits.
; Arguments:
;   A: the value to shift.
;   B: the number of bits to shift.
; Returns:
;   A: the shifted value.
shr_n:
    .loop_control:
        cmp b, #-1
        jg .loop_body
        jmp .loop_exit

    .loop_body:
        clc
        src a

        dec b
        jmp .loop_control

    .loop_exit:
        rts

; Perform a logical shift right without carry of the specified number of bits.
; Arguments:
;   A: the value to shift.
;   B: the number of bits to shift
; Returns:
;   A: the shifted value.
shr_n_optimized:
    ; Mask the top 5 bits so that B between 0 and 7
    and b, #0b0000_0111

    ; Offset into the table should be 2 x B since the label table has 16 bit words
    ; (I think.. should that table label be aligned?)
    clc
    adc b, b

    ; Load the base pointer, add the computed offset, then jump on it.
    load y, #.shift_table
    lea y, b
    jmp y

    .b7:
        src a
    .b6:
        src a
    .b5:
        src a
    .b4:
        src a
    .b3:
        src a
    .b2:
        src a
    .b1:
        src a

        ; mask away the carried-in bits
        load y, #.mask_table
        clc
        src b
        load b, [y, b]
        and a, b

    .b0:
        rts

    .mask_table:    ; TODO: get the correct masks here
        #d8 0x7F, 0x3F, 0x1F, 0xF0, 0x70, 0x30, 0x10, 0x00
    .shift_table:
        #d16 .b0, .b1, .b2, .b3, .b4, .b5, .b6, .b7

; Perform an arithmetic right shift of the specified number of bits.
; Arguments:
;   A: the value to shift.
;   B: the number of bits to shift.
; Returns:
;   A: the shifted value.
asr_n:
    .loop_control:
        cmp b, #-1
        jg .loop_body
        jmp .loop_exit

    .loop_body:
        asr a

        dec b
        jmp .loop_control

    .loop_exit:
        rts

; Perform a binary search for a byte within a
; sorted array in the given bounds.
; Arguments:
;   A: the lower bound
;   B: the upper bound
;   Y: pointer to the array
;   FP+3: target byte to search for
; Returns:
;   A: index into array of byte, if found
;   B: 1 if byte was found, else 0
search:
    .ARG_TARGET = 3
    .NLOCALS = 1
    .LOC_MID = -1

    ; Prolouge
    push c
    push d
    push x
    mov x, sp
    lea sp, #-.NLOCALS

    ; Recursive Base case: the endpoints have
    ; converged or crossed, so target byte is
    ; not present
    cmp a, b
    jg .not_found

    ; Compute the midpoint as (low + high) / 2
    ; and save it to the stack
    mov c, b
    clc
    adc c, a
    clc
    src c
    store c, [x, #.LOC_MID]

    ; Compare target to array[mid]
    ; if target == array[mid] => mid is found index
    ; elif target < array[mid] => target is in first half, or not present
    ; else => target is in second half, or not present
    load d, [x, #.ARG_TARGET]
    load c, [y, c]
    cmp d, c
    je .found
    jl .descend_left
    jmp .descend_right

    .descend_left:
        ; Set up arguments to search from low to mid - 1
        load b, [x, #.LOC_MID]
        dec b
        jmp search

    .descend_right:
        ; Set up arguments to search from mid + 1 to high
        load a, [x, #.LOC_MID]
        inc a
        jmp search

    .found:
        load a, [x, #.LOC_MID]
        load b, #1
        jmp .return

    .not_found:
        load b, #0

    .return:
        ; Epilouge
        mov sp, x
        pop x
        pop d
        pop c
        rts

; Perform quick sort on a given byte array within the given bounds
; Arguments:
;   A: low bound
;   B: high bound
;   Y: array pointer
; Returns:
;   None (array modified in place)
sort:
    .NLOCALS = 3
    .LOC_ARR = -4
    .LOC_PI = -5

    ; Prolouge
    push c
    push d
    push x
    mov x, sp
    lea x, #-.NLOCALS

    ; if lower bound is not strictly less than the upper bound
    ; then there is nothing left to sort
    cmp a, b
    jge .return

    ; Copy the offset arguments into C, D for quicker subroutine calls
    mov c, a
    mov d, b

    ; Partition the array. Use the last element as the pivot element
    ; and place it in the correct position. Return value is the position
    ; of the pivot.
    store y, [x, #.LOC_ARR]
    jsr .partition
    store a, [x, #.LOC_PI]

    ; sort(arr, low, pi - 1)
    mov a, c
    load b, [x, #.LOC_PI]
    dec b
    load y, [x, #.LOC_ARR]
    jsr sort

    ; sort(arr, pi + 1, high)
    load a, [x, #.LOC_PI]
    inc a
    mov b, d
    load y, [x, #.LOC_ARR]
    jmp sort

    .return:
        ; Epilouge
        mov sp, x
        pop x
        pop d
        pop c
        rts

    ; Partition the given array such that the pivot element is
    ; placed into its correct position, with all elements less
    ; than it to the left, and all elements greater than it to
    ; the right.
    ; Arguments:
    ;   A: low bound
    ;   B: high bound
    ;   Y: array pointer
    ; Returns:
    ;   A: the position of the pivot element
    .partition:
        ..NLOCALS = 1
        ..LOC_IDX = -1
        ..LOC_LO = -2
        ..LOC_HI = -3
        ..LOC_ARR = -5

        ; Prolouge
        push c
        push d
        push x
        mov x, sp
        lea x, #-..NLOCALS

        ; compute i = low - 1 onto the stack. This will converge
        ; to the correct position of the pivot element
        mov d, a
        dec d
        store d, [x, #..LOC_IDX]

        ; for (j = low; j <= high - 1; j++)
        ; d -> j
        ; c -> high - 1
        mov d, a
        mov c, b
        dec c
        ..loop_control:
        cmp d, c
        jg ..loop_exit
 
        ..loop_body:
            push c
            push d

            ; d -> arr[j]
            ; c -> pivot (arr[high])
            load d, [y, d]
            load c, [y, b]
            cmp d, c
            jge ...continue

            ; i++
            load c, [x, #..LOC_IDX]
            inc c
            store c, [x, #..LOC_IDX]

            ; swap arr[i] and arr[j]
            ; Y is already loaded
            ; j is on stack, pop into A
            ; i is in C, move to B
            store a, [x, #..LOC_LO]
            store b, [x, #..LOC_HI]
            store y, [x, #..LOC_ARR]

            pop a
            push a
            mov b, c
            jsr arrswap8

            load a, [x, #..LOC_LO]
            load b, [x, #..LOC_HI]
            load y, [x, #..LOC_ARR]

            ...continue:
                pop d
                pop c
                inc d
                jmp ..loop_control

        ..loop_exit:
            load a, [x, #..LOC_IDX]
            inc a
            store a, [x, #..LOC_IDX]
            jsr arrswap8

            load a, [x, #..LOC_IDX]

        ; Epilouge
        mov sp, x
        pop x
        pop d
        pop c
        rts

; Swap the array elements at the given indices
; Arguments:
;   A: Index 1
;   B: Index 2
;   Y: Array pointer
; Returns:
;   None (memory modified in place)
arrswap8:
    ; Prolouge
    push c
    push d

    load c, [y, a]
    load d, [y, b]

    store c, [y, b]
    store d, [y, a]

    ; Epilouge
    pop d
    pop c
    rts
