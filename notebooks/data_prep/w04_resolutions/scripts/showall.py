import sys,re
# print each RESOLVED clause that occurs within 4000 chars after any occurrence of phrase (body occurrences)
f,ph,n=sys.argv[1],sys.argv[2],int(sys.argv[3])
T=re.sub(r'\s+',' ',open(f).read())
seen=set()
for m in re.finditer(re.escape(ph),T,re.I):
    w=T[m.start():m.start()+5000]; r=re.search(r'resolved',w,re.I)
    if r:
        k=m.start()+r.start()
        if k in seen: continue
        seen.add(k); print('  @',m.start(),'RES:',T[k:k+n]); 
