import streamlit as st
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

# Fond d'écran adaptatif
image_base64 = get_base64_image("/home/ariel/photo & video memoire/generated-image(15).png")
if image_base64:
    bg_img = f"url('data:image/jpeg;base64,{image_base64}')"
else:
    bg_img = "linear-gradient(135deg,#434a7e 0%, #b8a1f6 100%)"

st.set_page_config(page_title="Connexion", page_icon="🔒", layout="centered")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;900&display=swap');
html, body, .stApp {{
    font-family: 'Montserrat', 'Arial', sans-serif !important;
    background: {bg_img};
    background-size: cover !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
}}
#glass-login {{
    max-width: 400px;
    margin: 10vh auto 4vh auto;
    background: rgba(48,60,110,0.28);
    border-radius: 30px;
    box-shadow: 0 8px 42px 0 rgba(49,45,103,0.22);
    border: 1.8px solid rgba(255,255,255,0.23);
    padding: 36px 35px 28px 35px;
    backdrop-filter: blur(20px);
    position: relative;
    z-index: 10;
    transition: background 0.27s;
}}
#glass-login .login-avatar {{
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: rgba(255,255,255,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid rgba(255,255,255,0.19);
    margin: -54px auto 25px auto;
}}
#glass-login .login-avatar img {{
    border-radius: 50%;
    width: 70px; height: 70px;
    object-fit: cover;
}}
#glass-login .form-title {{
    font-size: 2.18rem;
    font-weight: 900;
    color: #fff;
    text-align: center;
    margin-bottom: 0.40rem;
    letter-spacing: .02em;
    opacity: 0.97;
}}
#glass-login .form-sub {{
    font-size: 1.13rem;
    font-weight: 600;
    color: #efe8ff;
    text-align: center;
    margin-bottom: 2.20rem;
    opacity: 0.92;
}}
#glass-login label {{
    font-size: 1rem;
    font-weight: 600;
    color: #f6f6fd;
    margin-bottom: 6px;
    opacity: 0.94;
    display: block;
}}
#glass-login input[type="text"], #glass-login input[type="password"] {{
    background: rgba(255,255,255,0.92);
    border-radius: 14px;
    font-size: 1rem;
    font-weight: 500;
    padding: 13px 14px;
    border: none;
    margin-bottom: 18px;
    outline: none;
    color: #262163;
    box-shadow: 0 2px 12px #00000020;
    width: 100%;
    transition: .16s;
}}
#glass-login input[type="text"]:focus, #glass-login input[type="password"]:focus {{
    background: #eceafd;
    border: 2.2px solid #784cfd;
}}
#glass-login input::placeholder {{
    color: #7e6ecfaa;
    font-weight: 400;
}}
#glass-login button {{
    width: 100%;
    background: linear-gradient(90deg,#6e54e7 20%,#9260ff 100%);
    border-radius: 14px;
    color: #fff;
    padding: 15px 0;
    font-size: 1.12rem;
    font-weight: 900;
    border: none;
    margin-top: 11px;
    transition: .19s;
    cursor: pointer;
    box-shadow: 0 2px 10px #4b3ac61c;
    letter-spacing: 0.03em;
}}
#glass-login button:hover {{
    background: #e6dbfd;
    color: #6e54e7;
    outline: 2px solid #6e54e720;
}}
#glass-login .aux-row {{
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    align-items: center;
    opacity: 0.88;
    color: #e9e3fa;
    font-size: 0.98rem;
    font-weight: 500;
}}
#glass-login .aux-row a {{
    color: #d3cfff;
    text-decoration: underline;
    font-size: 0.93rem;
    font-weight: 400;
}}
#glass-login .footer {{
    margin-top: 28px;
    text-align: center;
    color: #f5f3fdad;
    font-size: 0.94rem;
    opacity: 0.73;
}}

/* Masquage total de la sidebar, menu, header, footer sur cette page */
#MainMenu, footer, header, [data-testid="stSidebar"] {{
    visibility: hidden;
    display: none !important;
}}
</style>
""", unsafe_allow_html=True)

# --- Variables d’authentification ---
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin:123"

def authenticate(username, password):
    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD

# --- Logique de connexion & redirection ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Formulaire visuel
    st.markdown("""
    <div id="glass-login">
        <div class="login-avatar">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png" alt="Avatar"/>
        </div>
        <div class="form-title">Bienvenue</div>
        <div class="form-sub">Connectez-vous à FH-CHECK</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("", placeholder="Nom d'utilisateur", label_visibility="collapsed", key="username_input")
        password = st.text_input("", type="password", placeholder="Mot de passe", label_visibility="collapsed", key="password_input")

        st.markdown(
            """
            <div class="aux-row">
                <label><input type="checkbox" style="accent-color:#9260ff;"> Se souvenir de moi</label>
                <a href="#">Mot de passe oublié ?</a>
            </div>
            """, unsafe_allow_html=True
        )

        submit = st.form_submit_button("Identification", use_container_width=True)
        if submit:
            if not username or not password:
                st.warning("Tous les champs sont requis !", icon="⚠️")
            elif authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Connexion réussie ! Redirection…")
                st.rerun()
            else:
                st.error("Identifiants invalides 😤")
    # Footer (branding, copyright)

else:
    st.switch_page("pages/1_Accueil.py")
