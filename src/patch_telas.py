"""Duas telas novas: Simulador de economia (Diretoria) e Reserva do pool (Diretoria, Gestor, Analista)."""
from pathlib import Path
p = Path(__file__).parent / "template.html"
s = p.read_text(encoding="utf-8")

def R(a, b, count=1):
    global s
    assert a in s, "não encontrado: " + a[:90]
    s = s.replace(a, b, count)

# ---------- perfis e rotas ----------
R('diretor:  {n:"Diretoria", d:"Tudo: economia, frota, ocorrências e custos.", views:["visao","ocorrencias","veiculos","veiculo","func","conectividade","dados"]},',
  'diretor:  {n:"Diretoria", d:"Tudo: economia, simulador, frota, ocorrências e custos.", views:["visao","simulador","ocorrencias","veiculos","pool","veiculo","func","conectividade","dados"]},')
R('gestor:   {n:"Gestor de unidade", d:"Frota, custos e ocorrências só da sua unidade.", views:["visao","ocorrencias","veiculos","veiculo","func"], unidade:true},',
  'gestor:   {n:"Gestor de unidade", d:"Frota, custos, ocorrências e reservas só da sua unidade.", views:["visao","ocorrencias","veiculos","pool","veiculo","func"], unidade:true},')
R('analista: {n:"Analista de frota", d:"Operação do dia a dia: veículos, trajetos, ocorrências e conectividade.", views:["ocorrencias","veiculos","veiculo","func","conectividade"]},',
  'analista: {n:"Analista de frota", d:"Operação do dia a dia: veículos, reservas do pool, trajetos e conectividade.", views:["ocorrencias","veiculos","pool","veiculo","func","conectividade"]},')
R('const views = ["visao","ocorrencias","veiculos","veiculo","func","conectividade","dados"];',
  'const views = ["visao","simulador","ocorrencias","veiculos","pool","veiculo","func","conectividade","dados"];')

# ---------- menu ----------
R('''    <a href="#ocorrencias" data-v="ocorrencias">''',
  '''    <a href="#simulador" data-v="simulador"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M20 18h0"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/></svg><span class="lg">Simulador</span><span class="sm">Simular</span></a>
    <a href="#ocorrencias" data-v="ocorrencias">''')
R('''    <a href="#conectividade" data-v="conectividade">''',
  '''    <a href="#pool" data-v="pool"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="m9 15 2 2 4-4"/></svg><span class="lg">Reservas do pool</span><span class="sm">Pool</span></a>
    <a href="#conectividade" data-v="conectividade">''')

