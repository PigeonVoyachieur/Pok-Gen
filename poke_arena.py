import streamlit as st
import json
from groq import Groq
import base64

def load_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ------------------------------
# Configuration de la page
# ------------------------------
st.set_page_config(
    page_title="🏟️ Arène Pokémon",
    page_icon="⚔️",
    layout="wide"
)

champion_img = load_image_base64("ChampionSprite.png")
adversaire_img = load_image_base64("AdversaireSprite.png")


st.title("🏟️ Arène Pokémon")
st.write("Préparez votre champion pour l'affrontement ! Chargez les JSON et choisissez le terrain.")

st.sidebar.header("⚙️ Paramètres")
cle_api = st.sidebar.text_input(
    "Clé API Groq",
    type="password",
    help="Entrez votre clé API Groq pour activer l'arbitre IA."
)
if not cle_api:
    st.sidebar.warning("Entrez votre clé API pour utiliser l'arbitre IA.")

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
    ["Volcan", "Océan", "Espace", "Forêt", "Désert", "Glace", "Montagne", "Plaines", "Caverne", "Ville", "Ruines", "Île Tropicale", "Champ de Fleurs", "Marais", "Jungle", "Savane", "Toundra", "Temple Ancien", "Côte Rocheuse"],
    index=0
)

# ------------------------------
# Colonnes pour afficher JSON
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mon Champion")
    st.markdown(
        f"""
        <img src="data:image/png;base64,{champion_img}" style="max-height:80px;">
        """,
        unsafe_allow_html=True
    )
    json_champion = st.text_area(
        "Collez ici le JSON de votre champion",
        height=200,
        placeholder='{"nom": "Flamgeist", "type": "Feu", ...}'
    )

with col2:
    st.subheader("L'Adversaire")
    st.markdown(
        f"""
        <img src="data:image/png;base64,{adversaire_img}" style="max-height:80px;">
        """,
        unsafe_allow_html=True
    )
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

# ==========================================================
# Simulation du combat
# ==========================================================

st.markdown("---")
st.header("⚔️ L'Arbitre IA : Simulation du combat")

# Bouton pour lancer le combat
if st.button("🔥 Lancer le combat !"):
    # Vérifier que les données existent dans session_state
    if "champion" not in st.session_state or "adversaire" not in st.session_state:
        st.error("❌ Vous devez d'abord valider les JSON des Pokémon.")
    else:
        champion = st.session_state["champion"]
        adversaire = st.session_state["adversaire"]
        terrain = st.session_state["terrain"]

        # Initialisation API Groq
        if cle_api:
            client = Groq(api_key=cle_api)
        else:
            client = None



        # ------------------------------------------------------
        # Prompt Système avec les règles obligatoires pour l'IA
        # ------------------------------------------------------
        prompt_system = """
Tu es un COMMENTATEUR SPORTIF épique et un ARBITRE impartial.

Tu dois STRICTEMENT respecter les règles suivantes :

1. Rôle :
   - Tu commentes le combat de manière héroïque, dynamique, comme si tu étais dans une grande arène.
   - Tu restes neutre, aucun favoritisme.

2. Analyse :
   - Compare les TYPES des Pokémon (ex : l’Eau bat le Feu).
   - Analyse aussi leurs DESCRIPTIONS et PERSONNALITÉS.
   - Utilise leurs STATS pour influencer le déroulement.

3. Contexte :
   - Le TERRAIN influence le combat (ex : Volcan avantage Feu, Océan avantage Eau...)

4. Storytelling :
   - Le combat doit toujours être raconté en 3 PHASES :
       Phase 1 : Le Début
       Phase 2 : Le Retournement
       Phase 3 : La Fin

5. Verdict :
   - Tu dois terminer par la phrase EXACTE :
     VAINQUEUR : [Nom du Pokémon]
   - Cette phrase doit être la dernière ligne de ta réponse.
        """

        # ------------------------------------------------------
        # Prompt Utilisateur avec les données du combat
        # ------------------------------------------------------
        prompt_user = f"""
Voici les données du combat :

=== COMBATTANT 1 ===
{json.dumps(champion, indent=2)}

=== COMBATTANT 2 ===
{json.dumps(adversaire, indent=2)}

=== TERRAIN ===
{terrain}

Raconte le combat comme demandé.
        """

        # Appel API
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user},
                ]
            )

            result = completion.choices[0].message.content

            # Affichage du commentaire de combat
            st.subheader("📣 Résumé Épique du Combat")
            st.write(result)

            # ------------------------------------------------------
            # Extraction automatique du vainqueur
            # ------------------------------------------------------
            import re
            match = re.search(r"VAINQUEUR\s*:\s*(.*)", result)
            if match:
                vainqueur = match.group(1).strip()
                st.success(f"🏆 **Vainqueur détecté : {vainqueur}**")
            else:
                st.warning("⚠️ Impossible d'extraire automatiquement le vainqueur.")

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'IA : {e}")
