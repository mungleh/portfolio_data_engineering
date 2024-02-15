import sqlite3

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

    print("-----------------------------------------------------------------")

    # create tables
    cursor.execute(
        """
                CREATE TABLE if not exists magasins
                (
                ID_Magasin INTEGER PRIMARY KEY,
                Ville TEXT,
                Nombre_de_salariés INTEGER NOT NULL
                )
                """
    )
    print("Created table magasins")

    cursor.execute(
        """
                CREATE TABLE if not exists produits
                (
                ID_Référence_produit TEXT PRIMARY KEY,
                Nom TEXT,
                Prix DOUBLE DEFAULT NULL,
                Stock INTEGER DEFAULT NULL
                )
                """
    )
    print("Created table produits")

    cursor.execute(
        """
                CREATE TABLE if not exists ventes
                (
                ID_Référence_produit TEXT,
                Quantité INTEGER DEFAULT NULL,
                ID_Magasin INTEGER,
                Date DATE,
                FOREIGN KEY(ID_Référence_produit) REFERENCES produits(ID_Référence_produit),
                FOREIGN KEY(ID_Magasin) REFERENCES magasins(ID_Magasin)
                )
                """
    )
    print("Created table ventes")

    cursor.execute(
        """
                CREATE TABLE if not exists CA
                (
                CA INTEGER DEFAULT NULL
                )
                """
    )
    print("Created table CA")

    cursor.execute(
        """
                CREATE TABLE if not exists nbr_ventes
                (
                ID TEXT PRIMARY KEY,
                Nombre_de_ventes INTEGER DEFAULT NULL
                )
                """
    )
    print("Created table nbr_ventes")

    # create tables ez
    # produits_df.to_sql("produits", conn, if_exists="replace")
    # print("produits table added")
    # magasins_df.to_sql("magasins", conn, if_exists="replace")
    # print("magasins table added")
    # ventes_df.to_sql("ventes", conn, if_exists="replace")
    # print("ventes table added")

    # tables show settings
    # cursor.execute(".header on")
    # cursor.execute(".mode column")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if conn:
        conn.close()
        print("The SQLite connection is closed")
