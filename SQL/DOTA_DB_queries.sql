-- Archivo para hacer consultas sin riesgo
USE DOTA_DB;

-- Ver primeros 10 héroes
SELECT * FROM Heroes LIMIT 10;

-- Contar total de héroes
SELECT COUNT(*) as total_heroes FROM Heroes;

-- Ver héroes por atributo
SELECT Primary_Attr, COUNT(*) as cantidad FROM Heroes GROUP BY Primary_Attr;



-- ¿Cuántas partidas tenemos?
SELECT COUNT(*) as total_matches FROM Matches;

-- ¿Cuántas tienen jugadores cargados?
SELECT COUNT(DISTINCT match_id) as matches_con_jugadores FROM Match_Players;

-- ¿El LEFT JOIN encuentra partidas sin jugadores?
SELECT m.match_id FROM Matches m 
LEFT JOIN Match_Players mp ON m.match_id = mp.match_id 
WHERE mp.match_id IS NULL 
LIMIT 5;


SELECT p.Persona_Name, mp.Kills, h.Localized_Name 
FROM Match_Players mp
JOIN Players p ON mp.Account_id = p.Account_id
JOIN Heroes h ON mp.Hero_id = h.Hero_id
ORDER BY mp.Kills DESC 
LIMIT 5;