"""Inspect v7 TCP game-info for the unmodified, no-NewGRF default world."""
import json
import socket


def read(sock, size):
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise RuntimeError('incomplete game-info packet')
        data += chunk
    return data


with socket.create_connection(('127.0.0.1', 3979), timeout=3) as sock:
    sock.sendall(b'\x03\x00\x07')
    header = read(sock, 3)
    assert header[2] == 6
    data = read(sock, int.from_bytes(header[:2], 'little') - 3)
assert data[0] == 7
assert data[14] == 0 and data[15] == 0  # no game script name and no NewGRFs
print(json.dumps({'ticks': int.from_bytes(data[1:9], 'little'),
                  'date': int.from_bytes(data[16:20], 'little'),
                  'companies': data[25]}))
