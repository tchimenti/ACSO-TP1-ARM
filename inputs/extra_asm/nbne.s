.text
movz X12, 10
cmp X11, X11
bne foo
adds X2, X0, 10

bar:
HLT 0

foo:
cmp X11, X11
bne bar
adds X3, X0, 10
HLT 0
