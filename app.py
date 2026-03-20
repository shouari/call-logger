"""
Qualification d'appel SAV — UX Widescreen Optimisée
===================================================
Ouverture automatique par 3CX via ?phone=...&name=...
Saisie rapide en 2 colonnes sans sections cachées.
"""

import streamlit as st
import streamlit.components.v1 as components

# ── Config ──────────────────────────────────────
st.set_page_config(
    page_title="Qualification Appel SAV",
    page_icon="📞",
    layout="wide",
)

# ── Paramètres URL (3CX) ───────────────────────
def get_param(key: str, default: str = "") -> str:
    val = st.query_params.get(key, default)
    if isinstance(val, list):
        return val[0] if val else default
    return str(val) if val else default

url_phone = get_param("phone")
url_name = get_param("name")

# ── En-tête : Titre & Barre de progression ─────
st.title("📞 Qualification Appel SAV")

# ── Barre de progression au sommet ─────────────
score = 0
total_champs_requis = 6

val_appelant = st.session_state.get("appelant", url_name)
val_telephone = st.session_state.get("telephone", url_phone)
if val_appelant or val_telephone: score += 1
if st.session_state.get("client"): score += 1
if st.session_state.get("probleme"): score += 1
if st.session_state.get("systeme"): score += 1
if st.session_state.get("acces"): score += 1
if st.session_state.get("priorite"): score += 1

progression = min(1.0, score / total_champs_requis)
st.markdown(f"**Fiche Completée à : {int(progression * 100)}%**")
st.progress(progression)
st.markdown("---")

# ── Disposition 2 Colonnes ─────────────────────
col_gauche, col_droite = st.columns([1, 1], gap="large")

with col_gauche:
    st.subheader("👤 Informations Principales")

    col_id1, col_id2 = st.columns(2)
    with col_id1:
        appelant = st.text_input("Nom / Appelant", value=url_name, key="appelant")
    with col_id2:
        telephone = st.text_input("Téléphone", value=url_phone, key="telephone")

    col_cli1, col_cli2 = st.columns(2)
    with col_cli1:
        client = st.text_input("Client", key="client")
    with col_cli2:
        contact = st.text_input("Contact sur place", key="contact")

    site = st.text_input("Site / Adresse", key="site")

    st.markdown("---")
    
    # ── Champ problème mis en valeur ───────────────
    probleme = st.text_area(
        "📝 Problème (OBLIGATOIRE)",
        height=150,
        placeholder="Décrivez clairement ce qui ne fonctionne pas...",
        key="probleme",
    )


with col_droite:
    st.subheader("⚙️ Qualification de l'intervention")

    # Boutons Système horizontaux au lieu d'un menu
    systeme = st.radio(
        "Système concerné",
        options=["", "Réseau", "Audio", "Vidéo", "Contrôle d'accès", "Alarme", "Éclairage", "Wifi", "Autres"],
        index=0,
        horizontal=True,
        key="systeme",
    )

    depuis = st.radio(
        "Depuis quand",
        options=["", "Aujourd'hui", "Hier", "Cette semaine", "Inconnu"],
        index=0,
        horizontal=True,
        key="depuis",
    )

    tentatives = st.text_area("Tentatives déjà faites", height=68, key="tentatives")

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        acces = st.radio(
            "Accès au site",
            options=["", "Libre", "Rdv", "Restreint"],
            index=0,
            key="acces",
        )
    with col_opt2:
        priorite = st.radio(
            "Priorité",
            options=["", "Aujourd'hui", "Urgent", "Semaine", "Planifiable"],
            index=0,
            key="priorite",
        )

    infos = st.text_area("Informations utiles", height=68, key="infos")



# ── Génération du résumé ────────────────────────
def generer_resume() -> str:
    lines = []
    
    # Bloc 1: Appelant
    if appelant: lines.append(f"Appelant: {appelant}")
    if telephone: lines.append(f"Téléphone: {telephone}")
    if client: lines.append(f"Client: {client}")
    if site: lines.append(f"Site: {site}")
    if contact: lines.append(f"Contact: {contact}")
    lines.append("")

    # Bloc 2: Qualification
    if systeme: lines.append(f"Système: {systeme}")
    if depuis: lines.append(f"Depuis: {depuis}")
    if tentatives: lines.append(f"Tentatives: {tentatives.strip()}")
    if acces: lines.append(f"Accès: {acces}")
    if priorite: lines.append(f"Priorité: {priorite}")
    
    if len(lines) > 6:  # S'il y a des infos de qualification on saute une ligne
        lines.append("")

    # Bloc 3: Problème
    if probleme:
        lines.append("Problème:")
        lines.append(probleme.strip())
        lines.append("")

    # Bloc 4: Infos utiles
    if infos:
        lines.append("Informations utiles:")
        lines.append(infos.strip())
        lines.append("")

    # Bloc 5: Résumé final condensé (pour copier dans une seule ligne)
    resume_compact = []
    if probleme:
        resume_compact.append(probleme.strip().split("\n")[0])
    if systeme: resume_compact.append(f"Système: {systeme}")
    if depuis: resume_compact.append(f"Depuis: {depuis}")
    if tentatives: resume_compact.append(f"Tentatives: {tentatives.strip()}")
    if acces: resume_compact.append(f"Accès: {acces}")
    if priorite: resume_compact.append(f"Priorité: {priorite}")
    if infos: resume_compact.append(f"Infos utiles: {infos.strip().split(chr(10))[0]}")
    
    if resume_compact:
        lines.append("Résumé:")
        lines.append(" | ".join(resume_compact))

    # Nettoyage des lignes vides consécutives
    final_text = "\n".join(lines).strip()
    return final_text.replace("\n\n\n", "\n\n")

resume = generer_resume()


# ── Action : Résumé et Copie ─────────────────────
st.markdown("---")
col_res, col_btn = st.columns([2, 1])

with col_res:
    st.subheader("📋 Résumé généré")
    st.code(resume if resume.strip() else "Remplissez les champs pour générer le résumé.", language=None)

with col_btn:
    st.write("<br><br>", unsafe_allow_html=True)
    resume_js = resume.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$").replace("'", "\\'")

    copy_html = f"""
    <button id="copyBtn" onclick="
        var btn = document.getElementById('copyBtn');
        navigator.clipboard.writeText(`{resume_js}`).then(function() {{
            btn.innerText = '✅ Copié !';
            btn.style.background = '#0f9d58'; /* Vert succès */
            setTimeout(function() {{
                btn.innerText = '📋 Copier le résumé';
                btn.style.background = '#ff4b4b'; /* Retour au rouge */
            }}, 2500);
        }}).catch(function() {{
            var ta = document.createElement('textarea');
            ta.value = `{resume_js}`;
            document.body.appendChild(ta);
            ta.select();
            document.execCommand('copy');
            document.body.removeChild(ta);
            btn.innerText = '✅ Copié !';
            btn.style.background = '#0f9d58';
            setTimeout(function() {{
                btn.innerText = '📋 Copier le résumé';
                btn.style.background = '#ff4b4b';
            }}, 2500);
        }});
    " style="
        width: 100%;
        padding: 20px;
        font-size: 1.3rem;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        background: #ff4b4b; /* Rouge Streamlit par defaut */
        color: white;
        transition: 0.2s all;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">📋 Copier le résumé</button>
    """
    components.html(copy_html, height=100)
    
    if st.button("🔄 Nouvel appel", use_container_width=True):
        for key in ["client", "contact", "site", "probleme", "tentatives", "infos"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()