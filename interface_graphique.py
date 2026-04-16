import random
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
import moteur_ia
import pandas as pd
import os

# COULEURS
FOND_GENERAL     = "#F5F5F5"   # gris très clair
FOND_BARRE       = "#FFFFFF"   # blanc
FOND_CONTENU     = "#FFFFFF"   # blanc
COULEUR_ACCENT   = "cornflowerblue" 
TEXTE_PRINCIPAL  = "#1a1a3e"   # bleu très foncé
TEXTE_SECONDAIRE = "#6B7280"   # gris
BORDURE          = "#E5E7EB"   # gris clair
SURVOL           = "#EEF2FF"   # bleu très pâle
CATEGORIE_ACTIVE = "#DBEAFE"   # bleu pâle
ROUGE_BOUTON     = "#4169E1"   # bleu roi pour les boutons principaux


#DONNÉES

CARACTERISTIQUES = {
    "Hair Color 💇":  ['Brown', 'Blond', 'Black', 'Gray'],
    "Hair Type ✂️":   ['Wavy', 'Straight', 'Receding Hairline', 'Bangs', 'Bald'],
    "Accessory 👒":   ['Earrings', 'Hat', 'Necklace', 'Lipstick', 'Necktie', 'Eyeglasses'],
    "Beard 🥸":       ['Mustache', 'Goatee', 'No Beard', 'Sideburns', "5 o'Clock Shadow"],
    "Sexe 🚻":        ['Male', 'Female'],
    "Mouth 👄":       ['Smiling', 'Mouth Slightly Open', 'Big Lips'],
    "Eyes 👁️":        ['Narrow Eyes', 'Bags Under Eyes', 'Bushy Eyebrows', 'Arched Eyebrows'],
    "Face 👤":        ['Oval Face', 'Pale Skin', 'Heavy Makeup', 'Rosy Cheeks',
                    'High Cheekbones', 'Double Chin', 'Chubby'],
    "Nose 👃":        ['Big Nose', 'Pointy Nose'],
    "Age 🕺🏼":         ['Young', 'Aged'],
    "Image 📷":       ['Blurry', 'Clear']
}

