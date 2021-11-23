EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 8850 7500 2    61   ~ 0
8-bit General Purpose Register
Text Notes 8800 7650 2    61   ~ 0
July 22, 2021
Text Notes 10650 7650 2    61   ~ 0
2\n
Entry Wire Line
	8950 700  9050 800 
Entry Wire Line
	9050 700  9150 800 
Entry Wire Line
	9150 700  9250 800 
Entry Wire Line
	9250 700  9350 800 
Entry Wire Line
	9350 700  9450 800 
Entry Wire Line
	9450 700  9550 800 
Entry Wire Line
	9550 700  9650 800 
Entry Wire Line
	9650 700  9750 800 
Entry Wire Line
	8950 1450 9050 1550
Entry Wire Line
	9050 1450 9150 1550
Entry Wire Line
	9150 1450 9250 1550
Entry Wire Line
	9250 1450 9350 1550
Entry Wire Line
	9350 1450 9450 1550
Entry Wire Line
	9450 1450 9550 1550
Entry Wire Line
	9550 1450 9650 1550
Entry Wire Line
	9650 1450 9750 1550
Entry Wire Line
	8950 2250 9050 2350
Entry Wire Line
	9050 2250 9150 2350
Entry Wire Line
	9150 2250 9250 2350
Entry Wire Line
	9250 2250 9350 2350
Entry Wire Line
	9350 2250 9450 2350
Entry Wire Line
	9450 2250 9550 2350
Entry Wire Line
	9550 2250 9650 2350
Entry Wire Line
	9650 2250 9750 2350
Wire Wire Line
	11100 4200 11100 4000
Wire Wire Line
	9050 4200 9050 4000
Wire Wire Line
	7000 4200 7000 4000
Wire Wire Line
	4950 4200 4950 4000
Wire Wire Line
	2700 4200 2700 4000
Wire Wire Line
	4750 6400 5050 6400
Wire Wire Line
	5050 6300 4750 6300
Wire Wire Line
	4750 6200 5050 6200
Wire Wire Line
	4750 6100 5050 6100
Wire Wire Line
	5050 6000 4750 6000
Wire Wire Line
	4750 5900 5050 5900
Wire Wire Line
	5050 5800 4750 5800
Wire Wire Line
	4750 5700 5050 5700
Wire Wire Line
	1200 3700 1200 2750
Wire Wire Line
	3750 3500 3850 3500
Wire Wire Line
	3850 3500 3850 3700
Connection ~ 3750 3500
Wire Wire Line
	3750 3500 3750 3700
Wire Wire Line
	1500 3500 1600 3500
Wire Wire Line
	1600 3500 1600 3700
Connection ~ 1500 3500
Wire Wire Line
	1500 3500 1500 3700
Text Notes 7050 7100 0    183  ~ 0
Homebrew 8-bit CPU\nBrady Burnsides\n
Wire Wire Line
	1050 3250 9800 3250
Wire Wire Line
	9800 3250 9800 3700
Wire Wire Line
	1050 3150 7750 3150
Wire Wire Line
	7750 3150 7750 3700
Wire Wire Line
	1050 3050 5700 3050
Wire Wire Line
	5700 3050 5700 3700
Wire Wire Line
	1050 2950 1500 2950
Connection ~ 1500 2950
Wire Wire Line
	1500 2950 1500 3500
Wire Wire Line
	1500 2950 3750 2950
Wire Wire Line
	3750 2950 3750 3500
Wire Wire Line
	1050 2850 1400 2850
Connection ~ 1400 2850
Wire Wire Line
	1400 2850 1400 3700
Wire Wire Line
	1400 2850 3650 2850
Wire Wire Line
	3650 2850 3650 3700
Wire Wire Line
	1050 2750 1200 2750
Connection ~ 1200 2750
Wire Wire Line
	1200 2750 3450 2750
Wire Wire Line
	3450 2750 3450 3700
Wire Wire Line
	1800 3600 1800 3650
Wire Wire Line
	1800 3650 1900 3650
Wire Wire Line
	1900 3650 1900 3700
Connection ~ 1800 3650
Wire Wire Line
	1800 3650 1800 3700
Wire Wire Line
	4050 3600 4050 3650
Wire Wire Line
	4050 3650 4150 3650
Wire Wire Line
	4150 3650 4150 3700
