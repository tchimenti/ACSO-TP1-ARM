.text
movz X1, 0x1000
lsl X1, X1, 16
movz X10, 0x1234
lsl X16, X10, 31
lsl X16, X16, 17
movz X10, 0x5678
lsl X10, X10, 16
lsl X10, X10, 16
orr X16, X16, X10
movz X10, 0x9abc
lsl X10, X10, 16
orr X16, X16, X10
movz X10, 0xdef1
orr X16, X16, X10
stur X16, [X1]
ldur X13, [X1]
ldur X13, [X1, 0x4]
HLT 0
