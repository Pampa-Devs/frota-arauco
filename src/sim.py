"""Simulação de dados da frota Arauco (protótipo). Tudo fictício."""
import json, math, random

random.seed(42)

UNIDADES = ["Fábrica", "UF Norte", "UF Sul", "UF Leste", "UF Oeste"]
# custo fixo mensal (locação) — variável (combustível/manut/pedágio/multas) completa ~R$8k e ~R$2k
FIXO = {"Caminhonete": 6200, "Carro": 1350, "Van": 4300}
KM_L = {"Caminhonete": 8.5, "Carro": 12.5, "Van": 9.0}
PRECO_DIESEL, PRECO_GAS = 6.10, 6.30

def perfil_pick():
    r = random.random()
    return "campo" if r < 0.62 else ("misto" if r < 0.84 else "urbano")

def gerar_veiculo(i, tipo):
    unidade = random.choices(UNIDADES, weights=[0.22, 0.2, 0.2, 0.19, 0.19])[0]
    if tipo == "Caminhonete":
        perfil = perfil_pick()
        if unidade == "Fábrica" and perfil == "campo" and random.random() < 0.25:
            perfil = "urbano"
    elif tipo == "Carro":
        perfil = "carro_terra" if random.random() < 0.06 else "urbano"
    else:
        perfil = "van"

    if perfil == "campo":
        km = random.uniform(2600, 4200); terra = random.uniform(0.35, 0.6); off = random.uniform(0.08, 0.22)
        dias_talhao = random.uniform(0.55, 0.95); rest = random.uniform(0.5, 3); cob = random.uniform(0.45, 0.72)
    elif perfil == "misto":
        km = random.uniform(2000, 3400); terra = random.uniform(0.12, 0.28); off = random.uniform(0.01, 0.06)
        dias_talhao = random.uniform(0.2, 0.45); rest = random.uniform(2, 6); cob = random.uniform(0.7, 0.88)
    elif perfil == "carro_terra":
        km = random.uniform(1800, 3000); terra = random.uniform(0.25, 0.45); off = random.uniform(0.0, 0.03)
        dias_talhao = random.uniform(0.15, 0.4); rest = random.uniform(2, 5); cob = random.uniform(0.65, 0.85)
    elif perfil == "van":
        km = random.uniform(3000, 5200); terra = random.uniform(0.1, 0.3); off = 0.0
        dias_talhao = random.uniform(0.1, 0.3); rest = random.uniform(1, 4); cob = random.uniform(0.7, 0.9)
    else:  # urbano
        km = random.uniform(900, 2100); terra = random.uniform(0.0, 0.09); off = random.uniform(0.0, 0.015)
        dias_talhao = random.uniform(0.0, 0.12); rest = random.uniform(8, 18); cob = random.uniform(0.93, 0.995)
    asf = max(0.0, 1 - terra - off)

    kml = KM_L[tipo] * random.uniform(0.9, 1.08)
    anomalia = random.random() < 0.035
    litros = km / kml * (random.uniform(1.25, 1.45) if anomalia else 1.0)
    preco = PRECO_DIESEL if tipo != "Carro" else PRECO_GAS
    comb = litros * preco
    manut = (km / 1000) * {"Caminhonete": 95, "Carro": 55, "Van": 80}[tipo] * (1 + terra * 1.2 + off * 2.5)
    pedagio = km * asf * random.uniform(0.0, 0.06)
    multas = random.choice([0] * 9 + [195.23, 293.47, 130.16])
    fim_semana = random.uniform(0.0, 0.04) if random.random() > 0.05 else random.uniform(0.15, 0.3)
    total = FIXO[tipo] + comb + manut + pedagio + multas

    return {
        "id": f"{ {'Caminhonete':'CM','Carro':'CR','Van':'VN'}[tipo] }-{i:03d}".replace(" ", ""),
        "placa": f"{random.choice('ABRQ')}{random.choice('BCDKXZ')}{random.choice('AEJTU')}{random.randint(0,9)}{random.choice('ABCDEFGHIJ')}{random.randint(10,99)}",
        "tipo": tipo, "unidade": unidade, "perfil": perfil,
        "km": round(km), "asf": round(asf, 3), "terra": round(terra, 3), "off": round(off, 3),
        "dias_talhao": round(dias_talhao, 2), "rest_sem": round(rest, 1), "fds": round(fim_semana, 3),
        "kml_real": round(km / litros, 2), "kml_ref": round(kml if not anomalia else KM_L[tipo], 2),
        "anomalia_comb": anomalia,
        "fixo": FIXO[tipo], "comb": round(comb), "manut": round(manut), "pedagio": round(pedagio), "multas": round(multas),
        "total": round(total), "cob4g": round(cob, 3),
    }

veics = []
n = 1
for tipo, qtd in [("Caminhonete", 190), ("Carro", 200), ("Van", 30)]:
    for _ in range(qtd):
        veics.append(gerar_veiculo(n, tipo)); n += 1

def custo_carro_equiv(v):
    km = v["km"]
    comb = km / KM_L["Carro"] * PRECO_GAS
    manut = km / 1000 * 55 * (1 + v["terra"] * 1.2)
    return FIXO["Carro"] + comb + manut + v["pedagio"]

