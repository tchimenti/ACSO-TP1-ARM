.text
movz X1, 0x1000
lsl X1, X1, 16

movz X10, 0x1234
lsl X10, X10, 16
movz X9, 0xabcd
orr X10, X10, X9

stur X10, [X1]
adds X1, X1, 1
ldur X11, [X1, 1]
ldur X11, [X1, -1]

HLT 0
