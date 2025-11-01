# src/affichage/pages/3_Apprentissage.py
import os
import graphviz;
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
from sklearn.tree import export_graphviz
from sklearn.metrics import confusion_matrix
from scipy.interpolate import make_interp_spline, PchipInterpolator

# --------------------------------------------------
# Page config & style (mode clair, thème FH-Check)
# --------------------------------------------------
st.set_page_config(page_title="Apprentissage Automatique - FH-Check", layout="wide")
page = st.sidebar.radio("Navigation", ["Affichage dataset", "Autres pages", "Apprentissage"])
st.markdown("""
<style>
//* --- Sidebar --- */
[data-testid="stSidebar"] {
    background: #eceef2;
    border-right: 1px solid #e0e0e0;
    padding-top: 10px;
}
/* Masquer complètement la barre supérieure (3 points + Deploy) */
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

/* Liens sidebar */
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

/* --- Fond général --- */
.stApp, .main, .block-container {
    background: #f9f9f9 !important;
    padding: 15px 20px;
}


/* --- FH-Check Card (grand titre) --- */
.title-card {
    background: #f4edf9;
    padding: 40px 50px;                 /* plus de padding */
    border-radius: 20px;
    text-align: center;
    font-size: 42px;               /* taille augmentée */
    font-weight: 800;
    color: #6a0dad;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); /* ombre plus marquée */
    margin-bottom: 30px;
}
.title-sub {
    font-size: 18px;               /* un peu plus grand */
    font-weight: 500;
    margin-top: 10px;
    color: #444;
}

/* Style all Streamlit buttons for a lighter, softer appearance */
.stButton > button,
.stDownloadButton > button {
    background-color: #fafafa !important;    /* Softer off-white background */
    color: #222 !important;                  /* Gentle dark text */
    border: 1.5px solid #bbb !important;     /* Softer light gray border */
    padding: 10px 22px;                      /* Comfortable padding */
    border-radius: 10px;                     /* Rounded edges for softness */
    font-size: 15px;                         /* Slightly larger, easy-to-read text */
    font-weight: 600;                        /* Semi-bold, not aggressive */
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);  /* Soft subtle shadow effect */
    transition: background 0.2s, box-shadow 0.2s;
    cursor: pointer;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #f0f0f0 !important;    /* Slightly darker on hover */
    border-color: #888 !important;           /* Subtle border color change */
    box-shadow: 0 4px 12px rgba(0,0,0,0.12); /* Slightly deeper shadow on hover */
    color: #222 !important;
    transform: none !important;
}
/* Small metric circles for comparison */
.metric-circle {
    width:110px;
    height:110px;
    border-radius:999px;
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    box-shadow: 0 4px 14px rgba(106,13,173,0.12);
    background: linear-gradient(180deg, #fff, #f6f0fb);
    border: 3px solid #d6b3f2;
    color:#000;
    font-weight:700;
    margin:8px;
}
.small-card {
    background:#f8f6fb;
    border-radius:10px;
    padding:10px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

/* Make seaborn/plot elements responsive in columns */
.canvas-small { width:100%; height:160px; }

/* File uploader */
.stFileUpload input[type="file"] { color: #000000; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    '<div class="title-card">Apprentissage Automatique<div class="title-sub">Entraînement, évaluation et sauvegarde des modèles</div></div>',
    unsafe_allow_html=True)

# --------------------------------------------------
# Step 1: Importation dataset
# --------------------------------------------------
st.markdown('<h4 style="margin-top:25px;">Importation du dataset</h4>', unsafe_allow_html=True)

# --- CSS personnalisé pour file uploader et info ---
st.markdown("""
<style>
/* Carré du file uploader : blanc transparent + bordure noire */
.stFileUpload {
    background-color: rgba(255, 255, 255, 0.8) !important;
    border: 2px solid #000000 !important;
    border-radius: 12px;
    padding: 10px;
}

/* Bouton "Browse files" violet */
.stFileUpload button {
    background-color: #6a0dad !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px;
    padding: 6px 16px;
    font-weight: bold;
}

/* Texte informatif en noir */
.stInfo {
    color: #000000 !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --- File uploader ---
uploaded_file = st.file_uploader("Importer un fichier CSV (dataset FH)", type=["csv"])

if not uploaded_file:
    st.info("Importer le fichier CSV contenant au moins la colonne 'Etat' (OK / Dégradé / KO) pour continuer.")
    st.stop()

df = pd.read_csv(uploaded_file)

# --------------------------------------------------
# Étape 2 : EDA (côte à côte)
# --------------------------------------------------
st.markdown('<h4 style="margin-top:25px;">EDA (Analyse Exploratoire)</h4>', unsafe_allow_html=True)
if "Etat" not in df.columns:
    st.error("Le jeu de données doit contenir la colonne 'Etat'. Renomme ta colonne cible en 'Etat' et réimporte.")
    st.stop()

labels = ["OK", "Dégradé", "KO"]

col1, col2 = st.columns([1, 1])

# 1. Distribution des états (diagramme en barres)
with col1:
    st.markdown("**Distribution des états**")
    counts = df["Etat"].value_counts().reindex(labels).fillna(0)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x=counts.index,
        y=counts.values,
        palette=["#442288", "#6ca2ea", "#b5d33d"],
        edgecolor="white",
        ax=ax
    )
    for i, v in enumerate(counts.values):
        ax.text(i, v + max(counts.values)*0.02, f"{int(v)}", ha='center', color='white', fontsize=15, fontweight='bold')
    ax.set_ylabel("Nombre", fontsize=12)
    ax.set_xlabel("État", fontsize=12)
    ax.set_title("Distribution des états", fontsize=14, fontweight='semibold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', color="#eeeeee", linestyle='-', linewidth=1.5, alpha=1)
    ax.set_facecolor("#f9f9f9")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# 2. Matrice de corrélation (carte thermique)
with col2:
    st.markdown("**Matrice de corrélation**")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr, annot=False,  # annot=True avec petits nombres si nécessaire
            cmap="plasma",
            linewidths=2,
            linecolor='white',
            cbar_kws={'shrink': 0.7}
        )
        ax.set_title("Matrice de corrélation", fontsize=14, fontweight='semibold')
        ax.set_facecolor("#f9f9f9")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    else:
        st.info("Aucune colonne numérique pour la matrice de corrélation.")

