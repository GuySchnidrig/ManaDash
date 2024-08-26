# importing required libraries
import mysql.connector

con = mysql.connector.connect(
host ="GuySchnidrig.mysql.pythonanywhere-services.com",
user ="GuySchnidrig",
passwd ="5ETB9t.z7MAg6Nc",
database = "GuySchnidrig$commander"
)

# preparing a cursor object
cursorObject = con.cursor()

query = "SELECT * FROM player_names"
cursorObject.execute(query)

myresult = cursorObject.fetchall()

for x in myresult:
	print(x)

# disconnecting from server
con.close()
