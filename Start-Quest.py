"""Serve the campus to an authorized Quest over USB using Android platform-tools."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import shutil
import subprocess
import sys

GAME = Path(__file__).with_name("Play-PC.html")
PORT = 8765
ADDRESS = f"http://localhost:{PORT}/"


class CampusPage(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?", 1)[0] not in ("/", "/Play-PC.html"):
            self.send_error(404)
            return
        content = GAME.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)


def run():
    candidates = [shutil.which("adb"), Path(__file__).with_name("adb.exe")]
    for key in ("ANDROID_HOME", "ANDROID_SDK_ROOT", "LOCALAPPDATA"):
        if value := os.getenv(key):
            base = Path(value)
            if key == "LOCALAPPDATA":
                base = base / "Android" / "Sdk"
            candidates.append(base / "platform-tools" / "adb.exe")
    adb = next((str(p) for p in candidates if p and Path(p).is_file()), None)
    if not adb:
        sys.exit("Install Android SDK Platform-Tools and add its folder to PATH, then run this launcher again.")
    if not GAME.is_file():
        sys.exit("Keep Play-PC.html next to this launcher.")
    devices = subprocess.check_output([adb, "devices"], text=True).splitlines()[1:]
    quests = []
    for row in devices:
        fields = row.split()
        if len(fields) != 2 or fields[1] != "device":
            continue
        serial = fields[0]
        model = subprocess.check_output([adb, "-s", serial, "shell", "getprop", "ro.product.model"], text=True)
        if "quest" in model.lower():
            quests.append(serial)
    if len(quests) != 1:
        sys.exit("Connect one Quest by USB, enable developer mode and accept USB debugging in the headset, then launch again.")
    command = [adb, "-s", quests[0]]
    with ThreadingHTTPServer(("127.0.0.1", PORT), CampusPage) as server:
        port = f"tcp:{PORT}"
        subprocess.run(command + ["reverse", "--no-rebind", port, port], check=True)
        try:
            print(f"Open {ADDRESS} in Quest Browser and select Enter Meta Quest. Keep this window open.")
            subprocess.run(command + ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", ADDRESS, "com.oculus.browser"], check=False)
            server.serve_forever()
        finally:
            subprocess.run(command + ["reverse", "--remove", port], check=False)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
    except (OSError, subprocess.SubprocessError) as error:
        sys.exit(str(error))