# --------------------------------------------------
# Étape 3 : Prétraitement (nettoyage + séparation)
# --------------------------------------------------
st.markdown('<h4 style="margin-top:25px;">Nettoyage et prétraitement des données</h4>', unsafe_allow_html=True)

df = df.drop_duplicates()

X = df.drop(columns=["Etat"])
y = df["Etat"].astype(str)
cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
if cat_cols:
    X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns, index=X_test.index)

st.markdown(
    """
    <div style="
        display: inline-block;
        padding: 12px 26px;
        border-radius: 10px;
        background: #f4edf9;
        color: #523179;
        font-weight: 600;
        font-size: 15px;
        box-shadow: 0 1px 6px rgba(106,13,173,0.06);
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: 0.03em;
    ">
        Prétraitement effectué : encodage + normalisation appliqués.
    </div>
    """,
    unsafe_allow_html=True
)
col_l, col_r = st.columns(2)
train_counts = y_train.value_counts().reindex(labels).fillna(0)
test_counts = y_test.value_counts().reindex(labels).fillna(0)
max_count = max(train_counts.max(), test_counts.max())

hist_palette = ["#6a0dad", "#d6b3f2", "#c99ff0"]

with col_l:
    st.markdown("**Entraînement (80%)**")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.barplot(
        x=train_counts.index, y=train_counts.values,
        palette=hist_palette, edgecolor="#fff", ax=ax
    )
    for i, v in enumerate(train_counts.values):
        ax.text(i, v + max_count*0.025, int(v), color="#222", ha='center', fontsize=13, fontweight='bold')
    ax.set_ylim(0, max_count * 1.1)
    ax.set_ylabel("Nombre", fontsize=12, color="#333")
    ax.set_xlabel("Classe", fontsize=12, color="#333")
    ax.set_title("Distribution du jeu d'entraînement", fontsize=14, fontweight='semibold', color="#222")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e0e0e0")
    ax.spines["bottom"].set_color("#e0e0e0")
    ax.grid(axis='y', color="#ededed", linestyle='--', linewidth=1, alpha=0.9)
    ax.set_facecolor("#fff")
    fig.patch.set_facecolor("#fff")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

