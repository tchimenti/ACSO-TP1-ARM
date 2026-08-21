.text

movz X1, 0x1
lsl X1, X1, 16
lsl X1, X1, 24
movz X2, 0x1
lsl X2, X2, 16
lsl X2, X2, 23
subs X0, X1, X2

HLT 0
