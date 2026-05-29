import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generer_pdf():
    # Nom du fichier final
    pdf_filename = "Rapport_Aviation_Exauce.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    # --- Création des styles personnalisés ---
    style_titre_principal = ParagraphStyle(
        'TitrePrincipal',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        alignment=1, # Centré
        spaceAfter=10
    )

    style_sous_titre = ParagraphStyle(
        'SousTitre',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=20
    )

    style_titre_section = ParagraphStyle(
        'TitreSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=15,
        spaceAfter=10
    )

    style_texte = ParagraphStyle(
        'TexteNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8,
        alignment=4 # Justifié
    )

    style_puce = ParagraphStyle(
        'TextePuce',
        parent=style_texte,
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=5
    )

    style_tableau = ParagraphStyle(
        'TexteTableau',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12
    )

    elements = []

    # --- EN-TÊTE ---
    elements.append(Paragraph("RAPPORT DE PROJET : PIPELINE &quot;DIGITAL DOMINO&quot;", style_titre_principal))
    elements.append(Paragraph("Phase 2 : Modélisation de l'Impact sur le Secteur de l'Aviation<br/><b>Auteur : Exaucé (Data Scientist Transport)</b>", style_sous_titre))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a365d'), spaceAfter=20))

    # --- SECTION 1 ---
    elements.append(Paragraph("1. Introduction et Contexte du Projet", style_titre_section))
    elements.append(Paragraph("Le projet Digital Domino a pour but de démontrer mathématiquement comment une crise informatique isolée peut se propager et provoquer un effondrement macroéconomique. L'objectif est de construire un pipeline prédictif en cascade divisé en trois secteurs : le Réseau (Cybersécurité), le Transport (Aviation) et la Finance (Bourse).", style_texte))
    elements.append(Paragraph("Mon rôle se situe au cœur de ce réacteur. Je suis chargé de faire le pont entre le monde virtuel (l'attaque réseau) et le monde physique (les infrastructures aéroportuaires). Sans ce maillon, il est impossible de quantifier financièrement l'impact de l'attaque. Mon travail consiste à récupérer le signal d'alerte cyber, à l'ingérer dans des données de vols réels, et à utiliser le Machine Learning pour prédire la paralysie du trafic aérien, qui servira ensuite de déclencheur pour le krach boursier.", style_texte))

    # --- SECTION 2 ---
    elements.append(Paragraph("2. Le Point d'Entrée : Le travail de Jérémie et Duc (Réseau &amp; Cyber)", style_titre_section))
    elements.append(Paragraph("Pour comprendre mes modèles, il faut comprendre les données que je reçois. L'équipe en amont a traité un flux de trafic réseau pour détecter une intrusion :", style_texte))
    elements.append(Paragraph("• <b>Jérémie (Architecte Data) :</b> Il a restructuré les données brutes. Face à un déséquilibre massif (811 lignes saines pour 187 attaques), il a appliqué un découpage StratifiedKFold pour garantir un apprentissage sain. Il a également créé des variables d'ingénierie (Feature Engineering) cruciales, comme le debit_paquets (vitesse) et la taille_moyenne_paquet (volume).", style_puce))
    elements.append(Paragraph("• <b>Duc (Ingénieur Cyber) :</b> Il a entraîné des modèles de classification sur ces données. Pour s'assurer de ne rater aucune menace (zéro Faux Négatif), il a optimisé son modèle en abaissant le seuil de décision de 0.5 à 0.35.", style_puce))
    elements.append(Paragraph("• <b>Le Relais :</b> Duc m'a transmis un fichier contenant une variable continue unique : proba_cyber. C'est un score entre 0.0 et 1.0 qui évalue la probabilité qu'une attaque soit en cours à un instant T.", style_puce))

    # --- SECTION 3 ---
    elements.append(Paragraph("3. Nettoyage et Ingénierie des Données (Phase Aviation)", style_titre_section))
    elements.append(Paragraph("J'ai réceptionné le fichier d'historique des vols (aviation.csv) que j'ai fusionné chronologiquement avec les scores de Duc. Pour que mes algorithmes puissent traiter ces informations, j'ai dû appliquer un traitement strict (Data Cleaning) :", style_texte))
    elements.append(Paragraph("• <b>Règle Métier sur les Retards :</b> Les données contenaient des retards négatifs (ex: -5 minutes), signifiant qu'un avion était en avance. En temps de crise, une avance n'est pas pertinente et fausse la moyenne. J'ai appliqué une fonction pour ramener toutes les valeurs négatives à 0.", style_puce))
    elements.append(Paragraph("• <b>Encodage One-Hot :</b> Les algorithmes ne lisent pas le texte. J'ai transformé les colonnes compagnie (Air France, Delta, etc.) et aeroport_depart en une matrice de zéros et de uns via la méthode get_dummies.", style_puce))
    elements.append(Paragraph("• <b>Isolation des Types Numériques :</b> Pour éviter les erreurs fatales de conversion (comme l'incapacité de convertir des dates textuelles en variables de type float), j'ai programmé un filtre strict qui exclut automatiquement tout format de texte pour ne conserver que les tenseurs mathématiques purs avant l'entraînement.", style_puce))
    elements.append(Paragraph("• <b>Correction des coupures réseau (NaN) :</b> Lors du pic de la cyberattaque (après la 200ème observation), les capteurs de Duc ont cessé d'émettre, générant des cases vides. J'ai imputé ces valeurs par 1.0 (certitude d'attaque à 100%) pour modéliser le black-out total du système.", style_puce))

    # --- SECTION 4 ---
    elements.append(Paragraph("4. Architecture de la Double Modélisation (Dual Modeling)", style_titre_section))
    elements.append(Paragraph("Le secteur aérien subit deux types de perturbations distinctes : les vols purement et simplement supprimés, et les vols qui partent, mais avec un retard accumulé. Un seul modèle ne peut pas prédire ces deux réalités. J'ai donc conçu une double architecture en cascade :", style_texte))
    elements.append(Paragraph("<b>Modèle A : Classification des Annulations</b><br/>Algorithme : Arbre de Décision (DecisionTreeClassifier).<br/>Objectif : Prédire la variable binaire annulation (1 = Annulé, 0 = Maintenu).<br/>Configuration : La profondeur de l'arbre a été limitée à max_depth=5. Cela empêche le modèle de mémoriser les données par cœur (surapprentissage) et l'oblige à se concentrer sur les règles générales, principalement pilotées par la montée de la variable proba_cyber.", style_puce))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<b>Modèle B : Régression des Retards</b><br/>Algorithme : Forêt Aléatoire (RandomForestRegressor).<br/>Objectif : Estimer la valeur continue du retard en minutes.<br/>Logique Métier : Un vol annulé n'a pas de retard, il n'existe plus. J'ai donc filtré ma base de données pour n'entraîner ce modèle que sur les vols maintenus (annulation == 0). L'algorithme a utilisé 100 arbres en parallèle (n_estimators=100) pour lisser les prédictions et offrir une estimation du temps d'attente extrêmement robuste.", style_puce))

    elements.append(Spacer(1, 10))

    # --- SECTION 5 (LE TABLEAU) ---
    elements.append(Paragraph("5. Dictionnaire Exhaustif des Données (Output Final)", style_titre_section))
    elements.append(Paragraph("Le fruit de cette modélisation est un fichier d'export nommé output_aviation.csv. Il contient 15 variables précises qui décrivent l'état complet du système.", style_texte))

    donnees_tableau = [
        [Paragraph("<b>Nom de la Colonne</b>", style_tableau), Paragraph("<b>Type &amp; Signification Métier</b>", style_tableau)],
        [Paragraph("date", style_tableau), Paragraph("Date calendaire du vol (Avril 2025). Permet l'analyse temporelle.", style_tableau)],
        [Paragraph("heure_depart_prevue", style_tableau), Paragraph("Heure théorique programmée pour le décollage.", style_tableau)],
        [Paragraph("compagnie", style_tableau), Paragraph("Nom de l'opérateur aérien en charge du vol (AirFrance, Ryanair, etc.).", style_tableau)],
        [Paragraph("aeroport_depart", style_tableau), Paragraph("Code IATA de l'aéroport d'origine (ex: LHR, FCO, CDG).", style_tableau)],
        [Paragraph("aeroport_arrivee", style_tableau), Paragraph("Code IATA de la destination du vol.", style_tableau)],
        [Paragraph("cyber_alert", style_tableau), Paragraph("Indicateur binaire historique présent dans la base de données brute.", style_tableau)],
        [Paragraph("retard_minutes", style_tableau), Paragraph("Temps de retard réel en minutes (Nettoyé : les avances sont à 0).", style_tableau)],
        [Paragraph("annulation", style_tableau), Paragraph("Statut d'annulation historique (0 = Vol opéré, 1 = Vol supprimé).", style_tableau)],
        [Paragraph("cause_perturbation", style_tableau), Paragraph("Motif textuel officiel déclaré (Météo, Grève, Technique, Aucune).", style_tableau)],
        [Paragraph("ml_alert", style_tableau), Paragraph("Niveau d'alerte matériel généré par les capteurs de l'aéroport.", style_tableau)],
        [Paragraph("niveau_crise", style_tableau), Paragraph("Indice de gravité globale de la situation historique.", style_tableau)],
        [Paragraph("proba_cyber", style_tableau), Paragraph("[Entrée de Duc] Probabilité d'attaque (0.0 à 1.0). C'est le déclencheur.", style_tableau)],
        [Paragraph("pred_annulation", style_tableau), Paragraph("[Sortie Modèle A] Prédiction de mon IA : 1 si le vol est condamné.", style_tableau)],
        [Paragraph("pred_retard", style_tableau), Paragraph("[Sortie Modèle B] Prédiction de mon IA : minutes de retard estimées.", style_tableau)],
        [Paragraph("aviation_perturbee", style_tableau), Paragraph("[Sortie pour Nathan] Variable pivot finale. Vaut 1 si le vol est annulé OU si son retard dépasse 60 minutes.", style_tableau)]
    ]

    t = Table(donnees_tableau, colWidths=[120, 390])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2c5282')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 10))

    # --- SECTION 6 ---
    elements.append(Paragraph("6. Validation Scientifique (Interprétation des Graphiques)", style_titre_section))
    elements.append(Paragraph("Pour prouver au jury la validité de notre pipeline, j'ai généré deux livrables visuels démontrant l'effet domino :", style_texte))

    elements.append(Paragraph("<b>A. Graphique d'Importance des Variables (Feature Importance)</b>", style_texte))
    elements.append(Paragraph("Ce diagramme en barres classe les variables selon leur poids mathématique dans la prise de décision de l'Intelligence Artificielle.", style_texte))
    elements.append(Paragraph("• <b>Observation :</b> La variable proba_cyber (transmise par Duc) domine écrasamment le graphique, captant près de 90 % de l'importance totale. Les variables liées aux compagnies aériennes ou aux aéroports ont un score marginal.", style_puce))
    elements.append(Paragraph("• <b>Conclusion Scientifique :</b> Cela prouve que le chaos prédit dans le ciel aérien n'est pas un dysfonctionnement de routine des aéroports, mais bien la conséquence unilatérale et directe de la cyberattaque.", style_puce))

    elements.append(Spacer(1, 5))

    elements.append(Paragraph("<b>B. Courbe de Rupture Temporelle (Avant/Après)</b>", style_texte))
    elements.append(Paragraph("Ce graphique superpose les jours du mois d'avril avec le volume d'annulations et de retards moyens.", style_texte))
    elements.append(Paragraph("• <b>Zone Saine (1er au 20 avril) :</b> Le réseau informatique va bien, la ligne des annulations est plate (0 vol annulé) et les retards sont minimes.", style_puce))
    elements.append(Paragraph("• <b>Le Point de Rupture (21 avril) :</b> Au moment où le script simule l'injection du code malveillant, la courbe des annulations subit une cassure verticale immédiate (montant à plus de 35 annulations par jour).", style_puce))
    elements.append(Paragraph("• <b>Zone de Crise (21 au 30 avril) :</b> Les deux indicateurs (annulations et retards) s'emballent simultanément. C'est la confirmation visuelle de l'effondrement systémique de l'infrastructure de transport.", style_puce))

    # --- SECTION 7 ---
    elements.append(Paragraph("7. Conclusion et Relais (Phase Finance)", style_titre_section))
    elements.append(Paragraph("Mon travail s'achève sur la création de la variable aviation_perturbee. Cette colonne est une traduction mathématique parfaite de la crise opérationnelle.", style_texte))
    elements.append(Paragraph("Le fichier est désormais transmis à Nathan (Quantitative Financial Analyst). Lors de la phase 3, Nathan n'aura plus besoin d'analyser le réseau informatique. Il va synchroniser mes données de vols avec les indices boursiers. Il utilisera un modèle de régression robuste (HuberRegressor ou Ridge) pour démontrer que l'accumulation des 1 dans ma colonne aviation_perturbee entraîne inévitablement une destruction massive de valeur en millions d'euros sur les marchés financiers.", style_texte))
    elements.append(Paragraph("L'effet Domino est ainsi prouvé de bout en bout.", style_texte))

    # Génération du document
    doc.build(elements)
    print(f"✅ Le fichier PDF '{pdf_filename}' a été généré avec succès dans ce dossier !")

if __name__ == "__main__":
    generer_pdf()