-- Archivo para hacer consultas sin riesgo
USE DOTA_DB;

-- Ver primeros 10 héroes
SELECT * FROM Heroes LIMIT 10;

-- Contar total de héroes
SELECT COUNT(*) as total_heroes FROM Heroes;

-- Ver héroes por atributo
SELECT Primary_Attr, COUNT(*) as cantidad FROM Heroes GROUP BY Primary_Attr;