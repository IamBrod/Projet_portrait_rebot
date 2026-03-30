from tkinter import *

# LES DIFFÉRENTES COULEURS

FOND_GENERAL      = "gainsboro"      # gris très clair, fond de la fenêtre
FOND_BARRE        = "white"          # blanc, fond de la barre latérale gauche
FOND_CONTENU      = "white"          # blanc, fond de la zone des cases à cocher
COULEUR_ACCENT    = "#4169E1"        # bleu roi, boutons et textes importants
TEXTE_PRINCIPAL   = "#1a1a3e"        # bleu très foncé, texte normal
TEXTE_SECONDAIRE  = "darkgray"       # gris, petits textes 
BORDURE           = "lightgrey"      # gris clair, lignes de séparation
SURVOL_CATEGORIE  = "#EEF2FF"        # bleu très pâle, quand la souris passe sur une catégorie
CATEGORIE_ACTIVE  = "#DBEAFE"        # bleu pâle, catégorie actuellement sélectionnée
FOND_CASE         = "white"          # blanc, intérieur des cases à cocher
 
# CRÉATION DE LA FENÊTRE

fenetre = Tk()                          # crée la fenêtre
fenetre.title("Portraits Robot")        # titre affiché en haut de la fenêtre
fenetre.geometry("1100x680")            
fenetre.configure(bg=FOND_GENERAL)     
fenetre.resizable(True, True)           # l'utilisateur peut redimensionner la fenêtre
 
# DONNÉES

categories = {
    "Hair Color":  ['Brown', 'Blond', 'Black', 'Gray'],
    "Hair Type":   ['Wavy', 'Straight', 'Receding Hairline', 'Bangs', 'Bald'],
    "Accessory":   ['Earrings', 'Hat', 'Necklace', 'Lipstick', 'Necktie', 'Eyeglasses'],
    "Beard":       ['Mustache', 'Goatee', 'No Beard', 'Sideburns', "5 o'Clock Shadow"],
    "Sexe":        ['Male', 'Female'],
    "Mouth":       ['Smiling', 'Mouth Slightly Open', 'Big Lips'],
    "Eyes":        ['Narrow Eyes', 'Bags Under Eyes', 'Bushy Eyebrows', 'Arched Eyebrows'],
    "Face":        ['Oval Face', 'Pale Skin', 'Heavy Makeup', 'Rosy Cheeks',
                    'High Cheekbones', 'Double Chin', 'Chubby'],
    "Nose":        ['Big Nose', 'Pointy Nose'],
    "Age":         ['Young', 'Aged'],
    "Image":       ['Blurry', 'Clear']
}


icones = {
    "Hair Color": "💇", "Hair Type": "✂️", "Accessory": "👒",
    "Beard": "🥸", "Sexe": "🚻", "Mouth": "👄",
    "Eyes": "👁️", "Face": "👤", "Nose": "👃",
    "Age": "🕺🏼", "Image": "📷"
}


# LISTE DE RÉFÉRENCE 

liste_reference = [
    "5_o_Clock_Shadow", "Arched_Eyebrows", "Attractive", "Bags_Under_Eyes",
    "Bald", "Bangs", "Big_Lips", "Big_Nose", "Black_Hair", "Blond_Hair",
    "Blurry", "Brown_Hair", "Bushy_Eyebrows", "Chubby", "Double_Chin",
    "Eyeglasses", "Goatee", "Gray_Hair", "Heavy_Makeup", "High_Cheekbones",
    "Male", "Mouth_Slightly_Open", "Mustache", "Narrow_Eyes", "No_Beard",
    "Oval_Face", "Pale_Skin", "Pointy_Nose", "Receding_Hairline", "Rosy_Cheeks",
    "Sideburns", "Smiling", "Straight_Hair", "Wavy_Hair", "Wearing_Earrings",
    "Wearing_Hat", "Wearing_Lipstick", "Wearing_Necklace", "Wearing_Necktie",
    "Young"
]

