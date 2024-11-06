import pandas as pd
import sqlite3
import os
import logging
# Connexion à la base de données (ajustez le chemin et le nom de votre base)
db_path = r'D:\TDUSCMAP\db.sqlite3'
print(db_path)
try:
    conn = sqlite3.connect(db_path)
    print("Connexion à la base de données établie.")
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données: {e}")

logging.basicConfig(filename='debug.log', level=logging.DEBUG)
# Lecture du fichier Excel
df = pd.read_excel('configuration reglage.xlsx')
print(df.head())
# Insertion des données
try:
    df.to_sql('tduscmap_configurationreglage', conn, if_exists='append', index=False)
    print("Table créée et données insérées avec succès.")
except Exception as e:
    print(f"Erreur lors de l'insertion des données: {e}")
# Vérification de l'insertion
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM tduscmap_configurationreglage")
nb_lignes_inseres = cursor.fetchone()[0]
print(f"{nb_lignes_inseres} lignes insérées dans la table.")

# Affichage des 5 premières lignes de la table (pour vérification)
cursor.execute("SELECT * FROM tduscmap_configurationreglage LIMIT 5")
results = cursor.fetchall()
for row in results:
    print(row)
conn.close()