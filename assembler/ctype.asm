#include "bw8cpu.asm"
#include "constants.asm"

; Look up table to define char class properties for
; the extended ASCII set
; Masks:
_ISALPHA  = 0b00000001
_ISUPPER  = 0b00000010
_ISLOWER  = 0b00000100
_ISDIGIT  = 0b00001000
_ISXDIGIT = 0b00010000
_ISSPACE  = 0b00100000
_ISPRINT  = 0b01000000
_ISCNTRL  = 0b10000000
ascii_properties:
    #d8 0b00000001 ; 0
    #d8 0b00000001 ; 1 ☺
    #d8 0b00000001 ; 2 ☻
    #d8 0b00000001 ; 3 ♥
    #d8 0b00000001 ; 4 ♦
    #d8 0b00000001 ; 5 ♣
    #d8 0b00000001 ; 6 ♠
    #d8 0b00000001 ; 7
    #d8 0b00000001 ; 8
    #d8 0b00000101 ; 9
    #d8 0b00000101 ; a
    #d8 0b00000101 ; b ♂
    #d8 0b00000101 ; c ♀
    #d8 0b00000101 ; d
    #d8 0b00000001 ; e ♫
    #d8 0b00000001 ; f ☼
    #d8 0b00000001 ; 10 ►
    #d8 0b00000001 ; 11 ◄
    #d8 0b00000001 ; 12 ↕
    #d8 0b00000001 ; 13 ‼
    #d8 0b00000001 ; 14 ¶
    #d8 0b00000001 ; 15 §
    #d8 0b00000001 ; 16 ▬
    #d8 0b00000001 ; 17 ↨
    #d8 0b00000001 ; 18 ↑
    #d8 0b00000001 ; 19 ↓
    #d8 0b00000001 ; 1a →
    #d8 0b00000001 ; 1b
    #d8 0b00000001 ; 1c ∟
    #d8 0b00000001 ; 1d ↔
    #d8 0b00000001 ; 1e ▲
    #d8 0b00000001 ; 1f ▼
    #d8 0b00000110 ; 20
    #d8 0b00000010 ; 21 !
    #d8 0b00000010 ; 22 "
    #d8 0b00000010 ; 23 #
    #d8 0b00000010 ; 24 $
    #d8 0b00000010 ; 25 %
    #d8 0b00000010 ; 26 &
    #d8 0b00000010 ; 27 '
    #d8 0b00000010 ; 28 (
    #d8 0b00000010 ; 29 )
    #d8 0b00000010 ; 2a *
    #d8 0b00000010 ; 2b +
    #d8 0b00000010 ; 2c ,
    #d8 0b00000010 ; 2d -
    #d8 0b00000010 ; 2e .
    #d8 0b00000010 ; 2f /
    #d8 0b00011010 ; 30 0
    #d8 0b00011010 ; 31 1
    #d8 0b00011010 ; 32 2
    #d8 0b00011010 ; 33 3
    #d8 0b00011010 ; 34 4
    #d8 0b00011010 ; 35 5
    #d8 0b00011010 ; 36 6
    #d8 0b00011010 ; 37 7
    #d8 0b00011010 ; 38 8
    #d8 0b00011010 ; 39 9
    #d8 0b00000010 ; 3a :
    #d8 0b00000010 ; 3b ;
    #d8 0b00000010 ; 3c <
    #d8 0b00000010 ; 3d =
    #d8 0b00000010 ; 3e >
    #d8 0b00000010 ; 3f ?
    #d8 0b00000010 ; 40 @
    #d8 0b11001010 ; 41 A
    #d8 0b11001010 ; 42 B
    #d8 0b11001010 ; 43 C
    #d8 0b11001010 ; 44 D
    #d8 0b11001010 ; 45 E
    #d8 0b11001010 ; 46 F
    #d8 0b11000010 ; 47 G
    #d8 0b11000010 ; 48 H
    #d8 0b11000010 ; 49 I
    #d8 0b11000010 ; 4a J
    #d8 0b11000010 ; 4b K
    #d8 0b11000010 ; 4c L
    #d8 0b11000010 ; 4d M
    #d8 0b11000010 ; 4e N
    #d8 0b11000010 ; 4f O
    #d8 0b11000010 ; 50 P
    #d8 0b11000010 ; 51 Q
    #d8 0b11000010 ; 52 R
    #d8 0b11000010 ; 53 S
    #d8 0b11000010 ; 54 T
    #d8 0b11000010 ; 55 U
    #d8 0b11000010 ; 56 V
    #d8 0b11000010 ; 57 W
    #d8 0b11000010 ; 58 X
    #d8 0b11000010 ; 59 Y
    #d8 0b11000010 ; 5a Z
    #d8 0b00000010 ; 5b [
    #d8 0b00000010 ; 5c \
    #d8 0b00000010 ; 5d ]
    #d8 0b00000010 ; 5e ^
    #d8 0b00000010 ; 5f _
    #d8 0b00000010 ; 60 `
    #d8 0b10101010 ; 61 a
    #d8 0b10101010 ; 62 b
    #d8 0b10101010 ; 63 c
    #d8 0b10101010 ; 64 d
    #d8 0b10101010 ; 65 e
    #d8 0b10101010 ; 66 f
    #d8 0b10100010 ; 67 g
    #d8 0b10100010 ; 68 h
    #d8 0b10100010 ; 69 i
    #d8 0b10100010 ; 6a j
    #d8 0b10100010 ; 6b k
    #d8 0b10100010 ; 6c l
    #d8 0b10100010 ; 6d m
    #d8 0b10100010 ; 6e n
    #d8 0b10100010 ; 6f o
    #d8 0b10100010 ; 70 p
    #d8 0b10100010 ; 71 q
    #d8 0b10100010 ; 72 r
    #d8 0b10100010 ; 73 s
    #d8 0b10100010 ; 74 t
    #d8 0b10100010 ; 75 u
    #d8 0b10100010 ; 76 v
    #d8 0b10100010 ; 77 w
    #d8 0b10100010 ; 78 x
    #d8 0b10100010 ; 79 y
    #d8 0b10100010 ; 7a z
    #d8 0b00000010 ; 7b {
    #d8 0b00000010 ; 7c |
    #d8 0b00000010 ; 7d }
    #d8 0b00000010 ; 7e ~
    #d8 0b00000001 ; 7f ⌂
    #d8 0b00000000 ; 80 Ç
    #d8 0b00000000 ; 81 ü
    #d8 0b00000000 ; 82 é
    #d8 0b00000000 ; 83 â
    #d8 0b00000000 ; 84 ä
    #d8 0b00000000 ; 85 à
    #d8 0b00000000 ; 86 å
    #d8 0b00000000 ; 87 ç
    #d8 0b00000000 ; 88 ê
    #d8 0b00000000 ; 89 ë
    #d8 0b00000000 ; 8a è
    #d8 0b00000000 ; 8b ï
    #d8 0b00000000 ; 8c î
    #d8 0b00000000 ; 8d ì
    #d8 0b00000000 ; 8e Ä
    #d8 0b00000000 ; 8f Å
    #d8 0b00000000 ; 90 É
    #d8 0b00000000 ; 91 æ
    #d8 0b00000000 ; 92 Æ
    #d8 0b00000000 ; 93 ô
    #d8 0b00000000 ; 94 ö
    #d8 0b00000000 ; 95 ò
    #d8 0b00000000 ; 96 û
    #d8 0b00000000 ; 97 ù
    #d8 0b00000000 ; 98 ÿ
    #d8 0b00000000 ; 99 Ö
    #d8 0b00000000 ; 9a Ü
    #d8 0b00000000 ; 9b ¢
    #d8 0b00000000 ; 9c £
    #d8 0b00000000 ; 9d ¥
    #d8 0b00000000 ; 9e ₧
    #d8 0b00000000 ; 9f ƒ
    #d8 0b00000000 ; a0 á
    #d8 0b00000000 ; a1 í
    #d8 0b00000000 ; a2 ó
    #d8 0b00000000 ; a3 ú
    #d8 0b00000000 ; a4 ñ
    #d8 0b00000000 ; a5 Ñ
    #d8 0b00000000 ; a6 ª
    #d8 0b00000000 ; a7 º
    #d8 0b00000000 ; a8 ¿
    #d8 0b00000000 ; a9 ⌐
    #d8 0b00000000 ; aa ¬
    #d8 0b00000000 ; ab ½
    #d8 0b00000000 ; ac ¼
    #d8 0b00000000 ; ad ¡
    #d8 0b00000000 ; ae «
    #d8 0b00000000 ; af »
    #d8 0b00000000 ; b0 ░
    #d8 0b00000000 ; b1 ▒
    #d8 0b00000000 ; b2 ▓
    #d8 0b00000000 ; b3 │
    #d8 0b00000000 ; b4 ┤
    #d8 0b00000000 ; b5 ╡
    #d8 0b00000000 ; b6 ╢
    #d8 0b00000000 ; b7 ╖
    #d8 0b00000000 ; b8 ╕
    #d8 0b00000000 ; b9 ╣
    #d8 0b00000000 ; ba ║
    #d8 0b00000000 ; bb ╗
    #d8 0b00000000 ; bc ╝
    #d8 0b00000000 ; bd ╜
    #d8 0b00000000 ; be ╛
    #d8 0b00000000 ; bf ┐
    #d8 0b00000000 ; c0 └
    #d8 0b00000000 ; c1 ┴
    #d8 0b00000000 ; c2 ┬
    #d8 0b00000000 ; c3 ├
    #d8 0b00000000 ; c4 ─
    #d8 0b00000000 ; c5 ┼
    #d8 0b00000000 ; c6 ╞
    #d8 0b00000000 ; c7 ╟
    #d8 0b00000000 ; c8 ╚
    #d8 0b00000000 ; c9 ╔
    #d8 0b00000000 ; ca ╩
    #d8 0b00000000 ; cb ╦
    #d8 0b00000000 ; cc ╠
    #d8 0b00000000 ; cd ═
    #d8 0b00000000 ; ce ╬
    #d8 0b00000000 ; cf ╧
    #d8 0b00000000 ; d0 ╨
    #d8 0b00000000 ; d1 ╤
    #d8 0b00000000 ; d2 ╥
    #d8 0b00000000 ; d3 ╙
    #d8 0b00000000 ; d4 ╘
    #d8 0b00000000 ; d5 ╒
    #d8 0b00000000 ; d6 ╓
    #d8 0b00000000 ; d7 ╫
    #d8 0b00000000 ; d8 ╪
    #d8 0b00000000 ; d9 ┘
    #d8 0b00000000 ; da ┌
    #d8 0b00000000 ; db █
    #d8 0b00000000 ; dc ▄
    #d8 0b00000000 ; dd ▌
    #d8 0b00000000 ; de ▐
    #d8 0b00000000 ; df ▀
    #d8 0b00000000 ; e0 α
    #d8 0b00000000 ; e1 ß
    #d8 0b00000000 ; e2 Γ
    #d8 0b00000000 ; e3 π
    #d8 0b00000000 ; e4 Σ
    #d8 0b00000000 ; e5 σ
    #d8 0b00000000 ; e6 µ
    #d8 0b00000000 ; e7 τ
    #d8 0b00000000 ; e8 Φ
    #d8 0b00000000 ; e9 Θ
    #d8 0b00000000 ; ea Ω
    #d8 0b00000000 ; eb δ
    #d8 0b00000000 ; ec ∞
    #d8 0b00000000 ; ed φ
    #d8 0b00000000 ; ee ε
    #d8 0b00000000 ; ef ∩
    #d8 0b00000000 ; f0 ≡
    #d8 0b00000000 ; f1 ±
    #d8 0b00000000 ; f2 ≥
    #d8 0b00000000 ; f3 ≤
    #d8 0b00000000 ; f4 ⌠
    #d8 0b00000000 ; f5 ⌡
    #d8 0b00000000 ; f6 ÷
    #d8 0b00000000 ; f7 ≈
    #d8 0b00000000 ; f8 °
    #d8 0b00000000 ; f9 ∙
    #d8 0b00000000 ; fa ·
    #d8 0b00000000 ; fb √
    #d8 0b00000000 ; fc ⁿ
    #d8 0b00000000 ; fd ²
    #d8 0b00000000 ; fe ■
    #d8 0b00000000 ; ff  

