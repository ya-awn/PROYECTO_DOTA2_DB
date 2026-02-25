import requests
import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='DOTA_DB'
    )

def load_my_data(account_id, persona_name):
    conn = get_connection()
    cursor = conn.cursor()

    print(f"📡 Pidiendo partidas recientes de: {persona_name} ({account_id})...")
    url = f"https://api.opendota.com/api/players/{account_id}/matches?limit=20"
    res = requests.get(url)
    
    if res.status_code == 200:
        matches = res.json()
        print(f"✅ Se encontraron {len(matches)} partidas recientes.")

        for m in matches:
            match_id = m['match_id']

            fecha_dt = datetime.fromtimestamp(m['start_time'])
            cursor.execute("""
                INSERT IGNORE INTO Matches (Match_id, Start_time, Duration)
                VALUES (%s, %s, %s)
            """, (match_id, fecha_dt, m['duration']))

            cursor.execute("""
                INSERT IGNORE INTO Match_Players (Match_id, Account_id, Hero_id, Kills, Deaths, Assists)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (match_id, account_id, m['hero_id'], m['kills'], m['deaths'], m['assists']))

            cursor.execute("""
                INSERT IGNORE INTO Players (Account_id, Persona_Name)
                VALUES (%s, %s)
            """, (account_id, persona_name))

        conn.commit()
        print(f"💾 ¡Datos de {persona_name} cargados correctamente!")
        print(f"📊 Total de partidas insertadas: {len(matches)}")

    else:
        print(f"❌ Error al conectar con OpenDota. Status code: {res.status_code}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_my_data(102099582, "Arteezy")