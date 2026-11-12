# Frota Arauco — protótipo

Protótipo de gestão de frota para a Arauco (Pampa Devs). **Todos os dados são simulados.**

- `index.html`: o site inteiro, num arquivo só, sem dependências. É o que vai para o ar.
- `src/`: template, simulação (`sim.py`), geografia da região (`build_geo.py`) e `build.py`, que monta o `index.html`.

## Publicar (Cloudflare Pages)

1. Cloudflare → Workers & Pages → Create → Pages → **Connect to Git** → `Pampa-Devs/frota-arauco`.
2. Build command: *vazio*. Output directory: `/`.
3. Custom domains → adicionar o subdomínio.
4. Opcional: Zero Trust → Access, para liberar só e-mails autorizados.
