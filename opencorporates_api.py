import requests
import pandas as pd
from geopy.geocoders import Nominatim
import time

class OpenCorporatesAPI:
    BASE_URL = "https://api.opencorporates.com/v0.4"

    def __init__(self, api_key=None):
        """
        Inizializza l'istanza dell'API.
        :param api_key: Chiave API di OpenCorporates (facoltativa)
        """
        self.api_key = api_key
        self.geolocator = Nominatim(user_agent="geo_locator")  # Inizializza il geocoder

    def search_company(self, query):
        """
        Cerca un'azienda per nome.
        :param query: Nome o keyword dell'azienda da cercare.
        :return: Dizionario con `company_number` e `jurisdiction_code`.
        """
        url = f"{self.BASE_URL}/companies/search?q={query}"
        if self.api_key:
            url += f"&api_token={self.api_key}"

        response = requests.get(url)
        data = self._handle_response(response)

        # Se ci sono risultati, prendiamo il primo
        if "results" in data and "companies" in data["results"] and len(data["results"]["companies"]) > 0:
            first_result = data["results"]["companies"][0]["company"]
            return {
                "company_number": first_result.get("company_number"),
                "jurisdiction_code": first_result.get("jurisdiction_code"),
                "name": first_result.get("name")
            }
        return None

    def get_company_details(self, company_number, jurisdiction):
        """
        Ottiene i dettagli di un'azienda specifica.
        :param company_number: Numero identificativo dell'azienda.
        :param jurisdiction: Codice della giurisdizione (es. 'us', 'gb', 'it').
        :return: Dizionario con dettagli aziendali e coordinate GPS.
        """
        url = f"{self.BASE_URL}/companies/{jurisdiction}/{company_number}"
        if self.api_key:
            url += f"?api_token={self.api_key}"

        response = requests.get(url)
        data = self._handle_response(response)

        if "company" in data:
            company_info = data["company"]
            address = company_info.get("registered_address_in_full", "Indirizzo non disponibile")

            # Ottenere coordinate GPS
            lat, lon = self.get_coordinates(address)
            company_info["latitude"] = lat
            company_info["longitude"] = lon

            return company_info
        else:
            return {"error": "Azienda non trovata"}

    def get_coordinates(self, address):
        """
        Converte un indirizzo in coordinate GPS (Latitudine e Longitudine).
        :param address: Indirizzo dell'azienda.
        :return: Latitudine e Longitudine come tuple (lat, lon).
        """
        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                time.sleep(1)  # Ritardo per evitare limiti API
                return location.latitude, location.longitude
        except Exception as e:
            print(f"Errore nella geocodifica: {e}")
        return None, None

    def _handle_response(self, response):
        """
        Gestisce la risposta API e gli eventuali errori.
        :param response: Oggetto della risposta HTTP.
        :return: Dati JSON se la richiesta ha avuto successo, altrimenti un messaggio di errore.
        """
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Errore {response.status_code}: {response.text}"}
        

    def process_dataframe(self, df):
        """
        Processa un DataFrame con la colonna 'Company' per ottenere i dettagli aziendali da OpenCorporates.
        
        :param df: DataFrame contenente una colonna 'Company' con i nomi delle aziende da cercare.
        :return: DataFrame con dettagli aziendali e coordinate GPS.
        """
        results = []

        for company in df["Company"].dropna().unique():
            print(f"🔍 Cercando informazioni per: {company}...")

            # 1️⃣ Ricerca dell'azienda su OpenCorporates
            search_result = self.search_company(company)

            if search_result:
                company_number = search_result["company_number"]
                jurisdiction = search_result["jurisdiction_code"]

                # 2️⃣ Ottenere i dettagli dell'azienda
                details = self.get_company_details(company_number, jurisdiction)

                # 3️⃣ Salvare i dati raccolti in una lista
                results.append({
                    "Company": search_result["name"],
                    "Company Number": company_number,
                    "Jurisdiction": jurisdiction,
                    "Address": details.get("registered_address_in_full", "N/A"),
                    "Latitude": details.get("latitude"),
                    "Longitude": details.get("longitude"),
                    "Status": details.get("company_status", "N/A"),
                    "Incorporation Date": details.get("incorporation_date", "N/A"),
                    "Company Type": details.get("company_type", "N/A")
                })
            else:
                print(f"⚠️ Nessuna informazione trovata per {company}.")
                results.append({
                    "Company": company,
                    "Company Number": "N/A",
                    "Jurisdiction": "N/A",
                    "Address": "N/A",
                    "Latitude": None,
                    "Longitude": None,
                    "Status": "N/A",
                    "Incorporation Date": "N/A",
                    "Company Type": "N/A"
                })

            # ⏳ Ritardo per evitare il blocco dell'API
            time.sleep(1)

        # 4️⃣ Convertire i risultati in DataFrame
        df_results = pd.DataFrame(results)

        # 5️⃣ Stampare e restituire il DataFrame finale
        print("✅ Estrazione completata. Ecco i risultati:")
        print(df_results)

        return df_results


