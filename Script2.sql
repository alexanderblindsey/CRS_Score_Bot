SELECT draw_num
FROM bot_db.Draws 
WHERE draw_num = (SELECT MAX(draw_num)
				  FROM bot_db.Draws)