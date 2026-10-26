# Build the reading library -> library/index.html (+ items.json)
# Add items: append dicts to items_new.py NEW (source: Essay|Podcast|Newsletter|Instagram|X|Pick, added: YYYY-MM-DD).
# Optional per item: featured=True (force into 'This week'), cat="Founders|Podcasts|Tech|Newsletters|Stories", score=0-10 quality.
# Then: python3 build.py && cd library && git add -A && git commit -m update && git push
import json,hashlib,datetime
exec(open('items.py').read()); exec(open('items_new.py').read())
SRC={"Founder essays":"Essay","Tech essays":"Essay","Podcast notes":"Podcast"}
CAT0={"Founder essays":"Founders","Tech essays":"Tech","Podcast notes":"Podcasts"}
D=[]
for s,t,a,u,m,g,k,q in ITEMS: D.append(dict(source=SRC[s],cat=CAT0[s],title=t,author=a,url=u,minutes=m,tags=g,ideas=k,q=q,added="2026-10-12"))
D+=NEW
STORY={'story','writing','craft','microdrama','creator','creativity','culture'}
def cat(d):
    if d.get('cat'): return d['cat']
    s=d['source'];T=set(d['tags'])
    if s=='Podcast': return 'Podcasts'
    if s=='Newsletter': return 'Stories' if T&{'story','writing'} else 'Newsletters'
    if s=='Pick': return 'Stories' if T&STORY else ('Founders' if 'founders' in T else 'Tech')
    if s=='Essay': return 'Founders' if 'founders' in T else 'Tech'
    return 'Tech'
def score(d):
    if 'score' in d: return d['score']
    T=set(d['tags']);s={'Pick':4,'Essay':3,'Podcast':3,'Newsletter':1,'Instagram':0,'X':1}.get(d['source'],1)
    s+=2*len(T&STORY)+(3 if 'microdrama' in T else 0)
    s+=1 if d['minutes']>=7 else (-2 if d['minutes']<=3 else 0)
    s-=3 if T&{'news'} else 0
    return s
seen=set();out=[]
for d in D:
    if d['url'] in seen: continue
    seen.add(d['url']); d['id']=hashlib.md5(d['url'].encode()).hexdigest()[:8]; d['cat']=cat(d); out.append(d)
# This week: featured overrides, then best of newest ~10 days, one per author
latest=max(d['added'] for d in out); cut=(datetime.date.fromisoformat(latest)-datetime.timedelta(days=10)).isoformat()
pool=sorted([d for d in out if d.get('featured')],key=lambda d:d['added'],reverse=True)+sorted([d for d in out if d['added']>=cut and not d.get('featured')],key=lambda d:(-score(d),d['added']),reverse=False)
hero=[];auth=set()
for d in pool:
    if d['author'] in auth: continue
    hero.append(d['id']);auth.add(d['author'])
    if len(hero)==5: break
for d in out: d['hero']=d['id'] in hero
json.dump(out,open('library/items.json','w'),indent=1)
html=open('template.html').read().replace('/*DATA*/[]',json.dumps(out,ensure_ascii=False).replace('</','<\\/')).replace('/*HERO*/[]',json.dumps(hero))
open('library/index.html','w').write(html)
print(len(out),'items; this week:',[d['title'][:40] for i in hero for d in out if d['id']==i])
