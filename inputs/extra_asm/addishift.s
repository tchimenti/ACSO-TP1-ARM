.text

movz X1, 0xFFF
lsl X1, X1, 12
adds X1, X11, 11
adds X0, X1, 0xFF000
adds X2, X12, 12

HLT 0
