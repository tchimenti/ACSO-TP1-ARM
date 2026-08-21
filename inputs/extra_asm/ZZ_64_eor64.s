.text
adds X1, X3, 0x1
adds X10, X3, 0x10
lsl X1, X1, 16
lsl X1, X1, 24
eor X0, X10, X1
eor X2, X1, X1
adds X4, X4, -1
eor X0, X0, X4


HLT 0
