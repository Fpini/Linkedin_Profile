from opencorporates_api import OpenCorporatesAPI
import pandas as pd

# Creare un DataFrame di esempio con nomi di aziende
df_companies = pd.read_csv("geolocalizzazione_aziende.csv")

# Inizializza l'API (senza API Key)
oc_api = OpenCorporatesAPI()

# Processa il DataFrame per ottenere i dettagli delle aziende
df_results = oc_api.process_dataframe(df_companies)

# Mostra i risultati
print(df_results)

# Salva i risultati in un CSV
df_results.to_csv("aziende_con_coordinate.csv", index=False)