Connection ~ 4050 3650
Wire Wire Line
	4050 3650 4050 3700
$Comp
L 74xx:74LS245 DataDriver1
U 1 1 60FAEC2A
P 10300 4200
F 0 "DataDriver1" V 10346 3356 50  0000 R CNN
F 1 "74LS245" V 10255 3356 50  0000 R CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 10300 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS245" H 10300 4200 50  0001 C CNN
	1    10300 4200
	0    1    1    0   
$EndComp
$Comp
L 74xx:74LS245 RHSDriver1
U 1 1 60FB109E
P 8250 4200
F 0 "RHSDriver1" V 8296 3356 50  0000 R CNN
F 1 "74LS245" V 8205 3356 50  0000 R CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 8250 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS245" H 8250 4200 50  0001 C CNN
	1    8250 4200
	0    1    1    0   
$EndComp
$Comp
L 74xx:74LS245 LHSDriver1
U 1 1 60FB2282
P 6200 4200
F 0 "LHSDriver1" V 6246 3356 50  0000 R CNN
F 1 "74LS245" V 6155 3356 50  0000 R CNN
F 2 "Package_DIP:DIP-20_W7.62mm" H 6200 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS245" H 6200 4200 50  0001 C CNN
	1    6200 4200
	0    1    1    0   
$EndComp
Text Label 2100 4700 3    61   ~ 0
B7
Text Label 2200 4700 3    61   ~ 0
B6
Text Label 2300 4700 3    61   ~ 0
B5
Text Label 2400 4700 3    61   ~ 0
B4
Text Label 4350 4700 3    61   ~ 0
B3
Text Label 4450 4700 3    61   ~ 0
B2
Text Label 4550 4700 3    61   ~ 0
B1
Text Label 4650 4700 3    61   ~ 0
B0
Text Label 6000 4700 3    61   ~ 0
B7
Text Label 6100 4700 3    61   ~ 0
B6
Text Label 6200 4700 3    61   ~ 0
B5
Text Label 6300 4700 3    61   ~ 0
B4
Text Label 6400 4700 3    61   ~ 0
B3
Text Label 6500 4700 3    61   ~ 0
B2
Text Label 6600 4700 3    61   ~ 0
B1
Text Label 6700 4700 3    61   ~ 0
B0
Text Label 8050 4700 3    61   ~ 0
B7
Text Label 8150 4700 3    61   ~ 0
B6
Text Label 8250 4700 3    61   ~ 0
B5
Text Label 8350 4700 3    61   ~ 0
B4
Text Label 8450 4700 3    61   ~ 0
B3
Text Label 8550 4700 3    61   ~ 0
B2
Text Label 8650 4700 3    61   ~ 0
B1
Text Label 8750 4700 3    61   ~ 0
B0
Text Label 10100 4700 3    61   ~ 0
B7
Text Label 10200 4700 3    61   ~ 0
B6
Text Label 10300 4700 3    61   ~ 0
B5
Text Label 10400 4700 3    61   ~ 0
B4
Text Label 10500 4700 3    61   ~ 0
B3
Text Label 10600 4700 3    61   ~ 0
B2
Text Label 10700 4700 3    61   ~ 0
B1
Text Label 10800 4700 3    61   ~ 0
B0
Text Label 2100 3700 1    61   ~ 0
D7
Text Label 2200 3700 1    61   ~ 0
D6
Text Label 2300 3700 1    61   ~ 0
D5
Text Label 2400 3700 1    61   ~ 0
D4
Text Label 4350 3700 1    61   ~ 0
D3
Text Label 4450 3700 1    61   ~ 0
D2
Text Label 4550 3700 1    61   ~ 0
D1
Text Label 4650 3700 1    61   ~ 0
D0
Text Label 6000 3700 1    61   ~ 0
L7
Text Label 6100 3700 1    61   ~ 0
L6
Text Label 6200 3700 1    61   ~ 0
L5
Text Label 6300 3700 1    61   ~ 0
L4
Text Label 6400 3700 1    61   ~ 0
L3
Text Label 6500 3700 1    61   ~ 0
L2
Text Label 6600 3700 1    61   ~ 0
L1
Text Label 6700 3700 1    61   ~ 0
L0
Text Label 8050 3700 1    61   ~ 0
R7
Text Label 8150 3700 1    61   ~ 0
R6
Text Label 8250 3700 1    61   ~ 0
R5
Text Label 8350 3700 1    61   ~ 0
R4
Text Label 8450 3700 1    61   ~ 0
R3
Text Label 8550 3700 1    61   ~ 0
R2
Text Label 8650 3700 1    61   ~ 0
R1
Text Label 8750 3700 1    61   ~ 0
R0
Text Label 10100 3700 1    61   ~ 0
D7
Text Label 10200 3700 1    61   ~ 0
D6
Text Label 10300 3700 1    61   ~ 0
D5
Text Label 10400 3700 1    61   ~ 0
D4
Text Label 10500 3700 1    61   ~ 0
D3
Text Label 10600 3700 1    61   ~ 0
D2
Text Label 10700 3700 1    61   ~ 0
D1
Text Label 10800 3700 1    61   ~ 0
D0
Text Label 9050 800  3    61   ~ 0
D7
Text Label 9150 800  3    61   ~ 0
D6
Text Label 9250 800  3    61   ~ 0
D5
Text Label 9350 800  3    61   ~ 0
D4
Text Label 9450 800  3    61   ~ 0
D3
Text Label 9550 800  3    61   ~ 0
D2
Text Label 9650 800  3    61   ~ 0
D1
Text Label 9750 800  3    61   ~ 0
D0
Text Label 9050 1550 3    61   ~ 0
L7
Text Label 9150 1550 3    61   ~ 0
L6
Text Label 9250 1550 3    61   ~ 0
L5
Text Label 9350 1550 3    61   ~ 0
L4
Text Label 9450 1550 3    61   ~ 0
L3
Text Label 9550 1550 3    61   ~ 0
L2
Text Label 9650 1550 3    61   ~ 0
L1
Text Label 9750 1550 3    61   ~ 0
L0
Text Label 9050 2350 3    61   ~ 0
R7
Text Label 9150 2350 3    61   ~ 0
R6
Text Label 9250 2350 3    61   ~ 0
R5
Text Label 9350 2350 3    61   ~ 0
R4
Text Label 9450 2350 3    61   ~ 0
R3
Text Label 9550 2350 3    61   ~ 0
R2
Text Label 9650 2350 3    61   ~ 0
R1
Text Label 9750 2350 3    61   ~ 0
R0
$Comp
L Device:R_Network08 RegLEDRes1
U 1 1 60FDC4FE
P 5250 6100
F 0 "RegLEDRes1" H 4770 6054 50  0000 R CNN
F 1 "R_Network08" H 4770 6145 50  0000 R CNN
F 2 "Resistor_THT:R_Array_SIP9" V 5725 6100 50  0001 C CNN
F 3 "http://www.vishay.com/docs/31509/csc.pdf" H 5250 6100 50  0001 C CNN
	1    5250 6100
	0    1    1    0   
