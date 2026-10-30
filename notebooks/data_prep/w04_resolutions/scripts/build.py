"""Build resolutions_long.csv, resolutions_firm_year.csv, excluded_candidates.csv.
Run: python3 -I scripts/build.py <dir>   (dir = w04_resolutions folder). Reads only local raw/ index files."""
import sys,os,csv,re,json
D=sys.argv[1]; RAW=os.path.join(D,'raw')
sys.path.insert(0,os.path.join(D,'scripts'))
from us_master import R
from nonus_master import N,X
CIK={'ExxonMobil':'34088','Chevron':'93410','ConocoPhillips':'1163165','Occidental':'797468'}
A='https://www.sec.gov/Archives/edgar/data'
# --- index lookups
proxy={}; k8={}
for line in open(f'{RAW}/filing_index.tsv'):
    cik,form,d,acc,doc,_=(line.rstrip('\n').split('\t')+[''])[:6]
    c=str(int(cik)); url=f'{A}/{c}/{acc.replace("-","")}/{doc}'
    if form=='DEF 14A': proxy[(c,int(d[:4]))]=url
    else: k8[(c,d)]=url
tenq={}
for line in open(f'{RAW}/tenq_index.txt'):
    c,d,acc,doc=line.split(); tenq[(c,d)]=f'{A}/{c}/{acc}/{doc}'
tenq[('797468','2016-05-05')]=f'{A}/797468/000079746816000023/oxyform10q33116.htm'
npx={}
for line in open(f'{RAW}/npx_energy_index.txt'):
    d,acc,doc=line.split(); npx[int(d[:4])]=f'{A}/734383/{acc.replace("-","")}/{doc}'
eu={}
for line in open(f'{RAW}/eu_6k_index.tsv'):
    cik,d,acc,doc,desc=line.rstrip('\n').split('\t'); eu[(str(int(cik)),d,acc.replace('-',''))]=f'{A}/{int(cik)}/{acc.replace("-","")}/{doc}'
def eu6k(c,d,a): return eu[(c,d,a)]
SH={'SHELL_RES_2006':('2006-05-19','000116854806000046'),'SHELL_RES_2010':('2010-05-20','000116854810000040'),'SHELL_RES_2015':('2015-05-21','000119312515196394'),
    'SHELL_RES_2016':('2016-05-25','000119312516601270'),'SHELL_RES_2017':('2017-05-24','000119312517180422'),'SHELL_RES_2018':('2018-05-23','000119312518171341'),
    'SHELL_RES_2019':('2019-05-21','000119312519152619'),'SHELL_NOM_2016':('2016-04-22','000119312516551029'),'SHELL_NOM_2017':('2017-04-21','000119312517131284'),
    'SHELL_NOM_2018':('2018-04-19','000119312518121779'),'SHELL_NOM_2019':('2019-04-11','000119312519103361')}
EQ={'EQ_2010':'000114062510000048/sto100519a_6-k.htm','EQ_2015':'000114062515000054/sto150519b_6-k.htm','EQ_2016':'000114062516000113/sto160511_6-k.htm',
    'EQ_2017':'000114062517000012/sto170511_6-k.htm','EQ_2018':'000114062518000011/sto180515_6-k.htm','EQ_2019':'000114062519000019/sto190515_6-k.htm'}
def src(key,firm,year):
    if key=='NPX': return npx[year]
    if key=='PROXY': return proxy[(CIK[firm],year)]
    if key in SH: d,a=SH[key]; return eu6k('1306965',d,a)
    if key in EQ: return f'{A}/1140625/{EQ[key]}'
    return key
