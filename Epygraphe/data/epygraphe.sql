PRAGMA encoding = 'UTF-8';
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	`user_id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_nom`	TINYTEXT NOT NULL,
	`user_prenom`	TINYTEXT NOT NULL,
	`user_login`	VARCHAR ( 45 ) NOT NULL,
	`user_email`	TINYTEXT NOT NULL,
	`user_password`	VARCHAR ( 45 ) NOT NULL,
	`user_is_admin`	BOOLEAN NOT NULL DEFAULT 0,
	`user_is_mod`	BOOLEAN NOT NULL DEFAULT 0,
	`user_last_seen`	DATETIME DEFAULT current_timestamp
);
DROP TABLE IF EXISTS `inscription`;
CREATE TABLE IF NOT EXISTS `inscription` (
	`inscription_id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`inscription_texte`	TEXT,
	`inscription_lieu`	VARCHAR ( 45 ),
	`inscription_no_hd`	VARCHAR ( 6 ),
	`inscription_language`	VARCHAR ( 45 ),
	`inscription_type`	VARCHAR ( 45 ),
	`inscription_date`	VARCHAR ( 45 )
);
DROP TABLE IF EXISTS `version`;
CREATE TABLE IF NOT EXISTS `version` (
	`version_id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`version_text`	TEXT,
	`version_inscription_id`	integer NOT NULL,
	`version_user_id`	integer NOT NULL,
	FOREIGN KEY(version_inscription_id) REFERENCES inscription(inscription_id),
	FOREIGN KEY(version_user_id) REFERENCES user(user_id)
);
DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
	`comment_id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`comment_inscription_id`	integer NOT NULL,
	`comment_user_id`	integer NOT NULL,
	`comment_date`	DATETIME DEFAULT current_timestamp,
	`comment_text`	TEXT,
	FOREIGN KEY(comment_inscription_id) REFERENCES inscription(inscription_id),
	FOREIGN KEY(comment_user_id) REFERENCES user(user_id)
);

INSERT INTO `user` (`user_id`, `user_nom`, `user_prenom`, `user_login`, `user_email`, `user_password`, `user_is_admin`, `user_is_mod`) VALUES (0, 'admin', 'admin', 'admin', 'admin@admin.com', 'admin', TRUE, FALSE);