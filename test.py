from confpluspy import confpluspy as cpp
cfg = cpp("examples.cfg")

for name  in ['int','float','bool','list','tuple','str','dict','long-list','long-dict','function']: print name,"=",cfg["TYPES"][name],type(cfg["TYPES"][name])

for name  in ['x','y','z']: print name,"=",cfg["LINKS"][name]

for name  in 'x','y','x+y','x*y','lst','filter': print name,"=",cfg["COMPUTATIONS"][name]

for name  in 'fun','operation','fun(x*y)': print name,"=",cfg["FUNCTIONS"][name]


for name  in 'x','y','exmp1','exmp2','exmp4': print name,"=",cfg["LINKS_AND_STRINGS"][name]

for name  in 'parameter','function': print name,"=",cfg["PARAMTERS_IN_FUNCTIONS"][name]

print "TEST Function in TYPES                         2**2:", cfg["TYPES"]["function"](2)
print "TEST Function in PARAMTERS_IN_FUNCTIONS 2+parameter:", cfg["PARAMTERS_IN_FUNCTIONS"]["function"](2)
