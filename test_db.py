# # 1.-Load module
# import sqlalchemy
# import pandas as pd
# #2.-Turn on database engine
# dbEngine=sqlalchemy.create_engine('sqlite:///adapte_moi.sqlite') # ensure this is the correct path for the sqlite file. 
# #3.- Read data with pandas
# df = pd.read_sql('select * from Film',dbEngine)
# print(df)

import sqlite3
import pandas as pd

# Connexion à la base de données SQLite
conn = sqlite3.connect("adapte_moi.sqlite")
cursor = conn.cursor()

# Création de la table User
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Création de la table Collection
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Collection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
    )
''')

# Création de la table collection_film
cursor.execute('''
    CREATE TABLE IF NOT EXISTS collection_film (
        id_collection INTEGER NOT NULL,
        id_film TEXT NOT NULL,
        FOREIGN KEY (id_collection) REFERENCES Collection(id) ON DELETE CASCADE
    )
''')

conn.commit()

# Création d'un DataFrame pandas avec des utilisateurs exemple
data_users = {
    "name": ["Sarah"],
    "email": ["sarahambec@gmail.com"],
    "password": ["123prout"]
}
df_users = pd.DataFrame(data_users)

# Insérer les données dans la table User
df_users.to_sql("User", conn, if_exists="append", index=False)

# Création d'un DataFrame pandas avec des collections exemple
data_collections = {
    "user_id": [1],
    "title": ["Sci-Fi Classics"],
    "description": ["A collection of timeless sci-fi films"]
}
df_collections = pd.DataFrame(data_collections)

# Insérer les données dans la table Collection
df_collections.to_sql("Collection", conn, if_exists="append", index=False)

# Création d'un DataFrame pandas avec des associations collection-film
data_collection_film = {
    "id_collection": [1, 1],
    "id_film": ["f1","f2"]
}
df_collection_film = pd.DataFrame(data_collection_film)

# Insérer les données dans la table collection_film
df_collection_film.to_sql("collection_film", conn, if_exists="append", index=False)
conn.commit()

# Vérification des données insérées
print(pd.read_sql("SELECT * FROM User", conn))
print(pd.read_sql("SELECT * FROM Collection", conn))
print(pd.read_sql("SELECT * FROM collection_film", conn))

# Fermeture de la connexion
conn.close()