$EndComp
Text Label 10450 700  0    61   ~ 0
DBUS
Text Label 10450 1450 0    61   ~ 0
LHS
Text Label 10450 2250 0    61   ~ 0
RHS
Text Label 1050 2850 2    61   ~ 0
CLK
Text Label 1050 2950 2    61   ~ 0
~DBUS_LOAD
Text Label 1050 3050 2    61   ~ 0
~LHS_ASSERT
Text Label 1050 3150 2    61   ~ 0
~RHS_ASSERT
Text Label 1050 3250 2    61   ~ 0
~DBUS_ASSERT
Text Label 1050 2750 2    61   ~ 0
CLR
$Comp
L Connector_Generic:Conn_01x08 DHdr1
U 1 1 6108E7E1
P 9450 1200
F 0 "DHdr1" V 9322 1580 50  0000 L CNN
F 1 "Conn_01x08" V 9413 1580 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 9450 1200 50  0001 C CNN
F 3 "~" H 9450 1200 50  0001 C CNN
	1    9450 1200
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x08 RHSHdr1
U 1 1 610911F8
P 9450 2800
F 0 "RHSHdr1" V 9322 3180 50  0000 L CNN
F 1 "Conn_01x08" V 9413 3180 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 9450 2800 50  0001 C CNN
F 3 "~" H 9450 2800 50  0001 C CNN
	1    9450 2800
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x08 LHSHdr1
U 1 1 6109376D
P 9450 2000
F 0 "LHSHdr1" V 9322 2380 50  0000 L CNN
F 1 "Conn_01x08" V 9413 2380 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 9450 2000 50  0001 C CNN
F 3 "~" H 9450 2000 50  0001 C CNN
	1    9450 2000
	0    1    1    0   
