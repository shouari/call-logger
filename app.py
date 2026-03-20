"""
Qualification d'appel SAV — Mini App Streamlit
================================================
Destinée à être ouverte par 3CX via URL avec paramètres ?phone=...&name=...
Génère un résumé structuré prêt à copier-coller dans D-Tools.
"""

import streamlit as st
from datetime import datetime

# ──────────────────────────────────────────────
# Configuration de la page
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Qualification Appel SAV",
    page_icon="📞",
    layout="centered",
)

# ──────────────────────────────────────────────
# Lecture sécurisée des paramètres URL
# ──────────────────────────────────────────────
def get_url_param(key: str, default: str = "") -> str:
    """Récupère un paramètre URL de manière sûre (gestion liste/str)."""
    params = st.query_params
    value = params.get(key, default)
    if isinstance(value, list):
        return value[0] if value else default
    return str(value) if value else default


url_phone = get_url_param("phone")
url_name = get_url_param("name")


# ──────────────────────────────────────────────
# En-tête
# ──────────────────────────────────────────────
st.title("📞 Qualification Appel SAV")
st.caption("Remplir · Générer · Copier dans D-Tools")

# Badge appelant (données 3CX)
if url_name or url_phone:
    phone_display = url_phone if url_phone else "—"
    name_display = url_name if url_name else "—"
    st.info(f"👤 **{name_display}**  ·  📱 {phone_display}")


# ──────────────────────────────────────────────
# Formulaire de saisie
# ──────────────────────────────────────────────

# --- Section 1 : Appelant ---
st.subheader("👤 Appelant")

col1, col2 = st.columns(2)
with col1:
    appelant = st.text_input("Nom / Appelant", value=url_name, key="appelant")
with col2:
    telephone = st.text_input("Téléphone", value=url_phone, key="telephone")

col3, col4 = st.columns(2)
with col3:
    client = st.text_input("Client (entreprise)", key="client")
with col4:
    contact = st.text_input("Contact sur place", key="contact")

site = st.text_input("Site / Adresse", key="site")


# --- Section 2 : Problème ---
st.subheader("⚠️ Problème")

col5, col6 = st.columns(2)
with col5:
    systeme = st.selectbox(
        "Système concerné",
        ["", "Réseau",  "Audio", "Vidéo", "Contrôle d'accès", "Alarme", "Éclairage", "Wifi", "Autres"],
        key="systeme",
    )
with col6:
    zone = st.text_input("Zone / Pièce", key="zone")

col7, col8 = st.columns(2)
with col7:
    depuis = st.selectbox(
        "Depuis quand",
        ["", "Aujourd'hui", "Hier", "Cette semaine", "Plus d'une semaine", "Inconnu"],
        key="depuis",
    )
with col8:
    frequence = st.selectbox(
        "Fréquence",
        ["", "Permanent", "Intermittent", "Ponctuel", "Première fois"],
        key="frequence",
    )

col9, col10 = st.columns(2)
with col9:
    acces = st.selectbox(
        "Accès au site",
        ["", "Libre", "Sur rendez-vous", "Restreint"],
        key="acces",
    )
with col10:
    priorite = st.selectbox(
        "Priorité",
        ["", "Urgent", "Aujourd'hui", "Cette semaine", "Planifiable"],
        key="priorite",
    )

tentatives = st.text_area("Tentatives déjà faites", height=80, key="tentatives")

probleme = st.text_area("Problème décrit par le client", height=100, key="probleme")
infos = st.text_area("Informations utiles / Notes", height=80, key="infos")


