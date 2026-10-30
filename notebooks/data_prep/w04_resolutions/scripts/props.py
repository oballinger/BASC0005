import sys,re,os
pat=re.compile(r'(submitted by|has notified|have notified|has advised|intends to (present|submit)|proponent|filed by|owner of [\d,]+ shares)',re.I)
for f in sys.argv[1:]:
    L=[l.strip() for l in open(f).read().split('\n') if l.strip()]
    print('=====',os.path.basename(f))
    last=-10
    for i,l in enumerate(L):
        if pat.search(l) and i-last>6:
            last=i
            ctx=' | '.join(x[:90] for x in L[max(0,i-3):i])
            print(f'  [{i}] {ctx}  >> {l[:80]}')
