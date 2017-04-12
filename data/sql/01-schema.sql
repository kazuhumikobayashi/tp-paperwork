DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tax;
DROP TABLE IF EXISTS estimation_sequence;
DROP TABLE IF EXISTS billings;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS project_attachments;
DROP TABLE IF EXISTS attachments;
DROP TABLE IF EXISTS engineer_skills;
DROP TABLE IF EXISTS engineer_business_categories;
DROP TABLE IF EXISTS assigned_members;
DROP TABLE IF EXISTS estimation_remarks;
DROP TABLE IF EXISTS order_remarks;
DROP TABLE IF EXISTS engineer_actual_results;
DROP TABLE IF EXISTS engineers;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS contract_forms;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS business_categories;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS statuses;


CREATE TABLE IF NOT EXISTS users (
  id INT NOT NULL AUTO_INCREMENT,
  shain_number VARCHAR(32) NOT NULL ,
  user_name VARCHAR(128) ,
  password VARCHAR(256) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE KEY (shain_number)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS engineers (
  id INT NOT NULL AUTO_INCREMENT,
  start_date DATE NOT NULL ,
  end_date DATE NOT NULL ,
  engineer_name VARCHAR(128),
  engineer_name_kana VARCHAR(128),
  company_id INT,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS engineer_skills (
  id INT NOT NULL AUTO_INCREMENT,
  engineer_id INT,
  skill_id INT,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS engineer_business_categories (
  id INT NOT NULL AUTO_INCREMENT,
  engineer_id INT,
  business_category_id INT,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS departments (
  id INT NOT NULL AUTO_INCREMENT,
  department_name VARCHAR(128) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS companies (
  id INT NOT NULL AUTO_INCREMENT,
  company_code VARCHAR(32) NOT NULL ,
  company_name VARCHAR(128) ,
  company_name_kana VARCHAR(128) ,
  trade_name VARCHAR(32) ,
  trade_name_position CHAR(1) ,
  client_flg CHAR(1) NOT NULL DEFAULT '0' ,
  consignment_flg CHAR(1) NOT NULL DEFAULT '0' ,
  start_date DATE NOT NULL ,
  end_date DATE NOT NULL ,
  postal_code VARCHAR(32) ,
  address1 VARCHAR(1024) ,
  address2 VARCHAR(1024) ,
  phone VARCHAR(32) ,
  fax VARCHAR(32) ,
  payment_site INT ,
  receipt_site INT ,
  tax CHAR(1) NOT NULL DEFAULT '0',
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS tax (
  id INT NOT NULL AUTO_INCREMENT,
  start_date DATE NOT NULL ,
  end_date DATE NOT NULL ,
  tax_rate DECIMAL(6,2),
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS projects (
  id INT NOT NULL AUTO_INCREMENT,
  project_name VARCHAR(128) NOT NULL ,
  end_user VARCHAR(128) ,
  client_company_id INT NOT NULL ,
  start_date DATE NOT NULL ,
  end_date DATE NOT NULL ,
  recorded_department_id INT NOT NULL ,
  over_time_calculation_id INT NOT NULL ,
  contract_form_id INT ,
  estimation_no VARCHAR(64) ,
  status_id INT NOT NULL,
  billing_timing CHAR(1) ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS engineer_actual_results (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  result_month DATE NOT NULL ,
  seq_no INT NOT NULL ,
  engineer_id INT NOT NULL ,
  fixed_flg CHAR(1) NOT NULL DEFAULT '0',
  working_hours DECIMAL(5,2) ,
  adjustment_hours DECIMAL(5,2) ,
  billing_amount INT ,
  billing_adjustment_amount INT ,
  payment_amount INT ,
  payment_adjustment_amount INT ,
  carfare INT ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS billings (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  billing_month DATE NOT NULL ,
  billing_amount INT ,
  billing_adjustment_amount INT ,
  tax INT ,
  carfare INT ,
  scheduled_billing_date DATE ,
  billing_date DATE ,
  bill_output_date DATE ,
  scheduled_payment_date DATE ,
  payment_date DATE ,
  status INT ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS payments (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  payment_month DATE NOT NULL ,
  engineer_id INT ,
  payment_amount INT ,
  payment_adjustment_amount INT ,
  tax INT ,
  carfare INT ,
  scheduled_payment_date DATE ,
  payment_date DATE ,
  status INT ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS assigned_members (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  seq_no INT NOT NULL ,
  engineer_id INT NOT NULL ,
  sales_unit_price INT NOT NULL ,
  payment_unit_price INT NOT NULL ,
  start_date DATE NOT NULL ,
  end_date DATE NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS estimation_remarks (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  scope VARCHAR(1024) ,
  contents VARCHAR(1024) ,
  deliverables VARCHAR(1024) ,
  delivery_place VARCHAR(1024) ,
  inspection_date DATE ,
  responsible_person VARCHAR(128) ,
  quality_control VARCHAR(128) ,
  subcontractor VARCHAR(128) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS order_remarks (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  order_no VARCHAR(64) ,
  order_amount INT ,
  contents VARCHAR(1024) ,
  responsible_person VARCHAR(128) ,
  subcontractor VARCHAR(128) ,
  scope VARCHAR(1024) ,
  work_place VARCHAR(1024) ,
  delivery_place VARCHAR(1024) ,
  deliverables VARCHAR(1024) ,
  inspection_date DATE ,
  payment_terms VARCHAR(1024) ,
  billing_company_id INT ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS project_attachments (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  attachment_id INT NOT NULL ,
  type CHAR(1) NOT NULL ,
  remarks VARCHAR(256) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS skills (
  id INT NOT NULL AUTO_INCREMENT,
  skill_name VARCHAR(32) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE KEY (skill_name)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS business_categories (
  id INT NOT NULL AUTO_INCREMENT,
  business_category_name VARCHAR(32) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE KEY (business_category_name)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS attachments (
  id INT NOT NULL AUTO_INCREMENT,
  filename VARCHAR(256) NOT NULL ,
  storage_filename VARCHAR(256) NOT NULL ,
  size INT NOT NULL ,
  content_type VARCHAR(256) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS statuses (
  id INT NOT NULL ,
  status_name VARCHAR(32) NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS contract_forms (
  id INT NOT NULL ,
  contract_form_name VARCHAR(32) NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS estimation_sequence (
  id INT NOT NULL AUTO_INCREMENT ,
  fiscal_year INT NOT NULL ,
  sequence INT NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;