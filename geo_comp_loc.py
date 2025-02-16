import pandas as pd
from geopy.geocoders import Nominatim
import time
import sys

# Inizializza il geolocator con un user-agent personalizzato
geolocator = Nominatim(user_agent="geo_locator")

# Caricare il file CSV originale con le aziende
df_start = pd.read_csv("Connections copy.csv")

df_clean = df_start.dropna(subset=["Location"])
df_clean = df_clean.drop(columns=['URL','Email Address'])
print(df_clean.columns)
print(df_clean.shape)

lst_loc = df_clean['Location'].unique()
print(lst_loc)
print(len(lst_loc))

df = pd.DataFrame(lst_loc,columns=['Location'])
print(df.shape)

# Creare un dizionario per salvare le coordinate e il conteggio
geo_data = {"Location": [], "Latitudine": [], "Longitudine": []}

# Ottenere le coordinate per ogni azienda
for _, row in df.iterrows():
    loc = row["Location"]
   
    try:
        location = geolocator.geocode(loc, timeout=10)
        if location:
            lat, lon = location.latitude, location.longitude
            print(f"✅ Geolocalizzazione trovata: {loc} -> ({lat}, {lon})")
        else:
            lat, lon = None, None
            print(f"⚠️ Geolocalizzazione non trovata: {loc}")

        geo_data["Location"].append(loc)
        geo_data["Latitudine"].append(lat)
        geo_data["Longitudine"].append(lon)
 
    except Exception as e:
        print(f"❌ Errore con {company}: {e}")
        geo_data["Location"].append(company)
        geo_data["Latitudine"].append(None)
        geo_data["Longitudine"].append(None)

    # Ritardo per evitare il blocco da parte del servizio Nominatim
    time.sleep(1)

# Creare un DataFrame con le coordinate e il conteggio
geo_df = pd.DataFrame(geo_data)

# Mostrare il DataFrame con le coordinate
print(geo_df)

# Salvare il risultato in un file CSV con il numero di occorrenze (Count)
geo_df.to_csv("geolocalizzazione_loc_aziende.csv", index=False)

