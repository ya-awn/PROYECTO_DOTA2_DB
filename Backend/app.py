from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Función para conectar a la BD
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='DOTA_DB'
    )

@app.route('/')
def home():
    return jsonify({"mensaje": "Servidor de Dota 2 activo"})

# NUEVA RUTA: Ver estadísticas de un jugador
@app.route('/api/jugador/<int:account_id>')
def get_jugador_stats(account_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True) # dictionary=True devuelve los datos como JSON
        
        # Consulta SQL para traer las últimas partidas del jugador
        query = """
            SELECT m.Match_id, h.Localized_Name, mp.Kills, mp.Deaths, mp.Assists
            FROM Match_Players mp
            JOIN Matches m ON mp.Match_id = m.Match_id
            JOIN Heroes h ON mp.Hero_id = h.Hero_id
            WHERE mp.Account_id = %s
            ORDER BY m.Start_time DESC
            LIMIT 10;
        """
        cursor.execute(query, (account_id,))
        partidas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "account_id": account_id,
            "total_partidas_cargadas": len(partidas),
            "partidas": partidas
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


@app.route('/api/stats/top-heroes')
def get_top_heroes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Esta consulta cuenta cuántas veces aparece cada héroe y calcula el KDA promedio
        query = """
            SELECT 
                h.Localized_Name as heroe, 
                COUNT(*) as veces_jugado,
                ROUND(AVG(mp.Kills), 2) as promedio_kills,
                ROUND(AVG(mp.Deaths), 2) as promedio_muertes
            FROM Match_Players mp
            JOIN Heroes h ON mp.Hero_id = h.Hero_id
            GROUP BY h.Localized_Name
            ORDER BY veces_jugado DESC
            LIMIT 10;
        """
        cursor.execute(query)
        stats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500    