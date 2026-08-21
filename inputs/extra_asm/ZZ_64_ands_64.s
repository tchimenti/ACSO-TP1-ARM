.text
movz X1, 0x1
lsl X1, X1, 16
lsl X1, X1, 24
adds X11, X0, -1
ands X2, X1, X11
ands X11, X11, X11
ands X1, X1, X0

HLT 0
