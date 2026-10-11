# Device Heartbeat Geo-Mapper

## Project Overview

The Device Heartbeat Geo-Mapper is a real-time monitoring system that tracks devices based on periodic “heartbeat” signals and displays their locations on an interactive map.

Each device sends:
- ID
- Latitude & Longitude
- Status

The system visualizes this data live on a map.

---

## Real-World Applications

- IoT monitoring
- Server infrastructure tracking
- Fleet tracking (GPS)
- Network monitoring
- Smart systems supervision

---

## How It Works

Devices send a POST request:

POST /heartbeat

Backend:
- saves device
- updates last_seen timestamp
- determines online/offline

Online = heartbeat < 5s  
Offline = heartbeat >= 5s

---

## Map Interface

- Green → Online  
- Red → Offline  
- Click device → shows status  
- Offline → shows "Last seen"

---

## Simulation

### Automatic
- multiple devices
- send heartbeat every 2–5 sec
- move slightly

### Manual (Tkinter)
- create your own device
- send heartbeat manually

---

## Code Highlights

### Heartbeat route
@app.route('/heartbeat')
- receives data
- stores last_seen

### Devices route
@app.route('/devices')
- calculates online/offline
- sends JSON to frontend

### Frontend
- Leaflet map
- updates every 2 seconds

---

## Run the Project

1. Install:
pip install flask requests

2. Run app:
python app.py

3. Open:
http://127.0.0.1:5000

4. To send manually heartbeats, run:
python heartbeat_sim.py

---

## Test

1. Send heartbeat
2. Click device → online
3. Wait 6–10 sec
4. Click again → offline + last seen

---

## Features

- Real-time tracking
- Online/offline detection
- Interactive map
- Device simulation
- Human-readable time

---

## Conclusion

A full-stack real-time monitoring system using:
- Python (Flask)
- Leaflet
- Networking concepts
