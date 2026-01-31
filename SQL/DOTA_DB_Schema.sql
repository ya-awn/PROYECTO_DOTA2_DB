-- ESTE SCRIPT SOLO SE EJECUTA 1 VEZ
CREATE DATABASE IF NOT EXISTS DOTA_DB;
USE DOTA_DB;

-- Informacion sobre los heroes
CREATE TABLE Heroes(
Hero_id INT PRIMARY KEY ,
Name VARCHAR(250),
Localized_Name VARCHAR(100),
Primary_Attr VARCHAR(100)
);

-- Informacion sobre los jugadores
CREATE TABLE Players(
Account_id BIGINT PRIMARY KEY,
Persona_Name VARCHAR(250),
Avatar_url varchar(250)
);

-- Informacion sobre las partidas
CREATE TABLE Matches(
Match_id BIGINT PRIMARY KEY,
Start_time DATETIME,
Duration INT,
Radiant_win boolean,
Game_Mode VARCHAR(100)
);

-- informacion de estadisticas de la partida del jugador
CREATE TABLE Match_Players(
id INT AUTO_INCREMENT PRIMARY KEY,
Match_id BIGINT,
Account_id BIGINT,
Hero_id INT,
Kills INT,
Deaths INT,
Assists INT,
FOREIGN KEY (Match_id) REFERENCES Matches(Match_id),
FOREIGN KEY (Account_id) REFERENCES Players(Account_id),
FOREIGN KEY (Hero_id) REFERENCES Heroes(Hero_id)
);

CREATE INDEX idx_match_start_time ON Matches(Start_time);
CREATE INDEX idx_match_players_account ON Match_Players(Account_id);
CREATE INDEX idx_match_players_hero ON Match_Players(Hero_id);


SELECT * FROM Match_Players;


SELECT * FROM Heroes LIMIT 10;






























