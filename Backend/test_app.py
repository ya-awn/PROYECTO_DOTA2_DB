import requests
import json
import mysql.connector

# 1. Traer héroes de OpenDota (JSON)
response = requests.get('https://api.opendota.com/api/heroes')
heroes = response.json()  # Convertir a Python

# 2. Conectar a tu BD
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='DOTA_DB'
)
cursor = conn.cursor()

# 3. Insertar cada héroe en tu tabla
for hero in heroes:
    sql = "INSERT INTO Heroes (Hero_id, Name, Localized_Name, Primary_Attr) VALUES (%s, %s, %s, %s)"
    valores = (hero['id'], hero['name'], hero['localized_name'], hero['primary_attr'])
    cursor.execute(sql, valores)

conn.commit()
cursor.close()
conn.close()

print(f"✅ {len(heroes)} héroes insertados")

