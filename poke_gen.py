import streamlit as st
import pandas as pd
from groq import Groq
import json

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
    
    # on parse le JSON
    data_dict = json.loads(data)
    
    # on extrait la liste des Pokémon
    if "pokemon" in data_dict:
        pokemon_list = data_dict["pokemon"]
    else:
        # Si la structure est différente, on prend la première clé
        pokemon_list = list(data_dict.values())[0]
    
    # on crée le DataFrame à partir de la liste
    df = pd.DataFrame(pokemon_list)
    
    # on normalise les colonnes dès la création
    df.columns = [str(c).strip().lower() for c in df.columns]

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

# ------------------------------------------------------
# Fonction pour trouver le Pokémon le plus compatible
# ------------------------------------------------------
def trouver_compagnon(api_key, dataframe, description_user):
    client = Groq(api_key=api_key)

    # on converti le DataFrame en texte
    liste_texte = dataframe.to_json(orient="records", force_ascii=False)

    system_prompt = """
Tu es un moteur de recommandation Pokémon.
Tu DOIS répondre en JSON strict, sans texte supplémentaire.
Ton but : choisir le Pokémon dont la personnalité ou la description
correspond le mieux à l'utilisateur.
La réponse doit obligatoirement suivre ce format :

{
    "choix": "NomDuPokemon"
}
"""

    user_prompt = f"""
Voici la liste des Pokémon disponibles (en JSON) :
{liste_texte}

Voici la personnalité du dresseur :
"{description_user}"

Choisis le Pokémon le plus compatible et renvoie uniquement son nom dans le JSON demandé.
"""

    # on appel l'API
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    # on convertit le JSON en dict
    resultat_json = json.loads(completion.choices[0].message.content)
    nom_choisi = resultat_json["choix"]

    return nom_choisi


# ------------------------------------------------------
# Bouton : lancer la recommandation
# ------------------------------------------------------
if st.session_state["pokemons"] is not None and description_user:
    if st.button("🔍 Trouver mon Pokémon compagnon"):
        with st.spinner("Analyse de compatibilité en cours..."):
            nom_compagnon = trouver_compagnon(api_key, st.session_state["pokemons"], description_user)
            st.session_state["nom_compagnon"] = nom_compagnon
        st.success(f"Ton compagnon idéal est : **{nom_compagnon}** !")

# ------------------------------------------------------
# Affichage de la carte d'identité en JSON
# ------------------------------------------------------
st.subheader("📄 Carte d'identité du champion")

pokemons = st.session_state.get("pokemons")
nom_compagnon = st.session_state.get("nom_compagnon")

if pokemons is not None and isinstance(pokemons, pd.DataFrame) and not pokemons.empty:
    
    # on cherche dynamiquement la colonne correspondant au nom
    name_col = next((c for c in pokemons.columns if "nom" in c), None)
    
    if name_col is None:
        st.error("Impossible de trouver la colonne contenant le nom des Pokémon.")
        st.write("Colonnes trouvées :", pokemons.columns.tolist())
    elif not nom_compagnon:
        st.info("Cliquez d'abord sur 'Trouver mon Pokémon compagnon' pour générer la carte d'identité.")
    else:
        # on normalise le nom du compagnon pour la recherche
        nom_compagnon_lower = nom_compagnon.lower()
        
        # on filtrer le Pokémon choisi
        selection = pokemons[pokemons[name_col].str.lower() == nom_compagnon_lower]

        if not selection.empty:
            st.write("### ⭐ Pokémon choisi")
            
            # on affiche toutes les informations disponibles
            for col in pokemons.columns:
                valeur = selection.iloc[0][col]
                col_affichage = col.capitalize()
                st.write(f"**{col_affichage} :** {valeur}")

            # Carte d'identité JSON
            data_json = selection.iloc[0].to_dict()
            json_brut = json.dumps(data_json, ensure_ascii=False, indent=4)
            st.markdown("---")
            st.markdown("**📋 Copiez ce code JSON, il est la carte d'identité de votre champion :**")
            st.code(json_brut, language="json")
        else:
            st.warning(f"Le Pokémon '{nom_compagnon}' n'a pas été trouvé dans la liste.")
            st.write("Pokémon disponibles :", pokemons[name_col].tolist())
else:
    st.info("Aucun Pokémon généré pour le moment.")