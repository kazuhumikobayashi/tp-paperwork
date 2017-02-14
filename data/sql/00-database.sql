create database if not exists tp_paperwork character set utf8;
create user 'admin_user' identified by 'admin_user';
grant all on tp_paperwork.* to 'admin_user';