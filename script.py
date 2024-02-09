import csv
import sqlite3
import requests
import pandas as pd

PRODUITS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
MAGASINS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
VENTES_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"


def url_to_df(url: str):
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        data_list = list(cr)

        header = data_list[0]
        rows = data_list[1:]
        result_dict = {header[i]: [row[i] for row in rows] for i in range(len(header))}

        return pd.DataFrame(result_dict)


produits_df = url_to_df(PRODUITS_URL)
magasins_df = url_to_df(MAGASINS_URL)
ventes_df = url_to_df(VENTES_URL)

# print(produits_df)
# print(magasins_df)
# print(ventes_df)

db_path = "database/data.db"

try:
    # Create database
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()
    print("Database created and Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

    # create tables
    cursor.execute("""
                   CREATE TABLE if not exists magasins
                   (
                   ID_Magasin INTEGER PRIMARY KEY,
                   Ville TEXT,
                   Nombre_de_salariés INTEGER NOT NULL
                   )
                   """)
    print("Created table magasins")

    cursor.execute("""
                   CREATE TABLE if not exists produits
                   (
                   ID_Référence_produit TEXT PRIMARY KEY,
                   Nom TEXT,
                   Prix DOUBLE DEFAULT NULL,
                   Stock INTEGER DEFAULT NULL
                   )
                   """)
    print("Created table produits")

    cursor.execute("""
                   CREATE TABLE if not exists ventes
                   (
                   ID_Référence_produit TEXT,
                   Quantité INTEGER DEFAULT NULL,
                   ID_Magasin INTEGER,
                   Date DATE,
                   FOREIGN KEY(ID_Référence_produit) REFERENCES produits(ID_Référence_produit),
                   FOREIGN KEY(ID_Magasin) REFERENCES magasins(ID_Magasin)
                   )
                   """)
    print("Created table ventes")

    for index, row in magasins_df.iterrows():
        cursor.execute(f"""
                    INSERT OR REPLACE INTO magasins
                    (ID_Magasin, Ville, Nombre_de_salariés)
                    VALUES
                    ({row['ID Magasin']}, '{row['Ville']}', {row['Nombre de salariés']})
                    """)
        print(f"Inserted into table magasins ({row['ID Magasin']}, '{row['Ville']}', {row['Nombre de salariés']})")

    for index, row in produits_df.iterrows():
        cursor.execute(f"""
                    INSERT OR REPLACE INTO produits
                    (ID_Référence_produit, Nom, Prix, Stock)
                    VALUES
                    ('{row['ID Référence produit']}', '{row['Nom']}', {row['Prix']}, {row['Stock']})
                    """)
        print(f"Inserted into table produits ({row['ID Référence produit']}, {row['Nom']}, {row['Prix']}, {row['Stock']})")

    for index, row in ventes_df.iterrows():
        cursor.execute(f"""
                    INSERT OR REPLACE INTO ventes
                    (ID_Référence_produit, Quantité, ID_Magasin, Date)
                    VALUES
                    ('{row['ID Référence produit']}', {row['Quantité']}, {row['ID Magasin']}, {row['Date']})
                    """)
        print(f"Inserted into table ventes ({row['ID Référence produit']}, {row['Quantité']}, {row['ID Magasin']}, {row['Date']})")


    # printing all tables list
    print("List of tables")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cursor.fetchall())

    # tables show settings
    # cursor.execute(".header on")
    # cursor.execute(".mode column")

    # show table
    cursor.execute("SELECT * FROM produits;")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM magasins;")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM ventes;")
    print(cursor.fetchall())

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")


# https://pynative.com/python-sqlite/
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv
