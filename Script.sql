SHOW databases;

USE bot_db;

CREATE TABLE draws
(
	num_draw VARCHAR(10),
	date_drw DATE,
	program VARCHAR(30),
	num_invitations INT,
	score INT
);

CREATE TABLE reddit
(
	comment_id VARCHAR(10),
	replied_at DATETIME
)
