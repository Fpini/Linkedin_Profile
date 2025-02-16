import pandas as pd
import time
import sys

# Caricare il file CSV originale con le aziende
df_start = pd.read_csv("Connections copy.csv")

df_clean = df_start.dropna(subset=["Location"])
df_clean = df_clean.drop(columns=['Email Address'])
print(df_clean.columns)
print(df_clean.shape)

df_geo = pd.read_csv("geolocalizzazione_loc_aziende.csv")

df_result=pd.merge(df_clean,df_geo, on="Location", how="inner")

print(df_result.shape)

df_result.to_csv("geo_Connections")