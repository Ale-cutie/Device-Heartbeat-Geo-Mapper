from flask import Flask, jsonify, request, render_template_string
import threading
import time
import random
import requests

app = Flask(__name__)

devices = {}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Geo Mapper</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
</head>
<body>

<h2 div class="text">Device Geo Mapper (Live)</h2>
<div id="map" style="height: 500px;"></div>

<style>
    .text {
        font-family: Arial, sans-serif;}
</style>

<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>
var map = L.map('map').setView([45, 25], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var markers = {};

function formatTime(seconds) {
    if (seconds < 60) {
        return seconds + ' seconds ago';
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        return minutes + ' minute' + (minutes > 1 ? 's' : '') + ' ago';
    } else if (seconds < 86400) {
        const hours = Math.floor(seconds / 3600);
        return hours + ' hour' + (hours > 1 ? 's' : '') + ' ago';
    } else if (seconds < 2592000) {
        const days = Math.floor(seconds / 86400);
        return days + ' day' + (days > 1 ? 's' : '') + ' ago';
    } else {
        const months = Math.floor(seconds / 2592000);
        return months + ' month' + (months > 1 ? 's' : '') + ' ago';
    }
}

function loadDevices() {
    fetch('/devices')
        .then(res => res.json())
        .then(data => {

            data.forEach(device => {
                var color = device.status === "online" ? "green" : "red";

                if (!markers[device.id]) {
                    markers[device.id] = L.circleMarker([device.lat, device.lon], {
                        color: color,
                        radius: 8
                    }).addTo(map);
                }

                var marker = markers[device.id];

                marker.setLatLng([device.lat, device.lon]);

                marker.setStyle({ color: color });

                let popupContent = `
                    <b>${device.id}</b><br>
                    Status: <span style="color:${device.status === 'online' ? 'green' : 'red'}">${device.status}</span>
                `;

                if (device.status === "offline") {
                    popupContent += `<br>Last seen: ${formatTime(device.last_seen_ago)}`;
                }

                let popup = marker.getPopup();
                if (popup) {
                    popup.setContent(popupContent);
                } else {
                    marker.bindPopup(popupContent);
                }

                if (marker.isPopupOpen && marker.isPopupOpen()) {
                    marker.openPopup();
                }
            });
        });
}

setInterval(loadDevices, 2000);
loadDevices();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/devices')
def get_devices():
    current_time = time.time()
    result = []

    for device in devices.values():
        time_diff = current_time - device["last_seen"]

        if time_diff >= 5:
            status = "offline"
        else:
            status = "online"

        result.append({
            "id": device["id"],
            "lat": device["lat"],
            "lon": device["lon"],
            "status": status,
            "last_seen_ago": int(time_diff)
        })

    return jsonify(result)

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json

    data["last_seen"] = time.time()
    devices[data["id"]] = data

    print("Heartbeat:", data)

    return {"message": "OK"}

# ---------------- DEVICE SIMULATION ----------------
def simulate_device(device_id, base_lat, base_lon):
    while True:
        lat = base_lat + random.uniform(-0.1, 0.1)
        lon = base_lon + random.uniform(-0.1, 0.1)

        data = {
            "id": device_id,
            "lat": lat,
            "lon": lon,
            "status": "online"
        }

        try:
            requests.post("http://127.0.0.1:5000/heartbeat", json=data)
        except:
            pass

        time.sleep(random.randint(2, 5))


def start_simulation():
    devices_info = [
        ("device-1", 44.43, 26.10),
        ("device-2", 46.77, 23.62),
        ("device-3", 45.75, 21.23),
        ("device-4", 47.15, 27.58),
    ]

    for dev_id, lat, lon in devices_info:
        t = threading.Thread(target=simulate_device, args=(dev_id, lat, lon))
        t.daemon = True
        t.start()

# ---------------- MAIN ----------------
if __name__ == '__main__':
    start_simulation()
    app.run(debug=True)