.text
movz X1, 0x1000
lsl X1, X1, 16
movz X10, 0x1234
stur X10, [X1, 0x0]
ldurb W0, [X1, 0x0]
movz X10, 0x5678
stur X10, [X1, 0x1]
adds X1, X1, 2

ldurb W4, [X1, -1]
HLT 0
