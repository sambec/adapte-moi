from ..app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

# class Users(UserMixin, db.Model):

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def ajout(pseudo, password):
        erreurs = []
        if not pseudo:
            erreurs.append("Pas de pseudo")
        if not password or len(password) < 7:
            erreurs.append("Le mot de passe doit contenir au moins 7 caractères")
        unique = Users.query.filter(
            db.or_(Users.pseudo == pseudo)
        ).count()
        if unique > 0:
            erreurs.append("Le pseudo est déjà pris ! Choisis-en un autre :)")
    
        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = Users(
            pseudo=pseudo,
            password=generate_password_hash(password)
        )

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]
    # @staticmethod
    # def identification(prenom, password):
    #     utilisateur = Users.query.filter(Users.prenom == prenom).first()
    #     if utilisateur and check_password_hash(utilisateur.password, password):
    #         return utilisateur
    #     return None

    # @staticmethod
    # def ajout(prenom, password):
    #     erreurs = []
    #     if not prenom:
    #         erreurs.append("Le prénom est vide")
    #     if not password or len(password) < 6:
    #         erreurs.append("Le mot de passe est vide ou trop court")

    #     unique = Users.query.filter(
    #         db.or_(Users.prenom == prenom)
    #     ).count()
    #     if unique > 0:
    #         erreurs.append("Le prénom existe déjà")

    #     if len(erreurs) > 0:
    #         return False, erreurs
        
    #     utilisateur = Users(
    #         prenom=prenom,
    #         password=generate_password_hash(password)
    #     )

    #     try:
    #         db.session.add(utilisateur)
    #         db.session.commit()
    #         return True, utilisateur
    #     except Exception as erreur:
    #         return False, [str(erreur)]

    # def get_id(self):
    #     return self.id

    # @login.user_loader
    # def get_user_by_id(id):
    #     return Users.query.get(int(id))