; Returns whether operand is in the character class
; Arguments:
;   A - operand char (unsigned)
;   B - char class mask
; Returns:
;   A - TRUE if ischarclass else FALSE
ischarclass:
    load y, #(ascii_properties + 127)
    clc
    adc a, #127

    load a, [y, a]
    and a, b
    je .return_false

    .return_true:
        load a, #TRUE
        rts
    .return_false:
        load a, #FALSE
        rts

; Return whether operand is alphanumeric
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isalnum else FALSE
isalnum:
    load b, #(_ISALPHA | _ISDIGIT)
    jmp ischarclass

; Return whether operand is alphabetic
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isalpha else FALSE
isalpha:
    load b, #_ISALPHA
    jmp ischarclass

; Return whether operand is lowercase
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if islower else FALSE
islower:
    load b, #_ISLOWER
    jmp ischarclass

; Return whether operand is uppercase
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isupper else FALSE
isupper:
    load b, #_ISUPPER
    jmp ischarclass

; Return whether operand is decimal digit
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isdigit else FALSE
isdigit:
    load b, #_ISDIGIT
    jmp ischarclass

; Return whether operand is hexadecimal digit
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isxdigit else FALSE
isxdigit:
    load b, #_ISXDIGIT
    jmp ischarclass

; Return whether operand is control character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if iscntrl else FALSE
iscntrl:
    load b, #_ISCNTRL
    jmp ischarclass

; Return whether operand is graphical character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isgraph else FALSE
isgraph:
    push a
    load b, #_ISPRINT
    jsr ischarclass
    je .return_false

    pop a
    cmp a, #" "
    je .return_false

    .return_true:
        load b, #TRUE
        rts

    .return_false:
        load b, #FALSE
        rts

; Return whether operand is space character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isspace else FALSE
isspace:
    load b, #_ISSPACE
    jmp ischarclass

; Return whether operand is blank character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isblank else FALSE
isblank:
    brk

; Return whether operand is printable character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if isprint else FALSE
isprint:
    load b, #_ISPRINT
    jmp ischarclass

; Return whether operand is punctuation character
; Arguments:
;   A - operand char (unsigned)
; Returns:
;   A - TRUE if ispunct else FALSE
ispunct:
    load b, #(_ISCNTRL | _ISALPHA)
    jsr ischarclass
    je .return_true

    .return_true:
        load a, #TRUE
        rts
    .return_false:
        load a, #FALSE
        rts
