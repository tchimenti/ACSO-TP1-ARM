.text
cmp X11, X11
beq foo
adds X2, X0, 10

bar:
cmp X11, 0x2
beq foo
HLT 0

foo:
movz X11, 0x3
cmp X11, 0x3
beq bar

adds X3, X0, 10
HLT 0