# TRADUCTION ENTRE LE NOM AFFICHÉ ET LE NOM TECHNIQUE 
traduction = {
    "5 o'Clock Shadow":    "5_o_Clock_Shadow",
    "Arched Eyebrows":     "Arched_Eyebrows",
    "Bags Under Eyes":     "Bags_Under_Eyes",
    "Bald":                "Bald",
    "Bangs":               "Bangs",
    "Big Lips":            "Big_Lips",
    "Big Nose":            "Big_Nose",
    "Black":               "Black_Hair",
    "Blond":               "Blond_Hair",
    "Blurry":              "Blurry",
    "Brown":               "Brown_Hair",
    "Bushy Eyebrows":      "Bushy_Eyebrows",
    "Chubby":              "Chubby",
    "Double Chin":         "Double_Chin",
    "Eyeglasses":          "Eyeglasses",
    "Goatee":              "Goatee",
    "Gray":                "Gray_Hair",
    "Heavy Makeup":        "Heavy_Makeup",
    "High Cheekbones":     "High_Cheekbones",
    "Male":                "Male",
    "Mouth Slightly Open": "Mouth_Slightly_Open",
    "Mustache":            "Mustache",
    "Narrow Eyes":         "Narrow_Eyes",
    "No Beard":            "No_Beard",
    "Oval Face":           "Oval_Face",
    "Pale Skin":           "Pale_Skin",
    "Pointy Nose":         "Pointy_Nose",
    "Receding Hairline":   "Receding_Hairline",
    "Rosy Cheeks":         "Rosy_Cheeks",
    "Sideburns":           "Sideburns",
    "Smiling":             "Smiling",
    "Straight":            "Straight_Hair",
    "Wavy":                "Wavy_Hair",
    "Earrings":            "Wearing_Earrings",
    "Hat":                 "Wearing_Hat",
    "Lipstick":            "Wearing_Lipstick",
    "Necklace":            "Wearing_Necklace",
    "Necktie":             "Wearing_Necktie",
    "Young":               "Young",
}

#  MÉMOIRE DE L'INTERFACE
#  BooleanVar() est une variable qui vaut True si la case est cochée, False sinon
#  On en crée une pour chaque option de chaque catégorie

cases_cochees    = {cat: {opt: BooleanVar() for opt in opts} for cat, opts in categories.items()}
categorie_active = StringVar(value=list(categories.keys())[0])  # mémorise la catégorie affichée

# FONCTIONS 

# récupérer le dictionnaire pour renvoyer une image avec les caratéristiques choisies
def construire_resultat():
    """
    Parcourt toutes les cases et construit un dictionnaire :
    renvoie 1 si coché, 0 sinon, et -1 pour les cas inverses
    """
    coches = {
        traduction[opt]
        for cat in categories
        for opt, var in cases_cochees[cat].items()
        if var.get() and opt in traduction      # var.get() = True si case cochée
    }
    resultat = {}
    for cle in liste_reference:
        resultat[cle] = 1 if cle in coches else 0
 
    options_cochees = {opt for cat in categories for opt, v in cases_cochees[cat].items() if v.get()}
    if "Female" in options_cochees:
        resultat["Male"]   = -1
    if "Aged"   in options_cochees:
        resultat["Young"]  = -1
    if "Clear"  in options_cochees:
        resultat["Blurry"] = -1
 
    return resultat
 
 
def valider():
    """Affiche le dictionnaire dans le terminal."""
    print(construire_resultat())
 
def mettre_a_jour_badge(cat):
    """
    Met à jour trois choses après qu'une case a été cochée ou décochée :
         Le petit chiffre à droite du nom de catégorie dans la barre latérale
         Le titre de la zone de droite
         Le sous-titre qui liste les options cochées
    """
    # On récupère la liste des options cochées dans cette catégorie
    coches = [opt for opt, var in cases_cochees[cat].items() if var.get()]
 
    # Badge : affiche le nombre si > 0, sinon texte vide
    badges[cat].configure(
        text=str(len(coches)) if coches else "")
 
    # Titre de la zone de droite
    titre_label.configure(text=f"{icones.get(cat, '•')}  {cat}")
 
    # Sous-titre 
    sous_titre_label.configure(
        text=", ".join(coches) if coches else "Aucune sélection"
    )


