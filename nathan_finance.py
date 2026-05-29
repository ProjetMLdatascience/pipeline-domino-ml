# ── BLOC 1 : Importation des librairies ──
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import HuberRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

# ── BLOC 2 : Chargement des données ──
df_finance = pd.read_csv("finance.csv")
df_aviation = pd.read_csv("output_aviation.csv")

print("✅ Finance chargé :", df_finance.shape)
print("✅ Aviation chargé :", df_aviation.shape)
print("\n--- Aperçu Finance ---")
print(df_finance.head())
print("\n--- Aperçu Aviation ---")
print(df_aviation.head())

# ── BLOC 3 : Fusion des données aviation et finance ──
df_aviation_agg = df_aviation.groupby("date").agg(
    proba_cyber_mean=("proba_cyber", "mean"),
    nb_annulations=("pred_annulation", "sum"),
    aviation_perturbee=("aviation_perturbee", "max")
).reset_index()

df = pd.merge(df_finance, df_aviation_agg, on="date", how="left")
df = df.fillna(0)

print("✅ Fusion réussie :", df.shape)
print(df.head())

# ── BLOC 4 : Préparation des données ──
# print("Colonnes disponibles :", df.columns.tolist())
# features = [
#     "aviation_perturbee_x",
#     "proba_cyber_mean",
#     "nb_annulations",
#     "volume_echanges_M",
#     "niveau_crise"
# ]

# X = df[features]
# y = df["variation_pct"]

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# print("✅ Données prêtes")
# print("Taille entrainement :", X_train.shape)
# print("Taille test :", X_test.shape)

# ── BLOC 4 : Préparation des données (agrégé par jour) ──
df_daily = df.groupby(["date", "indice"]).agg(
    variation_pct=("variation_pct", "sum"),
    volume_echanges_M=("volume_echanges_M", "sum"),
    aviation_perturbee_x=("aviation_perturbee_x", "max"),
    niveau_crise=("niveau_crise", "max"),
    proba_cyber_mean=("proba_cyber_mean", "max"),
    nb_annulations=("nb_annulations", "max")
).reset_index()

features = [
    "aviation_perturbee_x",
    "proba_cyber_mean",
    "nb_annulations",
    "volume_echanges_M",
    "niveau_crise"
]

X = df_daily[features]
y = df_daily["variation_pct"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("✅ Données prêtes par jour")
print("Taille entrainement :", X_train.shape)
print("Taille test :", X_test.shape)

# ── BLOC 5 : Entraînement du modèle HuberRegressor ──
modele = HuberRegressor(epsilon=1.35, max_iter=200)
modele.fit(X_train, y_train)

y_pred = modele.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("✅ Modèle entraîné avec succès")
print(f"Erreur absolue moyenne (MAE) : {mae:.4f}%")
print(f"Score R² : {r2:.4f}")

# ── BLOC 6 : Conversion des chutes en millions d'euros ──
CAPITALISATION_MARCHE = 180000  # en millions d'euros (ex: CAC40 ~ 180 milliards)

def chute_en_millions(variation_pct, capitalisation=CAPITALISATION_MARCHE):
    perte = (abs(variation_pct) / 100) * capitalisation
    return round(perte, 2)

df["pertes_millions_eur"] = df["variation_pct"].apply(
    lambda x: chute_en_millions(x) if x < 0 else 0
)

pertes_totales = df["pertes_millions_eur"].sum()
perte_max_jour = df["pertes_millions_eur"].max()

print("✅ Conversion en millions d'euros effectuée")
print(f"Pertes totales simulées : {pertes_totales:,.2f} millions d'€")
print(f"Pire journée : {perte_max_jour:,.2f} millions d'€ détruits")

# ── BLOC 7 : Graphique de l'effondrement boursier ──
df_graph = df[df["indice"] == "CAC40"].copy()
df_graph = df_graph.sort_values("date")
df_graph["date"] = pd.to_datetime(df_graph["date"])

plt.figure(figsize=(14, 6))

plt.plot(df_graph["date"], df_graph["valeur"],
         color="#2E86C1", linewidth=2, label="Valeur CAC40")

# Zone de crise
debut_crise = pd.to_datetime("2025-04-21")
fin_crise   = pd.to_datetime("2025-04-28")
plt.axvspan(debut_crise, fin_crise,
            color="red", alpha=0.15, label="Période de crise")

# Zone intervention CascadeGuard
debut_ml = pd.to_datetime("2025-04-28")
fin_ml   = pd.to_datetime("2025-04-30")
plt.axvspan(debut_ml, fin_ml,
            color="green", alpha=0.15, label="Intervention CascadeGuard")


# ── BLOC 8 : Export des résultats ──
df_daily["predicted_market_drop"] = modele.predict(
    scaler.transform(df_daily[features])
)

df_output = df_daily[[
    "date",
    "indice",
    "variation_pct",
    "predicted_market_drop",
    "aviation_perturbee_x",
    "niveau_crise"
]].copy()

df_output.to_csv("output_finance_nathan.csv", index=False)

print("✅ Fichier exporté : output_finance_nathan.csv")
print("\n=== RÉSUMÉ FINAL NATHAN ===")
print(f"Modèle           : HuberRegressor")
print(f"MAE              : {mae:.4f}%")
print(f"R²               : {r2:.4f}")
print(f"Pertes totales   : {pertes_totales:,.2f} millions d'€")
print(f"Pire journée     : {perte_max_jour:,.2f} millions d'€")

# Ligne du point le plus bas
idx_min = df_graph["valeur"].idxmin()
plt.annotate(
    f'Point bas\n{df_graph.loc[idx_min, "valeur"]:.0f} pts',
    xy=(df_graph.loc[idx_min, "date"], df_graph.loc[idx_min, "valeur"]),
    xytext=(df_graph.loc[idx_min, "date"], df_graph.loc[idx_min, "valeur"] + 50),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=9, color="red"
)

plt.title("Effondrement du CAC40 — Impact CascadeGuard", fontsize=14, fontweight="bold")
plt.xlabel("Date")
plt.ylabel("Valeur de l'indice (points)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graphique_effondrement.png", dpi=150)
plt.show()

print("✅ Graphique sauvegardé : graphique_effondrement.png")


# ── BLOC 9 : Comparaison Réel vs Prédit ──
plt.figure(figsize=(14, 5))

plt.plot(range(len(y_test)), y_test.values,
         label="Variation réelle", color="#2E86C1", linewidth=2)

plt.plot(range(len(y_pred)), y_pred,
         label="Variation prédite", color="#E74C3C",
         linewidth=2, linestyle="--")

plt.axhline(y=0, color="black", linewidth=0.8, linestyle=":")
plt.title("Réel vs Prédit — Variation boursière (%)", fontsize=13, fontweight="bold")
plt.xlabel("Observations")
plt.ylabel("Variation (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("reel_vs_predit.png", dpi=150)
plt.show()

print("✅ Graphique sauvegardé : reel_vs_predit.png")