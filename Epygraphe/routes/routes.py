from flask import render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user
from flask_sqlalchemy import Pagination
from sqlalchemy import or_
from ..app import app, login, db
from ..reglages import INSC_PAR_PAGE, TITRE_SITE, IMAGE_SITE
from ..models.commentaire import Comment
from ..models.inscription import Inscription
from ..models.utilisateur import User
from ..models.version import Version

# Sur chacune des pages on envoie IMAGE_SITE qui représente le background du site et qui peut êtres changé par
# l'administrateur du site dans les réglages à tout moment.
# On fait de même avec TITRE_SITE qui représente le nom que l'on voit partout sur le site mais qui peut être
# changé au gré de l'administrateur.

@app.route("/", methods=["POST", "GET"])
def accueil():
    """ Page d'accueil du site.
    """
    inscriptions = Inscription.query.order_by(Inscription.inscription_id.desc()).limit(5).all()
    utilisateurs = User.query.order_by(User.user_id.desc()).limit(5).all()
    # On Les 5 derniers utilisateurs et inscriptions entrés dans la base pour les afficher sur la page d'accueil.

    return render_template("pages/accueil.html",
                           title=TITRE_SITE,
                           image=IMAGE_SITE,
                           inscriptions=inscriptions,
                           utilisateurs=utilisateurs
                           )


@app.route("/item/<int:inscription_id>", methods=["POST", "GET"])
def item(inscription_id):
    """ Route permettant l'affichage des données d'une inscription
        Une liste de versions est aussi stockée et envoyée dans la page


    :param inscription_id: Identifiant numérique de l'inscription
    """

    unique_inscription = Inscription.query.get(inscription_id)
    # on demande l'inscription en fonction de l'idée renseigné lors du GET

    texte_unique = ""
    liste_version = Inscription.query.get(inscription_id).versions
    liste_commentaire = Inscription.query.get(inscription_id).comments
    # On récupère la liste des commentaires et des traductions en fonction de l'id actuelle de l'inscription.

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 5
    end = start + 5
    items = liste_commentaire[start:end]
    liste_paginee = Pagination(query=None, page=page, per_page=5, items=items, total=len(liste_commentaire))
    # Utilisation de Pagination pour pouvoir paginer les commentaires 5 par 5.

    if request.method == "POST":
        if 'btn_choix' in request.form:
            selection = request.form.get("choix")
            unique_version = Version.query.get(selection)
            texte_unique = unique_version.version_text
        # Si on reçoit un formulaire en POST c'est qu'on a envoyé un formulaire,
        # si c'est btn choix qui a envoyé ce formulaire c'est que c'est le bouton qui permet de choisir
        # la traduction dans la list déroulante où se trouve tous les différents traducteur du texte.

        elif 'traduire' in request.form:
            statut, donnees = Version.creer(
                iduser=current_user.user_id,
                idinscription=inscription_id,
                texte=request.form.get("trad", None)
            )
            if statut is True:
                flash("Traduction bien entrée en base", "success")
                return redirect(inscription_id)

            else:
                flash(donnees, "error")
        # Si c'est le btn traduire sur lequel on a appuyé c'est qu'un utilisateur a entré une nouvelle traduction
        # c'est alors qu'on récupère son id, l'id de l'inscription et le texte pour pouvoir créer une traduction.

        elif 'com' in request.form:
            statut, donnees = Comment.creer(
                iduser=current_user.user_id,
                idinscription=inscription_id,
                texte=request.form['com']
            )
            if statut is True:
                flash("Votre commentaire a bien été envoyé", "success")
                return redirect(inscription_id)
            else:
                flash(donnees, "error")
            # Si c'est com qui envoie un formulaire c'est que l'utilisateur à écrit un commentaire
            # là encore on récupère son id, l'id de l'inscription sur laquelle il y a eu le commentaire
            # et le commentaire en lui mm pour créer une entité Comment.

        elif 'delete' in request.form:
            id_comment = request.form['delete']
            del_comment = Comment.query.get(id_comment)
            statut, erreur = del_comment.suppression_commentaire()
            if statut is True:
                flash("Commentaire supprimé", "success")
                return redirect(inscription_id)
            else:
                flash(erreur, "error")
            # Si le formulaire est envoyé par delete, qui est une petite croix à côté de chaque commentaire
            # on récupère alors l'id du comment embarqué par le bouton.
            # on fait une requête pour instancié l'objet Comment grace à son id.
            # et on se sert de la fonction suppression pour le supprimer.

    return render_template(
        "pages/item.html",
        title=TITRE_SITE,
        image=IMAGE_SITE,
        item=unique_inscription,
        versions=liste_version,
        texte_envoye=texte_unique,
        commentaires=liste_paginee
    )


