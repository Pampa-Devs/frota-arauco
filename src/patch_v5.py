"""v5: shell de produto (sidebar + busca global), visual limpo, fotos com placa e animação do trajeto."""
from pathlib import Path
p = Path(__file__).parent / "template.html"
s = p.read_text(encoding="utf-8")

def R(a, b, count=1):
    global s
    assert a in s, "não encontrado: " + a[:80]
    s = s.replace(a, b, count)

# ---------- fonte ----------
R('family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500', 'family=Figtree:wght@400;500;600;700')
R('<title>Frota Arauco — Protótipo</title>', '<title>Frota · Arauco</title>')

# ---------- cabeçalho -> sidebar + topbar ----------
i = s.index('<header>'); j = s.index('</header>') + len('</header>')
ICON = {
 "visao": '<path d="M3 13h7V3H3zM14 21h7V11h-7zM3 21h7v-5H3zM14 7h7V3h-7z"/>',
 "ocorrencias": '<path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/>',
 "veiculos": '<path d="M3 13l2-5a2 2 0 0 1 2-1.3h10A2 2 0 0 1 19 8l2 5v4h-2"/><path d="M5 17H3v-4h18"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/>',
 "conectividade": '<path d="M2 9a16 16 0 0 1 20 0M5 12.5a11 11 0 0 1 14 0M8.5 16a6 6 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
 "dados": '<path d="M4 5c0-1.1 3.6-2 8-2s8 .9 8 2-3.6 2-8 2-8-.9-8-2z"/><path d="M4 5v14c0 1.1 3.6 2 8 2s8-.9 8-2V5M4 12c0 1.1 3.6 2 8 2s8-.9 8-2"/>',
}
NAV = [("visao","Visão geral","Visão"),("ocorrencias","Ocorrências","Alertas"),("veiculos","Veículos","Veículos"),("conectividade","Conectividade","Conexão"),("dados","Dados","Dados")]
navhtml = "\n".join(f'    <a href="#{k}" data-v="{k}"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[k]}</svg><span class="lg">{lg}</span><span class="sm">{sm}</span></a>' for k,lg,sm in NAV)
s = s[:i] + f'''<aside class="side">
  <a class="brand" href="#visao" aria-label="Frota Arauco, início">
    <span class="logo" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2c4 3 6 6.5 6 10a6 6 0 0 1-12 0c0-3.5 2-7 6-10z"/><path d="M12 22V9"/></svg></span>
    <span class="bname">Frota<small>Arauco · Sucuriú</small></span>
  </a>
  <nav aria-label="Seções">
{navhtml}
  </nav>
  <div class="sidefoot">
    <button type="button" id="tourGo" class="ghost" title="Roteiro guiado; setas ou passador de slides para avançar"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>Apresentar</button>
    <span class="demo">Demonstração · dados simulados</span>
  </div>
</aside>
<div class="topbar">
  <div class="tb-title"><h1 id="pgTitle">Visão geral</h1><button type="button" class="info" id="pgInfo" aria-label="Sobre esta tela" hidden>i</button></div>
  <div class="gsearch">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="gq" type="search" placeholder="Buscar placa, veículo ou condutor" autocomplete="off" aria-label="Buscar placa, veículo ou condutor">
    <div class="gres" id="gres" role="listbox" hidden></div>
  </div>
  <span class="tb-meta">Dados até 11/11/2026</span>
</div>
<div class="popover" id="pop" role="dialog" hidden></div>''' + s[j:]

