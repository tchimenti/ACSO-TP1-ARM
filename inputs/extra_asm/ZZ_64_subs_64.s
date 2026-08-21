.text

movz X1, 0x1
lsl X1, X1, 16
lsl X1, X1, 24
subs X0, X1, 0xFFF
adds X1, X1, 0xFFF
subs X11, X1, X0

HLT 0
