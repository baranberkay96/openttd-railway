"""Manage one OpenTTD process, persistent snapshots, and private readiness."""
import fcntl
import http.server
import os
from pathlib import Path
import re
import secrets
import signal
import socket
import subprocess
import threading
import time

DATA = Path('/data')
GAME_PORT = 3979
BINARY = '/opt/openttd/openttd'
stop = threading.Event()


def number(name, default, low, high):
    try:
        value = int(os.environ.get(name, str(default)))
        if low <= value <= high:
            return value
    except ValueError:
        pass
    print(f'{name} invalid; using {default}', flush=True)
    return default


def game_ready():
    try:
        with socket.create_connection(('127.0.0.1', GAME_PORT), timeout=2) as sock:
            sock.sendall(b'\x03\x00\x07')  # CLIENT_GAME_INFO, available before auth.
            header = b''
            while len(header) < 3:
                part = sock.recv(3 - len(header))
                if not part:
                    return False
                header += part
            return header[2] == 6 and int.from_bytes(header[:2], 'little') > 3
    except OSError:
        return False


class Health(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        ready = self.path == '/health' and not stop.is_set() and game_ready()
        self.send_response(200 if ready else 503)
        self.end_headers()
        self.wfile.write(b'ready\n' if ready else b'not ready\n')

    def log_message(self, *_args):
        pass


def main():
    os.umask(0o077)
    DATA.mkdir(parents=True, exist_ok=True)
    # Railway mounts new volumes as root. Drop privileges before starting any listener.
    if os.getuid() == 0:
        os.chown(DATA, 10001, 10001)
        for root, dirs, files in os.walk(DATA):
            for name in dirs + files:
                path = Path(root) / name
                if not path.is_symlink():
                    os.chown(path, 10001, 10001)
        os.setgroups([])
        os.setgid(10001)
        os.setuid(10001)
    os.chdir(DATA)
    lock = (DATA / '.server.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    saves = DATA / 'save'
    saves.mkdir(exist_ok=True)
    password_file = DATA / '.server-password'
    password = os.environ.get('SERVER_PASSWORD', '')
    if not re.fullmatch(r'[A-Za-z0-9_-]{16,32}', password):
        password = password_file.read_text().strip() if password_file.exists() else ''
        if not re.fullmatch(r'[A-Za-z0-9_-]{16,32}', password):
            password = secrets.token_hex(16)
        print('SERVER_PASSWORD invalid/empty; retaining or generating a locked password. Set 16–32 ASCII letters, digits, _ or - in Railway variables to regain access.')
    password_file.write_text(password)
    name = os.environ.get('SERVER_NAME', 'Railway OpenTTD')
    if not re.fullmatch(r'[A-Za-z0-9 ._-]{1,60}', name):
        name = 'Railway OpenTTD'
        print('SERVER_NAME invalid; using Railway OpenTTD')
    players = number('MAX_CLIENTS', 16, 2, 64)
    autosave = number('SAVE_INTERVAL_SECONDS', 60, 10, 3600)
    port = number('PORT', 8080, 1024, 65535)
    if port == GAME_PORT:
        port = 8080
    # Configuration is managed by this wrapper. Player saves remain untouched.
    (DATA / 'openttd.cfg').write_text(f'''[version]
ini_version = 7
[network]
server_port = {GAME_PORT}
server_game_type = local
max_clients = {players}
min_active_clients = 1
pause_on_join = true
[gui]
autosave_interval = 1
max_num_autosaves = 16
autosave_on_exit = true
threaded_saves = false
[game_creation]
map_x = 8
map_y = 8
starting_year = 1950
''')
    (DATA / 'private.cfg').write_text(f'''[network]
server_name = {name}
client_name = Railway Server
use_relay_service = never
participate_survey = no
[server_bind_addresses]
0.0.0.0 =
:: =
''')
    (DATA / 'secrets.cfg').write_text(f'''[network]
server_password = {password}
rcon_password =
admin_password =
''')
    # Select the newest completed checkpoint, including upstream's exit/autosaves.
    candidates = list(saves.rglob('*.sav'))
    args = [BINARY, '-D', '-c', str(DATA / 'openttd.cfg'), '-d', 'net=1']
    if candidates:
        latest = max(candidates, key=lambda p: p.stat().st_mtime_ns)
        print(f'Restoring saved game: {latest}')
        args += ['-g', str(latest)]
    else:
        print('Creating first 256x256 world')
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    child = subprocess.Popen(args, stdin=subprocess.PIPE, text=True)
    health = http.server.ThreadingHTTPServer(('0.0.0.0', port), Health)
    threading.Thread(target=health.serve_forever, daemon=True).start()
    next_save = 0.0
    ready_logged = False
    while child.poll() is None and not stop.wait(1):
        if game_ready():
            if not ready_logged:
                print('OpenTTD ready on TCP 3979; direct-IP connections only; discovery, relay, admin and RCON disabled')
                ready_logged = True
            if time.monotonic() >= next_save:
                child.stdin.write('save /data/save/railway\n')
                child.stdin.flush()
                next_save = time.monotonic() + autosave
    if child.poll() is None:
        print('Saving world and stopping OpenTTD')
        # The upstream dedicated SIGTERM handler synchronously writes exit.sav
        # when autosave_on_exit is enabled, then exits the normal game loop.
        child.terminate()
        try:
            child.wait(timeout=90)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait()
    health.shutdown()
    raise SystemExit(child.returncode)


if __name__ == '__main__':
    main()
