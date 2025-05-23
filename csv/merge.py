import pandas as pd

deaths = pd.read_csv('csv/GOTdeaths.csv')
episodes = pd.read_csv('csv/GOTepisodes.csv')

merged = pd.merge(deaths, episodes, on=['Season', 'Episode'], how='inner')

merged.to_csv('csv/data.csv', index=False)

print("merge exitoso")
