import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import numpy as np
import streamlit.components.v1 as components


st.markdown("""
<h2 style="text-align: center; color: #5D4037;">📌 SCARPER LES DONNES</h2>

Cette application effectue le **webscraping** des données de Coin Afrique sur plusieurs pages.  
Et nous pouvons également **télécharger les données extraites** de l'application directement sans les extraire.  

### 📚 Bibliothèques Python :
- **base64, pandas, streamlit, requests, bs4**  

### 🔗 Source des données :
- [Vêtements enfants](https://sn.coinafrique.com/categorie/vetements-enfants)  
- [Chaussures enfants](https://sn.coinafrique.com/categorie/chaussures-enfants)  
""", unsafe_allow_html=True)


# PARTIE 1
# Fonction du background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
   <style>
    .stApp {{
        background-image: url(data:image/webp;base64,{encoded_string.decode()});
        background-size: cover;
        background-color: #4A4A4A; /* Noir */
        color: #000000; /* Noir */
    }}
    
    .stMarkdown, .stTextInput, .stButton>button {{
        color:#4A4A4A ;
        font-family: 'Poppins', sans-serif;
    }}
    
    .stButton>button {{
        background-color:#000000; 
        border-radius: 10px;
        border: none;
        padding: 8px 15px;
        transition: 0.3s ease-in-out;
    }}
    
    .stButton>button:hover {{
        background-color: #FFFFFF ; /* Gris plus clair au survol */
    }}
</style>

    """,
    unsafe_allow_html=True
)


# Fond d'écran de l'application
add_bg_from_local("orange.webp")

# Fonction pour convertir un DataFrame en CSV
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Fonction pour afficher et télécharger les données
def load(dataframe, title, key, key1):
    st.markdown(
        """
        <style>
        div.stButton {text-align:center}
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(title, key=key1):
        st.subheader("Dimension")
        st.write(f"Dimension des données: {dataframe.shape[0]} lignes et {dataframe.shape[1]} colonnes.")
        st.dataframe(dataframe)

        csv = convert_df(dataframe)
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name='Données.csv',
            mime='text/csv',
            key=key
        )

# PARTIE 2
# Fonction de scraping des données vêtements des enfants
def scrape_vetements_data(plusieurs_page):
    DF = pd.DataFrame()
    for index in range(1, int(plusieurs_page) + 1):
        url = f'https://sn.coinafrique.com/categorie/vetements-enfants?page={index}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_="col s6 m4 l3")
        donne = []
        for container in containers:
            try:
                type_habits = container.find("p", class_="ad__card-description").text.strip()
                Prix = container.find("p", class_="ad__card-price").text.strip().replace("CFA", "")
                Adresse = container.find("p", class_="ad__card-location").text.strip().replace("location_on", "")
                Image_lien = container.find("img", class_="ad__card-img")["src"]
                
                dic = {
                    "Type habits": type_habits,
                    "Prix": Prix,
                    "Adresse": Adresse,
                    "Image_lien": Image_lien,  
                }
                donne.append(dic)
            except Exception as e:
                st.error(f"Erreur lors du scraping des vêtements: {e}")
        Df = pd.DataFrame(donne)
        DF = pd.concat([DF, Df], axis=0).reset_index(drop=True)
    return DF

# PARTIE 3
# Fonction de scraping des données chaussures des enfants
def scrape_chaussures_data(plusieurs_page):
    df = pd.DataFrame()
    for p_index in range(1, int(plusieurs_page) + 1):
        url = f'https://sn.coinafrique.com/categorie/chaussures-enfants?page={p_index}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        Paquets = soup.find_all('div', class_="col s6 m4 l3")
        donne = []
        for Paquet in Paquets:
            try:
                Type_chaussures = Paquet.find("p", class_="ad__card-description").text.strip()
                Prix = Paquet.find("p", class_="ad__card-price").text.strip().replace("CFA", "")
                Adresse = Paquet.find("p", class_="ad__card-location").text.replace("location_on", "")
                Image_lien = Paquet.find("img", class_="ad__card-img")["src"]
                dic = {
                    "Type chaussure": Type_chaussures,
                    "Prix": Prix,
                    "Adresse": Adresse,
                    "Image lien": Image_lien,
                }
                donne.append(dic)
            except Exception as e:
                st.error(f"Erreur lors du scraping des chaussures: {e}")
        DF1 = pd.DataFrame(donne)
        df = pd.concat([df, DF1], axis=0).reset_index(drop=True)
    return df

# PARTIE 4
st.sidebar.header("Saisie de l'utilisateur")
Pages = st.sidebar.selectbox('Pages', list(np.arange(2, 30)))
Category = st.sidebar.selectbox("Options", ["Scrape les données avec beautifulSoup", "Scraper les données avec web Scraper", "Formulaire avec koblox", "Formulaire avec Google Forms"])

# Fonction pour injecter du CSS personnalisé
def local_css(css):
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)




if Category == "Scrape les données avec beautifulSoup":
    Vetements_enfants = scrape_vetements_data(Pages)
    Chaussures_enfants = scrape_chaussures_data(Pages)
    
    load(Vetements_enfants, "Données sur les vetements", '1', '110')
    load(Chaussures_enfants, "Données sur les chaussures", '2', '111')

elif Category == "Scraper les données avec web Scraper":
    try:
        Vetements = pd.read_csv("Vetements_enfants.csv")
        Chaussures = pd.read_csv("Chaussures_enfants.csv")
        
        load(Vetements, "Données sur les vetements", '1', '110')
        load(Chaussures, "Données sur les chaussures", '2', '111')
    except FileNotFoundError as e:
        st.error(f"Erreur: Fichier non trouvé - {e}")
    except Exception as e:
        st.error(f"Erreur inattendue: {e}")

elif Category == "Formulaire avec koblox":
    components.iframe("https://ee.kobotoolbox.org/x/lWB14KiL", width=800, height=1100)

elif Category == "Formulaire avec Google Forms":
    components.iframe("https://docs.google.com/forms/d/e/1FAIpQLScuuEKdEs1FmIeYDq3TrUT2TiNqc1OIT7GPG0hCa2fx52_q_A/viewform?usp=preview", width=800, height=1100)