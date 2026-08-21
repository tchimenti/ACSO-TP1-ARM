.text

movz X1, 0x1
lsl X1, X1, 31
lsl X1, X1, 17
movz X2, 0x1
lsl X2, X2, 31
lsl X2, X2, 17
adds X0, X1, X2



HLT 0
