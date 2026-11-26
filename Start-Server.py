"""
Dual HTTP + HTTPS Local Game Server for Anurag University: Campus Outbreak (PC + Meta Quest 3 VR).
- PC & USB Quest (via adb reverse): http://localhost:8765/
- Meta Quest 3 over Wi-Fi (WebXR requires HTTPS): https://<LAN-IP>:8443/
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import datetime
import ipaddress
import socket
import ssl
import threading

ROOT = Path(__file__).resolve().parent
GAME = ROOT / "Play-PC.html"
CERT_FILE = ROOT / "quest-cert.pem"
KEY_FILE = ROOT / "quest-key.pem"
HTTP_PORT = 8765
HTTPS_PORT = 8443


def get_lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def ensure_tls_cert(lan_ip):
    if CERT_FILE.is_file() and KEY_FILE.is_file():
        return
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, f"Anurag Campus VR ({lan_ip})"),
    ])
    san_list = [
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
    ]
    try:
        san_list.append(x509.IPAddress(ipaddress.ip_address(lan_ip)))
    except ValueError:
        pass

    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=365))
        .add_extension(x509.SubjectAlternativeName(san_list), critical=False)
        .sign(key, hashes.SHA256())
    )
    KEY_FILE.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    CERT_FILE.write_bytes(cert.public_bytes(serialization.Encoding.PEM))


class GameHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/Play-PC.html", "/game", "/index.html"):
            if not GAME.is_file():
                self.send_error(404, "Play-PC.html not found")
                return
            data = GAME.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def log_message(self, fmt, *args):
        print(f"[{self.client_address[0]}] {fmt % args}", flush=True)


def main():
    lan_ip = get_lan_ip()
    ensure_tls_cert(lan_ip)

    http_server = ThreadingHTTPServer(("0.0.0.0", HTTP_PORT), GameHandler)
    https_server = ThreadingHTTPServer(("0.0.0.0", HTTPS_PORT), GameHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))
    https_server.socket = ctx.wrap_socket(https_server.socket, server_side=True)

    t_http = threading.Thread(target=http_server.serve_forever, daemon=True)
    t_https = threading.Thread(target=https_server.serve_forever, daemon=True)
    t_http.start()
    t_https.start()

    print("=" * 68, flush=True)
    print("  ANURAG UNIVERSITY: CAMPUS OUTBREAK — LOCAL SERVER RUNNING", flush=True)
    print("=" * 68, flush=True)
    print(f"  PC Browser (Keyboard/Mouse):  http://localhost:{HTTP_PORT}/", flush=True)
    print(f"  Meta Quest 3 (Wi-Fi WebXR):   https://{lan_ip}:{HTTPS_PORT}/", flush=True)
    print(f"  Meta Quest 3 (USB ADB):       http://localhost:{HTTP_PORT}/  (via Start-Quest.py)", flush=True)
    print("=" * 68, flush=True)
    print("  On Meta Quest 3 Wi-Fi: open the HTTPS URL in Quest Browser,", flush=True)
    print("  tap 'Advanced' -> 'Proceed' once, then click 'Enter Meta Quest'.", flush=True)
    print("=" * 68, flush=True)

    try:
        t_http.join()
    except KeyboardInterrupt:
        http_server.shutdown()
        https_server.shutdown()


if __name__ == "__main__":
    main()
