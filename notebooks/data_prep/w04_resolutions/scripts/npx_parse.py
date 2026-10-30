import sys,re,os,csv
tg={'BP':r'^BP (P\.?L\.?C|PLC)','Shell':r'^ROYAL DUTCH SHELL','TotalEnergies':r'^TOTAL ?S\.?A|^TOTAL SE|^TOTALENERGIES','ENI':r'^ENI ','Repsol':r'^REPSOL','Equinor':r'^STATOIL|^EQUINOR',
    'ExxonMobil':r'^EXXON','Chevron':r'^CHEVRON','ConocoPhillips':r'^CONOCOPHILLIPS','Occidental':r'^OCCIDENTAL PETROLEUM'}
item=re.compile(r'(PROPOSAL ?#\s*\S+?:|ELECTION OF DIRECTOR:)\s*(.*?)\s(ISSUER|SHAREHOLDERS?|SECURITY HOLDER)\s(YES|NO)\b',re.I)
w=csv.writer(sys.stdout); w.writerow(['npx_file','firm','issuer','meeting_date','n_items','n_shareholder','prop_no','text'])
for f in sys.argv[1:]:
    T=re.sub(r'\s+',' ',open(f).read())
    blocks=re.split(r'ISSUER: ',T,flags=re.I)
    for b in blocks[1:]:
        name=b[:60].upper()
        firm=[k for k,p in tg.items() if re.match(p,name)]
        if not firm: continue
        md=re.search(r'MEETING DATE:? ?(\d{1,2}/\d{1,2}/\d{2,4})',b[:400],re.I)
        its=item.findall(b)
        sh=[x for x in its if x[2].upper()!='ISSUER']
        base=[os.path.basename(f),firm[0],b[:40].split(' TICKER')[0].split(' Ticker')[0],md.group(1) if md else '',len(its),len(sh)]
        if not sh: w.writerow(base+['',''])
        for x in sh: w.writerow(base+[x[0],x[1][:300]])