# ---------- CSS novo (sobrescreve o anterior) ----------
CSS = r'''
/* ===== v5: visual de produto ===== */
:root{
  --bg:#f5f6f4; --surface:#ffffff; --ink:#151b18; --muted:#6a746e; --line:#e5e8e4; --line2:#eef0ed;
  --accent:#15603f; --accent-soft:#e7f1eb;
  --display:"Figtree", system-ui, sans-serif; --body:"Figtree", system-ui, sans-serif; --mono:"Figtree", system-ui, sans-serif;
  --side:232px; --radius:12px;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){ --bg:#0f1311; --surface:#161b18; --ink:#e8ece9; --muted:#97a19b; --line:#252c28; --line2:#1c221f; --accent:#4fbf8a; --accent-soft:#183326; } }
:root[data-theme="dark"]{ --bg:#0f1311; --surface:#161b18; --ink:#e8ece9; --muted:#97a19b; --line:#252c28; --line2:#1c221f; --accent:#4fbf8a; --accent-soft:#183326; }
body{font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased;padding-left:var(--side)}
.mono{font-family:var(--body);font-variant-numeric:tabular-nums;letter-spacing:.01em}
h1,h2,h3{letter-spacing:-.01em}
h2{font-size:16px;font-weight:650} h3{font-size:14px;font-weight:650}
/* sidebar */
.side{position:fixed;inset:0 auto 0 0;width:var(--side);background:var(--surface);border-right:1px solid var(--line);display:flex;flex-direction:column;padding:18px 12px;gap:18px;z-index:30}
.brand{display:flex;gap:10px;align-items:center;text-decoration:none;color:var(--ink);padding:4px 8px}
.logo{width:32px;height:32px;border-radius:9px;background:var(--accent);display:grid;place-items:center}
.logo svg{width:18px;height:18px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.bname{font-weight:700;font-size:16px;line-height:1.1;display:flex;flex-direction:column}
.bname small{font-weight:500;font-size:12px;color:var(--muted)}
.side nav{display:flex;flex-direction:column;gap:2px;margin:0;overflow:visible}
.side nav a{display:flex;align-items:center;gap:10px;padding:9px 10px;border-radius:8px;border:none;color:var(--muted);font-weight:500;font-size:14px}
.side nav a svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}
.side nav a:hover{background:var(--line2);color:var(--ink)}
.side nav a.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
.side nav a .sm{display:none}
.sidefoot{margin-top:auto;display:flex;flex-direction:column;gap:8px;padding:0 6px}
.sidefoot .demo{font-size:11.5px;color:var(--muted)}
button.ghost{display:inline-flex;gap:8px;align-items:center;justify-content:center;background:var(--surface);border:1px solid var(--line);color:var(--ink);font-weight:600}
button.ghost svg{width:14px;height:14px;fill:currentColor}
/* topbar */
.topbar{position:sticky;top:0;z-index:20;display:flex;align-items:center;gap:16px;padding:12px 28px;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.tb-title{display:flex;align-items:center;gap:8px;min-width:0}
.tb-title h1{font-size:19px;font-weight:700;margin:0;white-space:nowrap}
.tb-meta{margin-left:auto;color:var(--muted);font-size:12.5px;white-space:nowrap}
.gsearch{position:relative;flex:1;max-width:420px;margin-left:12px}
.gsearch>svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:16px;height:16px;fill:none;stroke:var(--muted);stroke-width:2}
.gsearch input{width:100%;padding:8px 12px 8px 34px;border-radius:9px;border:1px solid var(--line);background:var(--surface);font-size:14px}
.gres{position:absolute;top:calc(100% + 6px);left:0;right:0;background:var(--surface);border:1px solid var(--line);border-radius:10px;box-shadow:0 12px 32px rgba(0,0,0,.12);padding:6px;max-height:420px;overflow:auto}
.gres button{display:flex;gap:10px;align-items:center;width:100%;text-align:left;border:none;background:none;padding:6px 8px;border-radius:7px}
.gres button:hover,.gres button.on{background:var(--accent-soft)}
.gres .vph.xs{width:56px;flex:none}
.gres .gh{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding:6px 8px 2px}
.info{width:20px;height:20px;padding:0;border-radius:50%;font-size:12px;font-weight:700;font-style:italic;font-family:Georgia,serif;color:var(--muted);background:var(--surface);border:1px solid var(--line);display:inline-grid;place-items:center;flex:none;line-height:1}
.info:hover{color:var(--accent);border-color:var(--accent)}
.popover{position:fixed;z-index:60;max-width:340px;background:var(--ink);color:var(--surface);font-size:13px;line-height:1.5;padding:10px 12px;border-radius:9px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
main{max-width:1320px;padding:24px 28px 40px}
/* cartões e elementos */
.card{border-radius:var(--radius);border:1px solid var(--line);box-shadow:0 1px 2px rgba(16,24,20,.04);padding:18px 20px}
.lead{display:none}
.kpi .v{font-size:26px;letter-spacing:-.02em}
.kpi.hl{border-left:1px solid var(--line);background:linear-gradient(180deg,var(--accent-soft),var(--surface) 70%)}
.pill{border-radius:6px;font-weight:600}
button{border-radius:8px}
button.on{background:var(--accent);border-color:var(--accent)}
.tablewrap{border-radius:var(--radius)}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;font-weight:600}
td{border-bottom-color:var(--line2)}
.sim{display:none}
/* foto do veículo com placa */
.vph{position:relative;margin:0;border-radius:10px;overflow:hidden;background:linear-gradient(160deg,#dfe4e0,#c9d0cb);aspect-ratio:16/10;color:#8b958f}
.vph-img,.vph-img>img,.vph-img>svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.vph-img>img{object-fit:cover}
.vph .sil{display:none;padding:18% 10% 10%;fill:currentColor}
.vph.nofoto .sil{display:block} .vph.nofoto .vph-img>img{display:none}
.vph .placa{position:absolute;left:8px;bottom:8px}
.vph.lg{width:260px;flex:none} .vph.md{width:120px;flex:none} .vph.sm{width:72px;flex:none;border-radius:7px} .vph.xs{width:56px;border-radius:6px}
.vph.sm .placa,.vph.xs .placa,.vph.md .placa{display:none}
.placa{display:inline-flex;flex-direction:column;align-items:stretch;background:#fff;border:1.5px solid #222;border-radius:4px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.25);line-height:1;vertical-align:middle}
.placa i{background:#1c4e9e;color:#fff;font-style:normal;font-size:7px;font-weight:700;letter-spacing:.14em;text-align:center;padding:2px 0 1px}
.placa b{font-size:17px;letter-spacing:.07em;color:#111;padding:3px 9px 2px;font-weight:700;font-variant-numeric:tabular-nums}
.placa.mini i{font-size:5.5px;padding:1.5px 0 1px} .placa.mini b{font-size:12px;padding:2px 6px 1px}
.vcell{display:flex;gap:10px;align-items:center}
.vcell .vt{display:flex;flex-direction:column;gap:3px;align-items:flex-start}
.vhead{display:flex;gap:18px;align-items:center;flex-wrap:wrap}
.vtitle{font-size:24px;margin:0 0 2px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.og-v{display:flex;gap:10px;align-items:center}
/* animação do trajeto */
.slider .play{width:34px;height:34px;padding:0;border-radius:50%;display:grid;place-items:center;flex:none;background:var(--accent);border-color:var(--accent);color:#fff}
.slider .play svg{width:14px;height:14px;fill:currentColor}
.slider select{padding:5px 6px;font-size:13px}
#vmark .pulse{transform-box:fill-box;transform-origin:center}
.animando #vmark .pulse{animation:pulse 1.4s ease-out infinite}
@keyframes pulse{from{opacity:.35;transform:scale(.6)}to{opacity:0;transform:scale(1.6)}}
/* celular: barra inferior */
@media (max-width:860px){
  body{padding-left:0;padding-bottom:64px}
  .side{inset:auto 0 0 0;width:auto;height:60px;flex-direction:row;padding:0;border-right:none;border-top:1px solid var(--line)}
  .side .brand,.sidefoot{display:none}
  .side nav{flex-direction:row;flex:1;justify-content:space-around}
  .side nav a{flex-direction:column;gap:2px;padding:7px 4px;font-size:11px;flex:1;border-radius:0}
  .side nav a.on{background:none}
  .side nav a .lg{display:none} .side nav a .sm{display:inline}
  .topbar{flex-wrap:wrap;padding:10px 14px;gap:8px}
  .tb-meta{display:none}
  .gsearch{order:3;flex-basis:100%;max-width:none;margin:0}
  main{padding:14px}
  .vph.lg{width:100%}
}
@media (prefers-reduced-motion: reduce){ .animando #vmark .pulse{animation:none} }
'''
R('</style>', CSS + '</style>')

