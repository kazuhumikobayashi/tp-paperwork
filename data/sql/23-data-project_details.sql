insert into project_details (project_id, detail_type, work_name, engineer_id, billing_money, remarks, billing_start_day, billing_end_day, billing_per_month, billing_rule, billing_bottom_base_hour, billing_top_base_hour, billing_free_base_hour, billing_per_hour, billing_per_bottom_hour, billing_per_top_hour, billing_fraction, billing_fraction_rule, created_at, created_user, updated_at, updated_user) values
  (1, 1, NULL, 1, 2000000, '2人月（1,000,000×2）', '2016/9/1', '2016/11/30', 750000, 2, 120, 180, NULL, '1/120、1/180', 5000, 3750, 100, 2, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
  (1, 1, NULL, 2, 2000000, '2人月（1,000,000×2）', '2016/9/1', '2016/11/30', 750000, 2, 120, 180, NULL, '1/120、1/180', 5000, 3750, 100, 2, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');
