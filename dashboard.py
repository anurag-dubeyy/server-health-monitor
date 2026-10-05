from flask import Flask
import sqlite3

app = Flask(__name__)
DB_FILE = "monitor.db"
CPU_LIMIT = 80
RAM_LIMIT = 90
DISK_LIMIT = 85

def get_latest_readings(limit=10):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT timestamp, cpu, ram, disk FROM readings ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return rows
def card(label, value, limit):
    css =  "warn" if value > limit else "ok"
    return f"<div class='card'><div class='label'>{label}</div><div class='value {css}' > {value}%</div></div>"

@app.route("/")
def home():
    rows = get_latest_readings()
    if not rows:
        return "<h1>No data yet. Run monitor.py first. </h1>"

    latest = rows[0]
    html = """
    <html><head>
    <meta http-equiv='refresh' content='5'>
    <title>Server Health Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; background:#0f172a; color: #e2e8f0; padding: 30px; }
        h1 { margin-bottom: 4px; }
        .sub { color: #94a3b8; margin-bottom: 24px; }
        .cards { display: flex; gap: 16px; margin-bottom: 30px; }
        .card { background: #1e293b; padding: 20px 28px; border-radius: 10px; min-width: 140px; text-align: center; }
        .label { color: #94a3b8; font-size: 14px; }
        .value { font-size: 32px; font-weight: bold; }
        .ok { color: #4ade80; }
        .warn { color: #f87171; }
        table { border-collapse: collapse; background: #1e293b; width: 100%; }
        th, td { padding: 10px 18px; text-align: left; border-bottom: 1px solid #334155; color: #facc15; }
        th {color: #facc15; }
    </style></head><body>
       """
    html += "<h1>Server Health Monitor</h1>"
    html += f"<div class='sub'>Latest updated: {latest[0]} (refreshes every 5 seconds)</div>"
    html += "<div class='cards'>"
    html += card("CPU ", latest[1], CPU_LIMIT)
    html += card("RAM ", latest[2], RAM_LIMIT)
    html += card("Disk ", latest[3], DISK_LIMIT)
    html += "</div>"

    html += "<h3>Recent Readings</h3>"
    html += "<table><tr><th>Time</th><th>CPU</th><th>RAM</th><th>Disk</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}%</td><td>{row[2]}%</td><td>{row[3]}%</td></tr>"
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    app.run(debug=True)