# ---------- foto do veículo ----------
FOTO_JS = r'''
/* ---------- foto do veículo com placa ---------- */
// caminhonetes: fotos embutidas (Wikimedia Commons, placas borradas). Carros e vans: Wikimedia Commons por link, com ilustração de reserva.
const FOTO_COMMONS = {
  "Fiat Cronos":"Fiat_Cronos_1.8_16V_E.Torq_Precision.jpg",
  "Volkswagen Virtus":"VW_Virtus_MSI_(Brazil,_front_view).png",
  "Chevrolet Onix":"Chevrolet_Onix_006.jpg",
  "Renault Master":"Renault_master.JPG",
  "Mercedes-Benz Sprinter":"P6010008_small.jpg",
};
const commonsURL = f => "https://commons.wikimedia.org/wiki/Special:FilePath/"+encodeURIComponent(f)+"?width=480";
const SIL = {
  Caminhonete:'<path d="M4 46V31l40-1 10-12h26l14 13 14 3 4 12z"/><circle cx="26" cy="47" r="8"/><circle cx="92" cy="47" r="8"/>',
  Carro:'<path d="M4 46l2-10 22-3 14-12h32l16 12 20 3 2 10z"/><circle cx="28" cy="47" r="8"/><circle cx="94" cy="47" r="8"/>',
  Van:'<path d="M4 46V14q0-4 4-4h82l20 22 6 4v10z"/><circle cx="28" cy="47" r="8"/><circle cx="96" cy="47" r="8"/>',
};
const placaHTML = (p, mini) => `<span class="placa${mini?" mini":""}" aria-label="Placa ${p}"><i>BRASIL</i><b>${p}</b></span>`;
function vehPhoto(v, cls=""){
  const F=fichaOf(v); let img="";
  if(v.tipo==="Caminhonete"){ const op=/SW4/.test(F.modelo)?["c5","c6"]:["c1","c2"]; img=`<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><use href="#ft-${op[hashStr(v.id)%2]}"/></svg>`; }
  else { const k=Object.keys(FOTO_COMMONS).find(m=>F.modelo.startsWith(m)); if(k) img=`<img src="${commonsURL(FOTO_COMMONS[k])}" alt="" loading="lazy" referrerpolicy="no-referrer" onerror="this.closest('.vph').classList.add('nofoto')">`; }
  return `<figure class="vph ${cls} ${img?"":"nofoto"}" title="${F.modelo} · ${v.placa}"><div class="vph-img">${img}<svg class="sil" viewBox="0 0 124 56" aria-hidden="true">${SIL[v.tipo]||SIL.Carro}</svg></div>${placaHTML(v.placa)}</figure>`;
}
'''
R('/* ---------- km, terreno e custo', FOTO_JS + '\n/* ---------- km, terreno e custo')

