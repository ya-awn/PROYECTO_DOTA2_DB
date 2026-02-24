import requests
import mysql.connector
import time

def get_connection():
    return mysql.connector.connect(
        host='localhost', user='root', password='', database='DOTA_DB'
    )

def load_details():
    print("🚀 Iniciando carga de detalles...") # Agregamos esto para ver si arranca
    conn = get_connection()
    
    cursor_read = conn.cursor()
    cursor_write = conn.cursor()

    query_matches = """
        SELECT m.match_id FROM Matches m 
        LEFT JOIN Match_Players mp ON m.match_id = mp.match_id 
        WHERE mp.match_id IS NULL 
        LIMIT 10;
    """
    cursor_read.execute(query_matches)
    matches_to_process = cursor_read.fetchall()
    cursor_read.close()

    if not matches_to_process:
        print("✅ Todas las partidas ya tienen sus detalles cargados.")
        conn.close()
        return

    print(f"🔎 Encontradas {len(matches_to_process)} partidas para procesar.")

    for (match_id,) in matches_to_process:
        print(f"📡 Pidiendo detalles del match: {match_id}...")
        res = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
        
        if res.status_code == 200:
            data = res.json()
            players = data.get('players', [])
            
            for p in players:
                acc_id = p.get('account_id')
                if not acc_id:
                    continue

                cursor_write.execute(
                    "INSERT IGNORE INTO Players (Account_id, Persona_Name) VALUES (%s, %s)",
                    (acc_id, p.get('personaname', 'Anonymous'))
                )

                cursor_write.execute(
                    """INSERT IGNORE INTO Match_Players (Match_id, Account_id, Hero_id, Kills, Deaths, Assists)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (match_id, acc_id, p['hero_id'], p['kills'], p['deaths'], p['assists'])
                )
            
            conn.commit()
            print(f"   ✔️ Guardados {len(players)} jugadores.")
            time.sleep(1)
        else:
            print(f"   ❌ Error en API para match {match_id}")

    cursor_write.close()
    conn.close()
    print("🏁 Proceso finalizado.")

# ESTO ES LO MÁS IMPORTANTE:
if __name__ == "__main__":
    load_details()