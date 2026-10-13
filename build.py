import json,re
exec(open('items.py').read())
src=open('/workspace/ig/library/index.html').read()
css=src[src.find('<style>'):src.find('</style>')+8]
D=[dict(s=a,t=b,a=c,u=d,m=e,g=f,k=g,q=h) for a,b,c,d,e,f,g,h in ITEMS]
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reading Library — Pratik</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,500;6..72,600&display=swap" rel="stylesheet">'''+css+'''<style>.sec{display:flex;gap:8px;margin:0 0 14px}.sec .tag{font-size:14px;padding:7px 16px}.q{border-left:3px solid var(--acc);padding:12px 16px;background:var(--card);border-radius:8px;font:500 18px/1.4 Newsreader,Georgia,serif}textarea{width:100%;min-height:140px;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--ink);padding:14px;font:inherit}.card .cb{flex:1}.kick{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--acc)}</style></head><body>
<div class="wrap"><header><h1>Reading Library</h1><p id="sub"></p></header>
<div class="bar"><input id="q" placeholder="Search titles, authors, ideas…  ( / )"><button class="btn" id="tm">◐ Theme</button></div>
<div class="sec" id="secs"></div><div class="tags" id="tags"></div><div class="grid" id="grid"></div>
<footer>Curated for Pratik · Founder essays, podcast notes, tech essays. Notes are summaries; read the originals. Inspired by Gloss.</footer></div>
<div class="ov" id="ov"></div><aside class="pane" id="pane"></aside>
<script>const D='''+json.dumps(D,ensure_ascii=False)+''';
const $=s=>document.querySelector(s);let S='All',T=null;
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const host=u=>new URL(u).hostname.replace('www.','');
$('#sub').textContent=D.length+' hand-picked pieces to read, think about, and write back to. Each has key ideas and a question for your own take; notes are saved in your browser.';
function render(){const q=$('#q').value.toLowerCase();
$('#secs').innerHTML=['All','Founder essays','Podcast notes','Tech essays'].map(s=>`<span class="tag ${s==S?'on':''}" data-s="${s}">${s} · ${s=='All'?D.length:D.filter(d=>d.s==s).length}</span>`).join('');
const tg=[...new Set(D.filter(d=>S=='All'||d.s==S).flatMap(d=>d.g))].sort();
$('#tags').innerHTML=tg.map(t=>`<span class="tag ${t==T?'on':''}" data-t="${t}">#${t}</span>`).join('');
$('#grid').innerHTML=D.map((d,i)=>[d,i]).filter(([d])=>(S=='All'||d.s==S)&&(!T||d.g.includes(T))&&JSON.stringify(d).toLowerCase().includes(q)).map(([d,i])=>`<div class="card" data-i="${i}"><div class="cb"><div class="kick">${d.s}${localStorage['n'+i]?' · ✎ noted':''}</div><h3>${esc(d.t)}</h3><p>${esc(d.k[0])}</p></div><div class="cb" style="padding-top:0"><div class="meta"><span>${esc(d.a)}</span><span>${d.m} min</span></div></div></div>`).join('')}
function open_(i){const d=D[i];$('#pane').innerHTML=`<button class="btn x" onclick="cl()">✕</button><div class="kick">${d.s} · ${host(d.u)}</div><h2>${esc(d.t)}</h2><div class="row"><span>${esc(d.a)}</span><span class="pill">${d.m} min</span>${d.g.map(g=>`<span class="pill">#${g}</span>`).join('')}</div><p><a href="${d.u}" target="_blank" rel="noopener">Open original ↗</a></p><h4>Key ideas</h4><ul>${d.k.map(k=>`<li>${esc(k)}</li>`).join('')}</ul><h4>Question to reflect on</h4><div class="q">${esc(d.q)}</div><h4>Your take</h4><textarea id="nt" placeholder="Write your own opinion…">${esc(localStorage['n'+i]||'')}</textarea><div class="row" style="margin-top:8px"><button class="btn" onclick="navigator.clipboard.writeText('# '+D[${i}].t+'\\n'+D[${i}].q+'\\n\\n'+$('#nt').value)">Copy as markdown</button></div>`;
$('#nt').oninput=e=>localStorage['n'+i]=e.target.value;$('#pane').classList.add('on');$('#ov').classList.add('on')}
function cl(){$('#pane').classList.remove('on');$('#ov').classList.remove('on');render()}
document.addEventListener('click',e=>{const s=e.target.closest('[data-s]'),t=e.target.closest('[data-t]'),c=e.target.closest('.card');if(s){S=s.dataset.s;T=null;render()}else if(t){T=T==t.dataset.t?null:t.dataset.t;render()}else if(c)open_(+c.dataset.i)});
$('#ov').onclick=cl;$('#q').oninput=render;document.onkeydown=e=>{if(e.key=='/'&&document.activeElement.tagName!='TEXTAREA'&&document.activeElement.tagName!='INPUT'){e.preventDefault();$('#q').focus()}if(e.key=='Escape')cl()};
$('#tm').onclick=()=>{const r=document.documentElement;r.dataset.t=r.dataset.t=='dark'?'light':'dark'};render();</script></body></html>'''
open('library/index.html','w').write(html);json.dump(D,open('library/items.json','w'),indent=1,ensure_ascii=False)
