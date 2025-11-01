import streamlit as st
import pandas as pd
import time
import joblib
import plotly.graph_objects as go
from pydub import AudioSegment
from io import BytesIO
import base64

# --------------------------------------------------
# Config de la page
# --------------------------------------------------
st.set_page_config(page_title="Démonstration FH", layout="wide")
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Apprentissage", "Autres pages", "Démonstration"])

# --------------------------------------------------
# Styles CSS pour petits cadres collés
# --------------------------------------------------
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #eceef2;
    border-right: 1px solid #e0e0e0;
    padding-top: 10px;
}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
[data-testid="stSidebar"]::before {
    content: "📡";
    display: block;
    font-size: 75px;
    text-align: center;
    margin-bottom: 10px;
    color: #6a0dad;
}
[data-testid="stSidebarNav"] ul li a {
    border-radius: 8px;
    margin: 4px 8px;
    padding: 8px 12px;
    font-weight: 600;
    color: #333 !important;
    transition: 0.3s;
}
[data-testid="stSidebarNav"] ul li a:hover {
    background: #e7def9 !important;
    color: #000 !important;
}
.stApp, .main, .block-container {
    background: #f9f9f9 !important;
    padding: 15px 20px;
}
.title-mini-card {
    background: #f4edf9;
    padding: 20px 30px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
    color: #6a0dad;
    font-weight: 800;
    font-size: 36px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    font-family: 'Trebuchet MS', sans-serif;
}
.status-grid {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: stretch;
    width: 100%;
    gap: 19px;
    margin-bottom: 22px;
    margin-top: 10px;
    box-sizing: border-box;
}
.status-grid .status-card {
    min-width: 168px;
    max-width: 168px;
    width: 100%;
    min-height: 80px;
    max-height: 80px;
    height: 80px;
    margin: 0;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 9px rgba(0,0,0,0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
    box-sizing: border-box;
}
.status-grid .status-card-etat {
    min-width: 168px;
    max-width: 168px;
    width: 100%;
    min-height: 80px;
    max-height: 80px;
    height: 80px;
    margin: 0;
    border-radius: 14px;
    box-shadow: 0 2px 14px rgba(188,17,38,0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    font-family: 'Trebuchet MS', sans-serif;
    box-sizing: border-box;
    padding: 0;
    transition: background-color 0.3s ease;
}
.status-grid .etat-symbol-ko {
    font-size: 38px !important;
    display: block;
    line-height: 1.0;
    margin-bottom: 3px;
}
.status-grid .etat-ko-text {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 0.5px;
    margin: 0;
    line-height: 1.0;
}
.status-grid .etat-texte {
    font-size: 25px !important;
    font-weight: bold !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0;
}
.status-grid .etat-texte .etat-symbol {
    font-size: 38px !important;
    line-height: 1.0 !important;
    margin-bottom: 0px;
}
.timer-circle {
    background:#eddfef;
    border-radius:50%;
    border:4px solid #8000ff;
    width:78px;height:78px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:bold;
    font-size:26px;
    color:#8000ff;
    box-shadow:0 0 18px #d8b4fe;
    margin:auto;
}
.anomalie-croix {
    font-size: 21px;
    color: #e63946;
    margin-left: 6px;
    vertical-align: middle;
    font-weight: bold;
}
.ok-green {
    color: #2a9d8f;
    font-weight: 700;
    font-size: 24px;
}
.blink-orange {
    color: #f4a261;
    font-weight: 700;
    font-size: 24px;
    animation: blink 1s infinite;
}
.blink-red {
    color: #e63946;
    font-weight: 700;
    font-size: 24px;
    animation: blink 1s infinite;
}
.degrade-yellow {
    color: #ffd700;
    font-weight: 700;
    font-size: 24px;
}
.radar {
    width: 60px;
    height: 60px;
    background: #bddaed;
    border-radius: 50%;
    margin: 8px auto;
    box-shadow: inset 0 0 20px #4a90e2;
}
.radar.alarme {
    background: #ff6b6b;
    box-shadow: inset 0 0 20px #ff0000;
}
</style>
""", unsafe_allow_html=True)

# Petit cadre titre avec style
st.markdown('<div class="title-mini-card">Démo de la Liaison FH</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Charger les sons
# --------------------------------------------------
audio_ko_full = AudioSegment.from_file("/home/ariel/Downloads/censor-beep-1-372459.mp3")
audio_ko_3s = audio_ko_full[:3000]
audio_ko_bytes = BytesIO()
audio_ko_3s.export(audio_ko_bytes, format="mp3")
audio_ko_bytes.seek(0)

audio_anomalie_full = AudioSegment.from_file("/home/ariel/Downloads/heart-monitor-beep-96554.mp3")
audio_anomalie_3s = audio_anomalie_full[:3000]
audio_anomalie_bytes = BytesIO()
audio_anomalie_3s.export(audio_anomalie_bytes, format="mp3")
audio_anomalie_bytes.seek(0)

# Initialisation session variables
if "demo_start" not in st.session_state:
    st.session_state["demo_start"] = False

if "df_test" not in st.session_state:
    st.session_state["df_test"] = None
if "condition" not in st.session_state:
    st.session_state["condition"] = "Normal_Rural"
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "Random Forest"

# --- Upload
if not st.session_state["demo_start"]:
    uploaded_file = st.file_uploader("Importer les données test (Excel ou CSV)", type=["xlsx", "csv"])
    if uploaded_file is not None:
        df_test = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
        st.session_state["df_test"] = df_test
        col_cond, col_model = st.columns([1, 1])
        with col_cond:
            condition = st.selectbox(
                "Changer la condition de la liaison FH",
                [
                    "Normal_Rural", "Normal_Urbain", "Pluie_Rural", "Pluie_Urbain",
                    "Brouillard_Rural", "Brouillard_Urbain",
                    "Cyclone", "Orage", "Foret_dense", "Vent_fort", "Montagneux"
                ],
                index=[
                    "Normal_Rural", "Normal_Urbain", "Pluie_Rural", "Pluie_Urbain",
                    "Brouillard_Rural", "Brouillard_Urbain",
                    "Cyclone", "Orage", "Foret_dense", "Vent_fort", "Montagneux"
                ].index(st.session_state["condition"]),
                key="select_condition_pre_demo"
            )
            st.session_state["condition"] = condition

        with col_model:
            model_name = st.selectbox(
                "Changer le modèle à utiliser",
                ["Random Forest", "KNN", "SVM", "Régression Logistique"],
                index=["Random Forest", "KNN", "SVM", "Régression Logistique"].index(st.session_state["model_name"]),
                key="select_model_pre_demo"
            )
            st.session_state["model_name"] = model_name

        if st.button("Lancer la démo"):
            st.session_state["demo_start"] = True

# --- Simulation/Démo
if st.session_state["demo_start"] and st.session_state["df_test"] is not None:
    if "pause" not in st.session_state:
        st.session_state["pause"] = False
    col_cond, col_model = st.columns([1, 1])
    with col_cond:
        condition = st.selectbox(
            "Changer la condition de la liaison FH",
            [
                "Normal_Rural", "Normal_Urbain", "Pluie_Rural", "Pluie_Urbain",
                "Brouillard_Rural", "Brouillard_Urbain",
                "Cyclone", "Orage", "Foret_dense", "Vent_fort", "Montagneux"
            ], index=[
                "Normal_Rural", "Normal_Urbain", "Pluie_Rural", "Pluie_Urbain",
                "Brouillard_Rural", "Brouillard_Urbain",
                "Cyclone", "Orage", "Foret_dense", "Vent_fort", "Montagneux"
            ].index(st.session_state["condition"]),
            key="select_condition_post_demo"
        )
        st.session_state["condition"] = condition

    with col_model:
        model_name = st.selectbox(
            "Changer le modèle à utiliser",
            ["Random Forest", "KNN", "SVM", "Régression Logistique"],
            index=["Random Forest", "KNN", "SVM", "Régression Logistique"].index(st.session_state["model_name"]),
            key="select_model_post_demo"
        )
        st.session_state["model_name"] = model_name

    df_test = st.session_state["df_test"]
    st.subheader(f"Démo pour la condition : {condition} - Modèle : {model_name}")

    # Renommer les colonnes
    col_mapping = {}
    for col in df_test.columns:
        col_lower = col.lower().replace(" ", "").replace("_", "").replace("é","e").replace("è","e")
        if "rssi" in col_lower: col_mapping[col] = "RSSI"
        elif "ber" in col_lower: col_mapping[col] = "BER"
        elif "snr" in col_lower: col_mapping[col] = "SNR"
        elif "dispon" in col_lower or "availability" in col_lower: col_mapping[col] = "Disponibilite"
        elif "frequence" in col_lower or "frequency" in col_lower: col_mapping[col] = "Frequence"
        elif "txpower" in col_lower or "tx_power" in col_lower: col_mapping[col] = "TxPower"
        elif "gain" in col_lower: col_mapping[col] = "Gain"
        elif "distance" in col_lower: col_mapping[col] = "Distance"
        elif "bandwidth" in col_lower or "bandepassante" in col_lower: col_mapping[col] = "BandePassante"
        elif "etat" in col_lower: col_mapping[col] = "Etat"
    df_test.rename(columns=col_mapping, inplace=True)
    required_cols = ["RSSI", "BER", "SNR", "TxPower"]
    if not all(col in df_test.columns for col in required_cols):
        st.error(f"Les colonnes {required_cols} doivent exister dans les données test.")
        st.stop()

    # Charger le modèle IA selon sélection
    scaler = joblib.load("models/scaler.joblib")
    feature_cols = joblib.load("models/feature_cols.joblib")
    if model_name == "Random Forest":
        model_path = "models/model_Random_Forest.joblib"
    elif model_name == "KNN":
        model_path = "models/model_KNN.joblib"
    elif model_name == "SVM":
        model_path = "models/model_SVM.joblib"
    elif model_name == "Régression Logistique":
        model_path = "models/model_Logistic_Regression.joblib"
    else:
        st.error("Modèle inconnu sélectionné.")
        st.stop()
    model = joblib.load(model_path)

    X_test = df_test.drop(columns=["Etat"], errors="ignore")
    for col in feature_cols:
        if col not in X_test.columns:
            X_test[col] = 0
    X_test = X_test[feature_cols]
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)

    # --- Placeholders Streamlit
    placeholder_grid = st.empty()
    placeholder_graph = st.empty()
    placeholder_state = st.empty()
    x_vals, rssi_hist, ber_hist, snr_hist, txpower_hist = [], [], [], [], []
    anomalies_x, anomalies_y = [], []
    historique_etat = []
    max_time = min(len(df_test), 40)

    # --- Simulation réelle
    for t in range(max_time):
        while st.session_state["pause"]:
            time.sleep(0.5)

        x_vals.append(t+1)
        rssi_val = df_test["RSSI"].values[t]
        ber_val = df_test["BER"].values[t]
        snr_val = df_test["SNR"].values[t]
        txpower_val = df_test["TxPower"].values[t]
        rssi_hist.append(rssi_val)
        ber_hist.append(ber_val)
        snr_hist.append(snr_val)
        txpower_hist.append(txpower_val)

        anomalies_rssi = rssi_val < df_test["RSSI"].mean() - df_test["RSSI"].std()
        anomalies_ber = ber_val > df_test["BER"].mean() + df_test["BER"].std()
        anomalies = anomalies_rssi or anomalies_ber
        if anomalies:
            anomalies_x.append(t+1)
            anomalies_y.append(rssi_val if anomalies_rssi else ber_val)

        etat = "OK" if (
            rssi_val > -70 and snr_val > 15 and ber_val < 0.01
        ) else "Dégradée" if (
            rssi_val > -85 and snr_val > 10
        ) else "KO"
        historique_etat.append(etat)
        st.session_state["historique_etat"] = historique_etat

        tot = len(historique_etat)
        pct_ok = int(100 * historique_etat.count("OK") / tot)
        pct_degrade = int(100 * historique_etat.count("Dégradée") / tot)
        pct_ko = int(100 * historique_etat.count("KO") / tot)
        etat_courant = historique_etat[-1]

        # 5 cadres collés : timer dans le 4ᵉ cadre, état dans le 5ᵉ cadre (pas de boule en dessous)
        with placeholder_grid:
            st.markdown("""
            <div class="status-grid">
              <div class="status-card" style="background:#d6f3e9;">
                <span style="font-size:29px;color:#2a9d8f;font-weight:700;">{ok}%</span>
                <span style="font-size:13px;color:#222;">OK</span>
              </div>
              <div class="status-card" style="background:#fff9d6;">
                <span style="font-size:29px;color:#f4d35e;font-weight:700;">{deg}%</span>
                <span style="font-size:13px;color:#222;">Dégradé</span>
              </div>
              <div class="status-card" style="background:#ffd6d6;">
                <span style="font-size:29px;color:#e63946;font-weight:700;">{ko}%</span>
                <span style="font-size:13px;color:#222;">KO</span>
              </div>
              <div class="status-card" style="background:#eddfef;display:flex;align-items:center;justify-content:center;">
                <div class="timer-circle">{timer}s</div>
              </div>
              <div class="status-card" style="background:#fff;display:flex;align-items:center;justify-content:center;">
                <div class="etat-texte" style="color:{color};">
                  <span style="font-size:32px;font-weight:800;">{etat}</span>
                  {anom}
                </div>
              </div>
            </div>
            """.format(
                ok=pct_ok, deg=pct_degrade, ko=pct_ko,
                timer=t+1,
                color="#2a9d8f" if etat_courant == "OK" else "#FFD700" if etat_courant == "Dégradée" else "#e63946",
                etat=etat_courant,
                anom=("<div style='margin-top:6px; font-size:23px;color:#e63946;font-weight:700;'><span style='vertical-align:middle;'>Anomalie</span> <span class='anomalie-croix' style='font-size:30px;'>✖</span></div>" if anomalies else "")
            ), unsafe_allow_html=True)

        # ---- Graphe multi-traces + marqueur anomalies ----
        with placeholder_graph:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_vals, y=rssi_hist, mode="lines+markers", name="RSSI (dBm)", line=dict(color="orange", width=2)))
            fig.add_trace(go.Scatter(x=x_vals, y=snr_hist, mode="lines+markers", name="SNR (dB)", line=dict(color="green", width=2)))
            fig.add_trace(go.Scatter(x=x_vals, y=ber_hist, mode="lines+markers", name="BER", line=dict(color="blue", width=2)))
            fig.add_trace(go.Scatter(x=x_vals, y=txpower_hist, mode="lines+markers", name="TxPower (dBm)", line=dict(color="red", width=2)))
            # Ajout des croix rouges pour anomalies
            if anomalies_x and anomalies_y:
                fig.add_trace(go.Scatter(
                    x=anomalies_x, y=anomalies_y, mode="markers", name="Anomalies",
                    marker=dict(symbol="x", color="#e63946", size=15, line=dict(width=2, color="#9B2226")),
                    showlegend=True
                ))
            fig.update_layout(
                title="Évolution des paramètres radioélectriques",
                plot_bgcolor="#f2f2f8",
                paper_bgcolor="#f2f2f8",
                font=dict(color="black", size=16),
                xaxis=dict(
                    title='Temps (s)',
                    gridcolor='#bdbdbd',
                    zerolinecolor='#aaaaaa',
                    tickfont=dict(size=13, color='black'),
                    title_font=dict(size=17, color='black')
                ),
                yaxis=dict(
                    title='Valeur mesurée',
                    gridcolor='#bdbdbd',
                    zerolinecolor='#aaaaaa',
                    tickfont=dict(size=13, color='black'),
                    title_font=dict(size=17, color='black')
                ),
                legend=dict(
                    orientation="h", x=0.5, y=1.08, xanchor="center", font=dict(size=14)
                ),
                margin=dict(l=44, r=12, t=65, b=44),
            )
            st.plotly_chart(fig, use_container_width=True)

        # -- SUPPRIMER LA BOULE EN DESSOUS DU GRAPHIQUE --
        # On ne met plus d'affichage ici, sauf SONS :
        audio_data = None
        if etat_courant == "OK":
            audio_data = None
        elif anomalies:
            audio_data = audio_anomalie_bytes.getvalue()
        elif etat_courant == "KO":
            audio_data = audio_ko_bytes.getvalue()
        if audio_data:
            audio_b64 = base64.b64encode(audio_data).decode()
            st.markdown(f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
        time.sleep(3)

    # Pour page suivante
    st.session_state["df_test"] = df_test
    st.session_state["historique_etat"] = historique_etat

    # --------- BLOC FINAL ---------
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 2px; margin-bottom: 0px;">Paramètres Supplémentaires</h3>',
                unsafe_allow_html=True)

    tab_cols = {}
    if "Frequence" in df_test.columns:
        freqs = df_test["Frequence"].copy()
        if freqs.max() > 1e6:
            freqs = freqs / 1e9
        tab_cols["Fréquence (GHz)"] = freqs.round(3)
    if "Distance" in df_test.columns:
        distances = df_test["Distance"].copy()
        tab_cols["Distance (km)"] = distances.round(3)
    if "Disponibilite" in df_test.columns:
        dispo_pct = df_test["Disponibilite"].copy() * 100 if df_test["Disponibilite"].max() <= 1 else df_test[
            "Disponibilite"]
        tab_cols["Disponibilité (%)"] = dispo_pct.round(2)

    df_table = pd.DataFrame(tab_cols)

    col1, col2 = st.columns([2, 2])
    with col1:
        st.dataframe(df_table)
    with col2:
        cols_table = [col for col in df_test.columns if "Modulation" in col] + ["Distance", "BandePassante"]
        cols_table = [c for c in cols_table if c in df_test.columns]
        st.dataframe(df_test[cols_table])
    # ----------- FIN DU BLOC FINAL -----------
    # ----- BOUTONS CONTROLE EN BAS -----
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    if col_btn1.button("Arrêter"):
        st.session_state["pause"] = True
    if col_btn2.button("Continuer"):
        st.session_state["pause"] = False

    def reset_page():
        st.session_state.clear()

    if col_btn3.button(" Réinitialiser"):
        reset_page()
        st.rerun()

if st.button("Next"):
    st.switch_page("pages/7_Bilan.py")
