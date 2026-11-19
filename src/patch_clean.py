"""Branch clean-minimal: visual minimalista + login simulado com perfis de usuário."""
from pathlib import Path
p = Path(__file__).parent / "template.html"
s = p.read_text(encoding="utf-8")

def R(a, b, count=1):
    global s
    assert a in s, "não encontrado: " + a[:90]
    s = s.replace(a, b, count)

# ---------- sessão e perfis (antes de qualquer cálculo, para o gestor ver só a sua unidade) ----------
R('const RES = __RES__;', r'''const RES = __RES__;
/* ---------- sessão simulada: login e perfil de usuário ---------- */
const PERFIS = {
  diretor:  {n:"Diretoria", d:"Tudo: economia, frota, ocorrências e custos.", views:["visao","ocorrencias","veiculos","veiculo","func","conectividade","dados"]},
  gestor:   {n:"Gestor de unidade", d:"Frota, custos e ocorrências só da sua unidade.", views:["visao","ocorrencias","veiculos","veiculo","func"], unidade:true},
  analista: {n:"Analista de frota", d:"Operação do dia a dia: veículos, trajetos, ocorrências e conectividade.", views:["ocorrencias","veiculos","veiculo","func","conectividade"]},
  seguranca:{n:"Segurança e compliance", d:"Ocorrências de conduta e histórico de trajetos.", views:["ocorrencias","veiculo","func"]},
};
const SESSAO = (()=>{ try{ const x=JSON.parse(sessionStorage.getItem("frota.sessao")||"null"); return x&&PERFIS[x.perfil]?x:null; }catch(e){ return null; } })();
if(SESSAO && SESSAO.perfil==="gestor" && SESSAO.unidade){ for(let i=V.length-1;i>=0;i--) if(V[i].unidade!==SESSAO.unidade) V.splice(i,1); }
const podeVer = h => !SESSAO || PERFIS[SESSAO.perfil].views.includes(h);''')

# frota por tipo coerente com o recorte do gestor
R('  ["Caminhonete","Carro","Van"].forEach(t=>{ RES.porTipo[t].necessaria = V.filter(v=>v.rec!=="Desmobilizar" && fim(v)===t).length; });',
  '  ["Caminhonete","Carro","Van"].forEach(t=>{ RES.porTipo[t].atual = V.filter(v=>v.tipo===t).length; RES.porTipo[t].necessaria = V.filter(v=>v.rec!=="Desmobilizar" && fim(v)===t).length; });')

# roteador respeita o perfil
R('''  if(!views.includes(h) || h==="veiculo"&&!vid || h==="func"&&!fid) h = "visao";''',
  '''  if(!views.includes(h) || h==="veiculo"&&!vid || h==="func"&&!fid) h = "visao";
  if(!podeVer(h)){ h = PERFIS[SESSAO.perfil].views[0]; vid=null; fid=null; history.replaceState(null,"","#"+h); }''')

# ---------- tela de login ----------
LOGIN = '''<div class="login" id="login" hidden>
  <div class="login-l">
    <div class="brand"><span class="logo" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M12 2c4 3 6 6.5 6 10a6 6 0 0 1-12 0c0-3.5 2-7 6-10z"/><path d="M12 22V9"/></svg></span><span class="bname">Frota<small>Arauco · Sucuriú</small></span></div>
    <form id="lgForm" class="lg-form" novalidate>
      <h1>Entrar</h1>
      <label for="lgEmail">E-mail corporativo</label>
      <input id="lgEmail" type="email" autocomplete="username" placeholder="nome@empresa.com.br" required>
      <label for="lgSenha">Senha</label>
      <input id="lgSenha" type="password" autocomplete="current-password" placeholder="••••••••" required>
      <fieldset class="lg-perfis"><legend>Perfil de acesso</legend><div id="lgPerfis"></div></fieldset>
      <div id="lgUnBox" hidden><label for="lgUn">Unidade</label><select id="lgUn"></select></div>
      <p class="lg-erro" id="lgErro" role="alert" hidden></p>
      <button type="submit" class="lg-btn">Entrar</button>
      <p class="note lg-demo">Ambiente de demonstração com dados simulados. Qualquer e-mail e senha funcionam.</p>
    </form>
  </div>
  <div class="login-r" aria-hidden="true">
    <div class="lr-in">
      <p class="lr-k">420 veículos · 5 unidades · 90 dias</p>
      <p class="lr-t">A frota inteira, num lugar só.</p>
      <p class="lr-s">Uso real de cada veículo, custo por quilômetro, ocorrências e o tamanho certo da frota.</p>
    </div>
  </div>
</div>
'''
R('<aside class="side">', LOGIN + '<aside class="side">')