$EndComp
Wire Wire Line
	9050 800  9050 1000
Wire Wire Line
	9150 1000 9150 800 
Wire Wire Line
	9250 800  9250 1000
Wire Wire Line
	9350 1000 9350 800 
Wire Wire Line
	9450 800  9450 1000
Wire Wire Line
	9550 1000 9550 800 
Wire Wire Line
	9650 800  9650 1000
Wire Wire Line
	9750 1000 9750 800 
Wire Wire Line
	9050 1550 9050 1800
Wire Wire Line
	9150 1800 9150 1550
Wire Wire Line
	9250 1550 9250 1800
Wire Wire Line
	9350 1800 9350 1550
Wire Wire Line
	9450 1550 9450 1800
Wire Wire Line
	9550 1800 9550 1550
Wire Wire Line
	9650 1550 9650 1800
Wire Wire Line
	9750 1800 9750 1550
Wire Wire Line
	9750 2350 9750 2600
Wire Wire Line
	9650 2600 9650 2350
Wire Wire Line
	9550 2350 9550 2600
Wire Wire Line
	9450 2600 9450 2350
Wire Wire Line
	9350 2350 9350 2600
Wire Wire Line
	9250 2600 9250 2350
Wire Wire Line
	9150 2350 9150 2600
Wire Wire Line
	9050 2600 9050 2350
$Comp
L Connector_Generic:Conn_01x03 PwrHdr1
U 1 1 61117AD2
P 2450 1550
F 0 "PwrHdr1" H 2368 1225 50  0000 C CNN
F 1 "Conn_01x03" H 2368 1316 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 2450 1550 50  0001 C CNN
F 3 "~" H 2450 1550 50  0001 C CNN
	1    2450 1550
	-1   0    0    1   
$EndComp
Text Label 2650 1450 0    61   ~ 0
VCC
Text Label 2650 1550 0    61   ~ 0
GND
Text Label 2650 1650 0    61   ~ 0
CLK
$Comp
L Connector_Generic:Conn_01x05 CtrlHdr1
U 1 1 6111A1C2
P 1250 1650
F 0 "CtrlHdr1" H 1168 1225 50  0000 C CNN
F 1 "Conn_01x05" H 1168 1316 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 1250 1650 50  0001 C CNN
F 3 "~" H 1250 1650 50  0001 C CNN
	1    1250 1650
	-1   0    0    1   
$EndComp
Text Label 1450 1450 0    61   ~ 0
CLR
Text Label 1450 1550 0    61   ~ 0
~RHS_ASSERT
Text Label 1450 1650 0    61   ~ 0
~LHS_ASSERT
Text Label 1450 1750 0    61   ~ 0
~DBUS_ASSERT
Text Label 1450 1850 0    61   ~ 0
~DBUS_LOAD
Text Label 900  4400 3    61   ~ 0
GND
$Comp
L 74xx:74LS173 RegHi1
U 1 1 60FAE99B
P 1800 4200
F 0 "RegHi1" V 1846 3256 50  0000 R CNN
F 1 "74LS173" V 1755 3256 50  0000 R CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 1800 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS173" H 1800 4200 50  0001 C CNN
	1    1800 4200
	0    1    1    0   
$EndComp
Text Label 2700 4000 1    61   ~ 0
VCC
Text Label 3150 4400 3    61   ~ 0
GND
$Comp
L 74xx:74LS173 RegLo1
U 1 1 60FAC219
P 4050 4200
F 0 "RegLo1" V 4096 3256 50  0000 R CNN
F 1 "74LS173" V 4005 3256 50  0000 R CNN
F 2 "Package_DIP:DIP-16_W7.62mm" H 4050 4200 50  0001 C CNN
F 3 "http://www.ti.com/lit/gpn/sn74LS173" H 4050 4200 50  0001 C CNN
	1    4050 4200
	0    1    1    0   
