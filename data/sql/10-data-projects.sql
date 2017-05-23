insert into projects (project_name, status, recorded_department_id, sales_person, estimation_no, end_user_company_id, client_company_id, start_date, end_date, contract_form, billing_timing, estimated_total_amount, deposit_date, scope, contents, delivery_place, deliverables, inspection_date, responsible_person, quality_control, subcontractor, remarks, client_order_no, created_at, created_user, updated_at, updated_user) values
('A-PIM 下期改善', '01:契約開始', 1, '中沢', 'M17-17001', 6, 2, '2016-12-28', '2017-03-31', '請負契約（一括契約）', '契約期間末1回', 1000000, '2017-04-30', null, null, null, null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
('第一生命', '01:契約開始', 3, '小杉', 'M17-17002', 7, 3, '2016-12-28', '2017-03-31', '準委任契約', '契約期間末1回', 3000000, '2017-04-30', null, null, null, null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into assigned_members (project_id, seq_no, engineer_id, sales_unit_price, payment_unit_price, start_date, end_date, created_at, created_user, updated_at, updated_user) values
(1, 1, 1, 1000000, 750000, '2016-12-30', '2017-03-31', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
(1, 1, 2, 1000000, 750000, '2016-12-30', '2017-03-31', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into estimation_remarks (project_id, scope, contents, deliverables, delivery_place, inspection_date, responsible_person, quality_control, subcontractor, created_at, created_user, updated_at, updated_user) values
(1, '委託範囲', null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into order_remarks (project_id, order_no, order_amount, contents, responsible_person, subcontractor, scope, work_place, delivery_place, deliverables, inspection_date, payment_terms, billing_company_id, remarks, created_at, created_user, updated_at, updated_user) values
(1, null, null, '作業内容', null, null, null, null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');