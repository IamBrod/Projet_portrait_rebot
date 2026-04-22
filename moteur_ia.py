import torch
import os
import random
import urllib.request
from torchvision.utils import save_image
import torchvision.transforms as transforms
from PIL import Image
from architecture_ia import ImprovedConvVAE 


class MoteurPortraitRobot:
    def __init__(self, chemin_poids, chemin_vecteurs, latent_dim=1024, device="cuda"):
        """Initialise le moteur et télécharge les poids si nécessaire."""
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.latent_dim = latent_dim
        
        # 1. Le lien direct le fichier des poids sur github
        url_directe_poids = "https://github.com/IamBrod/Projet_portrait_rebot/releases/download/file/weight_ia.pth"
        
        # 2. Le moteur vérifie lui-même s'il a besoin de se télécharger
        self._telecharger_poids_si_besoin(chemin_poids, url_directe_poids)
        
        # 3. Chargement du modèle en RAM (le fichier existe forcément à ce stade)
        print("[MOTEUR] Démarrage du réseau de neurones...")
        self.model = ImprovedConvVAE(latent_dim=self.latent_dim).to(self.device)
        self.model.load_state_dict(torch.load(chemin_poids, map_location=self.device))
        self.model.eval()
        
        # 4. Chargement des vecteurs d'attributs
        self.vecteurs = torch.load(chemin_vecteurs, map_location=self.device)
        self.noms_attributs = list(self.vecteurs.keys())
        
        # ... (le reste du __init__ avec self.transform_in, etc.) ...
        self.transform_in = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.CenterCrop(128),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.transform_out = transforms.ToPILImage()
        self.z_actuel = None 
        self.etat_attributs = {}
        print("[MOTEUR] Prêt à recevoir les commandes de l'interface !")

    def _telecharger_poids_si_besoin(self, chemin_local, url_telechargement):
        """Méthode interne (privée) au moteur pour s'auto-installer."""
        if not os.path.exists(chemin_local):
            print(f"\n[INSTALLATION] Le fichier {chemin_local} est introuvable.")
            print("[INSTALLATION] Téléchargement en cours (environ 376 Mo), veuillez patienter...")
            
            # S'assurer que le dossier cible existe, sinon le créer
            dossier = os.path.dirname(chemin_local)
            if dossier:  # Évite une erreur si le fichier est à la racine
                os.makedirs(dossier, exist_ok=True)
            
            # Téléchargement silencieux
            urllib.request.urlretrieve(url_telechargement, chemin_local)
            print("[INSTALLATION] Téléchargement terminé avec succès !\n")
        else:
            print("[SYSTÈME] Fichier de poids détecté.")

    def _tensor_to_pil(self, tensor):
        """Utilitaire interne pour convertir le tenseur PyTorch en image pour l'interface"""
        img_denormalized = (tensor.squeeze(0) + 1) / 2
        return self.transform_out(img_denormalized.cpu())

    # ==========================================
    # FONCTION 1 : CRÉER LE SUSPECT DE DÉPART
    # ==========================================
    def creer_premier_individu(self, chemin_image=None):
        """
        Appelé par le bouton 'Nouveau Suspect'.
        Si un chemin est fourni, encode l'image. Sinon, génère un visage aléatoire pur.
        """
        self.etat_attributs = {attr: 0.0 for attr in self.noms_attributs}
        with torch.no_grad():
            if chemin_image:
                img = Image.open(chemin_image).convert('RGB')
                img_tensor = self.transform_in(img).unsqueeze(0).to(self.device)
                self.z_actuel, _ = self.model.encode(img_tensor)
                message = f"Suspect initialisé à partir de l'image : {chemin_image}"
            else:
                self.z_actuel = torch.randn(1, self.latent_dim, device=self.device)
                message = "Nouveau suspect généré totalement au hasard."
                
            img_generee = self.model.decode(self.z_actuel)
        
        return self._tensor_to_pil(img_generee), message

    # ==========================================
    # FONCTION 2 : L'ÉVOLUTION (MUTANTS)
    # ==========================================
    def creer_individus_mutants(self, nb_mutants=8, force_bruit=0.05):
        if self.z_actuel is None:
            return None, "Erreur : Créez d'abord un individu de départ."
          
        resultats = []
        messages = []
        limite_max = 2.5
        
        with torch.no_grad():
            for i in range(nb_mutants):
                z_mutant = self.z_actuel.clone()
                etat_mutant = self.etat_attributs.copy() # On copie le registre actuel
                recette = []
                
                # 1. Attributs aléatoires
                nb_modifs = random.randint(0, 2)
                #nb_modifs = 0
                attributs_choisis = random.sample(self.noms_attributs, nb_modifs)
                
                for attr in attributs_choisis:
                    # On tire une force aléatoire à ajouter
                    force_voulue = random.uniform(0.8, 2.5) * random.choice([-1.0, 1.0])
                    
                    # On calcule le total théorique si on l'ajoutait
                    total_theorique = etat_mutant[attr] + force_voulue
                    
                    # On plafonne ce total strictement entre -3.0 et +3.0
                    total_bloque = max(-limite_max, min(limite_max, total_theorique))
                    
                    # On calcule LA VRAIE force qu'on a le droit d'appliquer (le delta)
                    force_autorisee = total_bloque - etat_mutant[attr]
                    
                    # On met à jour le registre et le vecteur
                    etat_mutant[attr] = total_bloque
                    
                    if force_autorisee != 0.0:
                        z_mutant += force_autorisee * self.vecteurs[attr].to(self.device)
                        recette.append(f"{attr} ({force_autorisee:+.1f} -> Total: {total_bloque:+.1f})")
                    
                if random.random()>0.6:
                    # 2. Bruit pur aléatoire
                    z_mutant += torch.randn(1, self.latent_dim, device=self.device) * force_bruit
                
                # Décodage
                img_mutant = self.model.decode(z_mutant)
                
                # On sauvegarde temporairement ce mutant (ET SON REGISTRE)
                resultats.append({
                    "image": self._tensor_to_pil(img_mutant),
                    "z_vector": z_mutant,
                    "etat_attributs": etat_mutant  # <--- TRÈS IMPORTANT
                })
                
                # Si aucune modif n'a pu être faite (tout était déjà au max), on l'indique
                if not recette:
                    recette = ["Plafond atteint (que du bruit)"]
                    
                messages.append(f"Mutant {i+1}: " + ", ".join(recette))
                
        return resultats, messages

    # ==========================================
    # FONCTION 3 :
    # ==========================================
    def appliquer_mutations_choisies(self, dictionnaire_curseurs):
        """
        Appelé quand l'utilisateur bouge les curseurs dans l'interface.
        dictionnaire_curseurs = {"Smiling": 1.5, "Eyeglasses": 2.0}
        """
        
        if self.z_actuel is None:
            return None, "Erreur : Aucun individu en cours."

        with torch.no_grad():
            z_modifie = self.z_actuel.clone()
            modifs_faites = []
            
            for attribut, force in dictionnaire_curseurs.items():
                if force != 0.0 and attribut in self.vecteurs:
                    z_modifie += force * self.vecteurs[attribut].to(self.device)
                    modifs_faites.append(f"{attribut}({force})")
            
            img_resultat = self.model.decode(z_modifie)
            
            # On met à jour l'état actuel avec ces modifications validées
            self.z_actuel = z_modifie
            
            message = "Mutations appliquées : " + ", ".join(modifs_faites)
            
        return self._tensor_to_pil(img_resultat), message

    
    # ==========================================
    # FONCTION 4 : LA FUSION DE DEUX SUSPECTS (MORPHING)
    # ==========================================
    def fusionner_visages(self, z1, z2, nb_etapes=5):
        """
        Appelé pour créer un morphing fluide entre le suspect 1 et le suspect 2.
        z1 et z2 sont les tenseurs latents des deux visages.
        Renvoie une liste d'images (PIL) allant du visage 1 au visage 2.
        """
        if z1 is None or z2 is None:
            return None, "Erreur : Il faut deux visages encodés pour faire une fusion."

        images_fusion = []
        
        with torch.no_grad():
            # Crée une liste de pourcentages (alphas) allant de 0.0 à 1.0
            # Ex avec 5 étapes : [0.0, 0.25, 0.50, 0.75, 1.0]
            alphas = torch.linspace(0, 1, steps=nb_etapes).to(self.device)
            
            for alpha in alphas:
                # Mathématique du Morphing : (1 - %)*A + %*B
                z_etape = (1 - alpha) * z1 + alpha * z2
                
                # On décode cette étape intermédiaire
                img_etape = self.model.decode(z_etape)
                
                # On convertit en image pour l'interface
                images_fusion.append(self._tensor_to_pil(img_etape))
                
        message = f"Gamme de fusion générée avec succès en {nb_etapes} étapes."
        return images_fusion, message
    
    # ==========================================
    # FONCTION 5 : LA FUSION PARTIELLE (MORPHING CONTRÔLÉ)
    # ==========================================
    def fusionner_visages_partiel(self, z1, z2, pourcentage_morphing=0.5, nb_etapes=5):
        """
        Morphing stable : Garde une partie de z1 intacte, et ne fait le morphing
        que sur le reste des dimensions vers z2.
        pourcentage_morphing = 0.5 (morph la moitié du vecteur)
        """
        if z1 is None or z2 is None:
            return None, "Erreur : Il faut deux visages encodés."

        images_fusion = []
        point_coupure = int(self.latent_dim * pourcentage_morphing)

        with torch.no_grad():
            alphas = torch.linspace(0, 1, steps=nb_etapes).to(self.device)
            
            for alpha in alphas:
                # On clone z1 pour avoir notre "ancre de stabilité"
                z_etape = z1.clone()
                
                # On applique le morphing UNIQUEMENT sur la première partie du vecteur
                z_morph = (1 - alpha) * z1[:, :point_coupure] + alpha * z2[:, :point_coupure]
                
                # On remplace le début de z_etape par ce calcul fluide
                z_etape[:, :point_coupure] = z_morph
                
                # On décode et on sauvegarde l'image
                img_etape = self.model.decode(z_etape)
                images_fusion.append(self._tensor_to_pil(img_etape))
                
        return images_fusion, f"Fusion partielle ({pourcentage_morphing*100}%) générée."
    
    # ==========================================
    # FONCTION UTILITAIRE : SÉLECTIONNER UN MUTANT
    # ==========================================
    def definir_nouveau_suspect(self, mutant_choisi):
        """Appelé quand l'utilisateur clique sur un des mutants générés pour le valider."""
        self.z_actuel = mutant_choisi["z_vector"]
        self.etat_attributs = mutant_choisi["etat_attributs"]
        return "Nouveau suspect validé comme base."
    

