# Adapte-moi si tu peux 🎥📚

Bienvenue sur **Adapte-moi si tu peux**, une application web construite avec **Flask** pour vous aider à découvrir des films adaptés de livres. Cette application vous permet de rechercher des adaptations, de consulter des informations détaillées sur les livres et les films, et de gérer une liste personnalisée de films à voir.

---

## Notre application en images 🖼️  
Voici un aperçu de l'application :  

![Page d'accueil](../adapte-moi/app/statics/screenshots/home.png)  
<!-- ![Page de recherche](static/screenshots/search.png)   -->


## Fonctionnalités principales 🚀

### Fonctions de base :
- **Recherche intuitive 🔍**
  - Recherchez des livres adaptés en films par titre.
  - Accédez à des liens vers les pages Wikipedia pour plus d'informations.
  - Consultez un indice de recommandation pour chaque adaptation.
- **Top 10 des livres les plus recherchés 📖**
  - Découvrez les 10 livres les plus populaires adaptés en films.
- **Système d'authentification 🔐**
  - Inscription et connexion des utilisateurs.
  - Gérez votre profil utilisateur.
  - Consultez et mettez à jour une liste personnalisée de films à voir.
- **Pages dynamiques 🖥️**
  - Une page **"À propos"** expliquant ce qu'est une adaptation, des statistiques clés et l'objectif de l'application.
  - Une page **"Profil"** pour gérer les paramètres utilisateur et afficher les films enregistrés.

---

## Améliorations à venir 🌟

- Intégration avec des APIs comme **TMDB** ou **Open Library** pour des données en temps réel.
- Algorithmes de recommandation améliorés.
- Partage social des listes de films.

---

## Installation 🛠️

Suivez ces étapes pour configurer le projet en local :

### Prérequis :
- Python 3.7+
- Environnement virtuel (recommandé)

### Étapes :
1. **Clonez le dépôt :**
   ```bash
   git clone https://github.com/sambec/adapte-moi.git
   cd adapte-moi
   ```
2. **Créez un environnement virtuel :**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
3. **Installez les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurez la base de données :**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. **Lancez l'application :**
   ```bash
   flask run
   ```
   - Ouvrez l'application dans votre navigateur à : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Structure du projet 📂

```
/adapte-moi
├── app/
│   ├── routes/           # Routes de l'application
│   ├── models/           # Modèles de base de données
│   ├── forms.py          # Formulaires Flask-WTF
│   ├── static/           # CSS, JavaScript et images
│   └── templates/        # Templates HTML
│   └── utils/            # Boîte à outils
├── config.py             # Paramètres de configuration
├── run.py                # Point d'entrée de l'application
├── requirements.txt      # Dépendances du projet
└── README.md             # Documentation du projet
```

---

## Technologies utilisées 🛠️

- **Backend :** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend :** HTML, CSS, Bootstrap (optionnel)
- **Base de données :** SQLite (par défaut, peut être remplacée par PostgreSQL ou MySQL)

---

## Travail sur les données 📊

Cette application repose sur un travail approfondi de collecte, de nettoyage et de croisement de données provenant de plusieurs sources :
- **Wikidata** (via requêtes SPARQL) pour les informations sur les livres et les films.
- **Le Deuxième Texte** sur Data.gouv et **The  Movie Dataset** sur Kaggle pour des jeux de données complémentaires.

Ces données ont été intégrées dans des tableaux CSV dans Dataiku puis dans une base de données SQLite par un script Python, permettant de relier les livres à leurs adaptations cinématographiques et de fournir des résultats précis et pertinents.

---

## Comment contribuer 🤝

1. Forkez le dépôt.
2. Créez une nouvelle branche :
   ```bash
   git checkout -b nom-de-fonctionnalite
   ```
3. Commitez vos modifications :
   ```bash
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   ```
4. Pushez sur votre branche :
   ```bash
   git push origin nom-de-fonctionnalite
   ```
5. Ouvrez une pull request.

---

## Licence 📜

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Auteurs ✍️

Ce projet est le fruit d’un travail collaboratif des étudiants du **M2 Archives TNAH de l'École des Chartes** dans le cadre du cours de Python.

- [Sarah Ambec](https://github.com/sambec)
- [Joël Féral](https://github.com/desireesdata)
- [Camille Samsa](https://github.com/camillesamsa)
- [Juliette Terrien](https://github.com/julietteterrien)

---

N’hésitez pas à explorer le projet et à contribuer ! 😊
---

## Documentation 

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Framework Bootstrap](https://getbootstrap.com/)
- [Le Deuxième Texte](https://www.data.gouv.fr/fr/datasets/auteurs-et-autrices-dans-les-programmes-denseignement-ou-de-concours-de-lettres/)
- [The Movie Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)

---

Profitez de votre exploration du monde des adaptations cinématographiques ! 🎬📖

