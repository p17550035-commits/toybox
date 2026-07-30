import datetime

LOG_FILE = "logs/toybox.log"

def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)
    print(f"[ToyBox] {msg}")