# ---------- HTML das telas ----------
TELAS = '''<!-- SIMULADOR -->
<section class="view" id="v-simulador">
  <p class="lead">Ajuste as premissas e veja a economia recalculada na hora. Serve para testar cenários conservadores antes de decidir.</p>
  <div class="sim-grid">
    <div class="card sim-ctrl">
      <h2>Premissas</h2>
      <div class="sl"><label for="sRes">Reserva da frota <b id="sResV"></b></label><input type="range" id="sRes" min="0" max="25" step="1" value="8"><small>Folga para manutenção e imprevistos, acima do pico de uso.</small></div>
      <div class="sl"><label for="sPct">Dias cobertos sem faltar veículo <b id="sPctV"></b></label><input type="range" id="sPct" min="80" max="100" step="1" value="95"><small>100% dimensiona pelo dia de maior uso dos últimos 90 dias.</small></div>
      <div class="sl"><label for="sFora">Troca por carro: máx. do km fora do asfalto <b id="sForaV"></b></label><input type="range" id="sFora" min="5" max="40" step="1" value="15"><small>Acima disso, a caminhonete fica.</small></div>
      <div class="sl"><label for="sTal">Troca por carro: máx. de dias em talhão <b id="sTalV"></b></label><input type="range" id="sTal" min="5" max="50" step="1" value="20"><small>Quem vai a campo mais que isso mantém a caminhonete.</small></div>
      <div class="sl"><label for="sMulta">Multa da locadora por veículo devolvido <b id="sMultaV"></b></label><input type="range" id="sMulta" min="0" max="30000" step="1000" value="0"><small>Abatida da economia do primeiro ano.</small></div>
      <div class="sl"><label for="sInv">Valor do projeto (opcional)</label><input type="text" id="sInv" inputmode="numeric" placeholder="ex.: 500.000"><small>Para calcular em quantos meses a economia paga o projeto.</small></div>
      <button type="button" id="sReset" class="ghost">Voltar ao padrão</button>
    </div>
    <div class="sim-out">
      <div class="grid k4" id="simKpis"></div>
      <div class="card"><h2>De onde vem a economia</h2><div id="simComp"></div></div>
      <div class="card"><h2>E se a reserva mudar?</h2><p class="note" style="margin:0">Economia mensal com as outras premissas como estão.</p><div id="simSens"></div></div>
    </div>
  </div>
</section>

<!-- RESERVAS DO POOL -->
<section class="view" id="v-pool">
  <p class="lead">Quem trocou a caminhonete por carro reserva uma caminhonete compartilhada da unidade nos dias em que vai a campo. As reservas abaixo vêm dos dias de campo reais desses condutores.</p>
  <div class="card">
    <div class="pool-head">
      <div class="pool-sel"><label for="pUn" class="note">Unidade</label><select id="pUn"></select></div>
      <div class="pool-nav"><button type="button" id="pPrev" aria-label="Semana anterior">‹</button><b id="pSem"></b><button type="button" id="pNext" aria-label="Próxima semana">›</button></div>
    </div>
    <div class="grid k4" id="poolKpis"></div>
  </div>
  <div class="card">
    <h2>Agenda da semana</h2>
    <div class="tablewrap" style="max-height:none"><table class="pool-tbl" id="poolTbl"></table></div>
  </div>
  <div class="card">
    <h2>Nova reserva</h2>
    <form id="pForm" class="pool-form">
      <label>Condutor<select id="pCond"></select></label>
      <label>Dia<select id="pDia"></select></label>
      <label>Destino<select id="pTal"></select></label>
      <button type="submit" class="on">Reservar</button>
    </form>
    <p class="note" id="pMsg" role="status" style="margin:0"></p>
  </div>
</section>

'''
R('<!-- CONECTIVIDADE -->', TELAS + '<!-- CONECTIVIDADE -->')

