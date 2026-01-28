import requests
import pandas as pd
import sqlite3
import io

url = "https://en.wikipedia.org/wiki/Lists_of_association_football_clubs"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

html = io.StringIO(response.text)
tables = pd.read_html(html)

df = tables[0]

df = df.reset_index(drop=True)
df["Rank"] = df.index + 1

for col in df.columns:
    df[col] = df[col].astype(str).str.replace(r"\[.*?\]", "", regex=True)

conn = sqlite3.connect("football_clubs.db")
df.to_sql("clubs", conn, if_exists="replace", index=False)
conn.close()

print("Base de datos creada correctamente.")