# ──────────────────────────────────────────────
# Génération du résumé structuré
# ──────────────────────────────────────────────
def generer_resume() -> str:
    """Génère le texte structuré prêt à copier-coller dans D-Tools."""
    lignes = []

    # Bloc appelant
    lignes.append(f"Appelant: {appelant}")
    lignes.append(f"Téléphone: {telephone}")
    if client:
        lignes.append(f"Client: {client}")
    if site:
        lignes.append(f"Site: {site}")
    if contact:
        lignes.append(f"Contact: {contact}")

    # Séparateur
    lignes.append("")

    # Bloc problème
    if systeme:
        lignes.append(f"Système: {systeme}")
    if zone:
        lignes.append(f"Zone: {zone}")
    if depuis:
        lignes.append(f"Depuis: {depuis}")
    if frequence:
        lignes.append(f"Fréquence: {frequence}")
    if tentatives:
        lignes.append(f"Tentatives: {tentatives}")
    if acces:
        lignes.append(f"Accès: {acces}")
    if priorite:
        lignes.append(f"Priorité: {priorite}")

    # Séparateur + problème
    if probleme:
        lignes.append("")
        lignes.append("Problème:")
        lignes.append(probleme)

    # Infos utiles
    if infos:
        lignes.append("")
        lignes.append("Informations utiles:")
        lignes.append(infos)

    # Ligne résumé condensé
    parties_resume = []
    if probleme:
        # Première ligne seulement pour le résumé condensé
        premiere_ligne = probleme.strip().split("\n")[0]
        parties_resume.append(premiere_ligne)
    if systeme:
        parties_resume.append(f"Système: {systeme}")
    if depuis:
        parties_resume.append(f"Depuis: {depuis}")
    if frequence:
        parties_resume.append(f"Fréquence: {frequence}")
    if tentatives:
        parties_resume.append(f"Tentatives: {tentatives}")
    if acces:
        parties_resume.append(f"Accès: {acces}")
    if priorite:
        parties_resume.append(f"Priorité: {priorite}")
    if infos:
        premiere_info = infos.strip().split("\n")[0]
        parties_resume.append(f"Infos utiles: {premiere_info}")

    if parties_resume:
        lignes.append("")
        lignes.append("Résumé:")
        lignes.append(" | ".join(parties_resume))

    return "\n".join(lignes)


# ──────────────────────────────────────────────
# Bouton Générer + Affichage
# ──────────────────────────────────────────────
st.subheader("📋 Résumé généré")

resume = generer_resume()

# Affichage du résumé dans une zone lisible
st.code(resume, language=None)

st.markdown("")

# --- Boutons d'action ---
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Bouton copier via JS (clipboard API)
    # On échappe le texte pour JavaScript
    resume_escaped = resume.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    copy_js = f"""
    <button onclick="
        navigator.clipboard.writeText(`{resume_escaped}`).then(function() {{
            document.getElementById('copy-status').innerHTML = '✅ Copié dans le presse-papiers !';
            setTimeout(function() {{
                document.getElementById('copy-status').innerHTML = '';
            }}, 3000);
        }}).catch(function() {{
            // Fallback pour navigateurs restrictifs
            var ta = document.createElement('textarea');
            ta.value = `{resume_escaped}`;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            document.getElementById('copy-status').innerHTML = '✅ Copié !';
            setTimeout(function() {{
                document.getElementById('copy-status').innerHTML = '';
            }}, 3000);
        }});
    " style="
        width: 100%;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
    ">
        📋 Copier le texte
    </button>
    <div id="copy-status" style="text-align:center;margin-top:0.3rem;"></div>
    """
    st.markdown(copy_js, unsafe_allow_html=True)

with col_btn2:
    # Bouton télécharger en .txt
    horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"appel_{horodatage}.txt"
    st.download_button(
        label="💾 Télécharger (.txt)",
        data=resume,
        file_name=nom_fichier,
        mime="text/plain",
    )


# ──────────────────────────────────────────────
# Bouton Réinitialiser
# ──────────────────────────────────────────────
st.markdown("")
if st.button("🔄 Nouvel appel", use_container_width=True):
    # Nettoyer tous les champs sauf appelant/téléphone (qui viennent de l'URL)
    for key in ["client", "contact", "site", "systeme", "zone",
                 "depuis", "frequence", "tentatives", "acces", "priorite",
                 "probleme", "infos"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# ──────────────────────────────────────────────
# Debug : paramètres URL (repliable)
# ──────────────────────────────────────────────
with st.expander("🔧 Debug — Paramètres URL reçus"):
    all_params = dict(st.query_params)
    if all_params:
        for k, v in all_params.items():
            st.markdown(f"**{k}** = `{v}`")
    else:
        st.info("Aucun paramètre URL détecté.")
    st.markdown(f"**Horodatage** : `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")