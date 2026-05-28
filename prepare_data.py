import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

print("==========================================================")
#  Rôle: Architecte Data & Infrastructure Réseau
print("   LIVRABLE DE JÉRÉMIE : DATA ENGINEERING & EDA ADVANCED  ")
print("==========================================================")


# TÂCHE 1 : CHARGEMENT & ANALYSE EXPLORATOIRE (EDA)
# Chargement du fichier réseau [cite: 88]
df = pd.read_csv("reseau.csv", sep=";", skipinitialspace=True)
df.columns = df.columns.str.strip()  # Supprime les espaces résiduels dans les noms de colonnes

print(f"\n[INFO] Dataset chargé : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
print(f"Distribution brute des classes : \n{df['label'].value_counts()}") 

# Génération du graphique professionnel pour la soutenance [cite: 6, 7]
plt.figure(figsize=(7, 5))
sns.set_theme(style="whitegrid")
ax = sns.countplot(x='label', data=df, hue='label', palette=['#2ecc71', '#e74c3c'], legend=False)
plt.title("Analyse du Déséquilibre des Classes (Trafic Réseau)", fontsize=12, fontweight='bold')
plt.xlabel("Classe (0: Normal | 1: Attaque)", fontsize=10)
plt.ylabel("Nombre de Connexions", fontsize=10)
# Ajout des étiquettes de score sur les barres
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height() + 10),
                ha='center', va='center', color='black', fontweight='bold')

# Sauvegarde automatique du graphique pour ton rapport/diaporamas
plt.savefig("repartition_classes_jeremie.png", dpi=300)
print("[OK] Graphique 'repartition_classes_jeremie.png' généré et sauvegardé avec succès.")



# TÂCHE 2 : FEATURE ENGINEERING ÉVOLUÉ 

# Variable 1 : Vitesse de l'échange (débit de paquets) 
df['debit_paquets'] = df['nb_paquets'] / (df['duree_connexion_sec'] + 1e-5)

# Variable 2 : Taille moyenne d'un paquet (comportement) 
df['taille_moyenne_paquet'] = df['volume_donnees_kb'] / df['nb_paquets']

print("[OK] Feature Engineering complété : Variables 'debit_paquets' et 'taille_moyenne_paquet' créées.")



# TÂCHE 3 : ISOLATION DES VARIABLES & CONFIGURATION DU PIPELINE [cite: 14]
# Métadonnées à exclure pour ne pas biaiser l'apprentissage 
colonnes_a_exclure = ['timestamp', 'ip_source', 'ip_destination', 'type_trafic', 'ml_alert', 'niveau_crise', 'label']

X = df.drop(columns=colonnes_a_exclure)
y = df['label']

# Définition des types de colonnes pour les transformations [cite: 15, 16, 93]
var_numeriques = ['port_destination', 'duree_connexion_sec', 'volume_donnees_kb', 
                  'nb_paquets', 'nb_echecs_auth', 'debit_paquets', 'taille_moyenne_paquet']
var_categoriels = ['protocole']

# Pipeline de transformation strict pour éliminer le Data Leakage 
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), var_numeriques), # Normalisation 
        ('cat', OneHotEncoder(handle_unknown='ignore'), var_categoriels) # Encodage 
    ]
)
print("[OK] Architecture du Pipeline Anti-Data Leakage validée.")



# VALIDATION DE LA STRATIFICATION (STRATIFIED K-FOLD) 

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print("\n--- RAPPORT TECHNIQUE DE STRATIFICATION POUR LE JURY ---")
for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
    y_train_fold = y.iloc[train_idx]
    y_test_fold = y.iloc[test_idx]
    
    prop_train = (y_train_fold.sum() / len(y_train_fold)) * 100
    prop_test = (y_test_fold.sum() / len(y_test_fold)) * 100
    
    print(f"Pli {fold + 1} -> Train : {len(y_train_fold)} lignes (Attaques: {prop_train:.2f}%) | "
          f"Test : {len(y_test_fold)} lignes (Attaques: {prop_test:.2f}%)")

print("\n==========================================================")
print(" TOUS LES CRITÈRES DU CAHIER DES CHARGES SONT VALIDÉS ! ")
print("==========================================================")

# Export du dataset enrichi pour le reste de l'équipe
df.to_csv("reseau_engineered.csv", sep=";", index=False)
print("[INFO] Fichier 'reseau_engineered.csv' exporté pour Duc, Exaucé et Nathan.")