for v in veics:
    fora = v["terra"] + v["off"]
    rec, eco, motivo = "Manter", 0, ""
    if v["tipo"] == "Caminhonete":
        if fora < 0.15 and v["dias_talhao"] < 0.2:
            rec = "Trocar por carro"
            eco = v["total"] - custo_carro_equiv(v)
            motivo = f"{fora*100:.0f}% do km fora do asfalto; entrou em talhão em {v['dias_talhao']*100:.0f}% dos dias"
        elif fora < 0.35 and v["dias_talhao"] < 0.5:
            motivo = f"uso de campo eventual ({v['dias_talhao']*100:.0f}% dos dias); candidata ao pool da unidade"
        else:
            motivo = f"{fora*100:.0f}% do km em terra/fora de estrada"
    elif v["tipo"] == "Carro" and v["terra"] + v["off"] > 0.22:
        rec = "Revisar alocação"
        motivo = f"carro com {fora*100:.0f}% do km em estrada de terra: risco e manutenção maior"
    flags = []
    if v["anomalia_comb"]:
        flags.append("Consumo acima do esperado")
    if v["fds"] > 0.12:
        flags.append("Uso em fim de semana")
    if v["tipo"] == "Caminhonete" and v["rest_sem"] > 7:
        flags.append("Muitas idas a restaurante/cidade")
    v["rec"] = rec; v["eco"] = round(max(0, eco)); v["motivo"] = motivo; v["flags"] = flags

# ---------- utilização diária e tamanho de frota ----------
DIAS = 90
from datetime import date, timedelta
D0 = date(2026, 8, 14)  # 90 dias até 11/11/2026
USO = {"campo":(0.75,0.95),"misto":(0.3,0.6),"urbano":(0.35,0.75),"carro_terra":(0.45,0.8),"van":(0.8,0.97)}
for v in veics:
    lo,hi = USO[v["perfil"]]
    p = random.uniform(lo,hi)
    if random.random() < 0.14: p = random.uniform(0.06, 0.28)   # veículos ociosos
    serie = []
    for d in range(DIAS):
        wk = (D0 + timedelta(days=d)).weekday() < 5
        serie.append(1 if random.random() < (min(0.99,p*1.12) if wk else p*0.12 + v["fds"]) else 0)
    v["_serie"] = serie
    uteis = [d for d in range(DIAS) if (D0 + timedelta(days=d)).weekday() < 5]
    v["dias_uso"] = round(sum(serie[d] for d in uteis) / len(uteis), 2)
    v["tipo_final"] = "Carro" if v["rec"] == "Trocar por carro" else v["tipo"]

import math
def p95(xs):
    xs = sorted(xs); return xs[min(len(xs)-1, math.ceil(0.95*len(xs))-1)]
RESERVA = 1.08
necess = {}
for u in UNIDADES:
    for t in ["Caminhonete","Carro","Van"]:
        grp = [v for v in veics if v["unidade"]==u and v["tipo_final"]==t]
        if not grp: continue
        daily = [sum(v["_serie"][d] for v in grp) for d in range(DIAS)]
        need = min(len(grp), math.ceil(p95(daily)*RESERVA))
        necess[(u,t)] = (len(grp), need)
        excess = len(grp) - need
        for v in sorted(grp, key=lambda v: v["dias_uso"])[:excess]:
            v["rec"] = "Desmobilizar"
            # sai a locação e parte da manutenção; combustível e pedágio migram para outro veículo
            fixo = FIXO[v["tipo"]]
            v["eco"] = round(fixo + 0.3*v["manut"])
            v["motivo"] = f"usado em {v['dias_uso']*100:.0f}% dos dias úteis; a unidade {u} atende a demanda de {t.lower()}s com {need} veículos"

resumo = {"dias": DIAS, "porTipo": {}, "porUnidade": {}, "serieTotal": [], "serieTipo": {}}
for t in ["Caminhonete","Carro","Van"]:
    atual = sum(1 for v in veics if v["tipo"]==t)
    final = sum(n for (u,tt),(n,_) in necess.items() if tt==t)
    need = sum(nd for (u,tt),(_,nd) in necess.items() if tt==t)
    resumo["porTipo"][t] = {"atual": atual, "aposTroca": final, "necessaria": need}
    resumo["serieTipo"][t] = [sum(v["_serie"][d] for v in veics if v["tipo_final"]==t) for d in range(DIAS)]
for u in UNIDADES:
    resumo["porUnidade"][u] = {"atual": sum(1 for v in veics if v["unidade"]==u), "necessaria": sum(nd for (uu,t),(_,nd) in necess.items() if uu==u)}
resumo["serieTotal"] = [sum(v["_serie"][d] for v in veics) for d in range(DIAS)]
resumo["necessariaTotal"] = sum(nd for _,nd in necess.values())
for v in veics: v["uso"] = "".join(map(str, v.pop("_serie")))
json.dump(resumo, open("/home/claude/frota/resumo.json","w"), ensure_ascii=False)
print(resumo["porTipo"], resumo["necessariaTotal"], max(resumo["serieTotal"]))

# resumo para checagem
tot = sum(v["total"] for v in veics)
eco = sum(v["eco"] for v in veics)
pick = [v for v in veics if v["tipo"] == "Caminhonete"]
print("veiculos", len(veics), "custo mensal", tot, "economia/mes", eco, "ano", eco * 12)
print("media caminhonete", sum(v["total"] for v in pick) / len(pick))
cars = [v for v in veics if v["tipo"] == "Carro"]
print("media carro", sum(v["total"] for v in cars) / len(cars))
from collections import Counter
print(Counter(v["rec"] for v in veics))
print("cob media campo", sum(v["cob4g"] for v in veics if v["perfil"] == "campo") / max(1, len([v for v in veics if v["perfil"] == "campo"])))

json.dump(veics, open("/home/claude/frota/veiculos.json", "w"), ensure_ascii=False)
