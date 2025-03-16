# HellLogger

This is a the craziest keylogger with 35 features designed to spy on everything short of your target's dreams. It’s stealthy and dumps to Discord and wipes itself clean after an hour.

## Features
1. **Stealth Mode**: Hides as `svchost_{random}.exe` (Windows) or `systemd_{random}` (Linux), no console.
2. **System Info Grab**: OS, username, RAM, IP, etc.
3. **Key Capture**: Logs every keystroke.
4. **Timestamp Logging**: When they type.
5. **Keystroke Frequency**: Keys per minute.
6. **Screenshots**: Grabs screen every minute.
7. **Discord Reporting**: Embed first, `.txt` logs every X keys (configurable).
8. **File Encryption**: Optional (not used here).
9. **Mouse Tracking**: Logs clicks and positions.
10. **Self-Destruct**: Deletes itself after set time (configurable).
11. **Audio Recording**: 10-second mic clips every 5 minutes.
12. **Browser History**: Fake URL dump (hourly).
13. **Network Traffic**: Basic IP log (every 5 minutes).
14. **Battery Status**: Power levels (if laptop).
15. **File Watcher**: New files in directory.
16. **Process List**: Top 10 running apps (hourly).
17. **Clipboard Image**: Screenshots as proxy (every 5 minutes).
18. **Voice Command**: Fake keyword log (every 10 minutes).
19. **Mouse Heatmap**: Movement density and speed (every 5 minutes).
20. **USB Devices**: Disks detected (every 5 minutes).
21. **Discord Token**: Fake token log (hourly).
22. **Game Activity**: Guesses games from processes (every 10 minutes).
23. **Crypto Wallet**: Fake wallet log (hourly).
24. **Location Ping**: IP geolocation.
25. **Fake Error**: Console-only error message (every 30 minutes).
26. **Key Combo Logger**: Flags hotkeys (e.g., Ctrl+C).
27. **Idle Detector**: Logs 5+ minute inactivity.
28. **Screenshot Trigger**: Snaps on Enter or keywords (configurable).
29. **Audio Burst Mode**: 5-second clips on loud noises.
30. **Mouse Speed Tracker**: Measures cursor speed.
31. **System Load Spike**: Logs CPU/RAM spikes.
32. **Fake Crash Bluescreen**: Prints fake BSOD (hourly).
33. **IP Change Detector**: Catches IP switches.
34. **Keystroke Pattern Analyzer**: Spots repeated sequences.
35. **Self-Replication**: Copies to backup folder.

## How to Use:
1. **Install**: Use *Install.bat* file to **install** all dependencies.
2. **Run**: Use *Start.bat* to **start** the keylogger.
3. **Check Discord**: Embeds their PC info first then `.txt` logs every 50 keys plus screenshots and audio.

## Change Webhook by conmfiguring it with `config.json` 

## Notes
- Some features (e.g., browser history, tokens) are simplified without specific libs.
- Cross-platform, but some features work best on Windows.
- **DO NOT USE FOR ILLEGAL PURPOSES**. This is for educational purposes only. Key loggers are illegal in many jurisdictions and can be used for malicious purposes. This code is for educational purposes only.
