import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor
import joblib

# =====================================================================
# ÉTAPE 1 : Chargement et Fusion des Données (Lien entre Duc et Exaucé)
# =====================================================================
print(" Chargement des fichiers de données...")
df_aviation = pd.read_csv("aviation.csv")
df_cyber = pd.read_csv("output_proba_cyber_duc.csv")

# Alignement : on injecte la probabilité d'attaque de Duc dans le fichier aviation
df_aviation['proba_cyber'] = df_cyber['proba_cyber']

# Remplacement des cases vides après la ligne 200 par 1.0 (100% de chance d'attaque)
# Cela permet d'avoir des données complètes pour la suite de la simulation
df_aviation['proba_cyber'] = df_aviation['proba_cyber'].fillna(1.0)

# =====================================================================
# ÉTAPE 2 : Nettoyage Métier et Encodage Strict (Data Cleaning)
# =====================================================================
print(" Nettoyage des données et encodage des variables...")

# 1. Correction des retards négatifs (les avions en avance passent à 0 minute de retard)
if 'retard_minutes' in df_aviation.columns:
    df_aviation['retard_minutes'] = df_aviation['retard_minutes'].apply(lambda x: max(0, x))

# 2. Encodage One-Hot des variables de texte (Compagnies et Aéroports)
colonnes_a_encoder = [col for col in ['compagnie', 'aeroport_depart'] if col in df_aviation.columns]
df_encoded = pd.get_dummies(df_aviation, columns=colonnes_a_encoder, drop_first=True)

# 3. Sélection AUTOMATIQUE des colonnes numériques pour éliminer les dates textuelles
X_global = df_encoded.select_dtypes(include=[np.number, bool]).copy()

# On retire impérativement les cibles pour que l'algorithme ne triche pas
cibles_a_retirer = ['annulation', 'retard_minutes', 'aviation_perturbee', 'pred_annulation', 'pred_retard']
X_global = X_global.drop(columns=cibles_a_retirer, errors='ignore').astype(float)

# =====================================================================
# ÉTAPE 3 : Entraînement du Modèle A - Classification (Annulations)
# =====================================================================
print(" Entraînement du Modèle A (Arbre de Décision - Classification)...")
y_class = df_aviation['annulation']

modele_annulation = DecisionTreeClassifier(max_depth=5, random_state=42)
modele_annulation.fit(X_global, y_class)

# Sauvegarde du modèle de classification
joblib.dump(modele_annulation, "modele_annulation.pkl")

# =====================================================================
# ÉTAPE 4 : Entraînement du Modèle B - Régression (Minutes de Retard)
# =====================================================================
print("Entraînement du Modèle B (Random Forest - Régression)...")

# Règle métier : On entraîne la régression UNIQUEMENT sur les vols non annulés
indices_vols_maintenus = df_aviation[df_aviation['annulation'] == 0].index

X_reg = X_global.loc[indices_vols_maintenus]
y_reg = df_aviation.loc[indices_vols_maintenus, 'retard_minutes']

modele_retard = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
modele_retard.fit(X_reg, y_reg)

# Sauvegarde du modèle de régression
joblib.dump(modele_retard, "modele_retard.pkl")

# =====================================================================
# ÉTAPE 5 : Application des Prédictions sur le Dataset
# =====================================================================
print("Application des prédictions sur le fichier final...")
df_aviation['pred_annulation'] = modele_annulation.predict(X_global)
df_aviation['pred_retard'] = modele_retard.predict(X_global)

# Création de la variable pivot pour Nathan (1 si annulé OU si gros retard > 60 min)
df_aviation['aviation_perturbee'] = (
    (df_aviation['pred_annulation'] == 1) | (df_aviation['pred_retard'] > 60)
).astype(int)

# =====================================================================
# ÉTAPE 6 : Génération des Graphiques Obligatoires (Livrables Soutenance)
# =====================================================================
print("Création des graphiques détaillés pour le rapport...")

# Graphique 1 : Importance des variables (Feature Importance)
importances = modele_retard.feature_importances_
indices_tri = np.argsort(importances)[::-1]

plt.figure(figsize=(10, 5))
sns.barplot(x=importances[indices_tri[:5]], y=X_global.columns[indices_tri[:5]], palette="viridis")
plt.title("Importance des variables - Modèle Impact Aviation")
plt.xlabel("Score d'importance mathématique")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300)
plt.close()

# Graphique 2 : Courbe de Rupture Avant/Après Ultra-Détaillée
vols_par_jour = df_aviation.groupby('date').agg({
    'pred_annulation': 'sum',
    'pred_retard': 'mean'
}).reset_index()

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(14, 7))

# Axe gauche : Les Annulations (Ligne Rouge)
color_red = '#d9534f'
ax1.set_xlabel("Dates (Avril 2025)", fontsize=12, fontweight='bold', labelpad=15)
ax1.set_ylabel("Nombre total de vols annulés", color=color_red, fontsize=12, fontweight='bold')
line1 = ax1.plot(vols_par_jour['date'], vols_par_jour['pred_annulation'],
                 marker='o', color=color_red, linewidth=3, label="Vols annulés (Classification)")
ax1.tick_params(axis='y', labelcolor=color_red)
ax1.set_xticklabels(vols_par_jour['date'], rotation=45, ha='right')

# Axe droit : Les Retards (Ligne Orange)
ax2 = ax1.twinx()
color_orange = '#f0ad4e'
ax2.set_ylabel("Retard moyen estimé (Minutes)", color=color_orange, fontsize=12, fontweight='bold')
line2 = ax2.plot(vols_par_jour['date'], vols_par_jour['pred_retard'],
                 marker='s', linestyle='--', color=color_orange, linewidth=2, label="Retard moyen (Régression)")
ax2.tick_params(axis='y', labelcolor=color_orange)

# Définition visuelle de la rupture au Jour 21 (21 Avril 2025)
jour_choc = "2025-04-21"
plt.axvline(x=jour_choc, color='black', linestyle=':', linewidth=2.5, label="Déclenchement Cyberattaque")

# Coloration des arrière-plans (Vert = Normal, Rouge = Crise)
ax1.axvspan(vols_par_jour['date'].iloc[0], jour_choc, color='green', alpha=0.07, label="Zone Saine : Trafic Normal")
ax1.axvspan(jour_choc, vols_par_jour['date'].iloc[-1], color='red', alpha=0.07, label="Zone Critique : Système Paralysé")

# Titre, Légende et Ajustement
plt.title("ANALYSE DE RUPTURE : Impact de la Cyberattaque sur le Trafic Aérien", fontsize=14, fontweight='bold', pad=20)
all_lines = line1 + line2
all_labels = [l.get_label() for l in all_lines]
ax1.legend(all_lines, all_labels, loc='upper left', frameon=True, facecolor='white')

plt.tight_layout()
plt.savefig("courbe_rupture_aviation.png", dpi=300)
plt.close()

# =====================================================================
# ÉTAPE 7 : Exportation du Fichier de Relais pour Nathan (Finance)
# =====================================================================
df_aviation.to_csv("output_aviation.csv", index=False)

print("\n [SUCCÈS CENTRAL] TOUT EST ENREGISTRÉ ET PARFAIT CHEF !")
print("-> Fichier créé pour Nathan : 'output_aviation.csv'")
print("-> Graphiques mis à jour : 'feature_importance.png' et 'courbe_rupture_aviation.png'")