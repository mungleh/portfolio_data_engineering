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
    produits_df.to_sql("produits", conn, if_exists="replace")
    print("produits table added")
    magasins_df.to_sql("magasins", conn, if_exists="replace")
    print("magasins table added")
    ventes_df.to_sql("ventes", conn, if_exists="append")
    print("ventes table added")

    # printing all tables list
    print("List of tables")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM produits")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM magasins")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM ventes")
    print(cursor.fetchall())

    # cursor.close()

    # # Create table produits
    # conn = sqlite3.connect("SQLite_Python.db")
    # sqlite_create_table_query = """CREATE TABLE produits (
    #                             Nom VARCHAR(255),
    #                             ID_Référence_produit VARCHAR(255) PRIMARY KEY,
    #                             Prix FLOAT,
    #                             Stock INTEGER
    #                             );"""

    # cursor = conn.cursor()
    # print("Successfully Connected to SQLite")
    # cursor.execute(sqlite_create_table_query)
    # conn.commit()
    # print("SQLite table produits created")
    # cursor.close()

    # # Create table magasins
    # conn = sqlite3.connect("SQLite_Python.db")
    # sqlite_create_table_query = """CREATE TABLE produits (
    #                             ID_Magasin VARCHAR(255) PRIMARY KEY,
    #                             Ville VARCHAR(255),
    #                             Nombre_de_salariés VARCHAR(255)
    #                             );"""

    # cursor = conn.cursor()
    # print("Successfully Connected to SQLite")
    # cursor.execute(sqlite_create_table_query)
    # conn.commit()
    # print("SQLite table magasins created")
    # cursor.close()

    # # Create table ventes
    # conn = sqlite3.connect("SQLite_Python.db")
    # sqlite_create_table_query = """CREATE TABLE produits (
    #                             Date VARCHAR(255) ,
    #                             ID_Référence_produit VARCHAR(255),
    #                             produit VARCHAR(255),
    #                             Quantité INTEGER,
    #                             ID_Magasin INTEGER PRIMARY KEY,
    #                             );"""

    # cursor = conn.cursor()
    # print("Successfully Connected to SQLite")
    # cursor.execute(sqlite_create_table_query)
    # conn.commit()
    # print("SQLite table ventes created")
    # cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")


# https://pynative.com/python-sqlite/
# https://stackoverflow.com/questions/35371043/use-python-requests-to-download-csv
