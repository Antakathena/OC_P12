# OC_P12 EPIC-EVENT CRM API


## Training Project : API made with the Django REST Framework (DRF) :
OC_P12 EPIC-EVENT CRM API is made to manage a client database without risk of leaking information outside the company.
Every team involved (Sales, Support, Management) has different mission and receives authorisations accordingly.


## Infos Générales :
### Interface Admin
L'API peut entièrement être contrôlée depuis l'interface administrative django,
des permissions ont été attribuées en ce sens, plusieurs adaptations ont été réalisées dans les fichiers admin.py.
L'interface DRF est cependant aussi couverte.

### Conception
Le projet Epic-Event contient deux app : users et crm
Dans le dossier de projet epic_event, contruit selon l'architecture Django, on retrouve: 
- le dossier **epic_event** qui contient notamment les settings et les urls,
    dont celles pour bénéficier de l'interface DRF.
    A noter : *simpleJWT* a été utilisé pour l'authentification.
        documentation : https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

  - l'**app users** contient les urls de l'app, les modèles, vues et serializers liés au CustomUser,
          Les permissions aux utilisateurs sont attribuées aux utilisateurs en fonction de leur équipe, 
          (team est un attribut du CustomUser)
          des permissions supplémentaires sont attribuées aux commerciaux en charge d'un client
          ou au support en charge d'un évènement (change & delete)

- l'**app crm** contient les urls de l'app, les modèles, vues et serializers pour :

        - les clients (classe Client)
        
        - les contrats ( classe Contract)
        
        - les évènements organisés par l'entreprise (classe Event)

- l'API utilise comme base de données *PostGreSQL*, paramétrée dans les settings


## Utilité :
Destiné à une entreprise qui veut assurer la sécurité des informations liées à ses clients,
en utilisant notamment les possibilités de Django et DRF,
OC_P12 EPIC-EVENT CRM API a pour mission de contribuer au référencement des clients,
au travail des équipes management, vente (sales) et organisation d'évènement (support)
en toute sécurité pour les informations conservées.

## Fonctionnalités :

### Fonctions :
- Les superusers ont tous les accès.
- Tous les membres du staff peuvent voir les informations dont ils ont besoin (la plupart des éléments).
- Les managers (CustomUsers dont la team est management) gèrent les Employées avec les actions du CRUD
- Les vendeurs (sales) gèrent les clients et leurs contrats. Create/POST est accessible à chacun,
    mais il faut être responsable d'un client pour pouvoir interagir avec son dossier (change et delete)
- L'enregistrement d'un contrat signé créé automatiquement un évènement du même nom,
    attribué ensuite par l'équipe management à un membre du support
- Les organisateurs (support) gèrent les évènements. Il faut être responsable d'un évènement pour pouvoir interagir avec son dossier (change et delete)

## Une méthode possible pour explorer l'API
Dans un terminal, utiliser les commandes suivantes :

$ python3 -m venv env 
(créé un dossier env dans le répertoire où vous vous trouvez)
ou créez un autre environnement virtuel

$ source env/bin/activate (sous linux) ou env\Scripts\activate.bat (pour activer l'environnement virtuel sous windows)

$ git clone https://github.com/Antakathena/OC_P12

$ cd ../chemin/du/dossier (de la copie de OC_P12 dans votre dossier env)

$ pip install -r requirements.txt

$ cd epic_event

Une fois dans le dossier de projet epic_event (et non le sous-dossier epic_event!), utiliser la commande

$ python manage.py runserver

Vous pourrez alors explorer localement l'app
sur votre navigateur à l'adresse http://127.0.0.1:8000/
