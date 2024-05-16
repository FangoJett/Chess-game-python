import sqlite3

connection = sqlite3.connect("game_data.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM game_data")
data = cursor.fetchall()

print(data)

connection.close()