def choisir_categorie(cat):
    """
    Appelée quand on clique sur une catégorie dans la barre latérale.
    Surligne la catégorie cliquée et affiche ses options.
    """
    categorie_active.set(cat)  # mémorise la catégorie active
 
    # On recolorie TOUS les boutons de la barre latérale
    for nom, bouton in boutons_categorie.items():
        selectionne = (nom == cat) 
        bouton.configure(
            bg=CATEGORIE_ACTIVE if selectionne else FOND_BARRE,
            fg=COULEUR_ACCENT   if selectionne else TEXTE_PRINCIPAL,
            font=("Segoe UI", 12, "bold") if selectionne else ("Segoe UI", 12),
        )
 
    afficher_categorie(cat)  # affiche les options de cette catégorie
 
 
def afficher_categorie(cat):
    """
    Vide la zone de droite et recrée les cases à cocher
    pour la catégorie choisie.
    """
    # On supprime tous les widgets actuellement affichés
    for widget in zone_options.winfo_children():
        widget.destroy()
 
    # On met à jour le titre et le sous-titre
    mettre_a_jour_badge(cat)
 
    # On crée une case à cocher pour chaque option de la catégorie
    for option in categories[cat]:
        var = cases_cochees[cat][option]  # récupère le True/False de cette option
        carte = Frame(zone_options, bg=FOND_CONTENU,
                      highlightbackground=BORDURE, highlightthickness=1)
        carte.pack(fill=X, pady=4, ipady=2)
 
        # La case à cocher elle-même
        case = Checkbutton(
            carte,
            text=f"  {option}",
            variable=var,
            font=("Segoe UI", 13),
            bg=FOND_CONTENU, fg=TEXTE_PRINCIPAL,
            selectcolor=FOND_CASE,
            activebackground=FOND_CONTENU,
            activeforeground=COULEUR_ACCENT,
            anchor="w",
            padx=16, pady=10,
            relief=FLAT,
            command=lambda c=cat: mettre_a_jour_badge(c),  # appelée à chaque clic
        )
        case.pack(fill=X)
 
        # Effet visuel quand la souris passe sur la carte
        def survol_entre(e, f=carte):
            f.configure(bg=SURVOL_CATEGORIE)   # fond change au survol
        def survol_sort(e, f=carte):
            f.configure(bg=FOND_CONTENU)        # fond revient à la normale
 
        for widget in (carte, case):
            widget.bind("<Enter>", survol_entre)
            widget.bind("<Leave>", survol_sort)


# CONSTRUCTION DE L'INTERFACE 
# Barre de titre en haut
entete = Frame(fenetre, bg=FOND_GENERAL, height=56)
entete.pack(fill=X, side=TOP)
entete.pack_propagate(False)  # garde la hauteur fixe même si le contenu est petit
 
Label(entete, text="  🫆 Portraits Robot",
      font=("Segoe UI", 16, "bold"), bg=FOND_GENERAL, fg="black",
      anchor="w").pack(fill=Y, side=LEFT, padx=20)
 
#Corps principal (barre latérale + zone de droite)
corps = Frame(fenetre, bg=FOND_GENERAL)
corps.pack(fill=BOTH, expand=True)
 
# Barre latérale gauche
# Deux frames superposées : une pour la bordure grise, une pour le contenu blanc
barre_laterale_ext = Frame(corps, bg=BORDURE, width=232)
barre_laterale_ext.pack(side=LEFT, fill=Y)
barre_laterale_ext.pack_propagate(False)
 
barre_laterale = Frame(barre_laterale_ext, bg=FOND_BARRE, width=230)
barre_laterale.pack(fill=BOTH, expand=True, padx=(0, 1))
 
# Titre "CATÉGORIES" en haut de la barre latérale
Label(barre_laterale, text="CATÉGORIES",
      font=("Segoe UI", 9, "bold"), bg=FOND_BARRE, fg=TEXTE_SECONDAIRE,
      anchor="w").pack(fill=X, padx=20, pady=(18, 6))
 
#Création des boutons de catégories dans la barre latérale 
boutons_categorie = {}  # stocke les boutons pour pouvoir les recolorier plus tard
badges            = {}  # stocke les petits chiffres à droite des catégories
 