$EndComp
Text Label 4950 4000 1    61   ~ 0
VCC
Text Label 5400 4400 3    61   ~ 0
GND
Text Label 7000 4000 1    61   ~ 0
VCC
Text Label 7450 4400 3    61   ~ 0
GND
Text Label 9050 4000 1    61   ~ 0
VCC
Text Label 9500 4400 3    61   ~ 0
GND
Text Label 11100 4000 1    61   ~ 0
VCC
Text Label 9900 3700 1    61   ~ 0
GND
Text Label 7850 3700 1    61   ~ 0
GND
Text Label 5800 3700 1    61   ~ 0
GND
Text Label 4050 3600 1    61   ~ 0
GND
Text Label 1800 3600 1    61   ~ 0
GND
Text Label 5450 5700 0    61   ~ 0
GND
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 60FDEF50
P 2900 1450
F 0 "#FLG0101" H 2900 1525 50  0001 C CNN
F 1 "PWR_FLAG" V 2900 1578 50  0000 L CNN
F 2 "" H 2900 1450 50  0001 C CNN
F 3 "~" H 2900 1450 50  0001 C CNN
	1    2900 1450
	0    1    1    0   
$EndComp
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 60FDF73D
P 2900 1550
F 0 "#FLG0102" H 2900 1625 50  0001 C CNN
F 1 "PWR_FLAG" V 2900 1678 50  0000 L CNN
F 2 "" H 2900 1550 50  0001 C CNN
F 3 "~" H 2900 1550 50  0001 C CNN
	1    2900 1550
	0    1    1    0   
$EndComp
Wire Wire Line
	2900 1450 2650 1450
Wire Wire Line
	2650 1550 2900 1550
Text Label 1850 7150 2    61   ~ 0
CLR
Text Label 2900 6050 0    61   ~ 0
~DBUS_ASSERT
Text Label 2900 6750 0    61   ~ 0
~RHS_ASSERT
Text Label 2900 6400 0    61   ~ 0
~LHS_ASSERT
Text Label 2900 5700 0    61   ~ 0
~DBUS_LOAD
$Comp
L Device:LED D2
U 1 1 610178AC
P 2600 5700
F 0 "D2" H 2593 5445 50  0000 C CNN
F 1 "LED" H 2593 5536 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 2600 5700 50  0001 C CNN
F 3 "~" H 2600 5700 50  0001 C CNN
	1    2600 5700
	-1   0    0    1   
$EndComp
Wire Wire Line
	2750 5700 2900 5700
Wire Wire Line
	2450 5700 2300 5700
$Comp
L Device:R R1
U 1 1 610246D9
P 2150 5700
F 0 "R1" V 1943 5700 50  0000 C CNN
F 1 "R" V 2034 5700 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2080 5700 50  0001 C CNN
F 3 "~" H 2150 5700 50  0001 C CNN
	1    2150 5700
	0    1    1    0   
$EndComp
Wire Wire Line
	2000 5700 1850 5700
Text Label 1850 5700 2    61   ~ 0
VCC
$Comp
L Device:LED D3
U 1 1 610291C1
P 2600 6050
F 0 "D3" H 2593 5795 50  0000 C CNN
F 1 "LED" H 2593 5886 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 2600 6050 50  0001 C CNN
F 3 "~" H 2600 6050 50  0001 C CNN
	1    2600 6050
	-1   0    0    1   
$EndComp
Wire Wire Line
	2750 6050 2900 6050
Wire Wire Line
	2450 6050 2300 6050
$Comp
L Device:R R2
U 1 1 610291C9
P 2150 6050
F 0 "R2" V 1943 6050 50  0000 C CNN
F 1 "R" V 2034 6050 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2080 6050 50  0001 C CNN
F 3 "~" H 2150 6050 50  0001 C CNN
	1    2150 6050
	0    1    1    0   
$EndComp
Wire Wire Line
	2000 6050 1850 6050
Text Label 1850 6050 2    61   ~ 0
VCC
$Comp
L Device:LED D4
U 1 1 6102D3B8
P 2600 6400
F 0 "D4" H 2593 6145 50  0000 C CNN
F 1 "LED" H 2593 6236 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 2600 6400 50  0001 C CNN
F 3 "~" H 2600 6400 50  0001 C CNN
	1    2600 6400
	-1   0    0    1   
$EndComp
Wire Wire Line
	2750 6400 2900 6400
