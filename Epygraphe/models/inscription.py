import requests
from .. app import db

# Création de l'entité et de la table Inscription qui représente des inscriptions épigraphiques.
# Ses différents champs se composent ainsi :
# Un id qui est la clé primaire et qui s'auto incrémente
# Le texte de l'inscription en elle-même.
# Le lieu de découverte de l'inscription au format moderne du lieu.
# Le numéro de la base Heidelberg de l'inscription.
# La langue dans laquelle l'inscription a été tracée.
# Le type de l'inscription en anglais (Décret honorifique, loi, texte diplomatique, etc)
# La date supposée ou avérée de l'inscription.

class Inscription(db.Model):
    inscription_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    inscription_texte = db.Column(db.Text)
    inscription_lieu = db.Column(db.String(45))
    inscription_no_hd = db.Column(db.String(6))
    inscription_language = db.Column(db.String(45))
    inscription_type = db.Column(db.String(45))
    inscription_date = db.Column(db.String(45))
    comments = db.relationship("Comment", back_populates="inscription")
    versions = db.relationship("Version", back_populates="inscription")

    @staticmethod
    def creer(numero_hd):
        """ Crée une inscription en fonction des numéro de l'inscription de la base Heildeberg renseignée,
        ce numéro se compose comme suit : les deux lettres HD + 6 chiffres et permet d'allé chercher directement
        un fichier json qui permettra de créer l'entité.

        :param numero_hd: suite de 6 chiffres donnés par l'administrateur
        :type numero_hd: str

        :returns: True et une Inscription s'il n'y a pas eu d'erreurs, False et un message d'erreur sinon
        :rtype: True and Inscription or False and str

        """
        erreurs = []
        # On initialise la liste erreurs qui recueillera tous les éventuels texte d'erreur.

        if not numero_hd:
            erreurs.append("Veuillez renseigner un numéro Heildeberg")
        # Vérifie le format du numéro du le base Heildeberg, d'abord si ce qui a été renseigné n'est pas vide.

        elif len((numero_hd)) < 6:
            erreurs.append("Numéro trop court, le numéro doit se composer de 6 chiffres")
        # Puis si le numéro est bien composé de 6 chiffres.

        elif len((numero_hd)) > 6:
            erreurs.append("Numéro trop long, le numéro doit se composer de 6 chiffres")
        # S'il n'a pas plus de 6 chiffres

        if not numero_hd.isdigit():
          erreurs.append("Le numéro ne doit contenir que des chiffres")
        # et qu'il soit effectivement composé que de chiffres.

        double = Inscription.query.filter(Inscription.inscription_no_hd == "HD"+numero_hd).count()
        # Compte combien de cette adresse JSON a déjà été renseignées.


        if double > 0:
            erreurs.append("L'inscription est déjà présente en base")
        # S'ils sont déjà présent alors on ajoute un message d'erreur à la liste de nos erreurs


        if len(erreurs) > 0:
            return False, erreurs
        # Si on a au moins une erreur on arrête le processus et on renvoie le ou les messages d'erreurs.



        requete = requests.get("https://edh-www.adw.uni-heidelberg.de/edh/inschrift/HD"+str(numero_hd)+".json")
        donnees = requete.json()
        # On envoie une requête GET pour aller chercher notre JSON sur l'Epigraphic Database Heildeberg

        for item in donnees["items"]:
            texte = item["transcription"]
            lieu = item["findspot_modern"]
            langue = item["language"]
            nohd = item["id"]
            sujet = item["type_of_inscription"]
            date = ""
            # On parse ensuite les données Json pour ne récupérer que ce qui nous intéresse

            clef_de = "not_before"
            clef_a = "not_after"
            # Vérification de l'existence de la clef "not_before" dans le dictionnaire,
            # car il arrive que dans certains JSON elle n'y soit pas.

            if clef_de in item:
                de = str(item[clef_de])
                # Si elle existe, transformation de la valeur en String pour pouvoir la traiter ensuite

                if len(de) == 4:
                    if de.startswith("000"):
                        date += "De " + de[-1:] + " ap. J.-C. à "
                    elif de.startswith("00"):
                        date += "De " + de[-2:] + " ap. J.-C. à "
                    elif de.startswith("0"):
                        date += "De " + de[-3:] + " ap. J.-C. à "
                    else:
                        date += "De " + de + " ap. J.-C. à "
                    # On vérifie la longueur du String s'il est de 4 c'est qu'il est de la forme AAAA donc Ap. J.-C.
                    # s'il est de 5 c'est qu'il est de la forme -AAAA donc Av. J.-C.

                else:
                    if de.startswith("-000"):
                        date += "De " + de[-1:] + " av. J.-C. à "
                    elif de.startswith("-00"):
                        date += "De " + de[-2:] + " av. J.-C. à "
                    elif de.startswith("-0"):
                        date += "De " + de[-3:] + " av. J.-C. à "
                    else:
                        date += "De " + de[-4:] + " av. J.-C. à "
                # Ici on vérifie si l'année est négative auquel cas on récupère juste les décennies qui nous intéressent
                # pour pouvoir créer notre chaine.


            elif clef_de in item:
                a = str(item[clef_a])
                # Si elle n'y est pas ça veut dire que la clef "not_after" est la date précise à l'année près
                # ou alors on peut procéder à la concaténation
                # mais là aussi on vérifie la présence de "not_after" car il arrive que ce n'est pas renseigné

                if len(a) == 4:
                    if a.startswith("000"):
                        date += a[-1:] + " ap. J.-C."
                    elif a.startswith("00"):
                        date += a[-2:] + " ap. J.-C."
                    elif a.startswith("0"):
                        date += a[-3:] + " ap. J.-C."
                    else:
                        date += a + " ap. J.-C."
                    # On vérifie la longueur du String s'il est de 4 c'est qu'il est de la forme AAAA donc Ap. J.-C.
                    # s'il est de 5 c'est qu'il est de la forme -AAAA donc Av. J.-C.

                else:
                    if a.startswith("-000"):
                        date += a[-1:] + " av. J.-C."
                    elif a.startswith("-00"):
                        date += a[-2:] + " av. J.-C."
                    elif a.startswith("-0"):
                        date += a[-3:] + " av. J.-C."
                    else:
                        date += a[-4:] + " av. J.-C."

            else:
                date += "Inconnue"
            # S'il n'y a aucun des deux on estime que la date est Inconnue.


        inscription = Inscription(
            inscription_texte=texte,
            inscription_lieu=lieu,
            inscription_language=langue,
            inscription_no_hd=nohd,
            inscription_type=sujet,
            inscription_date=date
        )
        # S'il n'y a pas eu d'erreur on créé un objet Inscription que l'on entre dans la base
        try:
            db.session.add(inscription)
            db.session.commit()

            return True, inscription

        except Exception as erreurs:
            return False, [str(erreurs)]

    def suppression_inscription(self):
        """ Permet de supprimer l'objet Inscription actuellement utilisé.

        :returns: Renvoie True et un message de réussite si réussit, sinon False et un message d'erreur
        :rtype: bool and str
        """

        try:
            db.session.delete(self)
            db.session.commit()

            return True, "success"
        except Exception as erreur:
            return False, [str(erreur)]