# tabela de veículos: foto + placa
R('''      <td><b class="mono">${v.id}</b> <span class="note mono">${v.placa}</span>${v.flags.length?''',
  '''      <td><div class="vcell">${vehPhoto(v,"sm")}<div class="vt">${placaHTML(v.placa,true)}<span class="note">${v.id}</span></div></div>${v.flags.length?''')
# ocorrências: foto + placa
R('''<span class="og-v"><b class="mono">${v.id}</b> <span class="mono">${v.placa}</span><br><span class="note">${v.tipo} · ${v.unidade}</span></span>''',
  '''<span class="og-v">${vehPhoto(v,"sm")}<span class="vt">${placaHTML(v.placa,true)}<span class="note">${v.id} · ${v.tipo} · ${v.unidade}</span></span></span>''')
# cabeçalho da página do veículo
R('''<div><h1 style="font-size:24px"><span class="mono">${v.id}</span> · <span class="mono">${v.placa}</span></h1><span class="note">${v.tipo} · ${v.unidade} · condutor: <a href="#func-${v.func.mat}">${v.func.nome}</a>, ${v.func.cargo}</span></div>''',
  '''<div class="vhead">${vehPhoto(v,"lg")}<div><h1 class="vtitle">${v.id} ${placaHTML(v.placa)}</h1><span class="note">${fichaOf(v).modelo} · ${fichaOf(v).cor} · ${v.unidade}</span><br><span class="note">Condutor: <a href="#func-${v.func.mat}">${v.func.nome}</a>, ${v.func.cargo}</span></div></div>''')

# ---------- animação do trajeto ----------
R('''<div class="slider"><label for="rtT" class="note">Horário</label><input type="range" id="rtT" min="0" max="1000" value="1000">''',
  '''<div class="slider"><button type="button" class="play" id="rtPlay" aria-label="Reproduzir o trajeto"><svg viewBox="0 0 24 24"><path d="M7 4v16l13-8z"/></svg></button><label for="rtT" class="note">Horário</label><input type="range" id="rtT" min="0" max="10000" value="10000">''')
R('<span class="mono num" id="rtTl"></span>', '<span class="mono num" id="rtTl"></span><select id="rtSpd" aria-label="Velocidade da reprodução"><option value="0.12">1×</option><option value="0.3" selected>2×</option><option value="0.7">5×</option></select>')
R('sl.value=Math.round((RT.tSel-t0)/(t1-t0)*1000); RT.tSel=null; } now=t0+(t1-t0)*sl.value/1000;',
  'sl.value=Math.round((RT.tSel-t0)/(t1-t0)*sl.max); RT.tSel=null; } now=(ANIM.on&&ANIM.now!=null)?ANIM.now:t0+(t1-t0)*sl.value/sl.max;')
