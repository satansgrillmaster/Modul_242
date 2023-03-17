drop table if exists task_log;
create table task_log (id INTEGER NOT NULL PRIMARY KEY,log_type varChar(20),log_message varChar(255));