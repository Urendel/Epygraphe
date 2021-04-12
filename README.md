# Projet éPYgraphè

Ce projet a été développé dans le cadre du module Python de l'École nationale des Chartes.

Pendant mes années d'études en Histoire ancienne je participais à un séminaire sur les inscriptions
épigraphiques Grecques. Par la matière, le nombre de participant était de fait très limité 
et venant d'horizon tout à fait différents - étudiants, chercheurs, archéologues, historiens de l'art - ce qui permettait beaucoup d'échanges
et beaucoup de réflexion sur la restitution, la traduction et la mise en contexte de certains textes, le tout arbitré par
notre professeur.

Je me suis donc demandé comment, avec la crise sanitaire que nous connaissons tous à l'international,
des gens venant d'horizons et de pays totalement différents pouvait se retrouver pour échanger et débattre.
Bien sur la solution sont les programmes de visioconférences mais on perd alors la possibilité d'avoir la traduction et
l'échange sur un texte. Mon idée a alors été de développer un programme qui met en place un site très simple et qui perme
de récupérer des inscriptions sur des bases de données, les traduire et les commenter, le tout sous une forme très simple
et sans se frotter vraiment à la technologie. Le tout pouvant gérer un petit groupe d'étudiants ou de chercheur qui auraient
besoin d'une plateforme d'échange.



### Pré-requis

Pour pouvoir se servir de l'application il vous faut avoir installé au préalable
Python sur votre machine. De plus vous devez installer des packages qui se trouvent dans
le fichier requirements.txt.
Si vous passez par un environnement virtuel vous pouvez aussi lancer la commande
``pip install -r requirements.txt``.

## Démarrage et premiers pas

Une fois ceci fait vous pouvez lancer le site en lançant la commande ``python run.py``. Le site est conçu pour que
vous n'ayez rien à installer ou régler d'autre si vous le souhaitez, toutefois vous devez changer
la phrase de la SECRET_KEY qui se trouve dans reglages.py.

Dans ce fichier vous trouverez des petits réglages qui permet de personnaliser un peu votre site, mettre le nom
du fichier image du bandeau que vous placerez dans static/images/... . Vous pourrez aussi changer le nom du site
pour un nom qui vous conviendrait plus et remplacer le nom d'éPYgraphè. Pour finir vous pouvez aussi définir le nombre
de résultats d'affichage d'inscriptions par page qui seront visible sur la page de navigation et de recherche.

**ATTENTION**

Le site est conçu avec une base de données pré remplie pour que la personne qui installe le site soit
l'administrateur du dis site. Vous devrez passer par le site lui-même pour vous connecter en tant qu'administrateur
le login et le mot de passe sont tous les deux ``admin`` ensuite vous devrez passer sur votre page personnelle qui se trouve dans le menu Navigation
pour changer vos informations personnelles.

C'est aussi dans le menu Navigation que vous trouverez la page d'administration du site.
En tant qu'administrateur c'est à vous d'entrer de nouvelles inscriptions sur le site. Pour ce faire
veuillez visiter la base de données épigraphiques de l'université d'[Heidelberg](https://edh-www.adw.uni-heidelberg.de/home/), trouvez une inscription
qui vous intéresse et que vous aimeriez traiter, et entrez les 6 chiffres du numéro que vous trouverez dans l'url ou la description de l'inscription sous
le nom de N° Heidelberg (Sous le format HD000000).

Dans la page administrateur toujours vous pourrez supprimer des utilisateurs, vous pouvez aussi nommer d'autres administrateurs
ou des modérateurs, ces derniers serviront à modérer les zone de discussion dans chaque pages d'inscriptions.

Si vous avez un problème avec la base de données un double vide vous est fournis dans le dossier data nommée "epygraphe_bdd
.backup.sqlite", vous avez juste à détruire l'ancienne et a enlever le ".backup" du nom du fichier.
Ce backup sera toujours disponible sur le GitHub du projet et vous disposez aussi d'un script de création SQL de la base de données.

## TODO
* Améliorer la couche graphique du site qui est un peu austère.
* Pouvoir importer des inscriptions encodée en XML TEI.
* Pouvoir exporter les inscriptions au format Json ou XML TEI.
* Avoir un vrai menu de réglage graphique sur le site même pour éviter de toucher le moins possible au code.
* Avoir un script d'installation des différents scripts et de déploiement du site.

## Conçu avec

* [Bootstrap](https://getbootstrap.com/) - Framework CSS
* [Pycharm](https://www.jetbrains.com/fr-fr/pycharm/) - Environnement de développement Python



## Auteur

* **Julien Fenech** _alias_ [@Urendel](https://github.com/Urendel)