LISTE_REFERENCE = [
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

TRADUCTION = {
    "5 o'Clock Shadow": "5_o_Clock_Shadow", "Arched Eyebrows": "Arched_Eyebrows",
    "Bags Under Eyes": "Bags_Under_Eyes", "Bald": "Bald", "Bangs": "Bangs",
    "Big Lips": "Big_Lips", "Big Nose": "Big_Nose", "Black": "Black_Hair",
    "Blond": "Blond_Hair", "Blurry": "Blurry", "Brown": "Brown_Hair",
    "Bushy Eyebrows": "Bushy_Eyebrows", "Chubby": "Chubby", "Double Chin": "Double_Chin",
    "Eyeglasses": "Eyeglasses", "Goatee": "Goatee", "Gray": "Gray_Hair",
    "Heavy Makeup": "Heavy_Makeup", "High Cheekbones": "High_Cheekbones", "Male": "Male",
    "Mouth Slightly Open": "Mouth_Slightly_Open", "Mustache": "Mustache",
    "Narrow Eyes": "Narrow_Eyes", "No Beard": "No_Beard", "Oval Face": "Oval_Face",
    "Pale Skin": "Pale_Skin", "Pointy Nose": "Pointy_Nose",
    "Receding Hairline": "Receding_Hairline", "Rosy Cheeks": "Rosy_Cheeks",
    "Sideburns": "Sideburns", "Smiling": "Smiling", "Straight": "Straight_Hair",
    "Wavy": "Wavy_Hair", "Earrings": "Wearing_Earrings", "Hat": "Wearing_Hat",
    "Lipstick": "Wearing_Lipstick", "Necklace": "Wearing_Necklace",
    "Necktie": "Wearing_Necktie", "Young": "Young",
}

df = pd.read_csv("1000_attr.txt", sep=r"\s+")
def algo_genetique(caracteristiques: dict, n=6, parent_index=None, moteur=None):

    chemin_poids = "weight_ia.pth"
    chemin_vecteurs = "tous_les_vecteurs_attributs.pt"

    # Initialise le moteur une unique fois
    if moteur is None:
        moteur = moteur_ia.MoteurPortraitRobot(chemin_poids, chemin_vecteurs)

    # Crée un individu de base
    if parent_index is None:
        # nouveau visage
        image_base=select_image_base(caracteristiques, df)
        img_base, msg = moteur.creer_premier_individu(image_base)
    else:
        # ⚠️ ici parent_index doit être un mutant choisi
        moteur.definir_nouveau_suspect(parent_index)
        img_base = parent_index["image"]

    # Applique les critères
    moteur.appliquer_mutations_choisies(caracteristiques)

    # Génère les mutants
    mutants, messages = moteur.creer_individus_mutants(
        nb_mutants=n,
        force_bruit=0.05
    )

    # Retourne uniquement les images
    images = [m["image"] for m in mutants]

    return images, mutants

def select_image_base(dico:dict, df):
    if dico["Male"]==1:
        df_filtre = df[df["Male"] == 1]
        element = df_filtre.sample()
    else:
        df_filtre = df[df["Male"]==-1]
        element = df_filtre.sample()
    chemin = os.path.join("1000_image", element.index[0])
    return chemin


class PortraitRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portrait Robot")
        self.root.geometry("1100x700")
        self.photos          = []
        self.portrait_labels = []
        self.selected_index  = None
        self.cases_cochees = {cat: {opt: ctk.BooleanVar(value=False) for opt in opts} for cat, opts in CARACTERISTIQUES.items()}
        self.boutons_categorie = {}
        self.badges = {}
        self.categorie_active = None
        self.mode            = ctk.IntVar(value=1)
        self.nb_images       = ctk.StringVar(value="6")
        self.page0 = ctk.CTkFrame(root, fg_color="white")
        self.page1 = ctk.CTkFrame(root, fg_color=FOND_GENERAL)
        self.page2 = ctk.CTkFrame(root, fg_color=FOND_GENERAL)
        self.build_page0(self.page0)
        self.build_page1(self.page1)
        self.build_page2(self.page2)
        self.page0.pack(fill="both", expand=True)       
        self.choisir_categorie(list(CARACTERISTIQUES.keys())[0])
        self.dico = {}
        self.moteur = moteur_ia.MoteurPortraitRobot("weight_ia.pth","tous_les_vecteurs_attributs.pt")
        self.mutants = []
        
    # PAGE 0 : page d'accueil 

    def build_page0(self, parent):
        container = ctk.CTkFrame(parent, fg_color="white")
        container.pack(expand=True)     
        image = Image.open("photo.jpg")
        photo = CTkImage(light_image=image, size=(120, 120))

        # Afficher l'image
        ctk.CTkLabel(
            container,
            image=photo,
            text=""
        ).pack(pady=(40, 10))

        # Titre
        ctk.CTkLabel(
            container,
            text=" Portarait Robot  ",
            font=("Segoe UI", 40, "bold"),
            text_color=TEXTE_PRINCIPAL
        ).pack(pady=(80, 20))

        # Sous-titre
        ctk.CTkLabel(
            container,
            text="Séléctionnez les caractéristiques physiques souhaitées\n"
         " et générez plusieurs visages correspondant à vos critères.\n\n"
         "Vous pouvez choisir un portrait et le faire évoluer \n"
         "jusqu'à obtenir le visage recherché.",
            justify="center",

            font=("Segoe UI", 16),
            text_color=TEXTE_SECONDAIRE
        ).pack(pady=(0, 40))

        # Bouton commencer
        ctk.CTkButton(
            container,
            text="Commencer",
            font=("Segoe UI", 16, "bold"),
            fg_color=FOND_GENERAL,
            hover_color="#2952c4",
            text_color="palevioletred",
            height=50,
            width=200,
            command=self.go_to_page1
        ).pack(pady=10)



    #PAGE 1 : sélection des critères
    
    def build_page1(self, parent):
        top_header = ctk.CTkFrame(parent, fg_color=FOND_GENERAL, height=60, corner_radius=0)
        top_header.pack(fill="x", side="top")  
        ctk.CTkLabel(
            top_header, text="  🫆 Portraits Robot",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXTE_PRINCIPAL
        ).pack(side="left", padx=20, pady=15)        
        corps = ctk.CTkFrame(parent, fg_color=FOND_GENERAL, corner_radius=0)
        corps.pack(fill="both", expand=True)
        
        # Barre latérale gauche 
    
        barre_laterale_ext = ctk.CTkFrame(corps, fg_color=BORDURE, width=232, corner_radius=0)
        barre_laterale_ext.pack(side="left", fill="y")
        barre_laterale_ext.pack_propagate(False)
        
        barre_laterale = ctk.CTkFrame(barre_laterale_ext, fg_color=FOND_BARRE, width=230, corner_radius=0)
        barre_laterale.pack(side="left", fill="both", expand=True, padx=(0, 1))
        
        ctk.CTkLabel(
            barre_laterale, text="CATÉGORIES",
            font=("Segoe UI", 10, "bold"),
            text_color=TEXTE_SECONDAIRE
        ).pack(anchor="w", padx=20, pady=(18, 10))
        
        for cat in CARACTERISTIQUES:
            ligne = ctk.CTkFrame(barre_laterale, fg_color="transparent")
            ligne.pack(fill="x", padx=8, pady=2)
            
            btn = ctk.CTkButton(
                ligne,
                text=f"{cat}",
                font=("Segoe UI", 13),
                fg_color="transparent",
                text_color=TEXTE_PRINCIPAL,
                hover_color=SURVOL,
                anchor="w",
                command=lambda c=cat: self.choisir_categorie(c)
            )
            btn.pack(side="left", fill="x", expand=True)
            
            badge = ctk.CTkLabel(
                ligne, text="",
                font=("Segoe UI", 11, "bold"),
                text_color=COULEUR_ACCENT,
                width=24
            )
            badge.pack(side="right", padx=8)
            
            self.boutons_categorie[cat] = btn
            self.badges[cat] = badge

        # Zone droite
        zone_droite = ctk.CTkFrame(corps, fg_color=FOND_GENERAL, corner_radius=0)
        zone_droite.pack(side="left", fill="both", expand=True)
        
        # En-tête de la catégorie
        entete_cat = ctk.CTkFrame(zone_droite, fg_color=FOND_CONTENU, height=80, corner_radius=0)
        entete_cat.pack(fill="x")
        entete_cat.pack_propagate(False)
        
        self.titre_label = ctk.CTkLabel(
            entete_cat, text="",
            font=("Segoe UI", 20, "bold"),
            text_color=TEXTE_PRINCIPAL
        )
        self.titre_label.pack(side="left", padx=28, pady=(14, 2))
        
        self.sous_titre_label = ctk.CTkLabel(
            entete_cat, text="",
            font=("Segoe UI", 12),
            text_color=TEXTE_SECONDAIRE
        )
        self.sous_titre_label.pack(side="left", padx=(0, 20), pady=(20, 0))  
        ctk.CTkFrame(zone_droite, fg_color=BORDURE, height=1, corner_radius=0).pack(fill="x")    
        self.zone_options = ctk.CTkScrollableFrame(zone_droite, fg_color=FOND_GENERAL)
        self.zone_options.pack(fill="both", expand=True, padx=20, pady=10)        
        pied_de_page = ctk.CTkFrame(zone_droite, fg_color=FOND_CONTENU, height=70, corner_radius=0)
        pied_de_page.pack(fill="x", side="bottom")
        pied_de_page.pack_propagate(False)
        ctk.CTkFrame(pied_de_page, fg_color=BORDURE, height=1, corner_radius=0).pack(fill="x")    
        mode_frame = ctk.CTkFrame(pied_de_page, fg_color="transparent")
        mode_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkRadioButton(
            mode_frame, text="Plusieurs portraits", variable=self.mode, value=1,
            fg_color=COULEUR_ACCENT, text_color=TEXTE_PRINCIPAL, font=("Segoe UI", 12)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkRadioButton(
            mode_frame, text="Portrait unique", variable=self.mode, value=2,
            fg_color=COULEUR_ACCENT, text_color=TEXTE_PRINCIPAL, font=("Segoe UI", 12)
        ).pack(side="left", padx=(0, 15))
        
        ctk.CTkLabel(mode_frame, text="Images :", text_color=TEXTE_SECONDAIRE, font=("Segoe UI", 12)).pack(side="left", padx=(0, 5))
        
        ctk.CTkComboBox(
            mode_frame, values=[str(i) for i in range(1, 13)], variable=self.nb_images,
            width=70, fg_color=FOND_GENERAL, border_color=BORDURE, button_color=COULEUR_ACCENT,
            text_color=TEXTE_PRINCIPAL, font=("Segoe UI", 12)
        ).pack(side="left")
        
        ctk.CTkButton(
            pied_de_page, text="  ✔  Générer",
            command=self.go_to_page2,
            fg_color=FOND_GENERAL, hover_color="#2952c4", text_color="palevioletred",
            font=("Segoe UI", 14, "bold"), height=40, corner_radius=6
        ).pack(side="right", padx=20, pady=15)


    def choisir_categorie(self, cat):
        self.categorie_active = cat
        
        for nom, bouton in self.boutons_categorie.items():
            selectionne = (nom == cat)
            bouton.configure(
                fg_color=CATEGORIE_ACTIVE if selectionne else "transparent",
                font=("Segoe UI", 13, "bold") if selectionne else ("Segoe UI", 13)
            )
            
        self.afficher_categorie(cat)

    def afficher_categorie(self, cat):
        for widget in self.zone_options.winfo_children():
            widget.destroy()
            
        self.mettre_a_jour_badge(cat)
        
        for option in CARACTERISTIQUES[cat]:
            var = self.cases_cochees[cat][option]
            
            carte = ctk.CTkFrame(self.zone_options, fg_color=FOND_CONTENU, corner_radius=8, border_width=1, border_color=BORDURE)
            carte.pack(fill="x", pady=5, padx=10, ipady=4)
            
            case = ctk.CTkCheckBox(
                carte,
                text=f"  {option}",
                variable=var,
                font=("Segoe UI", 14),
                fg_color=COULEUR_ACCENT,
                text_color=TEXTE_PRINCIPAL,
                hover_color="#2952c4",
                command=lambda c=cat: self.mettre_a_jour_badge(c)
            )
            case.pack(fill="x", padx=16, pady=10)

    def mettre_a_jour_badge(self, cat):
        coches = [opt for opt, var in self.cases_cochees[cat].items() if var.get()]
        
        self.badges[cat].configure(text=str(len(coches)) if coches else "")
        
        if self.categorie_active == cat:
            self.titre_label.configure(text=f"{cat}")
            self.sous_titre_label.configure(text=", ".join(coches) if coches else "Aucune sélection")

    # PAGE 2 : affichage des portraits 
        
    def build_page2(self, parent):
        top_bar = ctk.CTkFrame(parent, fg_color=FOND_CONTENU, height=60, corner_radius=0)
        top_bar.pack(fill="x", side="top")
        ctk.CTkFrame(parent, fg_color=BORDURE, height=1, corner_radius=0).pack(fill="x")

        ctk.CTkButton(
            top_bar, text="← Retour", command=self.go_to_page1, fg_color=FOND_GENERAL,
            hover_color=SURVOL, text_color=TEXTE_PRINCIPAL, font=("Segoe UI", 12),
            width=100, border_width=1, border_color=BORDURE
        ).pack(side="left", padx=20, pady=12)

        self.info_label = ctk.CTkLabel(
            top_bar, text="Cliquez sur un portrait pour le sélectionner",
            text_color=TEXTE_SECONDAIRE, font=("Segoe UI", 12)
        )
        self.info_label.pack(side="left", expand=True, pady=12)

        self.evolve_button = ctk.CTkButton(
            top_bar, text="Évoluer le portrait", command=lambda: self.run(evolve=True),
            fg_color=COULEUR_ACCENT, hover_color="#2952c4", text_color="white",
            font=("Segoe UI", 12, "bold"), state="disabled"
        )
        self.evolve_button.pack(side="right", padx=8, pady=12)

        self.change_criteria_button = ctk.CTkButton(
            top_bar, text="Changer un critère", command=self.change_criteria,
            fg_color=FOND_GENERAL, hover_color=SURVOL, text_color=TEXTE_PRINCIPAL,
            font=("Segoe UI", 12), border_width=1, border_color=BORDURE, state="disabled"
        )
        self.change_criteria_button.pack(side="right", padx=4, pady=12)

        self.grid = ctk.CTkFrame(parent, fg_color=FOND_GENERAL)
        self.grid.pack(fill="both", expand=True, padx=20, pady=20)
 
    def go_to_page2(self):
        self.page1.pack_forget()
        self.page2.pack(fill="both", expand=True)
        self.run(evolve=self.selected_index is not None)

    def go_to_page1(self):
        self.selected_index = None
        self.evolve_button.configure(state="disabled")
        self.change_criteria_button.configure(state="disabled")
        self.page0.pack_forget()
        self.page2.pack_forget()
        self.page1.pack(fill="both", expand=True)

    def change_criteria(self):
        self.info_label.configure(text="Modifiez vos critères puis cliquez sur Générer.", text_color=COULEUR_ACCENT)
        self.page2.pack_forget()
        self.page1.pack(fill="both", expand=True)

    def build_grid(self, n):
        self.portrait_labels.clear()
        for w in self.grid.winfo_children():
            w.destroy()

        cols = 3
        rows = (n + cols - 1) // cols
        for i in range(n):
            f = ctk.CTkFrame(self.grid, fg_color=FOND_CONTENU, corner_radius=10, border_width=1, border_color=BORDURE, cursor="hand2")
            f.grid(row=i // cols, column=i % cols, padx=10, pady=10, sticky="nsew")

            lbl = ctk.CTkLabel(f, text="", fg_color=FOND_CONTENU)
            lbl.pack(expand=True, pady=8)

            for widget in (f, lbl):
                widget.bind("<Button-1>", lambda e, idx=i: self.select(idx))

            self.portrait_labels.append(lbl)
            self.grid.columnconfigure(i % cols, weight=1)

        for r in range(rows):
            self.grid.rowconfigure(r, weight=1)

    # Génération 
    
    def run(self, evolve=False):
        if evolve and self.selected_index is None:
            return
        choix = []
        for cat, opts in self.cases_cochees.items():
            for opt, var in opts.items():
                if var.get():
                    choix.append(opt)
                    
        coches = [TRADUCTION[opt] for opt in choix if opt in TRADUCTION]

        criteres = {cle: (1 if cle in coches else 0) for cle in LISTE_REFERENCE}
        if "Female" in choix: criteres["Male"]   = -1
        if "Aged"   in choix: criteres["Young"]  = -1
        if "Clear"  in choix: criteres["Blurry"] = -1

        n = int(self.nb_images.get()) if self.mode.get() == 1 else 1

        self.evolve_button.configure(state="disabled")
        self.change_criteria_button.configure(state="disabled")
        self.info_label.configure(text="Cliquez sur un portrait pour le sélectionner", text_color=TEXTE_SECONDAIRE)

        images, self.mutants = algo_genetique(criteres,n,parent_index=self.mutants[self.selected_index] if evolve else None,moteur=self.moteur)

        if self.mode.get() == 1:
            self.build_grid(n)
            self.photos.clear()
            self.selected_index = None
            for lbl, img in zip(self.portrait_labels, images):
                photo = CTkImage(light_image=img, size=(200, 240))
                lbl.configure(image=photo)
                lbl.image = photo
                self.photos.append(photo)
            if evolve:
                self.info_label.configure(text="Génération terminée ! Cliquez sur un nouveau portrait.", text_color=TEXTE_PRINCIPAL)
        else:
            for w in self.grid.winfo_children():
                w.destroy()
            photo = CTkImage(light_image=images[0], size=(300, 360))
            lbl = ctk.CTkLabel(self.grid, text="", image=photo, fg_color=FOND_GENERAL)
            lbl.image = photo
            lbl.pack(expand=True)
            self.photos.clear()
            self.photos.append(photo)
            self.selected_index = 0
            self.info_label.configure(text="Portrait généré. Vous pouvez l'évoluer.", text_color=TEXTE_PRINCIPAL)
            self.evolve_button.configure(state="normal")
            self.change_criteria_button.configure(state="normal")

    # Séléction d'un portrait
    
    def select(self, idx):
        self.selected_index = idx
        for i, lbl in enumerate(self.portrait_labels):
            couleur_bordure = COULEUR_ACCENT if i == idx else BORDURE
            couleur_fond    = CATEGORIE_ACTIVE if i == idx else FOND_CONTENU
            lbl.master.configure(border_color=couleur_bordure, fg_color=couleur_fond)
            lbl.configure(fg_color=couleur_fond)

        self.info_label.configure(
            text=f"Portrait {idx + 1} sélectionné — cliquez sur \"Évoluer\" pour de nouvelles variantes.",
            text_color=TEXTE_PRINCIPAL
        )
        self.evolve_button.configure(state="normal")
        self.change_criteria_button.configure(state="normal")

if __name__ == "__main__":
    ctk.set_appearance_mode("light")   
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    PortraitRobotApp(root)
    root.mainloop()
