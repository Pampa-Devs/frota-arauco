# Frota Arauco — protótipo

Protótipo de gestão de frota para a Arauco (Pampa Devs). **Todos os dados são simulados.**

- `index.html`: o site inteiro, num arquivo só, sem dependências. É o que vai para o ar.
- `src/`: template, simulação (`sim.py`), geografia da região (`build_geo.py`) e `build.py`, que monta o `index.html`.

## O que tem na v4

Tudo é gerado no navegador a partir dos mesmos dados (`veiculos.json`, `resumo.json` e `geo.json` não mudaram). O que foi acrescentado está em `template.html`:

- **Calendários:** um na página do veículo (um mês por vez, com os dias de ocorrência) e um da frota em Veículos. Clicar num dia mostra quantos veículos estavam em uso e parados, e filtra a tabela.
- **Ficha do veículo:** modelo, entrada na frota, km na aquisição, odômetro e km/dia. A próxima revisão é calculada pelo km ou pela data, o que vencer primeiro, no plano severo ou normal. Há ainda o histórico de manutenção e os problemas em aberto.
- **Câmeras com leitura de placa:** portarias, posto e MS-377, com galeria, foto ampliada e miniaturas no mapa. Só a chegada ou a saída no bar conta como parada proibida.
- **Condutores:** cada veículo tem um condutor com cargo (nomes fictícios). A Visão geral ganha a matriz Cargo × uso real e o gráfico colorido por cargo. A lista de veículos ganha a coluna Condutor e o filtro Cargo × uso.
- **Ficha do funcionário** (`#func-<matrícula>`):
  - "Precisa de caminhonete?", com três checagens: cargo, uso real e ordens de serviço;
  - habilitação e cursos;
  - onde mora, com a distância até o trabalho, quanto do km é ida e volta de casa e um mapa.
- **Modo apresentação:** botão "Apresentar", ou `?apresentar` na URL. São 15 passos com destaque na tela, controlados pelas setas ou por um passador de slides.

Para gerar o `index.html` sem Python: o `build.py` só troca `__DATA__`, `__RES__` e `__GEO__` pelos JSON e acrescenta o meta `robots`.

### Créditos das fotos

As fotos das caminhonetes são do Wikimedia Commons e estão embutidas no `template.html` em base64, com as placas originais borradas:

| Foto | Autor | Licença |
| --- | --- | --- |
| Toyota Hilux J 4x4 2021 | Ethan Llamas | CC BY-SA 4.0 |
| Toyota Hilux (48635556302) | crash71100 | CC0 |
| Toyota SW4 SRV 2012 | RL GNZLZ | CC BY-SA 2.0 |
| Toyota Fortuner 4x2 G 2017 | Captainmorlypogi1959 | CC BY-SA 4.0 |

Os créditos também aparecem na tela, na seção Câmeras do veículo.

## Publicar (Cloudflare Pages)

1. Cloudflare → Workers & Pages → Create → Pages → **Connect to Git** → `Pampa-Devs/frota-arauco`.
2. Build command: *vazio*. Output directory: `/`.
3. Custom domains → adicionar o subdomínio.
4. Opcional: Zero Trust → Access, para liberar só e-mails autorizados.
