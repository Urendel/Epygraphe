import datetime
from ..app import db

# Création de l'entité et de la table Comment qui représente les commentaires laissé par les utilisateurs
# sur la page de vu des inscriptions épigraphique.
# Ses différents champs se composent ainsi :
# Un id qui est la clé primaire et qui s'auto incrémente
# La date où a eu lieu le commentaire qui est entré automatiquement au moment du commentaire.
# Le texte du commentaire en lui même.
# Une clé étrangère qui renvoie à l'id de l'utilisateur ayant créé le commentaire.
# Une seconde clé étrangère qui renvoie à l'id de l'inscription sur laquelle il y a eu le commentaire.


class Comment(db.Model):
    comment_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    comment_inscription_id = db.Column(db.Integer, db.ForeignKey('inscription.inscription_id'))
    comment_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    comment_text = db.Column(db.Text)
    user = db.relationship("User", back_populates="comments", lazy='subquery')
    inscription = db.relationship("Inscription", back_populates="comments", lazy='subquery')

    @staticmethod
    def creer(iduser, idinscription, texte):
        """ Crée un commentaire par un utilisateur.

        :param iduser: id de l'utilisateur récupéré au moment de l'envoie du formulaire.
        :type iduser: int

        :param idinscription: id de l'inscription sur la page où le commentaire est envoyé, récupéré au moment de
        l'envoie du formulaire.
        :type iduser: int

        :param texte: le texte rentré par l'utilisateur.
        :type iduser: str

        :returns: True à l'envoie du message s'il n'y a pas eu d'erreurs et l'objet commentaire,
         False et un message d'erreur sinon
        :rtype: True and Comment or False and str

        """

        erreurs = []
        # On initialise la liste erreurs qui recueillera tous les éventuels texte d'erreur.

        # Ici comment les tests pour vérifier le format du commentaire posté par l'utilisateur.

        if not texte:
            erreurs.append("Vous ne pouvez faire un commentaire vide")
        # La première condition vérifie que le commentaire ne soit pas vide.

        if len(texte) < 3:
            erreurs.append("Commentaire beaucoup trop court, attention au spam")
        # Cette condition vérifie que le texte ne soit pas inférieur à 3 caractères.
        # (de nombreux commentaires sur internet se composent de 3 caractères)

        if len(texte) > 63206:
            erreurs.append("Commentaire beaucoup trop long, veuillez réduire votre commentaire s'il vous plait")
        # On vérifie que le texte ne soit pas non plus trop long, ici c'est une valeur un peu exagéré mais pourrait être
        # modifié à la convenance de l'administrateur du site.

        if len(erreurs) > 0:
            return False, erreurs
        # Si on a au moins une erreur on arrête le processus et on renvoie le ou les messages d'erreurs.


        commentaire = Comment(
            comment_inscription_id=idinscription,
            comment_user_id=iduser,
            comment_text=texte
        )
        # S'il n'y a pas eu d'erreur on créé un objet Comment que l'on entre dans la base

        try:
            db.session.add(commentaire)
            db.session.commit()

            return True, commentaire
        # On essaye de faire la connexion vers la base et créer la nouvelle entité
        except Exception as erreurs:
            return False, [str(erreurs)]
        # Si ça rate on envoie False et un message d'erreur

    def suppression_commentaire(self):
        """ Permet de supprimer l'objet Comment actuellement utilisé.

        :returns: Renvoie True et un message de réussite si ça réussit, sinon False et un message d'erreur
        :rtype: bool and str
        """

        try:
            db.session.delete(self)
            db.session.commit()

            return True, "success"
        except Exception as erreur:
            return False, [str(erreur)]
