# European Car Market Dashboard

Análise do mercado automóvel europeu em 2024: top 10 marcas, vendas por país, modelos best-sellers e tipo de combustível. Projeto de portfolio em análise de dados e visualização.

## O que mostra

- Novas matrículas por país (EU, EFTA, UK) — 31 mercados
- Top 10 marcas mais vendidas e crescimento vs 2023
- Market share por grupo de fabricantes
- Top 10 modelos best-sellers e respetivo tipo de combustível

## Estrutura

```
automotive-market-dashboard/
├── data/
│   ├── raw/          # Dados brutos (CSV, fonte ACEA/JATO)
│   └── processed/    # Dados tratados
├── notebooks/
│   └── 01_eda.ipynb  # Análise exploratória
├── src/
│   ├── constants.py  # Listas de referência
│   ├── loader.py     # Carregamento e tratamento
│   └── dashboard.py  # App Streamlit (em construção)
├── requirements.txt
└── README.md
```

## Como correr

```bash
pip install -r requirements.txt
python src/loader.py
jupyter notebook notebooks/01_eda.ipynb
streamlit run src/dashboard.py
```

## Fontes de dados

Dados de 2024 (ano completo) da ACEA e JATO Dynamics, compilados via best-selling-cars.com. Para uso educacional e de portfolio.

## Próximos passos

- [ ] Preço médio por marca/país
- [ ] Dados demográficos por género (fonte adicional necessária)
- [ ] Dashboard interativo em Streamlit
- [ ] Deploy em Streamlit Cloud