# rodapé do menu: usuário logado
R('''    <span class="demo">Demonstração · dados simulados</span>''',
  '''    <div class="me" id="me" hidden><span class="av" id="meAv"></span><span class="me-t"><b id="meNome"></b><small id="mePerfil"></small></span><button type="button" class="me-out" id="meSair" title="Sair" aria-label="Sair"><svg viewBox="0 0 24 24"><path d="M15 4h4v16h-4M10 8l-4 4 4 4M6 12h11"/></svg></button></div>
    <span class="demo">Demonstração · dados simulados</span>''')

LOGIN_JS = r'''
/* ---------- login simulado e perfis ---------- */
(function(){
  const lg=document.getElementById("login");
  const nomeDe = e => (e.split("@")[0]||"Usuário").split(/[._-]/).filter(Boolean).map(x=>x[0].toUpperCase()+x.slice(1)).join(" ");
  if(!SESSAO){
    document.body.classList.add("locked"); lg.hidden=false;
    lgPerfis.innerHTML=Object.entries(PERFIS).map(([k,p],i)=>`<label class="pf"><input type="radio" name="perfil" value="${k}" ${i===0?"checked":""}><span><b>${p.n}</b><small>${p.d}</small></span></label>`).join("");
    const uns=[...new Set(V.map(v=>v.unidade))]; lgUn.innerHTML=uns.map(u=>`<option>${u}</option>`).join("");
    lgPerfis.addEventListener("change",()=>{ lgUnBox.hidden = document.querySelector('input[name=perfil]:checked').value!=="gestor"; });
    lgForm.addEventListener("submit",e=>{
      e.preventDefault();
      const email=lgEmail.value.trim();
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){ lgErro.textContent="Digite um e-mail válido, por exemplo nome@empresa.com.br."; lgErro.hidden=false; lgEmail.focus(); return; }
      if(!lgSenha.value){ lgErro.textContent="Digite a senha."; lgErro.hidden=false; lgSenha.focus(); return; }
      const perfil=document.querySelector('input[name=perfil]:checked').value;
      const sess={email, nome:nomeDe(email), perfil, unidade: perfil==="gestor"?lgUn.value:null};
      try{ sessionStorage.setItem("frota.sessao", JSON.stringify(sess)); }catch(err){}
      location.hash = PERFIS[perfil].views[0]; location.reload();
    });
    setTimeout(()=>lgEmail.focus(),50);
    return;
  }
  // logado: menu só com o que o perfil vê, usuário no rodapé, recorte no topo
  document.querySelectorAll("nav a[data-v]").forEach(a=>{ if(!podeVer(a.dataset.v)) a.remove(); });
  me.hidden=false; meNome.textContent=SESSAO.nome; meAv.textContent=SESSAO.nome.split(" ").map(x=>x[0]).slice(0,2).join("");
  mePerfil.textContent=PERFIS[SESSAO.perfil].n+(SESSAO.unidade?" · "+SESSAO.unidade:"");
  meSair.addEventListener("click",()=>{ try{ sessionStorage.removeItem("frota.sessao"); }catch(e){} location.hash=""; location.reload(); });
  const meta=document.querySelector(".tb-meta"); if(meta) meta.textContent=(SESSAO.unidade?SESSAO.unidade+" · ":"")+"Dados até 11/11/2026";
  document.body.dataset.perfil=SESSAO.perfil;
  if(!podeVer(location.hash.replace("#","").split("-")[0]||"visao")) route();
})();
'''
R('/* ---------- shell: título, busca global', LOGIN_JS + '\n/* ---------- shell: título, busca global')

