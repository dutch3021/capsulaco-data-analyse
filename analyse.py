"""AI-assisted leerproject. Uitsluitend fictieve demonstratiedata."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parent

def main():
    bron = BASE / 'data' / 'capsulaco_productie_groot.csv'
    uitvoer = BASE / 'output'
    uitvoer.mkdir(exist_ok=True)
    df = pd.read_csv(bron, sep=';')
    vereist = {'datum', 'lijn', 'geproduceerd', 'nok'}
    if not vereist.issubset(df.columns):
        raise ValueError(f'Ontbrekende kolommen: {vereist - set(df.columns)}')
    print(f'Ingelezen: {len(df)} rijen (fictieve data).')
    schoon = df.copy()
    schoon['lijn'] = schoon['lijn'].str.strip().str.replace('lijn', 'Lijn', regex=False)
    schoon = schoon.dropna()
    q1, q3 = schoon['nok'].quantile([0.25, 0.75])
    iqr = q3 - q1
    schoon = schoon[schoon['nok'].between(q1 - 1.5 * iqr, q3 + 1.5 * iqr)]
    schoon = schoon.drop_duplicates()
    if schoon.empty:
        raise ValueError('Geen gegevens over na opschonen.')
    schoon[['geproduceerd', 'nok']] = schoon[['geproduceerd', 'nok']].astype(int)
    schoon.to_csv(uitvoer / 'productie_schoon.csv', sep=';', index=False)
    samenvatting = schoon.groupby('lijn')[['geproduceerd', 'nok']].sum()
    samenvatting['nok_percentage'] = (100 * samenvatting['nok'] / samenvatting['geproduceerd']).round(2)
    samenvatting.to_csv(uitvoer / 'samenvatting_per_lijn.csv', sep=';')
    fig, ax = plt.subplots(figsize=(8, 5))
    samenvatting['nok'].plot.bar(ax=ax, color='#287C8E', rot=0)
    ax.set(title='Afgekeurde producten per lijn - fictieve data', xlabel='Productielijn', ylabel='Aantal NOK na opschonen')
    fig.tight_layout()
    fig.savefig(uitvoer / 'capsulaco_nok_per_lijn.png', dpi=160)
    plt.close(fig)
    print(f'Na opschonen: {len(schoon)} rijen.')
    print(samenvatting.to_string())
    print(f'Resultaten opgeslagen in: {uitvoer}')

if __name__ == '__main__':
    main()
