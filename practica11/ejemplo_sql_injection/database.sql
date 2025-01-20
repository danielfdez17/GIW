BEGIN TRANSACTION;

CREATE TABLE users (
  email text primary key,
  country text not null,
  password text not null
);
INSERT INTO users VALUES ('pepe@gmail.com', 'Spain', '$pbkdf2-sha256$29000$YeydEwLgXKvV2psTwjhHSA$WFI6IHZKbSocJ/xKKe4HkBu7KyZXKEq/X0LwxSnDd0c');
INSERT INTO users VALUES ('eva@yahoo.es', 'France', '$pbkdf2-sha256$29000$4byXUqp1DiHEOKfU.h8DQA$j0tTFKulO0Cdh/HmqFQ4TOgp.YPe3PbqdBE94ixI.ms');


CREATE TABLE orders (
  id integer primary key,
  user text references users(email),
  item text
);
INSERT INTO orders VALUES(0,'pepe@gmail.com','silla');
INSERT INTO orders VALUES(1,'pepe@gmail.com','mesa');
INSERT INTO orders VALUES(2,'eva@yahoo.es','cohete');
INSERT INTO orders VALUES(3,'eva@yahoo.es','catapulta');
INSERT INTO orders VALUES(4,'eva@yahoo.es','botella');

COMMIT;
