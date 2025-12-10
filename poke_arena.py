import streamlit as st
import json
from groq import Groq

# ------------------------------
# Configuration de la page
# ------------------------------
st.set_page_config(
    page_title="🏟️ Arène Pokémon",
    page_icon="⚔️",
    layout="wide"
)

st.title("🏟️ Arène Pokémon")
st.write("Préparez votre champion pour l'affrontement ! Chargez les JSON et choisissez le terrain.")

# ------------------------------
# Sélecteur de terrain
# ------------------------------
terrain = st.selectbox(
    "Sélectionnez le terrain du combat",
    ["Volcan", "Océan", "Espace", "Forêt", "Désert", "Glace"],
    index=0
)

# ------------------------------
# Colonnes pour afficher JSON
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛡️ Mon Champion")
    json_champion = st.text_area(
        "Collez ici le JSON de votre champion",
        height=200,
        placeholder='{"Nom": "Flamgeist", "Type": "Feu", ...}'
    )

with col2:
    st.subheader("⚔️ L'Adversaire")
    json_adversaire = st.text_area(
        "Collez ici le JSON de l'adversaire",
        height=200,
        placeholder='{"Nom": "Aquashock", "Type": "Eau", ...}'
    )

# ------------------------------
# Bouton pour vérifier JSON
# ------------------------------
if st.button("Valider les JSON et préparer le combat"):
    try:
        champion_data = json.loads(json_champion)
        adversaire_data = json.loads(json_adversaire)
        st.success("✅ JSON valides et prêts pour l'arène !")
        st.write(f"Terrain sélectionné : **{terrain}**")
    except json.JSONDecodeError:
        st.error("❌ JSON invalide. Veuillez vérifier le format et réessayer.")