for cat in categories:
    # Ligne horizontale pour cette catégorie
    ligne = Frame(barre_laterale, bg=FOND_BARRE)
    ligne.pack(fill=X, padx=8, pady=1)
 
    # Bouton (c'est un Label cliquable)
    bouton = Label(ligne,
                   text=f"  {icones.get(cat, '•')}  {cat}",
                   font=("Segoe UI", 12),
                   bg=FOND_BARRE, fg=TEXTE_PRINCIPAL,
                   anchor="w", pady=10, padx=6)
    bouton.pack(side=LEFT, fill=X, expand=True)
 
    # Petit badge numérique à droite 
    badge = Label(ligne, text="",
                  font=("Segoe UI", 9, "bold"),
                  bg=FOND_BARRE, fg=COULEUR_ACCENT,
                  width=3, anchor="e", padx=8)
    badge.pack(side=RIGHT)
 
    badges[cat]            = badge
    boutons_categorie[cat] = bouton
 
    
    for widget in (ligne, bouton, badge):
        widget.bind("<Button-1>", lambda e, c=cat: choisir_categorie(c))
 
# Séparateur vertical 
Frame(corps, bg=BORDURE, width=1).pack(side=LEFT, fill=Y)
 
# Zone de contenu à droite
zone_droite = Frame(corps, bg=FOND_GENERAL)
zone_droite.pack(side=LEFT, fill=BOTH, expand=True)
 
# Petit en-tête avec le titre et sous-titre de la catégorie active
entete_cat = Frame(zone_droite, bg=FOND_CONTENU, height=70)
entete_cat.pack(fill=X)
entete_cat.pack_propagate(False)
 
titre_label = Label(entete_cat, text="",
                    font=("Segoe UI", 18, "bold"),
                    bg=FOND_CONTENU, fg=TEXTE_PRINCIPAL, anchor="w")
titre_label.pack(side=LEFT, padx=28, pady=(14, 2))
 
sous_titre_label = Label(entete_cat, text="",
                         font=("Segoe UI", 10),
                         bg=FOND_CONTENU, fg=TEXTE_SECONDAIRE, anchor="w")
sous_titre_label.pack(side=LEFT, padx=(0, 20), pady=(22, 0))
 
# Ligne de séparation sous l'en-tête
Frame(zone_droite, bg=BORDURE, height=1).pack(fill=X)
 
# Zone scrollable pour les cases à cocher
zone_scroll = Frame(zone_droite, bg=FOND_GENERAL)
zone_scroll.pack(fill=BOTH, expand=True, padx=24, pady=20)
 
# Canvas = zone qui peut défiler verticalement
canvas    = Canvas(zone_scroll, bg=FOND_GENERAL, highlightthickness=0)
scrollbar = Scrollbar(zone_scroll, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
 
# Frame à l'intérieur du canvas qui contiendra les cases à cocher
zone_options = Frame(canvas, bg=FOND_GENERAL)
canvas.create_window((0, 0), window=zone_options, anchor="nw")
 
# Quand le contenu change de taille → on recalcule la zone de défilement
zone_options.bind("<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
 
# Défilement à la molette de la souris
canvas.bind("<MouseWheel>",
    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
 
# Pied de page 
pied_de_page = Frame(fenetre, bg=FOND_CONTENU, height=52)
pied_de_page.pack(fill=X, side=BOTTOM)
pied_de_page.pack_propagate(False)
 
# Ligne de séparation au-dessus du pied de page
Frame(pied_de_page, bg=BORDURE, height=1).pack(fill=X)
 
# Bouton Valider (à droite, le plus important)
Button(pied_de_page, text="  ✔  Valider",
       command=valider,
       font=("Segoe UI", 11, "bold"),
       bg=COULEUR_ACCENT, fg="palevioletred",
       relief=FLAT, padx=24, pady=8,
       activebackground="#2952c4",
       activeforeground="white").pack(side=RIGHT, padx=4, pady=8)
 
 
#  LANCEMENT
 
choisir_categorie(list(categories.keys())[0])
fenetre.mainloop()   # boucle principale : la fenêtre reste ouverte jusqu'à fermeture


 