@app.route("/user/<int:user_id>", methods=["POST", "GET"])
def utilisateur(user_id):
    """ Route permettant l'affichage des données d'un utilisateur
        Cette page permet d'afficher les commentaires et les traductions
        de l'utilisateur. Si celui-ci est connecté sur sa propre page, il pourra
        changer ses informations personnelles.


    :param user_id: Identifiant numérique de l'utilisateur
    """
    unique_user = User.query.get(user_id)
    liste_traduction = unique_user.versions
    liste_commentaire = unique_user.comments
    # On récupère l'User en fonction de son ID et on charge la liste de ses traductions et commentaires

    if request.method == "POST":
        statut, donnees = unique_user.update(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            prenom=request.form.get("prenom", None),
            password=request.form.get("motdepasse", None)
        )
        # Si la méthode est en POST c'est que l'utilisateur change ses données personnelles
        # on lance alors la fonction update pour mettre à jour les données de l'utilisateur en fonction de
        # ce que l'on a récupéré dans le formulaire.

        if statut is True:
            flash("Vos informations personnelles ont bien été mises à jour", "success")
            return redirect(user_id)
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return redirect(user_id)
    else:
        return render_template(
            "pages/user.html",
            user=unique_user,
            title=TITRE_SITE,
            image=IMAGE_SITE,
            commentaires=liste_commentaire,
            traductions=liste_traduction
        )


@app.route("/recherche")
def recherche():
    """ Route permettant la recherche dans la base de donnée.
    """

    requete = request.args.get("q", None)
    page = request.args.get("page", 1)
    # On récupère par get les requêtes qui passe dans l'url de la page et qui proviennent du
    # champ de recherche qui se trouve dans la page html conteneur qui est le bandeau du site.

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1


    resultats = []
    # Initialisation de la liste qui recueillera les résultats.

    if requete:
        resultats = (db.session.query(Inscription)
                            .join(Inscription.versions)
                            .join(Version.user)
                            .join(User.comments)
                            .filter(or_(
                                Inscription.inscription_no_hd.like("%{}%".format(requete)),
                                User.user_nom.like("%{}%".format(requete)),
                                User.user_prenom.like("%{}%".format(requete)),
                                Version.version_text.like("%{}%".format(requete)),
                                Comment.comment_text.like("%{}%".format(requete)),
                                Inscription.inscription_texte.like("%{}%".format(requete))
                            ))).paginate(page=page, per_page=INSC_PAR_PAGE)

    # Si on a une une recherche on fait une requête sql qui va chercher dans la base en fonction de cette recherche.
    # Elle va chercher dans les textes de traductions ou les commentaires, ainsi que les noms d'utilisateurs ou encore
    # les numéro Heildeberg des inscriptions ou dans leur texte.
    # Elle ramène les objets Incriptions qui correspondent à ces recherches.

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        q=requete,
        image=IMAGE_SITE,
        title=TITRE_SITE
    )


@app.route("/browse")
def naviguer():
    """ Route permettant de naviguer dans la liste des inscriptions
    """
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    # On initie la pagination.

    resultats = Inscription.query.order_by(Inscription.inscription_id.asc())
    # on recupère toutes les inscriptions de la première entrée dans la base à la dernière
    resultats = resultats.paginate(page=page, per_page=INSC_PAR_PAGE)
    # on pagine ce résultat.

    return render_template(
        "pages/browse.html",
        resultats=resultats,
        image=IMAGE_SITE,
        title=TITRE_SITE
    )


