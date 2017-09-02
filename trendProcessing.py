import pandas as pd
import numpy as np
import html5lib, time, os.path
from datetime import timedelta

df = pd.read_csv('top5trending_.csv')
df['zip'] = df['zip'].astype(int).astype(str)
df['key'] = df[['zip','date']].apply(lambda x: '/'.join(x), axis=1)
df = df.sort(['key'],ascending=[True])
df.to_csv('top5trending.csv', encoding="utf-8", header=True, index=False)


# df = pd.read_csv('CompiledWeather.csv')
# df = df.sort(['key'],ascending=[True])
# df.to_csv('CompiledWeatherNew.csv', encoding="utf-8", header=True, index=False)
