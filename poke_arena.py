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
# Fonction de décodage JSON
# ------------------------------
def decoder_pokemon(json_string):
    """
    Convertit une chaîne JSON en dictionnaire Python.
    Retourne (success, data_or_error_message)
    """
    try:
        pokemon_data = json.loads(json_string)
        
        # Normalisation : accepter "nom" ou "Nom", "type" ou "Type"
        if "nom" in pokemon_data and "Nom" not in pokemon_data:
            pokemon_data["Nom"] = pokemon_data["nom"]
        if "type" in pokemon_data and "Type" not in pokemon_data:
            pokemon_data["Type"] = pokemon_data["type"]
        
        # Vérification que les champs essentiels existent
        if "Nom" not in pokemon_data or "Type" not in pokemon_data:
            return False, "Le JSON doit contenir au minimum 'nom' et 'type' (ou 'Nom' et 'Type')"
        
        return True, pokemon_data
    except json.JSONDecodeError as e:
        return False, f"JSON invalide : {str(e)}"
    except Exception as e:
        return False, f"Erreur inattendue : {str(e)}"

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
        placeholder='{"nom": "Flamgeist", "type": "Feu", ...}'
    )

with col2:
    st.subheader("⚔️ L'Adversaire")
    json_adversaire = st.text_area(
        "Collez ici le JSON de l'adversaire",
        height=200,
        placeholder='{"nom": "Aquashock", "type": "Eau", ...}'
    )

# ------------------------------
# Bouton pour vérifier JSON
# ------------------------------
if st.button("Valider les JSON et préparer le combat"):
    # Validation du champion
    success_champion, result_champion = decoder_pokemon(json_champion)
    success_adversaire, result_adversaire = decoder_pokemon(json_adversaire)
    
    if success_champion and success_adversaire:
        st.success("✅ JSON valides et prêts pour l'arène !")
        st.write(f"**Terrain sélectionné :** {terrain}")
        
        # Affichage des informations des Pokémon
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("### 🛡️ Champion")
            st.write(f"**Nom :** {result_champion['Nom']}")
            st.write(f"**Type :** {result_champion['Type']}")
            if 'description' in result_champion:
                st.write(f"**Description :** {result_champion['description']}")
            if 'personnalite' in result_champion:
                st.write(f"**Personnalité :** {result_champion['personnalite']}")
            if 'stats' in result_champion:
                st.write(f"**Stats :** {result_champion['stats']}")
            
        with col_info2:
            st.markdown("### ⚔️ Adversaire")
            st.write(f"**Nom :** {result_adversaire['Nom']}")
            st.write(f"**Type :** {result_adversaire['Type']}")
            st.write(f"**Description :** {result_adversaire['description']}")
            st.write(f"**Personnalité :** {result_adversaire['personnalite']}")
            st.write(f"**Stats :** {result_adversaire['stats']}")
            
        # Stocker dans session_state pour usage ultérieur
        st.session_state['champion'] = result_champion
        st.session_state['adversaire'] = result_adversaire
        st.session_state['terrain'] = terrain
        
    else:
        # Affichage des erreurs
        if not success_champion:
            st.error(f"❌ **Erreur Champion :** {result_champion}")
        if not success_adversaire:
            st.error(f"❌ **Erreur Adversaire :** {result_adversaire}")