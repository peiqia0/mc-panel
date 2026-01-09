from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from mcrcon import MCRcon
import psutil, os, queue, threading
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")

RCON_HOST = "127.0.0.1"
RCON_PORT = 25575
RCON_PASSWORD = os.environ.get("RCON_PASSWORD")

# Simple credentials (move to env vars if you prefer)
LOGIN_USER = os.environ.get("PANEL_USER", "admin")
LOGIN_PASS = os.environ.get("PANEL_PASS", "password")

command_queue = queue.Queue()
response_queue = queue.Queue()

# ---------- auth helpers ----------

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

# ---------- routes ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if user == LOGIN_USER and pw == LOGIN_PASS:
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/api/command", methods=["POST"])
@login_required
def send_command():
    cmd = request.json.get("command")
    if not cmd:
        return jsonify({"error": "No command"}), 400

    command_queue.put(cmd)
    response = response_queue.get()
    return jsonify({"output": response})

@app.route("/api/stats")
@login_required
def stats():
    mem = psutil.virtual_memory()
    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_used": round(mem.used / 1024 / 1024, 1),
        "ram_total": round(mem.total / 1024 / 1024, 1),
        "ram_percent": mem.percent
    })

# ---------- RCON loop ----------

def main_rcon_loop():
    with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
        while True:
            try:
                cmd = command_queue.get()
                result = mcr.command(cmd)
                response_queue.put(result)
            except Exception as e:
                response_queue.put(f"Error: {e}")

# ---------- entry ----------

if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(host="0.0.0.0", port=8000, debug=False, threaded=True),
        daemon=True
    ).start()

    main_rcon_loop()