R('''  if(!all && pts.length){ const pos=[...pts].reverse().find(q=>q.t<=now)||pts[0]; s+=`<circle cx="${pos.p[0]}" cy="${pos.p[1]}" r="${9*k*1.6}" fill="var(--ink)" stroke="var(--surface)" stroke-width="3" ${NS}/>`; }''',
  '''  RT.ptsDay = all ? null : pts; RT.kMap=k;
  if(!all && pts.length){ const m=markerAt(Math.min(now,pts.at(-1).t)); if(m) s+=vmarkSVG(m,k); }''')
ANIM_JS = r'''
/* ---------- animação: veículo andando no trajeto ---------- */
const ANIM={on:false,raf:0,last:0,lastFull:0,now:null};
function markerAt(now){
  const pts=RT.ptsDay; if(!pts||!pts.length) return null;
  let i=pts.findIndex(q=>q.t>now); if(i===-1) i=pts.length-1; if(i===0) i=1; if(pts.length<2) return {x:pts[0].p[0],y:pts[0].p[1],ang:0,parado:true};
  const a=pts[i-1], b=pts[i]; const f=b.t>a.t?Math.min(1,Math.max(0,(now-a.t)/(b.t-a.t))):1;
  const x=a.p[0]+(b.p[0]-a.p[0])*f, y=a.p[1]+(b.p[1]-a.p[1])*f;
  let j=i; while(j<pts.length-1 && Math.hypot(pts[j].p[0]-a.p[0],pts[j].p[1]-a.p[1])<0.05) j++;
  const c=pts[j]; const mov=Math.hypot(c.p[0]-a.p[0],c.p[1]-a.p[1])>=0.05;
  if(mov) RT.lastAng=Math.atan2(c.p[1]-a.p[1],c.p[0]-a.p[0])*180/Math.PI;
  return {x,y,ang:RT.lastAng||0,parado:(a.stop&&b.stop)||Math.hypot(b.p[0]-a.p[0],b.p[1]-a.p[1])<0.05};
}
function vmarkSVG(m,k){
  const r=10*k*1.6, NS='vector-effect="non-scaling-stroke"';
  return `<g id="vmark" transform="translate(${m.x.toFixed(2)} ${m.y.toFixed(2)})" pointer-events="none">
    <circle class="pulse" r="${(r*2.2).toFixed(2)}" fill="var(--accent)" opacity=".25"/>
    <g class="vm-rot" transform="rotate(${m.ang.toFixed(1)})"><circle r="${r.toFixed(2)}" fill="var(--accent)" stroke="#fff" stroke-width="2.5" ${NS}/><path d="M${(-r*.42).toFixed(2)},${(-r*.5).toFixed(2)} L${(r*.62).toFixed(2)},0 L${(-r*.42).toFixed(2)},${(r*.5).toFixed(2)} L${(-r*.12).toFixed(2)},0 Z" fill="#fff"/></g>
    <g transform="translate(0 ${(-r*2.3).toFixed(2)})"><rect x="${(-r*2.7).toFixed(2)}" y="${(-r*.8).toFixed(2)}" width="${(r*5.4).toFixed(2)}" height="${(r*1.6).toFixed(2)}" rx="${(r*.25).toFixed(2)}" fill="#fff" stroke="#222" stroke-width="1.2" ${NS}/><rect x="${(-r*2.7).toFixed(2)}" y="${(-r*.8).toFixed(2)}" width="${(r*5.4).toFixed(2)}" height="${(r*.42).toFixed(2)}" fill="#1c4e9e"/><text y="${(r*.58).toFixed(2)}" text-anchor="middle" font-size="${(r*.95).toFixed(2)}" style="fill:#111;font-weight:700;letter-spacing:.05em">${RT.v.placa}</text></g>
  </g>`;
}
function setPlayIcon(){ const b=document.getElementById("rtPlay"); if(!b) return; b.innerHTML=ANIM.on?'<svg viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>':'<svg viewBox="0 0 24 24"><path d="M7 4v16l13-8z"/></svg>'; b.setAttribute("aria-label",ANIM.on?"Pausar":"Reproduzir o trajeto"); const m=document.getElementById("rtMap"); if(m) m.classList.toggle("animando",ANIM.on); }
function stopAnim(){ if(!ANIM.on) return; ANIM.on=false; cancelAnimationFrame(ANIM.raf); ANIM.now=null; setPlayIcon(); }
function startAnim(){
  const sl=document.getElementById("rtT"), pts=RT.ptsDay; if(!sl||!pts||pts.length<2) return;
  const t0=pts[0].t, t1=pts.at(-1).t; let now=t0+(t1-t0)*sl.value/sl.max; if(now>=t1-1e-6) now=t0;
  ANIM.on=true; ANIM.now=now; ANIM.last=0; ANIM.lastFull=0; setPlayIcon(); drawRoute(); ANIM.raf=requestAnimationFrame(animTick);
}
function animTick(ts){
  if(!ANIM.on) return;
  const sl=document.getElementById("rtT"), pts=RT.ptsDay; if(!sl||!pts||!document.getElementById("rtPlay")){ ANIM.on=false; return; }
  const t0=pts[0].t, t1=pts.at(-1).t, dt=ANIM.last?Math.min(0.1,(ts-ANIM.last)/1000):0; ANIM.last=ts;
  const spd=+(document.getElementById("rtSpd")?.value||0.3); let m=markerAt(ANIM.now);
  ANIM.now=Math.min(t1, ANIM.now + dt*spd*(m&&m.parado?8:1));
  sl.value=Math.round((ANIM.now-t0)/(t1-t0)*sl.max); rtTl.textContent=hhmm(ANIM.now);
  m=markerAt(ANIM.now); const g=document.getElementById("vmark");
  if(g&&m){ g.setAttribute("transform",`translate(${m.x.toFixed(2)} ${m.y.toFixed(2)})`); g.querySelector(".vm-rot").setAttribute("transform",`rotate(${m.ang.toFixed(1)})`); }
  if(ts-ANIM.lastFull>600){ ANIM.lastFull=ts; drawRoute(); }
  if(ANIM.now>=t1){ ANIM.on=false; ANIM.now=null; drawRoute(); setPlayIcon(); return; }
  ANIM.raf=requestAnimationFrame(animTick);
}
document.addEventListener("click",e=>{
  if(e.target.closest("#rtPlay")){ ANIM.on?stopAnim():startAnim(); return; }
  if(e.target.closest(".dayrow,.mc,[data-mode],[data-zoom],.tl,.occi,[data-vgo],nav a")) stopAnim();
},true);
document.addEventListener("input",e=>{ if(e.target.id==="rtT" && ANIM.on && e.isTrusted) stopAnim(); },true);
addEventListener("hashchange",stopAnim);
'''
R('function drawRoute(){', ANIM_JS + '\nfunction drawRoute(){')

