import requests
import mysql.connector
from datetime import datetime

# 1. Conexión a la base de datos
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='DOTA_DB'
    )

def load_public_matches():
    # 2. Pedir datos a OpenDota
    print("📡 Conectando con OpenDota...")
    response = requests.get('https://api.opendota.com/api/publicMatches')
    
    if response.status_code == 200:
        matches = response.json() # Esto es una LISTA de OBJETOS JSON
        print(f"✅ Se obtuvieron {len(matches)} partidas.")
        
        conn = get_connection()
        cursor = conn.cursor()
        
        count = 0
        for m in matches:
            # 3. Preparar los datos
            # OpenDota da el tiempo en 'unix timestamp' (segundos desde 1970)
            # Lo convertimos a formato DATETIME de MySQL
            fecha_dt = datetime.fromtimestamp(m['start_time'])
            
            sql = """
                INSERT IGNORE INTO Matches (Match_id, Start_time, Duration, Radiant_win, Game_Mode)
                VALUES (%s, %s, %s, %s, %s)
            """
            # Usamos INSERT IGNORE para que si la partida ya existe, no tire error
            valores = (
                m['match_id'],
                fecha_dt,
                m['duration'],
                m['radiant_win'],
                str(m.get('game_mode', 'Unknown'))
            )
            
            try:
                cursor.execute(sql, valores)
                count += cursor.rowcount
            except Exception as e:
                print(f"❌ Error en match {m['match_id']}: {e}")
        
        conn.commit()
        print(f"💾 Se insertaron {count} nuevas partidas en la tabla Matches.")
        
        cursor.close()
        conn.close()
    else:
        print("❌ Error al conectar con la API")

if __name__ == "__main__":
    load_public_matches()