def pct(f,a): return round(100*f/(f+a),1) if f not in (None,'') and a not in (None,'') else ''
# --- long table
rows=[]
num=re.compile(r'\d{1,3}(?:,\d{3}){2,}')
for firm,yr,title,cat,status,bl,doc,ph,note in R:
    For=Ag=''
    vurl=''
    if doc:
        c,d=doc.split('_'); vurl=k8.get((c,d)) or tenq.get((c,d),'')
    if status=='voted' and ph:
        T=re.sub(r'\s+',' ',open(f'{RAW}/txt/{doc}.txt').read())
        ms=[m.start() for m in re.finditer(r'(submission of matters to a vote|5\.07)',T,re.I)]
        T=T[ms[-1]:] if ms else T
        i=T.lower().find(ph.lower()); assert i>=0,(firm,yr,title)
        ns=num.findall(T[i:i+700]); For,Ag=[int(x.replace(',','')) for x in ns[:2]]
    if firm=='ConocoPhillips' and yr==2017: note=(note+'; ' if note else '')+"8-K row label for these votes misprinted as 'Partial Deferral of Annual Bonus Based on Reserves Metrics' (figures differ from the 2016 vote on that topic)"
    rows.append(dict(firm=firm,year=yr,title=title,category=cat,status=status,borderline=bl,board_rec='against',
        votes_for=For,votes_against=Ag,support_pct=pct(For,Ag) if For!='' else '',
        source_url=proxy[(CIK[firm],yr)],vote_source_url=vurl,note=note))
for firm,yr,title,cat,status,bl,br,For,Ag,sp,srcs,note in N:
    urls=[src(s,firm,yr) for s in srcs]
    rows.append(dict(firm=firm,year=yr,title=title,category=cat,status=status,borderline=bl,board_rec=br,
        votes_for=For or '',votes_against=Ag or '',support_pct=sp if sp else pct(For,Ag),
        source_url=urls[0],vote_source_url=' '.join(urls[1:]) if len(urls)>1 else urls[0],note=note))
rows.sort(key=lambda r:(r['firm'],r['year'],r['title']))
F=list(rows[0].keys())
with open(f'{D}/resolutions_long.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=F); w.writeheader(); w.writerows(rows)
with open(f'{D}/excluded_candidates.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['firm','year','title','reason_not_counted','source_url'])
    for firm,yr,title,reason,srcs in X: w.writerow([firm,yr,title,reason,' '.join(src(s,firm,yr) for s in srcs)])
# --- coverage from N-PX for non-US firms
npxcov={}
for r in csv.DictReader(open(f'{RAW}/npx_parsed.csv')):
    m=re.match(r'(\d+)/(\d+)/(\d+)',r['meeting_date'])
    if not m: continue
    y=int(m.group(3)); y=y+2000 if y<100 else y; mo=int(m.group(1))
    if 3<=mo<=6 and int(r['n_items'])>=2: npxcov.setdefault((r['firm'],y),r['npx_file'])
FIRMS=['BP','Chevron','ConocoPhillips','ExxonMobil','Shell','Occidental','TotalEnergies','Equinor','ENI','Repsol']
out=[]
for firm in FIRMS:
    for y in range(2004,2020):
        rs=[r for r in rows if r['firm']==firm and r['year']==y]
        voted=[r for r in rs if r['status']=='voted']
        wd=[r for r in rs if r['status'].startswith('withdrawn')]
        if firm in CIK:
            note='checked: DEF 14A proxy items + vote results (8-K Item 5.07 from 2010; 10-Q pre-2010)'
        elif firm=='Shell' and y in (2004,2005):
            note='checked: pre-unification parents (Royal Dutch Petroleum Co., Shell T&T) - no shareholder-proposed items in Vanguard Energy N-PX'
        elif (firm,y) in npxcov:
            note='checked: full AGM ballot in Vanguard Energy Fund N-PX'
            if firm=='Shell': note+=' + Shell 6-K poll results'
            if firm=='BP' and y>=2016: note+=' + BP 6-K poll results'
            if firm=='Equinor' and y>=2010: note+=' + Statoil/Equinor AGM minutes (6-K)'
            if firm in ('TotalEnergies','ENI','Repsol'): note+=' (only source; lower confidence)'
        else:
            note='NOT CHECKED: firm not in N-PX source for this AGM'
        chk=not note.startswith('NOT')
        sup=[float(r['support_pct']) for r in voted if r['support_pct']!='']
        out.append(dict(firm=firm,year=y,n_climate_resolutions=len(voted) if chk else '',
            n_borderline=sum(r['borderline']=='Y' for r in voted) if chk else '',
            n_withdrawn='',n_withdrawn_after_notice=len(wd) if chk else '',
            max_support_pct=max(sup) if sup else '',coverage_note=note))
with open(f'{D}/resolutions_firm_year.csv','w',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print('long rows',len(rows),'firm-years',len(out))