with col_r:
    st.markdown("**Test (20%)**")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.barplot(
        x=test_counts.index, y=test_counts.values,
        palette=hist_palette, edgecolor="#fff", ax=ax
    )
    for i, v in enumerate(test_counts.values):
        ax.text(i, v + max_count*0.025, int(v), color="#222", ha='center', fontsize=13, fontweight='bold')
    ax.set_ylim(0, max_count * 1.1)
    ax.set_ylabel("Nombre", fontsize=12, color="#333")
    ax.set_xlabel("Classe", fontsize=12, color="#333")
    ax.set_title("Distribution du jeu de test", fontsize=14, fontweight='semibold', color="#222")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#e0e0e0")
    ax.spines["bottom"].set_color("#e0e0e0")
    ax.grid(axis='y', color="#ededed", linestyle='--', linewidth=1, alpha=0.9)
    ax.set_facecolor("#fff")
    fig.patch.set_facecolor("#fff")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)


# --------------------------------------------------
# Étape 3b : Boutons de téléchargement
# --------------------------------------------------
buf_train = BytesIO()
pd.concat([X_train, y_train.reset_index(drop=True)], axis=1).to_csv(buf_train, index=False)
buf_train.seek(0)
buf_test = BytesIO()
pd.concat([X_test, y_test.reset_index(drop=True)], axis=1).to_csv(buf_test, index=False)
buf_test.seek(0)

col_dl1, col_dl2 = st.columns(2)
with col_dl1:
    st.download_button(
        label="Télécharger données_train (80%)",
        data=buf_train,
        file_name="donnees_train.csv",
        mime="text/csv",
        key="download_train"
    )
with col_dl2:
    st.download_button(
        label="Télécharger données_test (20%)",
        data=buf_test,
        file_name="donnees_test.csv",
        mime="text/csv",
        key="download_test"
    )

# --------------------------------------------------
# Étape 4 : Choix de l'algorithme + entraînement
# --------------------------------------------------
st.markdown('<h4 style="margin-top:25px;">Choix de l\'algorithme & entraînement</h4>', unsafe_allow_html=True)
algo = st.selectbox("Sélectionnez un algorithme", ["Random Forest", "KNN", "SVM", "Régression Logistique"])

params = {}
if algo == "Random Forest":
    params["n_estimators"] = st.slider("n_estimators", 10, 300, 100)
elif algo == "KNN":
    params["n_neighbors"] = st.slider("n_neighbors", 1, 20, 5)
elif algo == "SVM":
    params["kernel"] = st.selectbox("Noyau (Kernel)", ["rbf", "linear", "poly"])
elif algo == "Régression Logistique":
    params["C"] = st.number_input("C", value=1.0)