# ==========================================
# TEST
# ==========================================
if __name__ == "__main__":
    from torchvision.utils import save_image
    import torchvision.transforms as transforms
    
    print("=== DÉMARRAGE DU CRASH TEST ===")
    
    # 1. Initialisation (Vérifiez les noms de vos fichiers !)
    chemin_poids = "weight_ia.pth"
    chemin_vecteurs = "tous_les_vecteurs_attributs.pt"
    image_source = "045097.jpg"

    moteur = MoteurPortraitRobot(chemin_poids, chemin_vecteurs)
    to_tensor = transforms.ToTensor() # Utilitaire pour refaire des grilles
    
    # ---------------------------------------------------------
    # TEST 1 : Création aléatoire
    print("\n--- TEST 1 : Création du suspect initial ---")
    img_base, msg = moteur.creer_premier_individu(image_source) # Sans image = Aléatoire
    print(msg)
    img_base.save("test1_suspect_base.png")
    
    # On sauvegarde ce premier ADN pour les tests de fusion plus tard
    z_visage_A = moteur.z_actuel.clone()
    
    # ---------------------------------------------------------
    # TEST 2 : Mutations
    print("\n--- TEST 2 : Génération de 4 mutants ---")
    mutants, messages = moteur.creer_individus_mutants(nb_mutants=6, force_bruit=0.5)
    for m in messages:
        print(" ->", m)
        
    # On crée une frise : [Original] + [Les 4 mutants]
    images_grille = [to_tensor(img_base)] + [to_tensor(m["image"]) for m in mutants]
    save_image(torch.stack(images_grille), "test2_mutants.png", nrow=5)
    
    # ---------------------------------------------------------
    # TEST 3 : Le Tableau de bord manuel
    print("\n--- TEST 3 : Curseur manuel (Sourire et Lunettes) ---")
    img_modifiee, msg = moteur.appliquer_mutations_choisies({
        "Smiling": 2.0, 
        "Eyeglasses": 1.5,
        "Young": -1.0
    })
    print(msg)
    
    # On sauvegarde l'avant/après
    save_image(torch.stack([to_tensor(img_base), to_tensor(img_modifiee)]), "test3_avant_apres.png", nrow=2)

    
    image_suspect_2 = "045098.jpg"
    img_B, msg_B = moteur.creer_premier_individu(image_suspect_2)
    print(msg_B)
    img_B.save("test3_visage_B.png")
    z_visage_B = moteur.z_actuel.clone()
    
    
    # ---------------------------------------------------------
    # TEST 4 : Morphing Total
    print("\n--- TEST 4 : Morphing Total (A vers B) ---")
    gamme_total, msg = moteur.fusionner_visages(z_visage_A, z_visage_B, nb_etapes=15)
    print(msg)
    save_image(torch.stack([to_tensor(img) for img in gamme_total]), "test4_morphing_total.png", nrow=6)

    # ---------------------------------------------------------
    # TEST 5 : Morphing Partiel (Style Mixing)
    print("\n--- TEST 5 : Morphing Partiel (A vers B à 50%) ---")
    gamme_partielle, msg = moteur.fusionner_visages_partiel(z_visage_A, z_visage_B, pourcentage_morphing=0.5, nb_etapes=6)
    print(msg)
    save_image(torch.stack([to_tensor(img) for img in gamme_partielle]), "test5_morphing_partiel.png", nrow=6)
    
    print("\n=== TESTS TERMINÉS AVEC SUCCÈS ! ===")
    print("Vérifiez votre dossier, 5 nouvelles images 'test_...' ont été créées.")

    # ---------------------------------------------------------
    # TEST 6 : Évolution Génétique (10 Générations)
    print("\n--- TEST 6 : Évolution Génétique sur 10 générations ---")
    
    # On repart du Visage A original pour l'expérience
    img_actuelle, msg = moteur.creer_premier_individu(image_source)
    
    # On stocke l'historique des visages choisis (la Génération 0 est l'original)
    historique_evolution = [to_tensor(img_actuelle)]
    
    nb_generations = 20
    for gen in range(1, nb_generations + 1):
        # 1. Le moteur génère 4 mutants autour du visage actuel
        mutants, messages = moteur.creer_individus_mutants(nb_mutants=4, force_bruit=0.0)
        
        # 2. Simulation de l'utilisateur : on choisit un mutant au hasard (entre 0 et 3)
        import random
        choix = random.randint(0, 3)
        mutant_choisi = mutants[choix]
        
        # 3. L'interface dit au moteur : "C'est lui la nouvelle base !"
        moteur.definir_nouveau_suspect(mutant_choisi)
        
        # 4. On l'ajoute à notre album photo chronologique
        historique_evolution.append(to_tensor(mutant_choisi["image"]))
        print(f"Génération {gen} : Choix du mutant n°{choix+1} -> Nouvelle base adoptée.")

    # 5. On sauvegarde la frise géante (11 images de gauche à droite)
    save_image(torch.stack(historique_evolution), "test6_evolution_10_generations.png", nrow=nb_generations + 1)
    print("Frise de l'évolution sauvegardée ! Regardez 'test6_evolution_10_generations.png'.")
    

