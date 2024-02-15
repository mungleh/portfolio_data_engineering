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

db_path = "database/data.db"

try:
    # Create database
    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()
    print("Successfully Connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)

    print("-----------------------------------------------------------------")

    for index, row in magasins_df.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO magasins
                        (ID_Magasin, Ville, Nombre_de_salariés)
                        VALUES
                        ({row['ID Magasin']}, '{row['Ville']}', {row['Nombre de salariés']});
                        """
            )
            conn.commit()
            print(
                f"Inserted into table magasins ({row['ID Magasin']}, '{row['Ville']}', {row['Nombre de salariés']})"
            )
        except sqlite3.Error as e:
            print(f"Error inserting into table magasins: {e}")

    print("-----------------------------------------------------------------")

    for index, row in produits_df.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO produits
                        (ID_Référence_produit, Nom, Prix, Stock)
                        VALUES
                        ('{row['ID Référence produit']}', '{row['Nom']}', {row['Prix']}, {row['Stock']});
                        """
            )
            conn.commit()
            print(
                f"Inserted into table produits ({row['ID Référence produit']}, {row['Nom']}, {row['Prix']}, {row['Stock']})"
            )
        except sqlite3.Error as e:
            print(f"Error inserting into table produits: {e}")

    print("-----------------------------------------------------------------")

    for index, row in ventes_df.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO ventes
                        (ID_Référence_produit, Quantité, ID_Magasin, Date)
                        VALUES
                        ('{row['ID Référence produit']}', {row['Quantité']}, {row['ID Magasin']}, '{row['Date']}');
                        """
            )
            conn.commit()
            print(
                f"Inserted into table ventes ({row['ID Référence produit']}, {row['Quantité']}, {row['ID Magasin']}, {row['Date']})"
            )
        except sqlite3.Error as e:
            print(f"Error inserting into table ventes: {e}")

    print("-----------------------------------------------------------------")

    # printing all tables list
    print("List of tables")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cursor.fetchall())

    print("-----------------------------------------------------------------")

    # show table
    print("Data in produits")
    cursor.execute("SELECT * FROM produits;")
    print(cursor.fetchall())

    print("-----------------------------------------------------------------")

    print("Data in magasins")
    cursor.execute("SELECT * FROM magasins;")
    print(cursor.fetchall())

    print("-----------------------------------------------------------------")

    print("Data in ventes")
    cursor.execute("SELECT * FROM ventes;")
    print(cursor.fetchall())

    print("-----------------------------------------------------------------")

    # analyse 1: chiffre d'affaire
    cursor.execute(
        """
            SELECT
                SUM(Prix * Quantité) AS total_price
            FROM
                ventes
            LEFT JOIN
                produits
            ON
                ventes.ID_Référence_produit = produits.ID_Référence_produit;
                                        """
    )
    analyse_1 = pd.DataFrame(cursor.fetchall(), columns=["CA"])
    print(analyse_1)

    print("-----------------------------------------------------------------")

    # analyse 2: ventes par produits
    cursor.execute(
        """
                                    SELECT
                                        produits.ID_Référence_produit,
                                        SUM(Quantité) AS nbr_ventes
                                    FROM
                                        ventes
                                    LEFT JOIN
                                        produits
                                    ON
                                        ventes.ID_Référence_produit = produits.ID_Référence_produit
                                    GROUP BY
                                        produits.ID_Référence_produit;
                                        """
    )
    analyse_2 = pd.DataFrame(cursor.fetchall(), columns=["ID", "Nombre_de_ventes"])
    print(analyse_2)

    print("-----------------------------------------------------------------")

    # analyse 3: ventes par région
    cursor.execute(
        """
                                    SELECT
                                        magasins.Ville, SUM(Quantité) AS nbr_ventes
                                    FROM
                                        ventes
                                    LEFT JOIN
                                        magasins
                                    ON
                                        ventes.ID_Magasin = magasins.ID_Magasin
                                    GROUP BY
                                        magasins.Ville;
                                        """
    )
    analyse_3 = pd.DataFrame(cursor.fetchall(), columns=["ID", "Nombre_de_ventes"])
    print(analyse_3)

    print("-----------------------------------------------------------------")

    # insert analyse 1
    for index, row in analyse_1.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO CA
                        (CA)
                        VALUES
                        ({row['CA']});
                        """
            )
            conn.commit()
            print(f"Inserted into table CA ({row['CA']})")
        except sqlite3.Error as e:
            print(f"Error inserting into table CA: {e}")

    print("-----------------------------------------------------------------")

    # insert analyse 2
    for index, row in analyse_2.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO nbr_ventes
                        (ID, Nombre_de_ventes)
                        VALUES
                        ('{row['ID']}', {row['Nombre_de_ventes']});
                        """
            )
            conn.commit()
            print(
                f"Inserted into table nbr_ventes ({row['ID']}, {row['Nombre_de_ventes']})"
            )
        except sqlite3.Error as e:
            print(f"Error inserting into table nbr_ventes: {e}")

    print("-----------------------------------------------------------------")

    # insert analyse 3
    for index, row in analyse_3.iterrows():
        try:
            cursor.execute(
                f"""
                        INSERT OR REPLACE INTO nbr_ventes
                        (ID, Nombre_de_ventes)
                        VALUES
                        ('{row['ID']}', {row['Nombre_de_ventes']});
                        """
            )
            conn.commit()
            print(
                f"Inserted into table nbr_ventes ({row['ID']}, {row['Nombre_de_ventes']})"
            )
        except sqlite3.Error as e:
            print(f"Error inserting into table nbr_ventes: {e}")

    print("-----------------------------------------------------------------")

    print("Data in CA")
    cursor.execute("SELECT * FROM CA;")
    print(cursor.fetchall())

    print("-----------------------------------------------------------------")

    print("Data in nbr_ventes")
    cursor.execute("SELECT * FROM nbr_ventes;")
    print(cursor.fetchall())

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")
