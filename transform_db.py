import sqlite3
import mysql.connector

# Connexion à la base de données SQLite
sqlite_db_path = 'adapte_moi.sqlite'
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# Connexion à la base de données MySQL
mysql_config = {
    'user': 'bob',
    'password': 'mdp',
    # 'host': 'billy',
    'database': 'adapte_moi'
}
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Récupération des tables SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Conversion des tables et des données
for table_name in tables:
    table_name = table_name[0]
    print(f"Conversion de la table {table_name}...")

    # Récupération de la structure de la table
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()

    # Création de la table dans MySQL
    create_table_query = f"CREATE TABLE {table_name} ("
    for column in columns:
        col_name = column[1]
        col_type = column[2]
        # Conversion des types de données SQLite en types MySQL
        if col_type == 'INTEGER':
            mysql_type = 'INT'
        elif col_type == 'TEXT':
            mysql_type = 'VARCHAR(255)'
        elif col_type == 'REAL':
            mysql_type = 'FLOAT'
        elif col_type == 'BLOB':
            mysql_type = 'BLOB'
        else:
            mysql_type = 'TEXT'  # Type par défaut
        create_table_query += f"{col_name} {mysql_type}, "
    create_table_query = create_table_query.rstrip(", ") + ");"
    mysql_cursor.execute(create_table_query)

    # Insertion des données dans la table MySQL
    sqlite_cursor.execute(f"SELECT * FROM {table_name};")
    rows = sqlite_cursor.fetchall()
    for row in rows:
        placeholders = ", ".join(["%s"] * len(row))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
        mysql_cursor.execute(insert_query, row)

    mysql_conn.commit()
    print(f"Table {table_name} convertie avec succès.")

# Fermeture des connexions
sqlite_conn.close()
mysql_conn.close()
