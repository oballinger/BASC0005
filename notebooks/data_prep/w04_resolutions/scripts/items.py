import sys,re,os
pat=re.compile(r'^\s*(item|proposal|stockholder proposal|shareholder proposal)\s*(no\.?\s*)?\d+\b',re.I)
for f in sys.argv[1:]:
    L=open(f).read().split('\n')
    seen=[];
    for i,l in enumerate(L):
        if pat.match(l) and len(l)<200:
            s=l.strip()
            if len(s)<25 and i+1<len(L): s+=' '+L[i+1].strip()
            k=re.sub(r'\W','',s.lower())[:40]
            if k not in [x[0] for x in seen]: seen.append((k,s[:150]))
    print('=====',os.path.basename(f),len(seen))
    for k,s in seen[:45]: print('  ',s)
