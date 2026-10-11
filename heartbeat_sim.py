import tkinter as tk
import requests
import random

SERVER_URL = "http://127.0.0.1:5000/heartbeat"

def send_heartbeat():
    device_id = entry_id.get()

    try:
        lat = float(entry_lat.get())
        lon = float(entry_lon.get())
    except:
        label_status.config(text="Invalid coordinates")
        return

    data = {
        "id": device_id,
        "lat": lat + random.uniform(-0.05, 0.05),
        "lon": lon + random.uniform(-0.05, 0.05),
        "status": "online"
    }

    try:
        requests.post(SERVER_URL, json=data)
        label_status.config(text="Heartbeat sent")
    except:
        label_status.config(text="Server not running")


# ---------------- UI ----------------
root = tk.Tk()
root.title("Manual Device Sender")

tk.Label(root, text="Device ID").pack()
entry_id = tk.Entry(root)
entry_id.insert(0, "tk-device")
entry_id.pack()

tk.Label(root, text="Latitude").pack()
entry_lat = tk.Entry(root)
entry_lat.insert(0, "44.43")
entry_lat.pack()

tk.Label(root, text="Longitude").pack()
entry_lon = tk.Entry(root)
entry_lon.insert(0, "26.10")
entry_lon.pack()

btn = tk.Button(root, text="Send Heartbeat", command=send_heartbeat)
btn.pack(pady=10)

label_status = tk.Label(root, text="")
label_status.pack()

root.mainloop()