if st.button("Lancer l'entraînement"):
    if algo == "Random Forest":
        model = RandomForestClassifier(n_estimators=params["n_estimators"], random_state=42)
    elif algo == "KNN":
        model = KNeighborsClassifier(n_neighbors=params["n_neighbors"])
    elif algo == "SVM":
        model = SVC(kernel=params["kernel"], probability=True, random_state=42)
    else:
        model = LogisticRegression(max_iter=2000, C=params["C"], random_state=42)

    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')

    # Créer dossier 'models' si inexistant
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, f"models/model_{algo.replace(' ', '_')}.joblib")
    joblib.dump(scaler, "models/scaler.joblib")
    joblib.dump(list(X_train_scaled.columns), "models/feature_cols.joblib")

    st.markdown(f"**Précision (accuracy) :** {acc * 100:.2f}%")
    st.markdown(f"**F1 (macro) :** {f1_macro * 100:.2f}%")

    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.markdown(f'<div class="small-card"><strong>Précision</strong><h3>{acc:.2%}</h3></div>',
                    unsafe_allow_html=True)
    with mcol2:
        st.markdown(f'<div class="small-card"><strong>F1-macro</strong><h3>{f1_macro:.2%}</h3></div>',
                    unsafe_allow_html=True)
    with mcol3:
        report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
        st.dataframe(report_df.round(2), use_container_width=True, height=160)
    st.markdown(
        """
        <style>
        thead tr th {
            background-color: #f4edf9 !important;
        }
        .stCard {
            background-color: #f4edf9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    plt.rcParams.update({'font.size': 12, 'font.family': 'DejaVu Sans'})

    fig, ax = plt.subplots(figsize=(4, 3))

    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # Créer une palette bleu clair
    light_blue_cmap = sns.light_palette("blue", as_cmap=True)

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=light_blue_cmap,
        linewidths=0,
        square=False,
        annot_kws={"size": 12, "weight": "bold", "color": "black", "va": "center", "ha": "center"},
        cbar=True,
        ax=ax,
        cbar_kws={"shrink": 0.8, "aspect": 15, "pad": 0.02, "orientation": "vertical"}
    )
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=10)

    ax.set_xlabel("Étiquette prédite", fontsize=14, labelpad=10)
    ax.set_ylabel("Étiquette réelle", fontsize=14, labelpad=10)
    ax.set_title("Matrice de confusion", fontsize=16, pad=14)

    ax.set_xticklabels(labels, fontsize=11, rotation=30, ha="right")
    ax.set_yticklabels(labels, fontsize=11, rotation=0, va="center")

    for _, spine in ax.spines.items():
        spine.set_visible(False)

    fig.patch.set_facecolor('#f9f9f9')
    ax.set_facecolor('#f9f9f9')

    plt.tight_layout(pad=1.5)

    # Affichage centré dans Streamlit
    st.markdown('<div style="display:flex;justify-content:center;">', unsafe_allow_html=True)
    st.pyplot(fig, use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    # --------------------------------------------------
    # Étape 4b : Visualisation du modèle obtenu
    # --------------------------------------------------
    st.subheader("Visualisation du modèle obtenu")

    if algo == "Random Forest":
        # Afficher le premier arbre du Random Forest
        tree = model.estimators_[0]
        # Utiliser l'attribut classes_ du modèle entraîné pour obtenir les noms des classes corrects
        class_names = model.classes_

        dot_data = export_graphviz(
            tree,
            out_file=None,
            feature_names=X_train_scaled.columns,
            class_names=class_names,
            filled=True,
            rounded=True,
            special_characters=True
        )
        graph = graphviz.Source(dot_data)
        st.graphviz_chart(graph)


    elif algo == "KNN":

        from sklearn.decomposition import PCA

        from sklearn.preprocessing import LabelEncoder

        # Réduire à 2 dimensions

        pca = PCA(n_components=2)

        X_train_2d = pca.fit_transform(X_train_scaled)

        # Encoder les labels en numériques

        le = LabelEncoder()

        y_train_enc = le.fit_transform(y_train)

        # Réentraîner le modèle sur 2D

        model.fit(X_train_2d, y_train_enc)

        # Création de la grille pour contourf

        x_min, x_max = X_train_2d[:, 0].min() - 1, X_train_2d[:, 0].max() + 1

        y_min, y_max = X_train_2d[:, 1].min() - 1, X_train_2d[:, 1].max() + 1

        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),

                             np.arange(y_min, y_max, 0.1))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)

        # Tracer

        fig_knn, ax_knn = plt.subplots(figsize=(10, 2))

        ax_knn.contourf(xx, yy, Z, alpha=0.3, cmap="Pastel1")

        scatter = ax_knn.scatter(X_train_2d[:, 0], X_train_2d[:, 1],

                                 c=y_train_enc, cmap="Set1", edgecolor='k')

        ax_knn.set_title("Frontières de décision KNN (2D PCA)")

        st.pyplot(fig_knn, use_container_width=True)


    elif algo == "SVM":

        from sklearn.decomposition import PCA

        from sklearn.preprocessing import LabelEncoder

        # PCA pour réduire à 2 dimensions

        pca = PCA(n_components=2)

        X_train_2d = pca.fit_transform(X_train_scaled)

        X_test_2d = pca.transform(X_test_scaled)

        # Encoder les labels en numériques

        le = LabelEncoder()

        y_train_enc = le.fit_transform(y_train)

        y_test_enc = le.transform(y_test)

        # Réentraîner le SVM sur 2D

        model.fit(X_train_2d, y_train_enc)

        y_pred_enc = model.predict(X_test_2d)

        # Création grille pour frontières

        x_min, x_max = X_train_2d[:, 0].min() - 1, X_train_2d[:, 0].max() + 1

        y_min, y_max = X_train_2d[:, 1].min() - 1, X_train_2d[:, 1].max() + 1

        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),

                             np.arange(y_min, y_max, 0.1))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)

        # Tracer frontière SVM avec gris clair
        fig_svm, ax = plt.subplots(figsize=(10, 2))

        # contourf avec couleur grise
        ax.contourf(xx, yy, Z, alpha=0.3, colors=['#d3d3d3'])  # gris clair uniforme

        # points d'entraînement
        scatter = ax.scatter(X_train_2d[:, 0], X_train_2d[:, 1],
                             c=y_train_enc, cmap="Set1", edgecolor='k')

        ax.set_title("Frontières de décision SVM (2D PCA)")

        st.pyplot(fig_svm, use_container_width=True)




    elif algo == "Régression Logistique":

        from sklearn.decomposition import PCA

        from sklearn.preprocessing import LabelEncoder

        # PCA pour réduire à 2 dimensions

        pca = PCA(n_components=2)

        X_train_2d = pca.fit_transform(X_train_scaled)

        X_test_2d = pca.transform(X_test_scaled)

        # Encoder les labels en numériques

        le = LabelEncoder()

        y_train_enc = le.fit_transform(y_train)

        y_test_enc = le.transform(y_test)

        # Réentraîner le modèle sur 2D

        model.fit(X_train_2d, y_train_enc)

        y_pred_enc = model.predict(X_test_2d)

        # Création grille pour frontières

        x_min, x_max = X_train_2d[:, 0].min() - 1, X_train_2d[:, 0].max() + 1

        y_min, y_max = X_train_2d[:, 1].min() - 1, X_train_2d[:, 1].max() + 1

        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),

                             np.arange(y_min, y_max, 0.1))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

        Z = Z.reshape(xx.shape)

        # Tracer frontière

        fig_logreg, ax = plt.subplots(figsize=(10, 2))

        ax.contourf(xx, yy, Z, alpha=0.3, cmap="Pastel1")

        scatter = ax.scatter(X_train_2d[:, 0], X_train_2d[:, 1], c=y_train_enc, cmap="Set1", edgecolor='k')

        ax.set_title("Frontières de décision Régression Logistique (2D PCA)")

        st.pyplot(fig_logreg, use_container_width=True)

    # Exemple de données (à remplacer par les données réelles)
    epochs = 10
    train_loss = np.linspace(0.9, 0.1, epochs)
    val_loss = np.linspace(1.0, 0.2, epochs)
    train_acc = np.linspace(0.5, 0.95, epochs)
    val_acc = np.linspace(0.45, 0.9, epochs)
    epochs_arr = np.arange(1, epochs + 1)

    # Échelle dense des époques
    xnew = np.linspace(1, epochs, 300)


    # Courbes lissées avec PchipInterpolator pour une interpolation monotone douce
    def smooth_curve(x, y):
        return PchipInterpolator(x, y)(xnew)
        # Ou utiliser : return make_interp_spline(x, y, k=3)(xnew)


    train_loss_smooth = smooth_curve(epochs_arr, train_loss)
    val_loss_smooth = smooth_curve(epochs_arr, val_loss)
    train_acc_smooth = smooth_curve(epochs_arr, train_acc)
    val_acc_smooth = smooth_curve(epochs_arr, val_acc)

    fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(11, 4), dpi=130)

    # Palettes de couleurs douces
    train_color = '#e57272'  # rouge doux
    val_color = '#72abdf'  # bleu doux
    dot_color = '#755bb4'  # violet doux pour le marqueur de meilleure époque

    # Graphe des pertes (loss)
    ax_loss.plot(xnew, train_loss_smooth, color=train_color, linewidth=2.3, alpha=0.78, label="Perte entraînement")
    ax_loss.plot(xnew, val_loss_smooth, color=val_color, linewidth=2.3, alpha=0.85, label="Perte validation")
    best_epoch_loss = np.argmin(val_loss) + 1
    ax_loss.scatter(best_epoch_loss, val_loss[best_epoch_loss - 1], c=dot_color, s=70, zorder=10,
                    label=f'Meilleure époque = {best_epoch_loss}', edgecolors='white', linewidths=1)
    ax_loss.set_title('Perte Entraînement et Validation', fontsize=13, weight='medium')
    ax_loss.set_xlabel('Époques', fontsize=11)
    ax_loss.set_ylabel('Perte', fontsize=11)
    leg_loss = ax_loss.legend(fontsize=9.7, frameon=False)
    for line in leg_loss.get_lines():
        line.set_linewidth(1.2)
    ax_loss.grid(alpha=0.13, linestyle='--')
    ax_loss.tick_params(axis='both', labelsize=10)

    # Graphe de précision (accuracy)
    ax_acc.plot(xnew, train_acc_smooth, color=train_color, linewidth=2.3, alpha=0.78, label="Précision entraînement")
    ax_acc.plot(xnew, val_acc_smooth, color=val_color, linewidth=2.3, alpha=0.85, label="Précision validation")
    best_epoch_acc = np.argmax(val_acc) + 1
    ax_acc.scatter(best_epoch_acc, val_acc[best_epoch_acc - 1], c=dot_color, s=70, zorder=10,
                   label=f'Meilleure époque = {best_epoch_acc}', edgecolors='white', linewidths=1)
    ax_acc.set_title('Précision Entraînement et Validation', fontsize=13, weight='medium')
    ax_acc.set_xlabel('Époques', fontsize=11)
    ax_acc.set_ylabel('Précision', fontsize=11)
    leg_acc = ax_acc.legend(fontsize=9.7, frameon=False)
    for line in leg_acc.get_lines():
        line.set_linewidth(1.2)
    ax_acc.grid(alpha=0.13, linestyle='--')
    ax_acc.tick_params(axis='both', labelsize=10)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# --------------------------------------------------
# Step 5: Comparaison rapide des algorithmes
# --------------------------------------------------

# --- CSS personnalisé pour ronds plus grands ---
st.markdown("""
<style>
.metric-circle {
    width:160px;       /* largeur augmentée */
    height:160px;      /* hauteur augmentée */
    border-radius:999px;
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    box-shadow: 0 6px 18px rgba(106,13,173,0.15);
    background: linear-gradient(180deg, #ffffff, #f3e8fc);
    border: 4px solid #6a0dad;
    color:#000;
    font-weight:700;
    margin:10px auto;
}
.metric-circle div:first-child { 
    font-size:18px;   /* nom de l'algorithme */
}
.metric-circle div:last-child { 
    font-size:22px;   /* score */
    font-weight:bold;
    margin-top:4px;
}
</style>
""", unsafe_allow_html=True)

# --- Comparaison des modèles ---
if st.button("Lancer comparaison des 4 algorithmes"):
    results = {}
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(kernel='rbf', probability=True, random_state=42),
        "LogReg": LogisticRegression(max_iter=2000, random_state=42)
    }

    for name, m in models.items():
        m.fit(X_train_scaled, y_train)
        results[name] = accuracy_score(y_test, m.predict(X_test_scaled))
        os.makedirs("models", exist_ok=True)
        joblib.dump(m, f"models/model_{name}.joblib")

    cols = st.columns(4)
    for i, (name, score) in enumerate(results.items()):
        with cols[i]:
            st.markdown(
                f'<div class="metric-circle"><div>{name}</div><div>{score * 100:.2f}%</div></div>',
                unsafe_allow_html=True
            )

# --------------------------------------------------
# Step 6: Navigation
# --------------------------------------------------
if st.button("Next (Démonstration)"):
    st.experimental_set_query_params(page="6_Demonstration.py")
    st.write("Clique sur le menu à gauche pour aller à la page Démonstration.")
