insert into calculations (calculation_name, amount, formula, created_at, created_user, updated_at, updated_user) values
 ('10円未満切り捨て', 10, 1, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
 ('10円以下切り捨て', 10, 2, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
 ('100円を超える場合切り上げ', 100, 3, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
 ('100円以上切り上げ', 100, 4, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
 ('100円単位四捨五入', 100, 5, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');
