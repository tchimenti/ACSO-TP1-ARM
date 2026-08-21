.text

movz X1, 0x1
lsl X1, X1, 31
lsl X1, X1, 17
adds X0, X1, 0xFFF
adds X11, X1, X0

HLT 0
