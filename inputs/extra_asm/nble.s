.text
adds X3, X0, 10
cmp X3, X11
ble foo
adds X2, X0, 10

bar:
HLT 0

foo:
adds X3, X0, 10
cmp X11, X3
ble bar
adds X3, X0, 10
HLT 0
