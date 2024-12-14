BEGIN TRANSACTION;

-- CAUTION
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS APART_OF;
DROP TABLE IF EXISTS GROUPS;
DROP TABLE IF EXISTS SIGNED_OUT;
DROP TABLE IF EXISTS ITEMS;
DROP TABLE IF EXISTS CATEGORIES;

--TABLES
CREATE TABLE USERS(
  username text NOT NULL, 
  password text NOT NULL,
  primary key (username) 
);

CREATE TABLE APART_OF (
  username text NOT NULL, 
  groupName text NOT NULL,
  primary key (username,groupName), 
  FOREIGN KEY (username) REFERENCES USERS (username) ON DELETE CASCADE,
  FOREIGN KEY (groupName) REFERENCES GROUPS (groupName) ON DELETE CASCADE
);

CREATE TABLE GROUPS (
  accessLevel text NOT NULL,  -- Refers to the category code
  groupName text NOT NULL,
  primary key (groupName),
  FOREIGN KEY (accessLevel) REFERENCES CATEGORIES (catCode) ON DELETE CASCADE
);

CREATE TABLE SIGNED_OUT (
  username text NOT NULL, 
  SKU integer NOT NULL,
  date text NOT NULL, 
  signOutQty  integer NOT NULL,
  primary key (username,SKU, date), --look into adding date????
  FOREIGN KEY (username) REFERENCES USERS (username) ON DELETE CASCADE,
  FOREIGN KEY (SKU) REFERENCES ITEMS (SKU) ON DELETE CASCADE
);

CREATE TABLE ITEMS (
  SKU integer NOT NULL,
  itemQty integer NOT NULL, 
  itemTitle text NOT NULL, 
  itemDesc  text NOT NULL,
  catCode   text NOT NULL, --maybe look into adding filepath soon
  primary key (SKU),
  FOREIGN KEY (catCode) REFERENCES CATEGORIES (catCode) ON DELETE CASCADE
);

CREATE TABLE CATEGORIES(
  catCode text NOT NULL,
  catTitle text NOT NULL, 
  catDesc  text NOT NULL,
  primary key (catCode)
);

--USERS
--INSERT INTO USERS (username,password) VALUES('user','password');
INSERT INTO USERS (username,password) VALUES('user','pass');
INSERT INTO USERS (username,password) VALUES('user2','pass');

--CATEGORIES
--INSERT INTO CATEGORIES (catCode,catTitle,catDesc) VALUES('','','');
INSERT INTO CATEGORIES (catCode,catTitle,catDesc) VALUES('AAA','Tech','anything electronic');
INSERT INTO CATEGORIES (catCode,catTitle,catDesc) VALUES('AAC','Office','stuff for the office');
INSERT INTO CATEGORIES (catCode,catTitle,catDesc) VALUES('ABC','Stationary','pens, paper, etc.');
INSERT INTO CATEGORIES (catCode,catTitle,catDesc) VALUES('FOO','Food','any little snacks or food');

--APART_OF
--INSERT INTO APART_OF (username,groupName) VALUES('','');
INSERT INTO APART_OF (username,groupName) VALUES('user','admin');
INSERT INTO APART_OF (username,groupName) VALUES('user2','tech_access');
INSERT INTO APART_OF (username,groupName) VALUES('user2','office_access');
INSERT INTO APART_OF (username,groupName) VALUES('user2','stationary_access');

--GROUPS
--INSERT INTO GROUPS (accessLevel,groupName) VALUES('','');
INSERT INTO GROUPS (accessLevel,groupName) VALUES('000','admin');
INSERT INTO GROUPS (accessLevel,groupName) VALUES('AAA','tech_access');
INSERT INTO GROUPS (accessLevel,groupName) VALUES('AAC','office_access');
INSERT INTO GROUPS (accessLevel,groupName) VALUES('ABC','stationary_access');

--SIGNED_OUT
--INSERT INTO SIGNED_OUT (username,SKU,date,signOutQty) VALUES('','','','');
INSERT INTO SIGNED_OUT (username,SKU,date,signOutQty) VALUES('user','10000001','2024-12-01 11:11:11.100','1');
INSERT INTO SIGNED_OUT (username,SKU,date,signOutQty) VALUES('user','10000004','2024-11-04 09:10:21.100','4');

--ITEMS
--INSERT INTO ITEMS (SKU,itemQty,itemTitle,itemDesc,catCode) VALUES('','','','','');
INSERT INTO ITEMS (SKU, itemQty, itemTitle, itemDesc, catCode) 
VALUES(10000001, 1, 'Apple Laptop', '15-inch display, 8GB RAM, 256GB SSD', 'AAA');

INSERT INTO ITEMS (SKU, itemQty, itemTitle, itemDesc, catCode) 
VALUES(10000002, 5, 'Wireless Mouse', 'Ergonomic design with Bluetooth connectivity', 'AAA');

INSERT INTO ITEMS (SKU, itemQty, itemTitle, itemDesc, catCode) 
VALUES(10000003, 4, 'Office Chair', 'Adjustable height with lumbar support', 'AAC');

INSERT INTO ITEMS (SKU, itemQty, itemTitle, itemDesc, catCode) 
VALUES(10000004, 10, 'Notebook', '80 pages, ruled, 5x8 inches', 'ABC');

INSERT INTO ITEMS (SKU, itemQty, itemTitle, itemDesc, catCode) 
VALUES(10000005, 5, 'Apple', 'some boring ol apple', 'FOO');




COMMIT;