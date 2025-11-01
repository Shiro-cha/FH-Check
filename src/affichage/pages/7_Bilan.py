import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import unicodedata


# --------------------------------------------------
# Config identique à demonstration.py
# --------------------------------------------------
st.set_page_config(page_title="Bilan de la Démonstration", layout="wide")
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Apprentissage", "Démonstration", "Autres pages", "Bilan"])

# --------------------------------------------------
# CSS hérité de demonstration.py pour la grille et style
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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-mini-card">Bilan de la Démonstration FH</div>', unsafe_allow_html=True)

# ---------- Fonctions utilitaires ----------
def normalize(s: str) -> str:
    if s is None: return ""
    s = str(s).lower().strip().replace(" ", "").replace("_", "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return s

def find_column(df, candidates):
    cols_norm = {normalize(c): c for c in df.columns}
    for cand in candidates:
        if normalize(cand) in cols_norm:
            return cols_norm[normalize(cand)]
    return None

def canonical_state(s):
    if s is None: return "KO"
    s_norm = normalize(s)
    if "ok" in s_norm: return "OK"
    if "deg" in s_norm or "degrad" in s_norm or "degrade" in s_norm: return "Dégradée"
    return "KO"

# ---------- Récupération de l'historique ----------
if "df_test" not in st.session_state or "historique_etat" not in st.session_state:
    st.warning("⚠️ Aucune démonstration trouvée. Lancez d'abord la page Démonstration.")
    st.stop()

df_test = st.session_state["df_test"]
historique_raw = st.session_state["historique_etat"]
historique_etat = [canonical_state(x) for x in historique_raw]

nb_total = len(historique_etat) if len(historique_etat) > 0 else 1
nb_ok = historique_etat.count("OK")
nb_deg = historique_etat.count("Dégradée")
nb_ko = historique_etat.count("KO")
pct_ok = int(round(nb_ok / nb_total * 100))
pct_deg = int(round(nb_deg / nb_total * 100))
pct_ko = int(round(nb_ko / nb_total * 100))
last_state = historique_etat[-1] if historique_etat else "KO"

# ---------- MINI GRILLE SYNTHÉTIQUE ----------
timer_s = f"{nb_total}s"
etat_color = "#e63946" if last_state == "KO" else "#2a9d8f" if last_state == "OK" else "#FFD700"
etat_label = last_state

st.markdown(f"""
<div class="status-grid">
  <div class="status-card" style="background:#d6f3e9;">
    <span style="font-size:29px;color:#2a9d8f;font-weight:700;">{pct_ok}%</span>
    <span style="font-size:13px;color:#222;">OK</span>
  </div>
  <div class="status-card" style="background:#fff9d6;">
    <span style="font-size:29px;color:#f4d35e;font-weight:700;">{pct_deg}%</span>
    <span style="font-size:13px;color:#222;">Dégradé</span>
  </div>
  <div class="status-card" style="background:#ffd6d6;">
    <span style="font-size:29px;color:#e63946;font-weight:700;">{pct_ko}%</span>
    <span style="font-size:13px;color:#222;">KO</span>
  </div>
  <div class="status-card" style="background:#eddfef;">
    <div class="timer-circle">{timer_s}</div>
  </div>
  <div class="status-card" style="background:#fff;">
    <div style="color:{etat_color};font-size:32px;font-weight:800;margin:0;">{etat_label}</div>
    <div style="font-size:13px;color:#444;margin-top:2px;">Dernier état</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Indicateurs de performance ----------
st.subheader("Indicateurs de Performance Moyenne")
candidates_map = {
    "RSSI": ["rssi"],
    "BER": ["ber"],
    "SNR": ["snr"],
    "Puissance (TxPower)": ["txpower", "tx_power", "txpowerdbm"],
}
gauge_colors = {
    "RSSI": "#FF8C00",
    "BER": "#1E90FF",
    "SNR": "#32CD32",
    "Puissance (TxPower)": "#FF4500"
}
units_map = {
    "RSSI": " dBm",
    "BER": "",
    "SNR": " dB",
    "Puissance (TxPower)": " dBm"
}
cols_layout = st.columns(4)
for i, (display_label, cands) in enumerate(candidates_map.items()):
    col = find_column(df_test, cands)
    if col is not None:
        vals = pd.to_numeric(df_test[col], errors="coerce").dropna()
        value = float(vals.mean()) if not vals.empty else 0
        vmin = float(np.nanmin(vals)) if not vals.empty else 0
        vmax = float(np.nanmax(vals)) if not vals.empty else 1
        if vmin == vmax:
            vmin, vmax = value - 2, value + 2
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": display_label, "font": {"size": 20, "color": "black"}},
            gauge={
                "axis": {"range": [vmin, vmax], "tickcolor": "black"},
                "bar": {"color": gauge_colors.get(display_label, "darkcyan")},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "lightgray",
                "steps": [
                    {"range": [vmin, vmax], "color": "whitesmoke"}
                ],
            },
            number={
                "valueformat": ".2f",
                "suffix": units_map.get(display_label, ""),
                "font": {"color": "black", "size": 18}
            }
        ))
        fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black'))
        cols_layout[i % 4].plotly_chart(fig, use_container_width=True)

# ---------- Graphique combiné : évolution 40s ----------
params_candidates = {
    "SNR": ["snr"],
    "BER": ["ber"],
    "Disponibilite": ["disponibilite", "disponibilité", "availability"],
    "RSSI": ["rssi"],
    "Frequence": ["frequence", "frequency"],
    "TxPower": ["txpower", "tx_power", "txpowerdbm"],
    "Gain": ["gain"],
}
colors = {"SNR": "green", "BER": "blue", "Disponibilite": "red",
          "RSSI": "orange", "Frequence": "purple", "TxPower": "brown", "Gain": "pink"}
fig = go.Figure()
max_points = min(len(df_test), 40)
for display, cands in params_candidates.items():
    col = find_column(df_test, cands)
    if col is not None:
        y = pd.to_numeric(df_test[col].values[:max_points], errors="coerce")
        fig.add_trace(go.Scatter(
            x=list(range(1, len(y)+1)), y=y,
            mode="lines+markers", name=display,
            line=dict(color=colors.get(display, None), width=1.5),
            marker=dict(size=10, symbol='circle', line=dict(width=0))
        ))
if fig.data:
    fig.update_layout(
        title=dict(
            text="Résumé Qualité Transmission (40s)",
            font=dict(size=22, color="black")
        ),
        xaxis=dict(
            title=dict(text="Temps (s)", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            showgrid=True, gridcolor='lightgray', zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Valeurs", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            showgrid=True, gridcolor='lightgray', zeroline=False
        ),
        legend=dict(
            orientation="h",
            font=dict(color="black", size=14)
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='black')
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------- Synthèse qualité globale ----------
st.subheader("Qualité globale de la liaison")
quality_score = (nb_ok * 1.0 + nb_deg * 0.5 + nb_ko * 0.0) / nb_total
quality_pct = quality_score * 100

col_left, col_right = st.columns([3, 1])
with col_left:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=quality_pct,
        number={'suffix': " %", 'font': {'color': 'black', 'size': 24}},
        title={'text': "Qualité Globale", 'font': {'color': 'black', 'size': 20}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'black'},
            'bar': {'color': "blue"},
            'bgcolor': "white",  # ✅ Fond clair
            'borderwidth': 2, 'bordercolor': 'black'
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='white',
        font=dict(color='black')
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.write(f"Détail pondéré : OK={nb_ok}, Dégradée={nb_deg}, KO={nb_ko}, total={nb_total}")

with col_right:
    if quality_pct >= 75 and pct_ko < 10:
        classification, box_color = "Classification : Bonne", "#d4f7d4"
    elif pct_ko > 30:
        classification, box_color = "Classification : Mauvaise", "#ffcccc"
    else:
        classification, box_color = "Classification : Normale", "#fff4cc"
    st.markdown(
        f"<div style='background:{box_color};padding:14px;border-radius:8px;text-align:center;'>"
        f"<h3 style='margin:6px 0;color:black'>{classification}</h3></div>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.caption("Interprétation automatique : basée sur la répartition temporelle des états observés pendant la démonstration.")

if st.button("Next"):
    st.switch_page("pages/8_Historique.py")
