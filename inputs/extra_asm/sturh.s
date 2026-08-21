.text
movz X1, 0x1000
lsl X1, X1, 16

movz X10, 0xdef1
sturh W10, [X1, 0x4]

HLT 0
