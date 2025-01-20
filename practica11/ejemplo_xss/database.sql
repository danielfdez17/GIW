BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `firmas` (
	`id`	INTEGER,
	`texto`	TEXT,
	`fecha`	TEXT DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
);
INSERT INTO `firmas` (id,texto,fecha) VALUES (1,'Una experiencia inolvidable -- María','2022-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (2,'Espectacular! -- Juan','2021-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (3,'Un poco caro, no? -- Sr. Agarrado','2020-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (4,'Me lo cuentan y no me lo creo! -- Eva','2019-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (5,'Decepcionante... -- Inés','2018-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (6,'pa k kieres saber eso jaja saludos -- Don Youtuber','2017-12-16 09:37:11');
INSERT INTO `firmas` (id,texto,fecha) VALUES (7,'Hola -- Enrique','2015-12-22 14:26:01');
INSERT INTO `firmas` (id,texto,fecha) VALUES (8,'Me gustó mucho -- Luis','2014-12-22 14:26:13');
INSERT INTO `firmas` (id,texto,fecha) VALUES (9,'No me gusta <script>alert("XSS persistente")</script>','2005-12-22 14:28:56');
INSERT INTO `firmas` (id,texto,fecha) VALUES (10,'Fatal -- Pedro','2002-12-22 14:32:27');
COMMIT;
