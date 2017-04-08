TP営業事務
==============
[![wercker status](https://app.wercker.com/status/1d08c3dd2718861b36c1680c228dfb92/s/master "wercker status")](https://app.wercker.com/project/byKey/1d08c3dd2718861b36c1680c228dfb92)
[![codecov](https://codecov.io/gh/technoplan-inc/tp-paperwork/branch/master/graph/badge.svg?token=SU2rTsmyVx)](https://codecov.io/gh/technoplan-inc/tp-paperwork)

Installation
------------
```
git clone https://ユーザー名@github.com/technoplan-inc/tp-paperwork
cd tp-paperwork
pip install -r requirements.txt
```


Database Setting
----------------------------
```
mysql -uroot -Dmysql -p******** < data/sql/00-database.sql
```
エラーになったら、sqlを書き換える。  
① 'admin_user'の後ろに@'localhost'をつける。  
```mysql
create database if not exists tp_paperwork character set utf8;
create user 'admin_user'@'localhost' identified by 'admin_user';
grant all on tp_paperwork.* to 'admin_user'@'localhost';
create database if not exists tp_paperwork_test character set utf8;
create user 'admin_user_test'@'localhost' identified by 'admin_user_test';
grant all on tp_paperwork_test.* to 'admin_user_test'@'localhost';
```

② passwordの桁数エラーだったら、以下のSQLを実行
```mysql
mysql> SET GLOBAL validate_password_length=4;
mysql> SET GLOBAL validate_password_policy=LOW;
```


Initialize Data
----------------------------
```
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/01-schema.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/02-data-users.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/03-data-statuses.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/04-data-skills.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/05-data-departments.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/06-data-tax.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/07-data-engineers.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/08-data-companies.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/09-data-engineer_skills.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/10-data-projects.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/11-data-contract_forms.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/12-data-calculations.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/13-data-engineer_actual_results.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/14-data-estimation_sequence.sql
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/15-data-attachments.sql
```


Run Server
----------------------------
```
python runserver.py
```
Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) (Press CTRL+C to quit)


Run Test
-----------------------------
```
nosetests --cover-tests --with-coverage --cover-erase --cover-package=application --cover-branches -v
coverage html
```


Deploy
-----------------------------
```
gcloud app deploy
```
