from sqlalchemy import create_engine
import os	
dbName = "sndb.db"
if os.path.exists(dbName):
	os.remove(dbName)
e = create_engine("sqlite:///{}".format(dbName))
e.execute("""
	create table accounts (
		id integer primary key,
		login varchar,
		password varchar,
		name varchar,
		lastname varchar,
		age bigint,
		city varchar,
		avatar varchar			
	)""")

e.execute("""
	create table photos (
		id integer primary key,
		accountId bigint,
		path varchar,
		FOREIGN KEY(accountId) REFERENCES accounts(id)						
	)""")

e.execute("""
	create table friendships (		
		accountId bigint,
		friendId bigint,
		messagePath varchar,
		messageLocPath varchar,
		FOREIGN KEY(accountId) REFERENCES accounts(id),
		FOREIGN KEY(friendId) REFERENCES accounts(id)						
	)""")
e.execute("""
	create table friendrequests (		
		accountId bigint,
		friendId bigint,
		FOREIGN KEY(accountId) REFERENCES accounts(id),
		FOREIGN KEY(friendId) REFERENCES accounts(id)						
	)""")
