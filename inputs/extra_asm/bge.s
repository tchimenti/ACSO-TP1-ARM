.text
cmp X11, X11
bge foo
adds X2, X0, 10

bar:
HLT 0

foo:
adds X3, X0, 10
cmp X3, X11
bge bar
adds X3, X0, 10
HLT 0
