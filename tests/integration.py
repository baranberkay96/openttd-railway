"""Real client integration across two networks with only a TCP bridge between them.

Run from template/: docker build --platform linux/amd64 -t railway-openttd:15.3 services/openttd
Then python3 tests/integration.py. All containers/networks/volume are isolated and cleaned.
"""
import json
from pathlib import Path
import subprocess
import time
import uuid

HERE = Path(__file__).resolve().parent
PREFIX = 'openttd-proof-' + uuid.uuid4().hex[:8]
IMAGE = 'railway-openttd:15.3'
PASSWORD = 'integration-password169'
containers = []
networks = []
volume = PREFIX + '-data'


def docker(*args, check=True):
    result = subprocess.run(['docker', *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout


def wait_for(fn, seconds=60):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = fn()
        if result:
            return result
        time.sleep(0.5)
    raise AssertionError('Timed out waiting for condition')


def logs(name):
    return docker('logs', name)


def run(name, *args):
    containers.append(name)
    return docker('run', '-d', '--platform', 'linux/amd64', '--name', name, *args)


def health(name):
    return 'ready' in docker('exec', name, 'python3', '-c', "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8080/health').read().decode())", check=False)


def client(name, password):
    run(name, '--network', networks[1], '-e', 'TEST_PASSWORD=' + password,
        '-v', str(HERE) + ':/test:ro', '--entrypoint', 'python3',
        'railway-openttd-client:15.3', '/test/client.py')


try:
    docker('build', '--platform', 'linux/amd64', '-f', str(HERE / 'Dockerfile.client'), '-t', 'railway-openttd-client:15.3', str(HERE))
    for suffix in ('server', 'client'):
        network = PREFIX + '-' + suffix
        docker('network', 'create', '--internal', network)
        networks.append(network)
    docker('volume', 'create', volume)
    game = PREFIX + '-game'
    run(game, '--init', '--memory=512m', '--cpus=1', '--network', networks[0], '--network-alias', 'game',
        '-v', volume + ':/data', '-e', 'SERVER_PASSWORD=' + PASSWORD, '-e', 'SAVE_INTERVAL_SECONDS=10', IMAGE)
    wait_for(lambda: health(game))
    bridge = PREFIX + '-bridge'
    run(bridge, '--network', networks[0], '-v', str(HERE) + ':/test:ro', '--entrypoint', 'python3', IMAGE, '/test/tcp_bridge.py')
    docker('network', 'connect', '--alias', 'bridge', networks[1], bridge)
    wrong = PREFIX + '-wrong'
    client(wrong, 'wrong-password169')
    wrong_logs = wait_for(lambda: (text if 'Receive_SERVER_ERROR' in (text := logs(wrong)) else None))
    assert 'status = ACTIVE' not in wrong_logs
    print('PASS: real client with wrong password rejected', flush=True)
    docker('rm', '-f', wrong)
    good = PREFIX + '-good'
    client(good, PASSWORD)
    good_logs = wait_for(lambda: (text if 'Client::status = ACTIVE' in (text := logs(good)) and 'Client::SendAck()' in text else None))
    assert 'Receive_SERVER_ENABLE_ENCRYPTION' in good_logs
    assert 'Receive_SERVER_MAP_DONE' in good_logs
    print('PASS: real client authenticated, encrypted, downloaded map, entered ACTIVE and acknowledged frames over TCP-only bridge', flush=True)
    # Client's company creation is visible in subsequent game-info packets.
    time.sleep(2)
    snapshot = docker('exec', game, 'python3', '-c', "import urllib.request,time,pathlib; p=pathlib.Path('/data/save/railway.sav'); print(p.stat().st_mtime_ns if p.exists() else 0)")
    wait_for(lambda: docker('exec', game, 'python3', '-c', "from pathlib import Path; p=Path('/data/save/railway.sav'); print(p.exists() and p.stat().st_mtime_ns > " + snapshot.strip() + ")").strip() == 'True', 20)
    print('PASS: periodic checkpoint updated', flush=True)
    docker('rm', '-f', good)
    before = json.loads(docker('exec', '-i', game, 'python3', '-c', (HERE / 'game_info.py').read_text()))
    assert before['companies'] == 1, before
    # Save bytes should survive load without silent world regeneration.
    docker('stop', '-t', '120', game)
    assert 'Saving world and stopping' in logs(game)
    info = json.loads(docker('inspect', game))[0]
    assert info['State']['ExitCode'] == 0 and not info['State']['OOMKilled']
    docker('start', game)
    wait_for(lambda: health(game))
    after = json.loads(docker('exec', '-i', game, 'python3', '-c', (HERE / 'game_info.py').read_text()))
    assert after['companies'] == before['companies'] and after['date'] >= before['date'] and after['ticks'] >= before['ticks'], (before, after)
    print('PASS: existing company and world date persisted through restart', flush=True)
    assert 'Restoring saved game:' in logs(game)
    assert logs(game).count('Creating first 256x256 world') == 1
    second = PREFIX + '-after'
    client(second, PASSWORD)
    wait_for(lambda: 'Client::status = ACTIVE' in logs(second) and 'Client::SendAck()' in logs(second))
    print('PASS: SIGTERM save, clean exit, automatic load, and real-client rejoin after restart', flush=True)
    forbidden = docker('exec', game, 'python3', '-c', "import socket; s=socket.socket(); print(s.connect_ex(('127.0.0.1',3977)))")
    assert forbidden.strip() != '0'
    print('PASS: admin TCP port3977 closed', flush=True)
    print(docker('stats', '--no-stream', '--format', '{{.MemUsage}} CPU={{.CPUPerc}}', game).strip(), flush=True)
    print('ALL INTEGRATION CHECKS PASSED', flush=True)
finally:
    for name in reversed(containers):
        docker('rm', '-f', name, check=False)
    for name in reversed(networks):
        docker('network', 'rm', name, check=False)
    docker('volume', 'rm', volume, check=False)
