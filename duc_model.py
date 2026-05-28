import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import (classification_report, confusion_matrix,
                            ConfusionMatrixDisplay, precision_recall_curve)

# ============================================================
# ÉTAPE 1 — Charger le dataset préparé par Jérémie
# ============================================================
df = pd.read_csv("reseau_engineered.csv", sep=";")
df.columns = df.columns.str.strip()

# Supprimer les colonnes non numériques inutiles
df = df.drop(columns=["timestamp", "ip_source", "ip_destination"], errors="ignore")

# Encoder TOUTES les colonnes texte automatiquement
cols_texte = df.select_dtypes(include=["object"]).columns.tolist()
cols_texte = [c for c in cols_texte if c != "label"]
df = pd.get_dummies(df, columns=cols_texte)

X = df.drop(columns=["label"])
y = df["label"]
# ============================================================
# ÉTAPE 2 — Découpage StratifiedKFold
# ============================================================
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
train_idx, test_idx = list(skf.split(X, y))[0]

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

# ============================================================
# ÉTAPE 3 — Entraîner et comparer les 2 modèles (baseline)
# ============================================================
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
print("=== Random Forest ===")
print(classification_report(y_test, rf.predict(X_test)))

hgb = HistGradientBoostingClassifier(random_state=42)
hgb.fit(X_train, y_train)
print("=== HistGradientBoosting ===")
print(classification_report(y_test, hgb.predict(X_test)))

# ============================================================
# ÉTAPE 4 — GridSearchCV sur les 2 modèles
# ============================================================
param_rf = {
   "max_depth": [5, 10, 20],
   "n_estimators": [50, 100, 200],
   "criterion": ["gini", "entropy"]
}
grid_rf = GridSearchCV(RandomForestClassifier(random_state=42),
                      param_rf, cv=skf, scoring="recall", n_jobs=-1)
grid_rf.fit(X, y)
print("Meilleurs params RF :", grid_rf.best_params_)

param_hgb = {
   "max_depth": [5, 10, 20],
   "max_iter": [50, 100, 200]
}
grid_hgb = GridSearchCV(HistGradientBoostingClassifier(random_state=42),
                       param_hgb, cv=skf, scoring="recall", n_jobs=-1)
grid_hgb.fit(X, y)
print("Meilleurs params HGB :", grid_hgb.best_params_)

# Garder le meilleur modèle
best_model = grid_rf.best_estimator_ if (
   grid_rf.best_score_ >= grid_hgb.best_score_
) else grid_hgb.best_estimator_

best_model.fit(X_train, y_train)
print("Modèle retenu :", type(best_model).__name__)

# ============================================================
# ÉTAPE 5 — Ajuster le seuil décisionnel à 0.35
# ============================================================
y_proba = best_model.predict_proba(X_test)[:, 1]

precision, recall, thresholds = precision_recall_curve(y_test, y_proba)
plt.figure()
plt.plot(thresholds, precision[:-1], label="Précision")
plt.plot(thresholds, recall[:-1], label="Rappel")
plt.axvline(x=0.35, color="red", linestyle="--", label="Seuil = 0.35")
plt.xlabel("Seuil")
plt.title("Courbe Precision-Recall")
plt.legend()
plt.savefig("precision_recall_curve.png")
plt.show()

SEUIL = 0.35
y_pred_ajuste = (y_proba >= SEUIL).astype(int)
print("=== Rapport avec seuil 0.35 ===")
print(classification_report(y_test, y_pred_ajuste))

# ============================================================
# ÉTAPE 6 — Matrice de Confusion (livrable obligatoire)
# ============================================================
cm = confusion_matrix(y_test, y_pred_ajuste)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=["Normal", "Attaque"])
disp.plot(cmap="Blues")
plt.title("Matrice de Confusion (seuil=0.35)")
plt.savefig("matrice_confusion.png")
plt.show()
print("Faux Négatifs :", cm[1][0])

# ============================================================
# ÉTAPE 7 — Exporter les probabilités pour Exaucé
# ============================================================
df_test = X_test.copy()
df_test["proba_cyber"] = y_proba
df_test["label_reel"] = y_test.values
df_test.to_csv("output_proba_cyber.csv", index=False)
print("✅ Fichier output_proba_cyber.csv exporté !")

joblib.dump(best_model, "modele_duc.pkl")
print("✅ Modèle sauvegardé : modele_duc.pkl")