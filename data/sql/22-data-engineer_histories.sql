insert into engineer_histories (engineer_id, receipt_start_day, receipt_end_day, receipt_per_month, receipt_rule, receipt_bottom_base_hour, receipt_top_base_hour, receipt_free_base_hour, receipt_per_hour, receipt_per_bottom_hour, receipt_per_top_hour, receipt_fraction, receipt_fraction_calculation1, receipt_fraction_calculation2, receipt_condition, remarks, created_at, created_user, updated_at, updated_user) values
  (5, '2016/9/1', '2016/11/30', 750000, 2, 120, 180, NULL, '1/120、1/180', 5000, 3750, 100, 3, 2, '自由入力（初期値は下記。●部分は支払サイトを参照し修正する必要あり。）発注者は、各月末日迄に請求書を受理し、●翌々月２０日●（金融機関が休みの場合は翌営業日）に銀行振込にて支払うものとする。但し、銀行振込手数料は受注者の負担とする。', '自由入力（初期値は下記。●の部分は修正する必要あり。）・月間作業時間を●150H～200H●とし、超減がある場合は、それぞれ上記の時間単価に超過あるいは欠業時間を乗じて当月請求時に調整する（●100円未満は切り捨て●）。・精算時間の単位は●0.25H●とする。', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
  (5, '2016/12/1', '2017/3/31', 750000, 2, 120, 180, NULL, '1/120、1/180', 5000, 3750, 100, 3, 2, '自由入力（初期値は下記。●部分は支払サイトを参照し修正する必要あり。）発注者は、各月末日迄に請求書を受理し、●翌々月２０日●（金融機関が休みの場合は翌営業日）に銀行振込にて支払うものとする。但し、銀行振込手数料は受注者の負担とする。', '自由入力（初期値は下記。●の部分は修正する必要あり。）・月間作業時間を●150H～200H●とし、超減がある場合は、それぞれ上記の時間単価に超過あるいは欠業時間を乗じて当月請求時に調整する（●100円未満は切り捨て●）。・精算時間の単位は●0.25H●とする。', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
  (5, '2017/4/1', '2017/7/31', 750000, 2, 120, 180, NULL, '1/120、1/180', 5000, 3750, 100, 3, 2, '自由入力（初期値は下記。●部分は支払サイトを参照し修正する必要あり。）発注者は、各月末日迄に請求書を受理し、●翌々月２０日●（金融機関が休みの場合は翌営業日）に銀行振込にて支払うものとする。但し、銀行振込手数料は受注者の負担とする。', '自由入力（初期値は下記。●の部分は修正する必要あり。）・月間作業時間を●150H～200H●とし、超減がある場合は、それぞれ上記の時間単価に超過あるいは欠業時間を乗じて当月請求時に調整する（●100円未満は切り捨て●）。・精算時間の単位は●0.25H●とする。', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');
