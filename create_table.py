import mysql.connector

mydb = mysql.connector.connect(
	host = "remotemysql.com",
	user = "VWRnLTM6RW",
	password = "HdCZfdhdbw",
    database = "VWRnLTM6RW"
)

cursor = mydb.cursor()
cursor.execute("CREATE Table IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name varchar(55),email varchar(55), contact varchar(55), username varchar(55), password varchar(55));")