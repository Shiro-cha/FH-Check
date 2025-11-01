import streamlit as st

# === Config page ===
st.set_page_config(page_title="FH-Check - Connexion", page_icon="🔒", layout="centered")

# === Initialisation session ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# === Page Login ===
if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            background-image: url("https://upload.wikimedia.org/wikipedia/commons/c/c1/Telecom_tower.jpg");
            background-size: cover;
            background-position: center;
        }
        .login-box {
            background: rgba(0,0,0,0.7);
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("📡 FH-Check")
    st.subheader("Système de supervision intelligente FH")
    st.write("Veuillez vous connecter pour continuer 🔒")

    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        if username == "admin" and password == "1234":   # exemple simple
            st.session_state.logged_in = True
            st.success("Connexion réussie ✅")
            st.switch_page("app.py")   # redirige vers ton app principale
        else:
            st.error("Identifiants incorrects ❌")

    st.markdown("</div>", unsafe_allow_html=True)
