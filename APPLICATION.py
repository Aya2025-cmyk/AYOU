import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import numpy as np
import streamlit.components.v1 as components

st.markdown("<h1>SCARPER LES DONNEES</h1>", unsafe_allow_html=True)

st.markdown(""" 
Cette application effectue le webscraping des données de Coin Afrique sur plusieurs pages. 
Et nous pouvons également télécharger les données extraites de l'application directement sans les extraire. 
* **Bibliothèques Python :** base64, pandas, streamlit, requests, bs4 
* **Source des données :** https://sn.coinafrique.com/categorie/vetements-enfants --https://sn.coinafrique.com/categorie/chaussures-enfants.
""")

# PARTIE 1
# Fond principal 
body {
    background: linear-gradient(to bottom, #2E8B57, #F5F5DC); /* Dégradé vert sapin → beige */
    color: white;
    font-family: 'Poppins', sans-serif;
}

#titres
h1, h2 {
    color: #FFD700; /* Doré */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

# Boutons 
button {
    background: linear-gradient(to right, #FF8C00, #FFD700);
    border: none;
    color: white;
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 10px;
    transition: 0.3s;
}

button:hover {
    background: linear-gradient(to right, #FFA500, #FFEC8B);
    transform: scale(1.05);
}

#Menu latéral 
.sidebar {
    background: linear-gradient(to bottom, #FF8C00, #FFD700); /* Orange → Doré */
    color: white;
}


# Fond d'écran de l'application
#add_bg_from_local("picture.webp")

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