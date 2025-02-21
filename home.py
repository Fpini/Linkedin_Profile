import streamlit as st
from utils import upload_file, process_csv_file
import duckdb
import time
from PIL import Image
import base64
import io

def get_image_base64(image):
    """Converti un oggetto PIL.Image in base64."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # Salva come PNG in memoria
    return base64.b64encode(buffered.getvalue()).decode()

def resize_image(image, max_width):
    """Ridimensiona l'immagine mantenendo il rapporto d'aspetto."""
    width_percent = (max_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))
    return image.resize((max_width, new_height), Image.LANCZOS)
  

st.set_page_config(page_title="Home - Profilo Linkedin", page_icon="📄", layout="wide")
st.cache_data.clear() 

if "image_clicked" not in st.session_state:
    st.session_state.image_clicked = False  # Inizializza lo stato


if "duckdb_conn" in st.session_state:
    del st.session_state["duckdb_conn"]

image = Image.open("a-high-quality-streamlit-application-hom_YAAA5HthTTiTa4Ze4j7hNw__ifsh2uiRhmYnWqNbwV6KQ.jpeg")

# Ridimensiona e Converti in Base64
image_resized = resize_image(image, max_width=400)
image_base64 = get_image_base64(image_resized)
image_format = image.format


# HTML con l'immagine e gestione del click
html_code = f"""
    <script>
        function imageClicked() {{
            var streamlitDoc = window.parent.document;
            var inputField = streamlitDoc.getElementById("image_click_input");
            inputField.value = "clicked";
            inputField.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    </script>

    <style>
        .clickable-image {{
            cursor: pointer;
            max-width: 100%;
            height: auto;
            display: block;
            margin: auto;
        }}
    </style>

    <img src="data:image/{image_format};base64,{image_base64}" class="clickable-image" onclick="imageClicked()">
    <input type="hidden" id="image_click_input">
"""

    # Usa st.components per iniettare l'HTML
clicked = st.components.v1.html(html_code, height=400)

if clicked:
    st.session_state.image_clicked = True
    file = st.file_uploader("Upload a new file")
#    file = upload_file()
    if file:
        context_data = process_csv_file(file)
        if context_data is not None:
            if "Location" in context_data.columns:
                nuovo_ordine = ["Last Name", "First Name", "Company", "Position", "Connected On", "Location", "Latitude", "Longitude"]
            else:
                nuovo_ordine = ["Last Name", "First Name", "Company", "Position", "Connected On"]
            context_data = context_data[nuovo_ordine]
            st.session_state["context_data"] = context_data
            st.success("File caricato con successo!")
            # Carica l'immagine usando un percorso relativo (assicurati che il file "immagine.jpg" sia nella stessa cartella o in una sottocartella)           
        else:
            st.error("Errore durante l'elaborazione del file.")
else:
    st.warning("Carica un file per iniziare.")
