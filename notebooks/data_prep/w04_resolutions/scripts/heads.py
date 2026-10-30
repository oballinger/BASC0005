import sys,re,os
p1=re.compile(r'^\s*(item|proposal)\s*(no\.?\s*)?\d+\s*[—–\-:.]\s*\S',re.I)
p2=re.compile(r'^\s*(stockholder|shareholder) proposal(\s+(no\.?\s*)?\d+)?\s*(regarding|to|for|on|:|requesting|relating|concerning|—|–|-)',re.I)
for f in sys.argv[1:]:
    L=[l.strip() for l in open(f).read().split('\n') if l.strip()]
    seen=[]
    for i,l in enumerate(L):
        if len(l)>220: continue
        if p1.match(l) or p2.match(l):
            s=l
            j=i+1
            while len(s)<45 and j<len(L) and j<i+3: s+=' '+L[j]; j+=1
            k=re.sub(r'[^a-z]','',s.lower())[:50]
            if k not in [x[0] for x in seen]: seen.append((k,s[:140]))
    print('=====',os.path.basename(f),len(seen))
    for k,s in seen[:60]: print('  ',s)