@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions des utilisateurs sur le site.
    """

    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            prenom=request.form.get("prenom", None),
            password=request.form.get("motdepasse", None)
        )
        # On récupère les informations envoyé en POST pour créer notre nouvel User.

        if statut is True:
            flash("Vous êtes maintenant enregitré, connectez vous.", "success")
            return redirect("/")
        # Si c'est correcte on en informe l'utilisateur et on le renvoit à la page d'accueil du site.
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html", title=TITRE_SITE)
        # S'il y a eu quoi que ce soit comme problème on reste sur la page des inscriptions et on renvoit les erreurs.
    else:
        return render_template("pages/inscription.html", title=TITRE_SITE)


@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route permettant aux utilisateurs de se connecter,
    C'est là qu'on va se servir de la fonction connexion créé pour la classe User.
    """

    if request.method == "POST":
        utilisateur = User.connexion(
            login=request.form.get("login", None),
            password=request.form.get("motdepasse", None)
        )
        # si on a l'envoie du formulaire de connexion, on récupère les données et on les fournie à la fonction
        # connexion.

        url = request.form['connexion']
        # On récupère l'url passé dans le bouton connexion, qui informe de l'url où se trouve l'utilisateur
        # au moment du clique.

        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url)
        # si tout se passe bien au moment du clique, on informe de la connexion, on connecte l'utilisateur qui reste sur
        # la même url de la page où il s'est connecté.
        else:
            flash("Login ou mot de passe non reconnu", "error")

    return redirect(url)


@app.route("/deconnexion")
def deconnexion():
    """ Route permettant de gérer les déconnexion des utilisateurs.
    """
    if current_user.is_authenticated is True:
        logout_user()
        flash("Déconnexion", "info")
    return redirect("/")
    # Si l'utilisateur et connecté il peut se déconnecter. On l'informe de ce fait.


@app.route("/admin", methods=["GET", "POST"])
def administrer():
    """ Route gérant l'administration du site, il n'y a que les administrateurs qui peuvent s'y connecter.
    """
    if not current_user.is_authenticated:
        return redirect("/")
    # Si un anonyme essaye de se connecter à la page en entrant l'adresse à la main,
    # ça le renvoie à la page d'accueil.

    elif not current_user.user_is_admin:
        return redirect("/")
    # Si l'utilisateur actuel n'est pas administrateur, même chose.

    else:
        if request.method == "POST":
            if 'action' in request.form:
                nohd = request.form.get("add", None)
                statut, erreur = Inscription.creer(
                    numero_hd=nohd
                )
                if statut is True:
                    flash("Inscription bien entrée en base", "success")

                else:
                    flash(erreur, "error")
        # Si le formulaire avec le bouton action est enclenché, c'est que
        # l'administrateur a entré le 6 chiffres du code Heildeberg.
        # On récupère se code et on l'envoie dans la fonction créer pour
        # créer une nouvelle inscription.

            elif 'delete' in request.form:
                id_user = request.form['delete']
                del_user = User.query.get(id_user)
                statut, erreur = del_user.suppression_utilisateur()
                if statut is True:
                    flash("Utilisateur supprimé", "success")

                else:
                    flash(erreur, "error")
            # Sinon si c'est le bouton delete qui est enclenché, c'est que l'administrateur à supprimé un
            # utilisateur.

            elif 'admin' in request.form:
                id_user = request.form['admin']
                promote_user = User.query.get(id_user)
                statut, erreur = promote_user.promouvoir_admin()
                if statut:
                    flash(
                        promote_user.user_prenom + " " + promote_user.user_nom + " " + " à changé de statut administrateur",
                        "success")

                else:
                    flash(erreur, "error")
            # Sinon si  l'admin appuie sur le bouton "admin", il promeut un utilisateur au rôle d'administrateur
            # Si cette personne est déjà admin ça le rétrograde.

            elif 'modo' in request.form:
                id_user = request.form['modo']
                promote_user = User.query.get(id_user)
                statut, erreur = promote_user.promouvoir_mod()
                if statut is True:
                    flash(
                        promote_user.user_prenom + " " + promote_user.user_nom + " " + " à changé de statut modérateur",
                        "success")

                else:
                    flash(erreur, "error")
            # Sinon si  l'admin appuie sur le bouton "modo", il promeut un utilisateur au rôle de modérateur
            # Si cette personne est déjà modérateur ça le rétrograde.

        page = request.args.get("page", 1)

        if isinstance(page, str) and page.isdigit():
            page = int(page)
        else:
            page = 1

        utilisateurs = User.query.paginate(page=page, per_page=5)

        return render_template("pages/menu_admin.html", image=IMAGE_SITE, title=TITRE_SITE, utilisateurs=utilisateurs)
