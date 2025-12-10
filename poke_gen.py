import streamlit as st
import pandas as pd
from groq import Groq

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

# ------------------------------------------------------
# Générer une liste de Pokémon via Groq
# ------------------------------------------------------
def generer_pokemon(api_key, nb_pokemon, type_dominant):
    client = Groq(api_key=api_key)

    # On impose la réponse en JSON strict
    system_prompt = f"""
Tu es une API de génération de Pokémon.
Tu DOIS répondre exclusivement en JSON, sans texte avant ou après.

Tu dois générer une liste de {nb_pokemon} Pokémon originaux.
Chaque Pokémon doit suivre EXACTEMENT cette structure :

{{
  "pokemon": [
    {{
      "Nom": "Nom du Pokémon",
      "Type": "Type principal (ou lié au thème si fourni)",
      "Description": "Description courte",
      "Personnalite": "Personnalité utile pour du matching futur",
      "Stats": "Résumé des statistiques (ex: 'Rapide mais fragile')"
    }}
  ]
}}

Si l'utilisateur fournit un type dominant ou un thème, comme "{type_dominant}",
il doit influencer légèrement les créations.
"""

    # On appel l'API Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Génère maintenant les Pokémon."}
        ],
        response_format={"type": "json_object"},
    )

    # On récupère le JSON généré
    data = completion.choices[0].message.content

    #  On convertie le JSON en DataFrame
    df = pd.DataFrame(pd.read_json(data)["pokemon"])

    return df

# ------------------------------------------------------
# Bloc Streamlit : Génération et affichage
# ------------------------------------------------------
st.subheader("🧬 Génération des Pokémon")

if "pokemons" not in st.session_state:
    st.session_state["pokemons"] = None

if api_key:
    if st.button("Générer des Pokémon"):
        with st.spinner("Création des Pokémon en cours..."):
            df_poke = generer_pokemon(api_key, nb_pokemon, type_dominant)
            st.session_state["pokemons"] = df_poke
        st.success("Pokémon générés avec succès !")

# On affiche les Pokémon de façon persistante
if st.session_state["pokemons"] is not None:
    st.dataframe(st.session_state["pokemons"])

# ------------------------------------------------------
# Zone de texte pour la personnalité du dresseur
# ------------------------------------------------------
st.subheader("🔮 Oracle de Recommandation")

description_user = st.text_area(
    "Décris ta personnalité",
    placeholder="Ex : J'aime les combats stratégiques et les créatures loyales."
)

