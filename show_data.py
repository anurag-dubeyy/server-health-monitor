import sqlite3

conn = sqlite3.connect("monitor.db")
rows = conn.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 5").fetchall()
for row in rows:
    print(row)
conn.close()    