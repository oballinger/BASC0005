import sys,re
# print raw context of shareholder-proposed items for firm regex in an N-PX file
f,firmre=sys.argv[1],sys.argv[2]
T=re.sub(r'\s+',' ',open(f).read())
blocks=re.split(r'ISSUER: ',T,flags=re.I)
seen=set()
for b in blocks[1:]:
    if not re.match(firmre,b[:60].upper()): continue
    md=re.search(r'MEETING DATE:? ?(\S+)',b[:400],re.I).group(1)
    for m in re.finditer(r'(PROPOSAL ?#\s*\S+?:)',b):
        seg=b[m.start():m.start()+700]
        nxt=re.search(r'PROPOSAL ?#|ELECTION OF DIRECTOR:|-{10}',seg[10:])
        seg=seg[:10+nxt.start()] if nxt else seg
        if (re.search(r"\sSHAREHOLDERS?\s(YES|NO)\b",seg) or re.search(r"(?i)shareholder proposal|requisition|proposed by shareholder|PROPOSAL FROM SHAREHOLDER",seg)) and seg[:120] not in seen:
            seen.add(seg[:120]); print(md,"|",seg[:600])
