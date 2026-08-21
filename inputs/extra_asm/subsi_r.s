.text

movz X1, 0x1
movz X2, 0x2
subs X0, X1, X2
subs X3, X0, 0xFF
subs X0, X2, X1
HLT 0
