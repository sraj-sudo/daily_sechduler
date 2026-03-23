from db import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("shivesh", "1234"))

conn.commit()
conn.close()