Wire Wire Line
	2450 6400 2300 6400
$Comp
L Device:R R3
U 1 1 6102D3C0
P 2150 6400
F 0 "R3" V 1943 6400 50  0000 C CNN
F 1 "R" V 2034 6400 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2080 6400 50  0001 C CNN
F 3 "~" H 2150 6400 50  0001 C CNN
	1    2150 6400
	0    1    1    0   
$EndComp
Wire Wire Line
	2000 6400 1850 6400
Text Label 1850 6400 2    61   ~ 0
VCC
$Comp
L Device:LED D5
U 1 1 61031128
P 2600 6750
F 0 "D5" H 2593 6495 50  0000 C CNN
F 1 "LED" H 2593 6586 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 2600 6750 50  0001 C CNN
F 3 "~" H 2600 6750 50  0001 C CNN
	1    2600 6750
	-1   0    0    1   
$EndComp
Wire Wire Line
	2750 6750 2900 6750
Wire Wire Line
	2450 6750 2300 6750
$Comp
L Device:R R5
U 1 1 61031130
P 2600 7150
F 0 "R5" V 2393 7150 50  0000 C CNN
F 1 "R" V 2484 7150 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2530 7150 50  0001 C CNN
F 3 "~" H 2600 7150 50  0001 C CNN
	1    2600 7150
	0    1    1    0   
$EndComp
Wire Wire Line
	2000 6750 1850 6750
Text Label 1850 6750 2    61   ~ 0
VCC
$Comp
L Device:LED D1
U 1 1 61035492
P 2150 7150
F 0 "D1" H 2143 6895 50  0000 C CNN
F 1 "LED" H 2143 6986 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 2150 7150 50  0001 C CNN
F 3 "~" H 2150 7150 50  0001 C CNN
	1    2150 7150
	-1   0    0    1   
$EndComp
Wire Wire Line
	2300 7150 2450 7150
Wire Wire Line
	2750 7150 2900 7150
Text Label 2900 7150 0    61   ~ 0
GND
$Comp
L Device:R R4
U 1 1 6103C9EE
P 2150 6750
F 0 "R4" V 1943 6750 50  0000 C CNN
F 1 "R" V 2034 6750 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 2080 6750 50  0001 C CNN
F 3 "~" H 2150 6750 50  0001 C CNN
	1    2150 6750
	0    1    1    0   
$EndComp
Wire Wire Line
	1850 7150 2000 7150
$Comp
L Device:LED D13
U 1 1 61073F2F
P 4600 6400
F 0 "D13" H 4593 6145 50  0000 C CNN
F 1 "LED" H 4593 6236 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 6400 50  0001 C CNN
F 3 "~" H 4600 6400 50  0001 C CNN
	1    4600 6400
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D12
U 1 1 6107C65C
P 4600 6300
F 0 "D12" H 4593 6045 50  0000 C CNN
F 1 "LED" H 4593 6136 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 6300 50  0001 C CNN
F 3 "~" H 4600 6300 50  0001 C CNN
	1    4600 6300
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D11
U 1 1 6107F138
P 4600 6200
F 0 "D11" H 4593 5945 50  0000 C CNN
F 1 "LED" H 4593 6036 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 6200 50  0001 C CNN
F 3 "~" H 4600 6200 50  0001 C CNN
	1    4600 6200
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D10
U 1 1 61081BCB
P 4600 6100
F 0 "D10" H 4593 5845 50  0000 C CNN
F 1 "LED" H 4593 5936 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 6100 50  0001 C CNN
F 3 "~" H 4600 6100 50  0001 C CNN
	1    4600 6100
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D9
U 1 1 61084435
P 4600 6000
F 0 "D9" H 4593 5745 50  0000 C CNN
F 1 "LED" H 4593 5836 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 6000 50  0001 C CNN
F 3 "~" H 4600 6000 50  0001 C CNN
	1    4600 6000
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D8
U 1 1 61086D13
P 4600 5900
F 0 "D8" H 4593 5645 50  0000 C CNN
F 1 "LED" H 4593 5736 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 5900 50  0001 C CNN
F 3 "~" H 4600 5900 50  0001 C CNN
	1    4600 5900
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D7
U 1 1 6108953D
P 4600 5800
F 0 "D7" H 4593 5545 50  0000 C CNN
F 1 "LED" H 4593 5636 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 5800 50  0001 C CNN
F 3 "~" H 4600 5800 50  0001 C CNN
	1    4600 5800
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D6
U 1 1 6108BF99
P 4600 5700
F 0 "D6" H 4593 5445 50  0000 C CNN
F 1 "LED" H 4593 5536 50  0000 C CNN
F 2 "LED_THT:LED_D2.0mm_W4.0mm_H2.8mm_FlatTop" H 4600 5700 50  0001 C CNN
F 3 "~" H 4600 5700 50  0001 C CNN
	1    4600 5700
	-1   0    0    1   
