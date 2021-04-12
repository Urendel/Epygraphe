import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .. app import db, login

# Création de l'entité et de la table User qui représente les utilisateurs inscrits sur le site.
# Ses différents champs se composent ainsi :
# Un id qui est la clé primaire et qui s'auto incrémente
# Le prénom de la personne.
# Le nom de la personne.
# Son login.
# Son email.
# Son mot de passe crypté
# Si l'utilisateur est administrateur
# Si l'utilisateur est modérateur.
# Quand l'utilisateur s'est connecté pour la dernière fois.

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_prenom = db.Column(db.Text, nullable=False)
    user_nom = db.Column(db.Text, nullable=False)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(45), nullable=False)
    user_is_admin = db.Column(db.Boolean, default=False)
    user_is_mod = db.Column(db.Boolean, default=False)
    user_last_seen = db.Column(db.DateTime)
    comments = db.relationship("Comment", back_populates="user")
    versions = db.relationship("Version", back_populates="user")


    @staticmethod
    def connexion(login, password):
        """ Connecte un utilisateur, si fonctionne renvoie l'utilisateur en fonction du login et password renseigné

        :param login: Login entré par l'utilisateur
        :param password: Mot de passe entré par l'utilisateur
        :returns: Si réussite, renvoit le User propre au login/mot de passe renseignés. Sinon None
        :rtype: User or None
        """


        utilisateur = User.query.filter(User.user_login == login).first()
        # Cherche le premier utilisateur qui a l'entrée login qui ressemble à login, login étant unique il ne doit en
        # remonter qu'un seul

        if utilisateur and check_password_hash(utilisateur.user_password, password):
            utilisateur.user_last_seen = datetime.datetime.now()
            print(utilisateur.user_last_seen)
            db.session.add(utilisateur)
            db.session.commit()

            return utilisateur
            
        return None
        # Si le password renseigné par l'utilisateur correspond à la base, renvoie cet objet User. Sinon ne renvoie
        # rien.
        # Avant de renvoyer l'utilisateur on ajoute en base la date de sa dernière connexion.

    @staticmethod
    def creer(login, email, nom, prenom, password, isadmin = False, ismod = False):
        """ Création d'un compte utilisateur en fonction des informations renseignées par un formulaire.
       Renvoie True et du User s'il n'y a pas eu de problèmes, False et un message d'erreur sinon.

        :param login: Login de l'utilisateur
        :type login: str
        :param email: Email de l'utilisateur
        :type email: str
        :param nom: Nom de l'utilisateur
        :type nom: str
        :param prenom: Prénom de l'utilisateur
        :type prenom: str
        :param isadmin: Niveau de droit administrateur de l'utilisateur, par défaut False.
        :type isadmin: bool
        :param ismod: Niveau de droit de modération de l'utilisateur, par défaut False.
        :type ismod: bool
        :param password: Mot de passe de l'utilisateur sur 6 caractères minimum.

        :returns: True et les données utilisateur s'il n'y a pas eu d'erreurs, False et un message d'erreur sinon
        :rtype: True and User or False and str

        """
        erreurs = []
        if not login:
            erreurs.append("Login ne peut être vide")
        if not email:
            erreurs.append("E-mail ne peut être vide")
        if not nom:
            erreurs.append("Nom ne peut être vide")
        if not prenom:
            erreurs.append("Prénom ne peut être vide")
        if not password:
            erreurs.append("Mot de passe ne peut être vide")
        if len(password) < 6:
            erreurs.append("Le mot de passe ne contient pas 6 caractères")


        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        # Compte combien de login ou d'email égaux à ceux renseignés sont présents dans la base


        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")
        # S'ils sont déjà présent alors on ajoute un message d'erreur à la liste de nos erreurs


        if len(erreurs) > 0:
            return False, erreurs
        # Si on a au moins une erreur on arrête le processus et on renvoie le ou les messages d'erreurs.

        utilisateur = User(
            user_prenom=prenom,
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(password),
            user_is_admin=isadmin,
            user_is_mod=ismod
        )
        # S'il n'y a pas eu d'erreur on créé un objet User que l'on entre dans la base

        try:
            db.session.add(utilisateur)
            db.session.commit()

            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def update(self, email, nom, prenom, password, login):
        """ Modifie le compte utilisateur. Retourne un tuple (booléen, User ou liste).

        :param self: Instanciation de la class User
        :type self: User
        :param email: Email de l'utilisateur
        :type email: str
        :param nom: Nom de l'utilisateur
        :type nom: str
        :param prenom: Prénom de l'utilisateur
        :type prenom: str
        :param password: Mot de passe de l'utilisateur sur 6 caractères minimum.
        :type password: str
        :param login: Login de l'utilisateur
        :type login: str

        :returns: True et un message de succès s'il n'y a pas eu d'erreurs, False et un message d'erreur sinon
        :rtype: True and User or False and str

        """
        erreurs = []
        if login:
            new_login = login
        else :
            new_login = self.user_login 
        if email:
            new_email = email
        else :
            new_email = self.user_email
        if nom:
            new_nom = nom
        else:
            new_nom = self.user_nom
        if prenom:
            new_prenom = prenom
        else:
            new_prenom = self.user_prenom
        if password:
            new_password = generate_password_hash(password)
        else:
            new_password = self.user_password

        if len(password) < 6 and len(password) != 0:
            erreurs.append("Le mot de passe ne contient pas 6 caractères")


        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        # Compte combien de login ou d'email égaux à ceux renseignés sont présents dans la base


        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")
        # S'ils sont déjà présent alors on ajoute un message d'erreur à la liste de nos erreurs


        if len(erreurs) > 0:
            return False, erreurs
        # Si on a au moins une erreur on arrête le processus et on renvoie le ou les messages d'erreurs.

        self.user_login = new_login
        self.user_nom = new_nom
        self.user_prenom = new_prenom
        self.user_email = new_email
        self.user_password = new_password
        # S'il n'y a pas eu d'erreur on udpate les nouvelles informations

        try:
            db.session.add(self)
            db.session.commit()

            return True, "success"
        except Exception as erreur:
            return False, [str(erreur)]
        
    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.user_id

    def promouvoir_admin(self):
        """ Permet de promouvoir un utilisateur au rang d'administrateur, ce qui fait
        qu'il aura des droits spécifiques de création et suppression.
        Dans l'idéal un seul administrateur devra être présent sur le site.
        Permet aussi de passer un administrateur à un simple utilisateur.
        Fait passer la valeur de user_is_admin de False à True et inversement.
        Renvoie True si réussit, sinon False et un message d'erreur.

        :returns: Renvoie True si réussite, sinon False et un message d'erreur
        :rtype: bool or bool and str
        """

        nombre_admin = User.query.filter(User.user_is_admin).count()
        # On compte le nombre d'administrateur


        if self.user_is_admin and nombre_admin > 1:
            self.user_is_admin = False

        elif not self.user_is_admin:
            self.user_is_admin = True

        else:
            erreur = "Vous ne pouvez pas rétrograger le dernier administrateur"
            return False, erreur
        # On vérifie la valeur de user_is_admin de l'objet, s'il est True on le change en False et inversement.
        # Par contre s'il n'y a qu'un seul administrateur dans la base
        # Et qu'on essaye de le supprimer on met un message d'erreur

        try:
            db.session.add(self)
            db.session.commit()

            return True, "success"

        except Exception as erreur:
            return False, [str(erreur)]

    def promouvoir_mod(self):
        """ Permet de promouvoir un utilisateur au rang de modérateur, ce qui fait
        qu'il aura des droits spécifiques de modérations des commentaires.
        Permet aussi de passer un modérateur à un simple utilisateur.
        Fait passer la valeur de user_is_mod de False à True et inversement.
        Renvoie True si réussit, sinon False et un message d'erreur.

        :returns: Renvoie True si réussit, sinon False et un message d'erreur
        :rtype: bool or bool and str
        """



        if self.user_is_mod:
            self.user_is_mod = False

        else:
            self.user_is_mod = True
        # On vérifie la valeur de user_is_mod de l'objet, s'il est True on le change en False et inversement.

        try:
            db.session.add(self)
            db.session.commit()

            return True, "success"

        except Exception as erreur:
            return False, [str(erreur)]

    def suppression_utilisateur(self):
        """ Permet de supprimer l'objet User actuellement utilisé.

        :returns: Renvoie True si réussit, sinon False et un message d'erreur
        :rtype: bool and str
        """

        try:
            db.session.delete(self)
            db.session.commit()

            return True, "success"
        except Exception as erreur:
            return False, [str(erreur)]


@login.user_loader
def trouver_utilisateur_via_id(identifiant):
    return User.query.get(int(identifiant))
