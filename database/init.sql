drop table if exists task_log;
create table task_log (
    id INTEGER NOT NULL PRIMARY KEY,
    request_info_lvl varChar(20),
    log_message varChar(255),
    request_ip varchar(64)
                      );

drop table if exists led_color;
create table led_color (
    id INTEGER NOT NULL PRIMARY KEY,
    description varChar(255),
    r int,
    g int,
    b int
                      );
insert into led_color (id, description, r, g, b) values (1, 'blue', 0, 0, 255);

drop table if exists halo_ring_config;
create table halo_ring_config (
    id INTEGER NOT NULL PRIMARY KEY,
    address varChar(255) unique,
    client_id varchar(64),
    led_color_idfk int,
    FOREIGN KEY (led_color_idfk) REFERENCES led_color(id)
                      );
