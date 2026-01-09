# mc-panel

An online, interactive control panel for managing a Minecraft server.

This project provides a simple web interface to:
- Send commands to a Minecraft server via RCON
- View live console output
- Monitor basic system statistics (CPU and RAM usage)

The goal of this project is to keep the panel lightweight, self-hosted, and easy to extend.

## Features

- RCON command execution
- Live command output
- Session-based login protection
- Dark, minimal UI

## Tech Stack

- Python (Flask)
- HTML + JavaScript (no frontend framework)
- RCON (`mcrcon`)
- `psutil`

## Setup

### Requirements

- Python 3.9+
- A running Minecraft server with RCON enabled

### Install dependencies

```bash
pip install flask mcrcon psutil
```
### Environment variables
```bash
export RCON_PASSWORD="your_rcon_password"
export FLASK_SECRET_KEY="a_long_random_secret"
export PANEL_USER="admin"
export PANEL_PASS="strong_password"
```
### Run
```bash
python3 app.py
```
then open
```
http://localhost:8000
```
### Project Status
This project is in early development, if you find any bugs report an issue on github. (the website was pulled off an old project so it looks bad)
