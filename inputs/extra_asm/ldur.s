.text
movz X1, 0x1000
lsl X1, X1, 16

movz X10, 0x1234
stur X10, [X1]
ldur X11, [X1]

HLT 0
