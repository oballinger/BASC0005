import sys,re,os
for f in sys.argv[1:]:
    T=re.sub(r'\s+',' ',open(f).read())
    print('=====',os.path.basename(f))
    last=-1000
    for m in re.finditer(r'(be it resolved|resolved[,:;]|resolved that|resolved:|resolved –|resolved —|resolved -)',T,re.I):
        if m.start()-last<1500: continue
        last=m.start()
        pre=T[max(0,m.start()-250):m.start()]
        print('  PRE:',pre[-250:]); print('  RES:',T[m.start():m.start()+300]); print()
