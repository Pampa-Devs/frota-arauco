"""Gera ../index.html a partir do template e dos dados simulados.

Uso (dentro de src/):
  python3 sim.py        # regera veiculos.json e resumo.json (ajuste os caminhos no fim do arquivo)
  python3 build.py      # monta ../index.html
"""
from pathlib import Path

here = Path(__file__).parent
html = (here / "template.html").read_text(encoding="utf-8")
html = (html.replace("__DATA__", (here / "veiculos.json").read_text(encoding="utf-8"))
            .replace("__RES__", (here / "resumo.json").read_text(encoding="utf-8"))
            .replace("__GEO__", (here / "geo.json").read_text(encoding="utf-8")))
html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
(here.parent / "index.html").write_text(html, encoding="utf-8")
print("index.html gerado")
