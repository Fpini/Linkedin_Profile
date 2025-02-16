import pandas as pd
from geopy.geocoders import Nominatim
import time

# Inizializza il geolocator con un user-agent personalizzato
geolocator = Nominatim(user_agent="geo_locator")

# Caricare il file CSV originale con le aziende
df_start = pd.read_csv("Connections.csv")

# Contare le aziende e selezionare solo quelle con più di 2 occorrenze
company_counts = df_start["Company"].value_counts()
df = company_counts[company_counts > 2].reset_index()
df.columns = ["Company", "Count"]  # Rinominare le colonne

# Creare un dizionario per salvare le coordinate e il conteggio
geo_data = {"Company": [], "Latitudine": [], "Longitudine": [], "Count": []}

# Ottenere le coordinate per ogni azienda
for _, row in df.iterrows():
    company = row["Company"]
    count = row["Count"]
    
    try:
        location = geolocator.geocode(company, timeout=10)
        if location:
            lat, lon = location.latitude, location.longitude
            print(f"✅ Geolocalizzazione trovata: {company} -> ({lat}, {lon})")
        else:
            lat, lon = None, None
            print(f"⚠️ Geolocalizzazione non trovata: {company}")

        geo_data["Company"].append(company)
        geo_data["Latitudine"].append(lat)
        geo_data["Longitudine"].append(lon)
        geo_data["Count"].append(count)  # Aggiunge il numero di contatti per l'azienda

    except Exception as e:
        print(f"❌ Errore con {company}: {e}")
        geo_data["Company"].append(company)
        geo_data["Latitudine"].append(None)
        geo_data["Longitudine"].append(None)
        geo_data["Count"].append(count)

    # Ritardo per evitare il blocco da parte del servizio Nominatim
    time.sleep(1)

# Creare un DataFrame con le coordinate e il conteggio
geo_df = pd.DataFrame(geo_data)

# Mostrare il DataFrame con le coordinate
print(geo_df)

# Salvare il risultato in un file CSV con il numero di occorrenze (Count)
geo_df.to_csv("geolocalizzazione_aziende.csv", index=False)
