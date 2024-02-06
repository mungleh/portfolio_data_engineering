import csv
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

        # header = data_list[0]
        # rows = data_list[1:]
        # result_dict = {header[i]: [row[i] for row in rows] for i in range(len(header))}

        return pd.DataFrame(data_list)


produits_df = url_to_df(PRODUITS_URL)
magasins_df = url_to_df(MAGASINS_URL)
ventes_df = url_to_df(VENTES_URL)

print(produits_df)
print(magasins_df)
print(ventes_df)
