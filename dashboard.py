from flask import Flask
import sqlite3

app = Flask(__name__)
DB_FILE = "monitor.db"

def get_latest_readings(limit=10):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT timestamp, cpu, ram, disk FROM readings ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows

@app.route("/")
def home():
    rows = get_latest_readings()
    if not rows:
        return "<h1>No data yet. Run monitor.py first. </h1>"

    latest = rows[0]
    html = "<h1>Server Health Monitor</h1>"
    html += f"<h2>Latest reading ({latest[0]})</h2>"
    html += f"<p>CPU: {latest[1]}%</p>"
    html += f"<p>RAM: {latest[2]}%</p>"
    html += f"<p>Disk: {latest[3]}%</p>"

    html += "<h3>Recent readings</h3>"
    html += "<table border='1' cellpaddings= '6'>"
    html += "<tr><th>Time</th><th>CPU</th><th>RAM</th><th>Disk</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}%</td><td>{row[2]}%</td><td>{row[3]}%</td></tr>"
    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(debug=True)