# ---------- JS ----------
JS = r'''
/* ---------- simulador de economia ---------- */
function simular(o){
  const ehTroca=v=>v.tipo==="Caminhonete" && (v.terra+v.off)<o.fora && v.dias_talhao<o.tal;
  const fim=v=>ehTroca(v)?"Carro":v.tipo;
  const carEq=v=>1350+v.km/12.5*6.30+v.km/1000*55*(1+v.terra*1.2)+v.pedagio;
  const desm=new Set();
  [...new Set(V.map(v=>v.unidade))].forEach(u=>["Caminhonete","Carro","Van"].forEach(t=>{
    const g=V.filter(v=>v.unidade===u&&fim(v)===t); if(!g.length) return;
    const daily=[...Array(NDIAS).keys()].map(d=>g.filter(v=>v.usoD[d]).length).sort((a,b)=>a-b);
    const q=daily[Math.min(daily.length-1,Math.max(0,Math.ceil(o.pct*daily.length)-1))];
    const need=Math.min(g.length,Math.ceil(q*(1+o.res)));
    g.slice().sort((a,b)=>a.dias_uso-b.dias_uso).slice(0,g.length-need).forEach(v=>desm.add(v.id));
  }));
  let ecoT=0,ecoD=0,nT=0,nD=0,nDp=0;
  V.forEach(v=>{ if(desm.has(v.id)){ nD++; if(v.tipo==="Caminhonete") nDp++; ecoD+=v.fixo+0.3*v.manut; } else if(ehTroca(v)){ nT++; ecoT+=Math.max(0,v.total-carEq(v)); } });
  const mens=ecoT+ecoD, multas=(nD+nT)*o.multa;
  return {nT,nD,nDp,ecoT,ecoD,mens,ano:mens*12-multas,multas,frota:V.length-nD};
}
(function(){
  const el=id=>document.getElementById(id); if(!el("sRes")) return;
  const PAD={sRes:8,sPct:95,sFora:15,sTal:20,sMulta:0};
  const num=t=>+String(t||"").replace(/\D/g,"")||0;
  function ler(){ return {res:+sRes.value/100, pct:+sPct.value/100, fora:+sFora.value/100, tal:+sTal.value/100, multa:+sMulta.value}; }
  function render(){
    const o=ler(); sResV.textContent=sRes.value+"%"; sPctV.textContent=sPct.value+"%"; sForaV.textContent=sFora.value+"%"; sTalV.textContent=sTal.value+"%"; sMultaV.textContent=brl(+sMulta.value);
    const r=simular(o), base=simular({res:.08,pct:.95,fora:.15,tal:.20,multa:0});
    const inv=num(sInv.value); const pay=inv&&r.mens>0?Math.max(0,(inv+r.multas)/r.mens):null;
    const dif=r.mens-base.mens;
    el("simKpis").innerHTML=`
      <div class="card kpi hl"><span class="l">Economia por mês</span><span class="v">${brlk(r.mens)}</span><span class="s">${Math.abs(dif)<500?"igual ao cenário padrão":(dif>0?"+":"−")+brlk(Math.abs(dif))+" vs. padrão"}</span></div>
      <div class="card kpi"><span class="l">Economia no 1º ano</span><span class="v">${brlk(r.ano)}</span><span class="s">${r.multas?"já descontadas "+brlk(r.multas)+" de multas":"sem multa de devolução"}</span></div>
      <div class="card kpi"><span class="l">Frota necessária</span><span class="v">${r.frota} <small style="font-size:15px;color:var(--muted)">de ${V.length}</small></span><span class="s">${r.nD} desmobilizados · ${r.nT} trocas por carro</span></div>
      <div class="card kpi"><span class="l">${inv?"O projeto se paga em":"Retorno do projeto"}</span><span class="v">${pay==null?"—":pay<1?"< 1 mês":Math.ceil(pay)+" meses"}</span><span class="s">${inv?"investimento de "+brl(inv):"informe o valor do projeto"}</span></div>`;
    const mx=Math.max(r.ecoT,r.ecoD,1);
    el("simComp").innerHTML=[["Trocar caminhonete por carro",r.nT,r.ecoT,"--good","pessoas continuam com veículo, um carro"],["Desmobilizar veículos ociosos",r.nD,r.ecoD,"--sat","devolução à locadora; demanda passa para o pool"]].map(([t,n,e,c,d])=>`
      <div class="simrow"><div><b>${t}</b> <span class="note">· ${n} veículos</span><br><span class="note">${d}</span></div>
      <div class="bar" style="height:10px"><i style="width:${e/mx*100}%;background:var(${c})"></i></div><b class="num">${brl(e)}<span class="note" style="font-weight:400">/mês</span></b></div>`).join("");
    const cen=[0,5,8,12,15,20,25].map(rv=>({rv, r:simular({...o,res:rv/100})})); const mxs=Math.max(...cen.map(c=>c.r.mens),1);
    el("simSens").innerHTML=cen.map(c=>`<div class="sens ${c.rv===+sRes.value?"on":""}"><span class="num">${c.rv}% de reserva</span><div class="bar" style="height:8px"><i style="width:${c.r.mens/mxs*100}%;background:var(--accent)"></i></div><span class="num">${brlk(c.r.mens)}/mês</span></div>`).join("");
  }
  ["sRes","sPct","sFora","sTal","sMulta"].forEach(id=>el(id).addEventListener("input",render));
  sInv.addEventListener("input",()=>{ const n=num(sInv.value); sInv.value=n?n.toLocaleString("pt-BR"):""; render(); });
  sReset.addEventListener("click",()=>{ Object.entries(PAD).forEach(([k,v])=>el(k).value=v); sInv.value=""; render(); });
  render();
})();

/* ---------- reservas do pool ---------- */
(function(){
  const el=id=>document.getElementById(id); if(!el("pUn")) return;
  const uns=[...new Set(V.map(v=>v.unidade))];
  const MON=(()=>{ const t=dateOf(0); return (t.getDay()+6)%7; })(); // dia da semana (seg=0) do dia 0
  const semanas=[]; for(let s0=-MON; s0<NDIAS; s0+=7) semanas.push([...Array(7).keys()].map(i=>s0+i));
  let sem=semanas.length-1; const extra=[];
  // pedidos: dias em que quem trocou de caminhonete para carro foi a campo
  const POOL={};
  function montaUnidade(u){
    if(POOL[u]) return POOL[u];
    const cond=V.filter(v=>v.unidade===u && v.rec==="Trocar por carro");
    const pedidos={};
    cond.forEach(v=>{ for(let d=0;d<NDIAS;d++){ const P=planDay(v,d); const f=P.ev.find(e=>e.k==="field"); if(f){ (pedidos[d]=pedidos[d]||[]).push({v, ini:P.ev[0].t0, fim:P.ev.at(-1).t1, tal:f.at}); } } });
    const porDia=Object.values(pedidos).map(a=>a.length).sort((a,b)=>a-b);
    const K=Math.max(1, porDia.length?porDia[Math.floor(.9*(porDia.length-1))]:1);
    const frota=V.filter(v=>v.unidade===u && v.tipo==="Caminhonete" && (v.rec==="Desmobilizar"||v.rec==="Trocar por carro")).sort((a,b)=>a.id.localeCompare(b.id)).slice(0,K);
    while(frota.length<K) frota.push({id:"POOL-"+(frota.length+1), placa:"POOL "+(frota.length+1), tipo:"Caminhonete", unidade:u});
    const tals=TALHOES.filter(t=>t.base===({"Fábrica":"BL","UF Norte":"BN","UF Sul":"BS","UF Leste":"BL","UF Oeste":"BO"}[u])).map(t=>t.id);
    return POOL[u]={cond,pedidos,K,frota,tals};
  }
  function aloca(u,d){
    const P=montaUnidade(u); const lista=[...(P.pedidos[d]||[]), ...extra.filter(x=>x.u===u&&x.d===d)].sort((a,b)=>a.ini-b.ini);
    const ocup=P.frota.map(()=>[]); const espera=[];
    lista.forEach(r=>{ const i=ocup.findIndex(o=>o.every(x=>x.fim<=r.ini||x.ini>=r.fim)); if(i>=0) ocup[i].push(r); else espera.push(r); });
    return {ocup,espera};
  }
  function render(){
    const u=pUn.value; const P=montaUnidade(u); const dias=semanas[sem];
    pSem.textContent=`${fmtDia(Math.max(0,dias[0]))} a ${fmtDia(Math.min(NDIAS-1,dias[6]))}`;
    pPrev.disabled=sem===0; pNext.disabled=sem===semanas.length-1;
    const al=dias.map(d=>d>=0&&d<NDIAS?aloca(u,d):{ocup:P.frota.map(()=>[]),espera:[]});
    const nRes=al.reduce((s,a)=>s+a.ocup.reduce((x,o)=>x+o.length,0),0), nEsp=al.reduce((s,a)=>s+a.espera.length,0);
    const uteis=dias.filter(d=>d>=0&&d<NDIAS&&isWeekday(d)).length||1;
    const ocupDias=al.reduce((s,a,i)=>s+(isWeekday(dias[i])?a.ocup.filter(o=>o.length).length:0),0);
    el("poolKpis").innerHTML=`
      <div class="card kpi"><span class="l">Caminhonetes no pool</span><span class="v">${P.K}</span><span class="s">atendem ${P.cond.length} condutores que trocaram por carro</span></div>
      <div class="card kpi"><span class="l">Reservas na semana</span><span class="v">${nRes}</span><span class="s">dias de campo atendidos</span></div>
      <div class="card kpi"><span class="l">Ocupação em dias úteis</span><span class="v">${pct(ocupDias/(P.K*uteis))}</span><span class="s">das caminhonetes do pool</span></div>
      <div class="card kpi ${nEsp?"":"hl"}"><span class="l">Em espera</span><span class="v" style="${nEsp?"color:var(--warn)":""}">${nEsp}</span><span class="s">${nEsp?"pedidos sem caminhonete livre no horário":"ninguém ficou sem veículo"}</span></div>`;
    const chip=r=>`<button type="button" class="rchip ${r.novo?"novo":""}" data-vgo="${r.v.id}" title="${r.v.func?.nome||""} · ${hhmm(r.ini)}–${hhmm(r.fim)} · talhão ${r.tal}"><b>${(r.v.func?.nome||r.v.id).split(" ")[0]}</b><span>${hhmm(r.ini)}–${hhmm(r.fim)} · ${r.tal}</span></button>`;
    el("poolTbl").innerHTML=`<thead><tr><th>Caminhonete</th>${dias.map(d=>`<th class="${d>=0&&d<NDIAS&&!isWeekday(d)?"fds":""}">${d>=0&&d<NDIAS?fmtDia(d):""}</th>`).join("")}</tr></thead><tbody>
      ${P.frota.map((pv,i)=>`<tr><td><div class="vcell">${pv.fixo?vehPhoto(pv,"vp-xs"):""}<div class="vt">${placaHTML(pv.placa,true)}<span class="note">${pv.fixo?"ex-"+pv.id:"a definir"}</span></div></div></td>${al.map((a,j)=>`<td class="${dias[j]>=0&&dias[j]<NDIAS&&!isWeekday(dias[j])?"fds":""}">${(a.ocup[i]||[]).map(chip).join("")}</td>`).join("")}</tr>`).join("")}
      ${nEsp?`<tr class="esp"><td><b>Em espera</b></td>${al.map(a=>`<td>${a.espera.map(chip).join("")}</td>`).join("")}</tr>`:""}</tbody>`;
    pCond.innerHTML=P.cond.map(v=>`<option value="${v.id}">${v.func?.nome||v.id} · ${v.func?.cargo||""}</option>`).join("")||'<option value="">Nenhum condutor nesta unidade</option>';
    pDia.innerHTML=dias.filter(d=>d>=0&&d<NDIAS).map(d=>`<option value="${d}">${fmtDia(d)}</option>`).join("");
    pTal.innerHTML=P.tals.map(t=>`<option>Talhão ${t}</option>`).join("");
  }
  uns.forEach(u=>pUn.insertAdjacentHTML("beforeend",`<option>${u}</option>`));
  if(SESSAO&&SESSAO.unidade){ pUn.value=SESSAO.unidade; pUn.disabled=true; }
  pUn.addEventListener("change",()=>{ pMsg.textContent=""; render(); });
  pPrev.addEventListener("click",()=>{ if(sem>0){ sem--; render(); } });
  pNext.addEventListener("click",()=>{ if(sem<semanas.length-1){ sem++; render(); } });
  el("poolTbl").addEventListener("click",e=>{ const b=e.target.closest("[data-vgo]"); if(b) goVehicle(b.dataset.vgo); });
  pForm.addEventListener("submit",e=>{
    e.preventDefault(); const v=V.find(x=>x.id===pCond.value); if(!v) return;
    const d=+pDia.value, u=pUn.value, r={u,d,v,ini:7.5,fim:16,tal:pTal.value.replace("Talhão ",""),novo:true};
    extra.push(r); const a=aloca(u,d); const i=a.ocup.findIndex(o=>o.includes(r));
    const P=montaUnidade(u);
    pMsg.innerHTML = i>=0 ? `Reserva confirmada: <b>${v.func?.nome||v.id}</b> leva a caminhonete ${placaHTML(P.frota[i].placa,true)} em ${fmtDia(d)}, das 07:30 às 16:00.` : `Sem caminhonete livre em ${fmtDia(d)} das 07:30 às 16:00. O pedido de <b>${v.func?.nome||v.id}</b> entrou na lista de espera.`;
    render();
  });
  render();
})();
'''
R('/* ---------- login simulado e perfis ---------- */', JS + '\n/* ---------- login simulado e perfis ---------- */')

