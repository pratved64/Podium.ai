# Merging CSVs
import pandas as pd

trackChar = {
    'Sakhir': 'Mid-Circuit',
    'Jeddah': 'High-Street',
    'Melbourne': 'High-Street',
    'Imola': 'Mid-Circuit',
    'Miami': 'Mid-Circuit',
    'Barcelona': 'Mid-Circuit',
    'Monaco': 'Low-Street',
    'Monte Carlo': 'Low-Street',
    'Baku': 'Low-Street',
    'Montréal': 'High-Street',
    'Montreal': 'High-Street',
    'Silverstone': 'Mid-Circuit',
    'Spielberg': 'High-Circuit',
    'Le Castellet': 'High-Circuit',
    'Hockenheim': 'Mid-Circuit',
    'Budapest': 'Low-Circuit',
    'Spa-Francorchamps': 'High-Circuit',
    'Zandvoort': 'Mid-Circuit',
    'Monza': 'High-Circuit',
    'Marina Bay': 'Low-Street',
    'Singapore': 'Low-Street',
    'Sochi': 'High-Circuit',
    'Suzuka': 'High-Circuit',
    'Austin': 'Mid-Circuit',
    'Mexico City': 'Mid-Circuit',
    'São Paulo': 'Mid-Circuit',
    'Sao Paulo': 'Mid-Circuit',
    'Yas Island': 'Mid-Circuit',
    'Yas Marina': 'Mid-Circuit',
    'Shanghai': 'Mid-Circuit',
    'Lusail': 'High-Circuit',
    'Las Vegas': 'High-Street',
    'Nürburgring': 'Mid-Circuit',
    'Portimão': 'Mid-Circuit',
    'Istanbul': 'High-Circuit',
    'Mugello': 'High-Circuit'
}  # Map for track type

df = pd.read_csv('../currentResults.csv')

df.insert(3, 'Track_Type', 'T')

charCol = []
for _, row in df.iterrows():
    t_type = trackChar[row['Circuit']]
    charCol.append(t_type)

df['Track_Type'] = charCol
df.to_csv('../currentResults.csv', index=False)
