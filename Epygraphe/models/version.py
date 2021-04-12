from .. app import db

# Création de l'entité et de la table Version qui représente les traductions faites par
# les utilisateurs en fonction d'une inscription.
# Ses différents champs se composent ainsi :
# Un id qui est la clé primaire et qui s'auto incrémente
# Le texte de la traduction.
# Une clé étrangère qui représente l'id de l'inscription sur laquelle porte la traduction.
# Une clé étrangère qui représente l'id de l'utilisateur qui a créé la traduction.


class Version(db.Model):
    version_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    version_text = db.Column(db.Text)
    version_inscription_id = db.Column(db.Integer, db.ForeignKey('inscription.inscription_id'))
    version_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", back_populates="versions")
    inscription = db.relationship("Inscription", back_populates="versions")

    @staticmethod
    def creer(iduser, idinscription, texte):
        """ Crée une version par un utilisateur

        :param iduser: id de l'utilisateur récupéré au moment de l'envoie du formulaire
        :type iduser: int

        :param idinscription: id de l'inscription sur la page d'où la version est envoyée, récupéré au moment du click
        :type iduser: int

        :param texte: le texte rentré par l'utilisateur
        :type iduser: str

        :returns: True à l'envoie du message s'il n'y a pas eu d'erreurs, False et un message d'erreur sinon
        :rtype: True and Version or False and str

        """
        erreurs = []

        if not texte:
            erreurs.append("Vous ne pouvez pas proposer une traduction vide")
        # Vérifie si le texte récupéré n'est pas vide.

        if len(erreurs) > 0:
            return False, erreurs
        # Si on a au moins une erreur on arrête le processus et on renvoie le ou les messages d'erreurs.

        version = Version(
            version_inscription_id=idinscription,
            version_user_id=iduser,
            version_text=texte
        )
        # S'il n'y a pas eu d'erreur on créé un objet Comment que l'on entre dans la base

        try:
            db.session.add(version)
            db.session.commit()

            return True, version
        except Exception as erreurs:
            return False, [str(erreurs)]

    def suppression_version(self):
        """ Permet de supprimer l'objet Version actuellement utilisé.

        :returns: Renvoie True si réussit, sinon False et un message d'erreur
        :rtype:  bool and str
        """

        try:
            db.session.delete(self)
            db.session.commit()
            return True, "success"

        except Exception as erreur:
            return False, [str(erreur)]