# ---------- busca global, título da página e textos explicativos recolhidos ----------
SHELL_JS = r'''
/* ---------- shell: título, busca global e textos recolhidos em "i" ---------- */
(function(){
  const pop=document.getElementById("pop");
  const showPop=(btn,txt)=>{ if(!pop.hidden && pop._b===btn){ pop.hidden=true; return; } pop.textContent=txt; pop.hidden=false; pop._b=btn; const r=btn.getBoundingClientRect(); const w=Math.min(340,innerWidth-24); pop.style.maxWidth=w+"px"; pop.style.left=Math.max(12,Math.min(r.left,innerWidth-w-12))+"px"; pop.style.top=(r.bottom+8)+"px"; };
  document.addEventListener("click",e=>{ const b=e.target.closest("button.info"); if(b){ e.stopPropagation(); showPop(b,b.dataset.tip); return; } if(!e.target.closest("#pop")) pop.hidden=true; });
  addEventListener("scroll",()=>{ pop.hidden=true; },{passive:true});
  // título da tela + "i" com a explicação que antes ficava em parágrafo
  const pgTitle=document.getElementById("pgTitle"), pgInfo=document.getElementById("pgInfo");
  function titulo(){
    const h=location.hash.replace("#","");
    let t=document.querySelector("nav a.on .lg")?.textContent||"Frota";
    if(h.startsWith("veiculo-")) t="Veículo "+h.slice(8);
    if(h.startsWith("func-")) t="Condutor";
    pgTitle.textContent=t;
    const lead=document.querySelector("section.view.on > p.lead");
    pgInfo.hidden=!lead; if(lead){ pgInfo.dataset.tip=lead.textContent.trim(); }
    document.title=t+" · Frota Arauco";
  }
  addEventListener("hashchange",()=>setTimeout(titulo)); setTimeout(titulo);
  // parágrafo explicativo logo abaixo do título de um cartão vira um "i" ao lado do título
  function recolhe(root){
    root.querySelectorAll(".card h2").forEach(h=>{
      if(h.dataset.rec) return; h.dataset.rec=1;
      const card=h.closest(".card"); let box=h; while(box.parentElement && box.parentElement!==card) box=box.parentElement;
      const p=box===h?h.nextElementSibling:box.nextElementSibling;
      if(!p||p.tagName!=="P"||!p.classList.contains("note")||p.querySelector("a,button,b,input")) return;
      const txt=p.textContent.trim(); if(txt.length<50) return;
      const b=document.createElement("button"); b.type="button"; b.className="info"; b.textContent="i"; b.dataset.tip=txt; b.setAttribute("aria-label","Como ler: "+txt.slice(0,60));
      h.style.display="inline-flex"; h.style.alignItems="center"; h.style.gap="8px"; h.appendChild(b); p.hidden=true;
    });
  }
  let pend=0; new MutationObserver(()=>{ if(pend) return; pend=requestAnimationFrame(()=>{ pend=0; recolhe(document.querySelector("main")); }); }).observe(document.querySelector("main"),{childList:true,subtree:true});
  recolhe(document.querySelector("main"));
  // busca global
  const q=document.getElementById("gq"), res=document.getElementById("gres"); let sel=0, itens=[];
  const norm=t=>t.normalize("NFD").replace(/[̀-ͯ]/g,"").toUpperCase().replace(/[^A-Z0-9 ]/g,"");
  function busca(){
    const t=norm(q.value).trim(); if(t.length<2){ res.hidden=true; return; }
    const tc=t.replace(/ /g,"");
    const vs=V.filter(v=>norm(v.placa).includes(tc)||norm(v.id).replace(/ /g,"").includes(tc)).slice(0,6);
    const fs=V.filter(v=>v.func&&norm(v.func.nome).includes(t)).slice(0,5);
    itens=[...vs.map(v=>({h:"#veiculo-"+v.id,html:`${vehPhoto(v,"xs")}<span>${placaHTML(v.placa,true)} <span class="note">${v.id} · ${v.tipo} · ${v.unidade}</span></span>`})), ...fs.map(v=>({h:"#func-"+v.func.mat,html:`<span class="logo" style="width:28px;height:28px;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-weight:700;font-size:12px">${v.func.nome.split(" ").map(x=>x[0]).slice(0,2).join("")}</span><span><b>${v.func.nome}</b><br><span class="note">${v.func.cargo} · ${v.id}</span></span>`}))];
    sel=0;
    res.innerHTML = itens.length ? (vs.length?`<div class="gh">Veículos</div>`:"")+itens.map((it,i)=>(i===vs.length&&fs.length?`<div class="gh">Condutores</div>`:"")+`<button type="button" role="option" data-h="${it.h}" class="${i===0?"on":""}">${it.html}</button>`).join("") : `<div class="note" style="padding:8px">Nada encontrado para "${q.value}".</div>`;
    res.hidden=false;
  }
  const vai=h=>{ res.hidden=true; q.value=""; q.blur(); location.hash=h; };
  q.addEventListener("input",busca);
  q.addEventListener("keydown",e=>{ const bs=[...res.querySelectorAll("button")]; if(e.key==="ArrowDown"||e.key==="ArrowUp"){ e.preventDefault(); sel=(sel+(e.key==="ArrowDown"?1:-1)+bs.length)%bs.length; bs.forEach((b,i)=>b.classList.toggle("on",i===sel)); } else if(e.key==="Enter"&&bs[sel]){ vai(bs[sel].dataset.h); } else if(e.key==="Escape"){ res.hidden=true; } });
  res.addEventListener("click",e=>{ const b=e.target.closest("button[data-h]"); if(b) vai(b.dataset.h); });
  document.addEventListener("click",e=>{ if(!e.target.closest(".gsearch")) res.hidden=true; });
  document.addEventListener("keydown",e=>{ if(e.key==="/"&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){ e.preventDefault(); q.focus(); } });
})();
'''
R('</body>', '<script>' + SHELL_JS + '</script>\n</body>')

p.write_text(s, encoding="utf-8")
print("ok")
