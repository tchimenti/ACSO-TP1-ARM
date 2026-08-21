.text

movz X1, 0x1
lsl X1, X1, 16
lsl X1, X1, 24
lsr X2, X1, 25
adds X3, X3, -1
lsr X4, X3, 16
lsr X4, X3, 19
adds X10, X10, 0xFF
lsr X10, x10, 4

HLT 0
