import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION ---
DESTINATAIRE = "contact@cafe-corto.com"
# /!\ REMPLACEZ CES DEUX LIGNES PAR VOS INFOS GMAIL /!\
EMAIL_EXPEDITEUR = "contact@cafe-corto.com" 
MOT_DE_PASSE_APP = "wqaa uqkp tftl wngm" 

st.set_page_config(page_title="Café Corto - Espace Pro", page_icon="☕", layout="wide")

# STYLE CAFÉ CORTO (Blanc, Noir, Rouge)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .stButton>button {{ background-color: #E63946; color: white; font-weight: bold; border: none; }}
    .stButton>button:hover {{ background-color: #000000; color: white; }}
    h1, h2, h3, p, span, label {{ color: #000000 !important; }}
    div[data-testid="stMetricValue"] {{ color: #E63946 !important; }}
    </style>
    """, unsafe_allow_html=True)

# DONNÉES CLIENTS ET PRODUITS
USERS = {
    "corto_pro": {"password": "cafe2026", "nom": "Client Partenaire"},
    "sylvain_ruf": {"password": "emmalaplusbelle", "nom": "Sylvain Ruf"}
}
data_produits = {
    'Réf': ['GUAPO', 'KOPI', 'BACAN', 'COSURCA', 'SIDAMA', 'TAFACCE'],
    'Nom': ['GUAPO - Guatemala', 'KOPI - Indonésie', 'BACAN - Pérou', 'COSURCA - Colombie', 'SIDAMA - Éthiopie', 'TAFACCE - Éthiopie'],
    'Prix_HT': [28.0, 32.0, 26.5, 29.0, 31.0, 33.0]
}
df_tarifs = pd.DataFrame(data_produits)

# FONCTION ENVOI MAIL
def envoyer_email(client_nom, detail_commande, total, notes):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EXPEDITEUR
    msg['To'] = DESTINATAIRE
    msg['Subject'] = f"🔴 NOUVELLE COMMANDE PRO - {client_nom}"

    corps = f"Client : {client_nom}\n\nProduits commandés :\n{detail_commande}\n\nTOTAL : {total}€ HT\n\nNotes client : {notes}"
    msg.attach(MIMEText(corps, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE_APP)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erreur d'envoi : {e}")
        return False

# LOGIQUE D'ACCÈS
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        try: st.image("CAFE-CORTO-Logo-noir.png", width=300)
        except: st.header("Café Corto")
        with st.form("login"):
            u, p = st.text_input("Identifiant"), st.text_input("Mdp", type="password")
            if st.form_submit_button("Se connecter"):
                if u in USERS and USERS[u]["password"] == p:
                    st.session_state["logged_in"], st.session_state["user"] = True, USERS[u]
                    st.rerun()
else:
    # INTERFACE COMMANDE
    st.title("🛒 Atelier Café Corto - Commandes")
    panier = []
    for idx, row in df_tarifs.iterrows():
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.write(f"**{row['Nom']}**")
        c2.write(f"{row['Prix_HT']}€ HT/kg")
        qte = c3.number_input("kg", min_value=0, key=f"q_{idx}")
        if qte > 0:
            panier.append({"Produit": row['Nom'], "Qté": qte, "Total": qte * row['Prix_HT']})
    
    if panier:
        st.divider()
        df_p = pd.DataFrame(panier)
        st.table(df_p)
        total = df_p["Total"].sum()
        st.metric("Réglement selon vos conditions habituelles", f"{total:.2f} € HT")
        notes = st.text_area("Notes de livraison")
        
        if st.button("🚀 VALIDER LA COMMANDE"):
            detail = df_p.to_string(index=False)
            if envoyer_email(st.session_state["user"]["nom"], detail, total, notes):
                st.success("Commande envoyée avec succès à l'atelier !")
                st.balloons()
