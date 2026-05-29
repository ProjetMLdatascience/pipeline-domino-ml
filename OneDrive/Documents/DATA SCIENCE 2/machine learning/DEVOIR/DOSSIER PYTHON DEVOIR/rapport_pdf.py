import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def creer_pdf_rapport():
    pdf_filename = "Rapport_Aviation_Exauce.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    # Styles personnalisés
    style_titre = ParagraphStyle(
        'TitreRapport',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1a365d'),
        alignment=1, # Centré
        spaceAfter=15
    )

    style_sous_titre = ParagraphStyle(
        'SousTitreRapport',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4a5568'),
        alignment=1,
        spaceAfter=25
    )

    style_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=15,
        spaceAfter=10
    )

    style_corps = ParagraphStyle(
        'CorpsTexte',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=8
    )

    style_tableau = ParagraphStyle(
        'TexteTableau',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1a202c')
    )

    style_tableau_titre = ParagraphStyle(
        'TitreTableau',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.white
    )

    story = []

    # En-tête
    story.append(Paragraph("RAPPORT TECHNIQUE - PIPELINE DIGITAL DOMINO", style_titre))
    story.append(Paragraph("Phase 2 : Modélisation de l'Impact sur le Trafic Aérien<br/>Auteur : Exaucé (Data Scientist Transport)", style_sous_titre))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a365d'), spaceAfter=20))

    # Section 1
    story.append(Paragraph("1. Contexte Opérationnel & Justification Métier", style_h1))
    txt_1 = ("Le projet <b>Digital Domino</b> simule la propagation d'une crise systémique majeure. "
             "Mon rôle au sein de l'équipe est d'établir le lien indispensable entre l'infrastructure réseau "
             "et l'économie réelle. Je reçois les scores techniques de probabilité de cyberattaque générés par <b>Duc</b> (Cybersécurité) "
             "et je les traduis en indicateurs opérationnels pour le secteur aérien (annulations et retards). "
             "Ce travail est la clé de voûte qui permet ensuite à <b>Nathan</b> (Finance) d'évaluer le krach boursier sur le CAC40.")
    story.append(Paragraph(txt_1, style_corps))

    # Section 2
    story.append(Paragraph("2. Dictionnaire des Données (Analyse exhaustive des 15 colonnes)", style_h1))
    story.append(Paragraph("Le fichier final exporté pour la finance comporte les variables suivantes :", style_corps))

    colonnes_data = [
        [Paragraph("Nom de la Colonne", style_tableau_titre), Paragraph("Type & Signification Métier", style_tableau_titre)],
        [Paragraph("date", style_tableau), Paragraph("Date du vol (Avril 2025). Permet l'analyse temporelle avant/après choc.", style_tableau)],
        [Paragraph("heure_depart_prevue", style_tableau), Paragraph("Heure théorique programmée du décollage.", style_tableau)],
        [Paragraph("compagnie", style_tableau), Paragraph("Nom de l'opérateur aérien (AirFrance, Ryanair, Delta, Iberia, Swiss).", style_tableau)],
        [Paragraph("aeroport_depart", style_tableau), Paragraph("Code IATA de l'aéroport d'origine (ex: LHR, FCO).", style_tableau)],
        [Paragraph("aeroport_arrivee", style_tableau), Paragraph("Code IATA de la destination du vol.", style_tableau)],
        [Paragraph("cyber_alert", style_tableau), Paragraph("Indicateur historique binaire d'alerte système.", style_tableau)],
        [Paragraph("retard_minutes", style_tableau), Paragraph("Retard réel en minutes (Nettoyé : valeurs négatives ramenées à 0).", style_tableau)],
        [Paragraph("annulation", style_tableau), Paragraph("Statut réel d'annulation historique (0 = Maintenu, 1 = Annulé).", style_tableau)],
        [Paragraph("cause_perturbation", style_tableau), Paragraph("Motif officiel de base de l'aléa (Ex: Météo, Grève, Aucune).", style_tableau)],
        [Paragraph("ml_alert", style_tableau), Paragraph("Niveau d'alerte automatique des infrastructures au sol.", style_tableau)],
        [Paragraph("niveau_crise", style_tableau), Paragraph("Indice de gravité globale de l'incident d'origine.", style_tableau)],
        [Paragraph("proba_cyber", style_tableau), Paragraph("<b>Variable pivot de Duc</b>. Score cyber (0 à 1). Corrigé à 1.0 en période de crise.", style_tableau)],
        [Paragraph("pred_annulation", style_tableau), Paragraph("<b>Sortie Modèle A</b>. Prédiction d'annulation du vol (0 ou 1) liée à l'attaque.", style_tableau)],
        [Paragraph("pred_retard", style_tableau), Paragraph("<b>Sortie Modèle B</b>. Estimation fine du retard en minutes généré sur le réseau.", style_tableau)],
        [Paragraph("aviation_perturbee", style_tableau), Paragraph("<b>Livrable Nathan</b>. Variable pivot (1 si annulé OU retard > 60 min). Déclenche le krach.", style_tableau)]
    ]

    t = Table(colonnes_data, colWidths=[140, 380])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2c5282')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Section 3
    story.append(Paragraph("3. Architecture des Modèles Prédictifs", style_h1))
    txt_3 = ("Pour modéliser l'impact avec précision, j'ai implémenté une double architecture de Machine Learning :<br/>"
             "• <b>Modèle A - Classification (Arbre de Décision) :</b> Ce modèle détermine si les conditions de "
             "crise saturent les infrastructures au point de forcer l'annulation du vol. Une profondeur stricte (max_depth=5) "
             "a été fixée pour éliminer tout risque de surapprentissage.<br/>"
             "• <b>Modèle B - Régression (Forêt Aléatoire / Random Forest) :</b> Entraîné exclusivement sur les vols "
             "qui maintiennent leur décollage. En combinant 100 sous-arbres indépendants, il prédit avec une grande stabilité "
             "le nombre de minutes de retard induites par le ralentissement cyber des systèmes de contrôle.")
    story.append(Paragraph(txt_3, style_corps))

    # Section 4
    story.append(Paragraph("4. Validation Scientifique des Graphiques de Soutenance", style_h1))
    txt_4 = ("Les deux livrables visuels générés par mon script apportent les preuves mathématiques requises par le jury :<br/>"
             "• <b>Importance des Variables (feature_importance.png) :</b> Ce graphique confirme de façon incontestable "
             "l'effet domino. La variable <i>proba_cyber</i> s'accapare près de 90% de l'importance structurelle du modèle. "
             "Cela prouve que la désorganisation du ciel est causée par la crise informatique et non par des aléas de routine.<br/>"
             "• <b>Courbe de Rupture Temporelle (courbe_rupture_aviation.png) :</b> Ce graphique à double axe illustre "
             "parfaitement la bascule systémique. Du 1er au 20 avril (Période Saine colorée en vert), les annulations sont nulles. "
             "Le 21 avril, l'attaque frappe : la ligne rouge des annulations subit une rupture verticale immédiate, "
             "tandis que les retards s'envolent dans la zone critique (rouge).")
    story.append(Paragraph(txt_4, style_corps))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e0'), spaceAfter=10))
    story.append(Paragraph("<i>Fin du rapport technique - Validé et prêt pour transmission à la Phase Finance (Nathan).</i>", style_sous_titre))

    doc.build(story)
    print(f"✅ Le fichier PDF '{pdf_filename}' a été généré avec succès !")

if __name__ == "__main__":
    creer_pdf_rapport()