$EndComp
Text Label 4450 5700 2    61   ~ 0
B0
Text Label 4450 5800 2    61   ~ 0
B1
Text Label 4450 5900 2    61   ~ 0
B2
Text Label 4450 6000 2    61   ~ 0
B3
Text Label 4450 6100 2    61   ~ 0
B4
Text Label 4450 6200 2    61   ~ 0
B5
Text Label 4450 6300 2    61   ~ 0
B6
Text Label 4450 6400 2    61   ~ 0
B7
$Comp
L Device:C_Small C1
U 1 1 6118EC2C
P 1750 5000
F 0 "C1" V 1521 5000 50  0000 C CNN
F 1 "C_Small" V 1612 5000 50  0000 C CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm" H 1750 5000 50  0001 C CNN
F 3 "~" H 1750 5000 50  0001 C CNN
	1    1750 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	1850 5000 2700 5000
Wire Wire Line
	2700 5000 2700 4200
Connection ~ 2700 4200
Wire Wire Line
	1650 5000 900  5000
Wire Wire Line
	900  4200 900  5000
$Comp
L Device:C_Small C2
U 1 1 611954D5
P 4000 4950
F 0 "C2" V 3771 4950 50  0000 C CNN
F 1 "C_Small" V 3862 4950 50  0000 C CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm" H 4000 4950 50  0001 C CNN
F 3 "~" H 4000 4950 50  0001 C CNN
	1    4000 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	3900 4950 3150 4950
Wire Wire Line
	3150 4200 3150 4950
Wire Wire Line
	4100 4950 4950 4950
Wire Wire Line
	4950 4950 4950 4200
Connection ~ 4950 4200
$Comp
L Device:C_Small C3
U 1 1 6119C45B
P 5700 4950
F 0 "C3" V 5471 4950 50  0000 C CNN
F 1 "C_Small" V 5562 4950 50  0000 C CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm" H 5700 4950 50  0001 C CNN
F 3 "~" H 5700 4950 50  0001 C CNN
	1    5700 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	5600 4950 5400 4950
Wire Wire Line
	5400 4200 5400 4950
Wire Wire Line
	5800 4950 7000 4950
Wire Wire Line
	7000 4950 7000 4200
Connection ~ 7000 4200
$Comp
L Device:C_Small C4
U 1 1 611A2B0D
P 7750 4950
F 0 "C4" V 7521 4950 50  0000 C CNN
F 1 "C_Small" V 7612 4950 50  0000 C CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm" H 7750 4950 50  0001 C CNN
F 3 "~" H 7750 4950 50  0001 C CNN
	1    7750 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	7650 4950 7450 4950
Wire Wire Line
	7450 4200 7450 4950
Wire Wire Line
	7850 4950 9050 4950
Wire Wire Line
	9050 4950 9050 4200
Connection ~ 9050 4200
$Comp
L Device:C_Small C5
U 1 1 611A9952
P 9800 4950
F 0 "C5" V 9571 4950 50  0000 C CNN
F 1 "C_Small" V 9662 4950 50  0000 C CNN
F 2 "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P2.50mm" H 9800 4950 50  0001 C CNN
F 3 "~" H 9800 4950 50  0001 C CNN
	1    9800 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	9700 4950 9500 4950
Wire Wire Line
	9500 4200 9500 4950
Wire Wire Line
	9900 4950 11100 4950
Wire Wire Line
	11100 4950 11100 4200
Wire Bus Line
	8950 2250 10450 2250
Wire Bus Line
	8950 1450 10450 1450
Wire Bus Line
	8950 700  10450 700 
Connection ~ 11100 4200
$EndSCHEMATC
