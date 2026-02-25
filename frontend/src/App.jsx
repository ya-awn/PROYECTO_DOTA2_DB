import { useState } from 'react'
import axios from 'axios'

function App() {
  const [accountId, setAccountId] = useState('')
  const [datos, setDatos] = useState(null)
  const [error, setError] = useState(null)

  const buscarJugador = async () => {
    try {
      setError(null)
      // Llamamos a TU servidor Flask
      const res = await axios.get(`http://127.0.0.1:5000/api/jugador/${accountId}`)
      setDatos(res.data)
    } catch {
      setError("No se encontró el jugador o el servidor está apagado")
      setDatos(null)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#1a1a1a', color: 'white', minHeight: '100vh' }}>
      <h1>Dota 2 Dashboard 🎮</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <input 
          type="text" 
          placeholder="Ingresá Account ID (ej: 61374303)" 
          value={accountId}
          onChange={(e) => setAccountId(e.target.value)}
          style={{ padding: '10px', borderRadius: '5px', border: 'none', marginRight: '10px' }}
        />
        <button onClick={buscarJugador} style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: '#646cff', color: 'white', border: 'none', borderRadius: '5px' }}>
          Buscar
        </button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {datos && (
        <div style={{ backgroundColor: '#2a2a2a', padding: '20px', borderRadius: '10px' }}>
          <h2>Resultados para ID: {datos.account_id}</h2>
          <p>Partidas encontradas: {datos.total_partidas_cargadas}</p>
          
          <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
            <thead>
              <tr style={{ backgroundColor: '#333' }}>
                <th>Héroe</th>
                <th>Kills</th>
                <th>Deaths</th>
                <th>Assists</th>
              </tr>
            </thead>
            <tbody>
              {datos.partidas.map((p, index) => (
                <tr key={index} style={{ textAlign: 'center' }}>
                  <td>{p.Localized_Name}</td>
                  <td style={{ color: '#4caf50' }}>{p.Kills}</td>
                  <td style={{ color: '#f44336' }}>{p.Deaths}</td>
                  <td>{p.Assists}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default App