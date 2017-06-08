DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS estimation_sequence;
DROP TABLE IF EXISTS project_attachments;
DROP TABLE IF EXISTS attachments;
DROP TABLE IF EXISTS engineer_skills;
DROP TABLE IF EXISTS engineer_business_categories;
DROP TABLE IF EXISTS engineers;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS business_categories;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS banks;
DROP TABLE IF EXISTS company_client_flags;
DROP TABLE IF EXISTS engineer_histories;
DROP TABLE IF EXISTS holidays;
DROP TABLE IF EXISTS project_details;
DROP TABLE IF EXISTS project_billings;
DROP TABLE IF EXISTS project_months;


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
  engineer_name VARCHAR(128) NOT NULL,
  engineer_name_kana VARCHAR(128),
  birthday DATE,
  gender INT,
  company_id INT NOT NULL,
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
  group_name VARCHAR(128) NOT NULL ,
  department_name VARCHAR(128) NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS companies (
  id INT NOT NULL AUTO_INCREMENT,
  company_name VARCHAR(128) NOT NULL ,
  company_name_kana VARCHAR(128) ,
  company_short_name VARCHAR(128) ,
  contract_date DATE ,
  postal_code VARCHAR(32) ,
  address VARCHAR(1024) ,
  phone VARCHAR(32) ,
  fax VARCHAR(32) ,
  client_code VARCHAR(128) ,
  bp_code VARCHAR(128) ,
  billing_site INT ,
  payment_site INT ,
  billing_tax INT ,
  payment_tax INT ,
  bank_id INT,
  bank_holiday_flag INT ,
  remarks VARCHAR(1024) ,
  print_name VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS projects (
  id INT NOT NULL AUTO_INCREMENT,
  project_name VARCHAR(128) NOT NULL ,
  project_name_for_bp VARCHAR(128) ,
  status INT ,
  recorded_department_id INT ,
  sales_person VARCHAR(128) ,
  estimation_no VARCHAR(64) ,
  end_user_company_id INT ,
  client_company_id INT ,
  start_date DATE ,
  end_date DATE ,
  contract_form INT ,
  billing_timing INT ,
  estimated_total_amount INT ,
  deposit_date DATE ,
  scope VARCHAR(1024) ,
  contents VARCHAR(1024) ,
  working_place VARCHAR(1024) ,
  delivery_place VARCHAR(1024) ,
  deliverables VARCHAR(1024) ,
  inspection_date DATE ,
  responsible_person VARCHAR(128) ,
  quality_control VARCHAR(128) ,
  subcontractor VARCHAR(128) ,
  remarks VARCHAR(1024) ,
  client_order_no VARCHAR(64) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE KEY (estimation_no)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS project_details (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  detail_type INT NOT NULL,
  work_name VARCHAR(128) ,
  engineer_id INT ,
  billing_money INT ,
  remarks VARCHAR(1024) ,
  billing_start_day DATE ,
  billing_end_day DATE ,
  billing_per_month INT ,
  billing_rule INT ,
  billing_bottom_base_hour INT ,
  billing_top_base_hour INT ,
  billing_free_base_hour VARCHAR(128) ,
  billing_per_hour VARCHAR(128) ,
  billing_per_bottom_hour INT ,
  billing_per_top_hour INT ,
  billing_fraction INT ,
  billing_fraction_calculation1 INT ,
  billing_fraction_calculation2 INT ,
  bp_order_no VARCHAR(64) ,
  client_order_no_for_bp VARCHAR(64) ,
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
  type INT NOT NULL ,
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


CREATE TABLE IF NOT EXISTS banks (
  id INT NOT NULL AUTO_INCREMENT ,
  bank_name VARCHAR(32) NOT NULL ,
  text_for_document VARCHAR(128) NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS company_client_flags (
  id INT NOT NULL AUTO_INCREMENT ,
  company_id INT NOT NULL ,
  client_flag INT NOT NULL ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS engineer_histories (
  id INT NOT NULL AUTO_INCREMENT,
  engineer_id INT NOT NULL ,
  payment_start_day DATE NOT NULL ,
  payment_end_day DATE NOT NULL ,
  payment_per_month INT NOT NULL ,
  payment_rule INT NOT NULL ,
  payment_bottom_base_hour INT ,
  payment_top_base_hour INT ,
  payment_free_base_hour VARCHAR(128) ,
  payment_per_hour VARCHAR(128) ,
  payment_per_bottom_hour INT ,
  payment_per_top_hour INT ,
  payment_fraction INT ,
  payment_fraction_calculation1 INT ,
  payment_fraction_calculation2 INT ,
  payment_condition VARCHAR(1024) ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;


CREATE TABLE IF NOT EXISTS holidays (
  id INT NOT NULL AUTO_INCREMENT ,
  holiday DATE NOT NULL ,
  holiday_name VARCHAR(128) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id) ,
  UNIQUE KEY (holiday)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS project_billings (
  id INT NOT NULL AUTO_INCREMENT,
  project_detail_id INT NOT NULL ,
  billing_month DATE NOT NULL ,
  billing_content VARCHAR(128) ,
  billing_amount VARCHAR(128) ,
  billing_confirmation_money INT ,
  remarks VARCHAR(1024) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;

CREATE TABLE IF NOT EXISTS project_months (
  id INT NOT NULL AUTO_INCREMENT,
  project_id INT NOT NULL ,
  project_month DATE NOT NULL ,
  result_input_flag INT ,
  billing_input_flag INT ,
  deposit_input_flag INT ,
  deposit_date DATE ,
  billing_estimated_money INT ,
  billing_confirmation_money  INT ,
  billing_transportation INT ,
  remarks VARCHAR(1024) ,
  client_billing_no VARCHAR(64) ,
  created_at DATETIME NOT NULL ,
  created_user VARCHAR(128) NOT NULL ,
  updated_at DATETIME NOT NULL ,
  updated_user VARCHAR(128) NOT NULL ,
  PRIMARY KEY (id)
) ENGINE = INNODB;