CSS = r'''
/* simulador */
.sim-grid{display:grid;grid-template-columns:340px minmax(0,1fr);gap:18px;align-items:start}
.sim-out{display:flex;flex-direction:column;gap:18px;min-width:0}
.sim-ctrl{gap:16px;position:sticky;top:72px}
.sl{display:flex;flex-direction:column;gap:6px}
.sl label{display:flex;justify-content:space-between;gap:10px;font-size:13.5px;font-weight:500}
.sl label b{font-variant-numeric:tabular-nums;color:var(--accent)}
.sl input[type=range]{accent-color:var(--accent);width:100%}
.sl small{color:var(--muted);font-size:12px}
.sl input[type=text]{padding:8px 10px}
.simrow{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(80px,1fr) 150px;gap:14px;align-items:center;padding:10px 0;border-top:1px solid var(--line2)}
.simrow>b{text-align:right}
.sens{display:grid;grid-template-columns:130px 1fr 110px;gap:12px;align-items:center;padding:5px 8px;border-radius:6px;font-size:13px}
.sens>span:last-child{text-align:right}
.sens.on{background:var(--accent-soft);font-weight:600}
@media (max-width:980px){ .sim-grid{grid-template-columns:1fr} .sim-ctrl{position:static} }
@media (max-width:640px){ .simrow{grid-template-columns:1fr auto} .simrow .bar{display:none} .sens{grid-template-columns:100px 1fr 90px} }
/* pool */
.pool-head{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;align-items:end}
.pool-sel{display:flex;flex-direction:column;gap:4px}
.pool-nav{display:flex;gap:10px;align-items:center}
.pool-nav button{width:32px;height:32px;padding:0;font-size:18px}
.pool-nav button:disabled{opacity:.35}
.pool-tbl th,.pool-tbl td{vertical-align:top;white-space:normal}
.pool-tbl th{white-space:nowrap}
.pool-tbl td{min-width:112px}
.pool-tbl td:first-child{min-width:150px}
.pool-tbl .fds{background:color-mix(in srgb,var(--line2) 60%,transparent)}
.pool-tbl tr.esp td{background:color-mix(in srgb,var(--warn) 6%,transparent)}
.rchip{display:flex;flex-direction:column;align-items:flex-start;gap:1px;width:100%;text-align:left;padding:5px 8px;margin:2px 0;border-radius:6px;border:1px solid color-mix(in srgb,var(--accent) 30%,var(--line));background:var(--accent-soft);font-size:12px;line-height:1.3}
.rchip span{color:var(--muted);font-size:11px}
.rchip.novo{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 25%,transparent)}
.esp .rchip{background:color-mix(in srgb,var(--warn) 10%,var(--surface));border-color:color-mix(in srgb,var(--warn) 40%,var(--line))}
.pool-form{display:flex;gap:12px;flex-wrap:wrap;align-items:end}
.pool-form label{display:flex;flex-direction:column;gap:4px;font-size:12.5px;color:var(--muted)}
.pool-form select{min-width:180px}
'''
R('</style>', CSS + '</style>')
p.write_text(s, encoding="utf-8")
print("ok")
