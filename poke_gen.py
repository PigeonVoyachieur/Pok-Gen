import streamlit as st

logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/2052px-Pok%C3%A9_Ball_icon.svg.png"

# ------------------------------
# Configuration de la page
# ------------------------------
st.set_page_config(
    page_title="Laboratoire PokéGen",
    page_icon=logo,
    layout="centered"
)

# ------------------------------
# Titre & Introduction
# ------------------------------
st.title("Bienvenue au laboratoire PokéGen")
st.write("""
Bienvenue dans votre laboratoire de création de Pokémon générés par IA !  
Configurez les paramètres dans la barre latérale, puis passez à l'étape suivante.
""")

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.header("⚙️ Paramètres du générateur")

# Clé API Groq
api_key = st.sidebar.text_input(
    "Clé API Groq",
    type="password",
    help="Entrez votre clé API Groq pour générer des Pokémon."
)

# Nombre de Pokémon à générer
nb_pokemon = st.sidebar.slider(
    "Nombre de Pokémon à générer",
    min_value=3,
    max_value=10,
    value=3
)

# Type dominant (optionnel)
type_dominant = st.sidebar.selectbox(
    "Type dominant (optionnel)",
    ["Aucun", "Feu", "Eau", "Plante", "Électrik", "Psy", "Ténèbres", "Acier", "Roche", "Sol", "Insecte", "Vol", "Glace", "Combat", "Fée", "Spectre", "Dragon", "Poison", "Normal"],
    index=0
)

# debug
st.subheader("🔍 Paramètres sélectionnés")
st.write(f"- **Clé API fournie :** {'✔️ Oui' if api_key else '❌ Non'}")
st.write(f"- **Nombre de Pokémon :** {nb_pokemon}")
st.write(f"- **Type dominant :** {type_dominant}")
