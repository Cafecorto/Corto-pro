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

# STYLE CAFÉ CORTO
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .stButton>button { background-color: #E63946; color: white; font-weight: bold; border: none; width: 100%; }
    h1, h2, h3, p, span, label { color: #000000 !important; }
    div[data-testid="stMetricValue"] { color: #E63946 !important; }
    </style>
    """, unsafe_allow_html=True)

# DONNÉES
USERS = {
    "corto_pro": {"password": "cafe2026", "nom": "Client Partenaire"},
    "sylvain_ruf": {"password": "emmalaplusbelle", "nom": "Sylvain Ruf"}
}

data_produits = [
    {"Café": "GUAPO - Guatemala", "Prix_1kg": 28.00, "Prix_250g": 6.50},
    {"Café": "KOPI - Indonésie", "Prix_1kg": 28.00, "Prix_250g": 7.20},
    {"Café": "BACAN - Pérou", "Prix_1kg": 28.00, "Prix_250g": 6.70},
    {"Café": "SIDAMA - Éthiopie", "Prix_1kg": 33.00, "Prix_250g": 8.20},
    {"Café": "COSURCA - Colombie", "Prix_1kg": 30.00, "Prix_250g": 7.70},
    {"Café": "TAFACCE - Éthiopie", "Prix_1kg": 35.00, "Prix_250g": 9.00},
    {"Café": "DECAF - Mexique", "Prix_1kg": 28.00, "Prix_250g": 7.00}
]

def envoyer_email(client_nom, detail_commande, total, notes):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_EXPEDITEUR
    msg['To'] = DESTINATAIRE
    msg['Subject'] = f"🔴 COMMANDE PRO - {client_nom}"
    corps = f"Client : {client_nom}\n\nProduits :\n{detail_commande}\n\nTOTAL : {total:.2f}€ HT\n\nNotes : {notes}"
    msg.attach(MIMEText(corps, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_EXPEDITEUR, MOT_DE_PASSE_APP)
        server.send_message(msg)
        server.quit()
        return True
    except: return False

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
                else: st.error("Erreur d'accès")
else:
    st.title("🛒 Atelier Café Corto - Commandes")
    st.write(f"Bienvenue, **{st.session_state['user']['nom']}**")
    
    panier_liste = []
    
    # En-tête
    h1, h2, h3 = st.columns([2, 1, 1])
    h1.write("**Variété**")
    h2.write("**Format 1kg**")
    h3.write("**Format 250g**")
    st.divider()

    # ICI LA BOUCLE QUI DEVAIT S'AFFICHER
    for p in data_produits:
        c1, c2, c3 = st.columns([2, 1, 1])
        c1.write(f"**{p['Café']}**")
        
        q_1k = c2.number_input(f"Qté (à {p['Prix_1kg']}€)", min_value=0, step=1, key=f"1k_{p['Café']}")
        if q_1k > 0:
            panier_liste.append({"Produit": p['Café'], "Format": "1kg", "Qté": q_1k, "Total": q_1k * p['Prix_1kg']})
            
        q_25 = c3.number_input(f"Qté (à {p['Prix_250g']}€)", min_value=0, step=1, key=f"25_{p['Café']}")
        if q_25 > 0:
            panier_liste.append({"Produit": p['Café'], "Format": "250g", "Qté": q_25, "Total": q_25 * p['Prix_250g']})

    if panier_liste:
        st.divider()
        df_p = pd.DataFrame(panier_liste)
        st.table(df_p[["Produit", "Format", "Qté", "Total"]])
        total_final = df_p["Total"].sum()
        st.metric("Total", f"{total_final:.2f} € HT")
        notes = st.text_area("Notes de livraison")
        
        if st.button("🚀 VALIDER LA COMMANDE"):
            if envoyer_email(st.session_state["user"]["nom"], df_p.to_string(index=False), total_final, notes):
                st.success("Commande envoyée !")
                st.balloons()