# ---------- visual minimalista ----------
CSS = r'''
/* ===== minimalista ===== */
:root{
  --bg:#fafaf9; --surface:#ffffff; --ink:#18181b; --muted:#71717a; --line:#ececea; --line2:#f4f4f2;
  --accent:#166145; --accent-soft:#eef5f1; --radius:10px;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){ --bg:#0e0f0f; --surface:#141515; --ink:#ededed; --muted:#9a9a9f; --line:#232425; --line2:#1a1b1b; --accent:#5ec295; --accent-soft:#16251e; } }
:root[data-theme="dark"]{ --bg:#0e0f0f; --surface:#141515; --ink:#ededed; --muted:#9a9a9f; --line:#232425; --line2:#1a1b1b; --accent:#5ec295; --accent-soft:#16251e; }
body{font-size:14px;letter-spacing:-.003em}
h2{font-size:15px;font-weight:600} h3{font-size:13px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.side{background:var(--bg);border-right:1px solid var(--line)}
.side nav a.on{background:var(--surface);color:var(--ink);box-shadow:0 0 0 1px var(--line)}
.side nav a.on svg{color:var(--accent)}
.topbar{background:color-mix(in srgb,var(--bg) 92%,transparent);border-bottom:none}
main{gap:28px}
section.view{gap:22px}
.card{border:1px solid var(--line);box-shadow:none;padding:20px 22px}
/* indicadores: números soltos, separados por linha fina */
#kpis{gap:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius)}
#kpis>.card{border:none;border-radius:0;background:none;padding:18px 22px}
#kpis>.card+.card{border-left:1px solid var(--line)}
.kpi .v{font-size:28px;font-weight:600}
.kpi.hl{background:none} .kpi.hl .v{color:var(--accent)}
/* selos discretos: ponto colorido + texto */
.pill{background:none!important;padding:0;font-weight:500;color:var(--ink)!important;display:inline-flex;align-items:center;gap:6px}
.pill::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.p-troca::before{background:var(--good)} .p-desm::before{background:var(--sat)} .p-rev::before{background:var(--warn)} .p-crit::before{background:var(--crit)} .p-man::before{background:var(--muted)} .p-pool::before{background:var(--info)}
.flag{border:none;background:var(--line2);color:var(--muted)}
.occb{background:none;color:var(--crit);padding:0;font-weight:600}
th{background:var(--surface);color:var(--muted);font-weight:500;letter-spacing:.02em}
td,th{border-bottom:1px solid var(--line2)}
.tablewrap{border:1px solid var(--line)}
button{border-color:var(--line)}
button.on{background:var(--ink);border-color:var(--ink);color:var(--surface)}
.acao-c{border:none;border-left:2px solid var(--c);border-radius:0;padding:4px 0 4px 16px}
.og{border:1px solid var(--line);border-left:2px solid var(--crit);border-radius:8px}
.og.warn{border-left-color:var(--warn)}
/* menos coisa na visão geral */
#scatter,#scLegend,#scCor,#alerts,#alerts+*,#v-visao h2:has(+ #alerts){display:none!important}
.calhead:has(+ #scatter) h2{display:none}
#v-visao .card:has(#alerts) h3:last-of-type{display:none}
/* usuário no rodapé do menu */
.me{display:flex;gap:10px;align-items:center;padding:8px 6px;border-top:1px solid var(--line);margin-top:4px}
.av{width:30px;height:30px;border-radius:50%;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-weight:700;font-size:12px;flex:none}
.me-t{display:flex;flex-direction:column;min-width:0;line-height:1.25}
.me-t b{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.me-t small{font-size:11.5px;color:var(--muted)}
.me-out{margin-left:auto;width:30px;height:30px;padding:0;display:grid;place-items:center;background:none;border:none;color:var(--muted)}
.me-out svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.me-out:hover{color:var(--ink)}
/* tela de login */
body.locked{overflow:hidden}
body.locked>:not(#login):not(script):not(svg){visibility:hidden}
.login{position:fixed;inset:0;z-index:100;display:grid;grid-template-columns:minmax(360px,1fr) 1.1fr;background:var(--surface)}
.login[hidden]{display:none}
.login-l{display:flex;flex-direction:column;padding:32px 48px;gap:40px;overflow:auto}
.lg-form{display:flex;flex-direction:column;gap:8px;max-width:380px;width:100%;margin:auto 0}
.lg-form h1{font-size:26px;font-weight:650;margin:0 0 14px}
.lg-form label{font-size:13px;font-weight:500;margin-top:8px}
.lg-form input[type=email],.lg-form input[type=password],.lg-form select{padding:10px 12px;font-size:15px;border-radius:8px;border:1px solid var(--line);background:var(--surface)}
.lg-perfis{border:none;padding:0;margin:14px 0 0;display:flex;flex-direction:column;gap:6px}
.lg-perfis legend{font-size:13px;font-weight:500;margin-bottom:6px}
.pf{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:1px solid var(--line);border-radius:8px;cursor:pointer;margin:0!important}
.pf:has(input:checked){border-color:var(--accent);background:var(--accent-soft)}
.pf input{margin-top:3px;accent-color:var(--accent)}
.pf span{display:flex;flex-direction:column;font-size:13.5px;line-height:1.35} .pf small{color:var(--muted);font-size:12.5px}
.lg-btn{margin-top:16px;padding:11px;font-size:15px;font-weight:600;background:var(--ink);color:var(--surface);border:none;border-radius:8px}
.lg-btn:hover{opacity:.9}
.lg-erro{color:var(--crit);font-size:13px;margin:4px 0 0}
.lg-demo{margin-top:6px}
.login-r{background:#0f3d2b;color:#e9f3ee;display:flex;align-items:flex-end;padding:56px;position:relative;overflow:hidden}
.login-r::before{content:"";position:absolute;inset:0;background:repeating-linear-gradient(115deg,transparent 0 46px,rgba(255,255,255,.035) 46px 47px)}
.lr-in{position:relative;max-width:440px}
.lr-k{font-size:13px;letter-spacing:.06em;text-transform:uppercase;opacity:.7;margin:0 0 12px}
.lr-t{font-size:36px;line-height:1.1;font-weight:650;margin:0 0 12px;letter-spacing:-.02em}
.lr-s{font-size:15px;opacity:.8;margin:0}
@media (max-width:860px){ .login{grid-template-columns:1fr} .login-r{display:none} .login-l{padding:24px 20px} }
'''
R('</style>', CSS + '</style>')

p.write_text(s, encoding="utf-8")
print("ok")
