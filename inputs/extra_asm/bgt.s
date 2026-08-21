.text
movz X12, 10
cmp X12, X11
bgt foo
adds X2, X0, 10

bar:
HLT 0

foo:
cmp X11, X12
bgt bar
adds X3, X0, 10
cmp X12, X11
bgt bar

HLT 0
