CREATE TABLE bot_db.draws
(
	draw_num INT,
	draw_date VARCHAR(100),
	program VARCHAR(100),
	num_inv INT,
	score INT
);

CREATE TABLE bot_db.reddit
(
	comment_id VARCHAR(10),
	replied_at DATETIME
);
