import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURATION ---
DESTINATAIRE = "contact@cafe-corto.com"
EMAIL_EXPEDITEUR = "contact@cafe-corto.com" 
MOT_DE_PASSE_APP = "wqaa uqkp tftl wngm" 

st.set_page_config(page_title="Café Corto - Espace Pro", page_icon="☕", layout="wide")

# STYLE CAFÉ CORTO (Blanc, Noir, Rouge)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF; }}
    .stButton>button {{ background-color: #E63946; color: white; font-weight: bold; border: none; width: 100%; }}
    .stButton>button:hover {{ background-color: #000000; color: white; }}
    h1, h2, h3, p, span, label {{ color: #000000 !important; }}
    div[data-testid="stMetricValue"] {{ color: #E63946 !important; }}
    .product-row {{ padding: 10px; border-bottom: 1px solid #eee; }}
    </style>
    """, unsafe_allow_html=True)

# DONNÉES CLIENTS
USERS = {
    "corto_pro": {"password": "cafe2026", "nom": "Client Partenaire"},
    "sylvain_ruf": {"password": "emmalaplusbelle", "nom": "Sylvain Ruf"}
}

# --- CATALOGUE PRODUITS ---
data_produits = [
    {"Café": "GUAPO - Guatemala", "Prix_1kg": 28.00, "Prix_250g": 6.50},
    {"Café": "KOPI - Indonésie", "Prix_1kg": 28.00, "Prix_250g": 7.20},
    {"Café": "BACAN - Pérou", "Prix_1kg": 28.00, "Prix_250g": 6.70},
    {"Café": "SIDAMA - Éthiopie", "Prix_1kg": 33.00, "Prix_250g": 8.20},
    {"Café": "COSURCA - Colombie", "Prix_1kg": 30.00, "Prix_250g": 7.70},
    {"Café": "TAFACCE - Éthiopie", "Prix_1kg": 35.00, "Prix_250g": 9.00},
    {"Café": "DECAF - Mexique", "Prix_1kg": 28.00, "Prix_250g": 7.00}
]

# FONCTION ENVOI MAIL
def envoyer_email(client_nom, detail_commande, total, notes):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EXPEDITEUR
    msg['To'] = DESTINATAIRE
    msg['Subject'] = f"🔴 NOUVELLE COMMANDE PRO - {client_nom}"

    corps = f"Client : {client_nom}\n\nProduits commandés :\n{detail_commande}\n\nTOTAL : {total:.2f}€ HT\n\nNotes client : {notes}"
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
            u = st.text_input("Identifiant")
            p = st.text_input("Mdp", type="password")
            if st.form_submit_button("Se connecter"):
                if u in USERS and USERS[u]["password"] == p:
                    st.session_state["logged_in"], st.session_state["user"] = True, USERS[u]
                    st.rerun()
                else:
                    st.error("Identifiants incorrects")
else:
    # INTERFACE COMMANDE
    st.title("🛒 Atelier Café Corto - Commandes")
    st.write(f"Bienvenue, **{st.session_state['user']['nom']}**")
    
    panier_liste = []
    
   # En-tête du tableau
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.write("**Variété de Café**")
    h2.write("**Format 1kg**")
    h3.write("**Format 250g**")
    st.divider()
