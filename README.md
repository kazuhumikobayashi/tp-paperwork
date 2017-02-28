TP営業事務
==============
<!-- [![Build Status](https://travis-ci.org//tp-paperwork.png?branch=master)](https://travis-ci.org//tp-paperwork) -->


Installation
------------
```
git clone https://ユーザー名@github.com/technoplan-inc/tp-paperwork
cd tp-paperwork
```


Database Setting
----------------------------
```
mysql -uroot -Dmysql -p******** < data/sql/00-database.sql
```


Initialize Data
----------------------------
```
mysql -uadmin_user -Dtp_paperwork -padmin_user < data/sql/00-database.sql
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
nosetests --cover-tests --with-coverage --cover-erase --cover-package=application --cover-branches
coverage html
```


Deploy
-----------------------------
```
gcloud app deploy
```