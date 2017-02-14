insert into projects (project_name, end_user, client_company_id, start_date, end_date, recorded_department_id, over_time_calculation_id, contract_form_id, estimation_no, status_id, billing_timing, remarks, created_at, created_user, updated_at, updated_user) values
('A-PIM 下期改善', '味の素', 1, '2016-12-28', '2017-03-31', 1, 1, 1, 'M17-17001', 1, '1', null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
('第一生命', NULL , 3, '2016-12-28', '2017-03-31', 4, 1, 2, 'M17-17002', 1, '2', null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into assigned_members (project_id, seq_no, engineer_id, sales_unit_price, payment_unit_price, start_date, end_date, created_at, created_user, updated_at, updated_user) values
(1, 1, 1, 1000000, 750000, '2016-12-30', '2017-03-31', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴'),
(1, 1, 2, 1000000, 750000, '2016-12-30', '2017-03-31', CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into estimation_remarks (project_id, scope, contents, deliverables, delivery_place, inspection_date, responsible_person, quality_control, subcontractor, created_at, created_user, updated_at, updated_user) values
(1, '委託範囲', null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');

insert into order_remarks (project_id, order_no, order_amount, contents, responsible_person, subcontractor, scope, work_place, delivery_place, deliverables, inspection_date, payment_terms, billing_company_id, remarks, created_at, created_user, updated_at, updated_user) values
(1, null, null, '作業内容', null, null, null, null, null, null, null, null, null, null, CURRENT_TIMESTAMP, '竹内大貴', CURRENT_TIMESTAMP, '竹内大貴');