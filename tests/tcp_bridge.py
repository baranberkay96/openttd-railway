"""Test-only TCP forwarder: intentionally no UDP socket or UDP forwarding."""
import select
import socket
import socketserver


class Bridge(socketserver.BaseRequestHandler):
    def handle(self):
        with socket.create_connection(('game', 3979), timeout=10) as upstream:
            peers = (self.request, upstream)
            while True:
                ready, _, _ = select.select(peers, [], [], 30)
                for source in ready:
                    chunk = source.recv(65536)
                    if not chunk:
                        return
                    (upstream if source is self.request else self.request).sendall(chunk)


server = socketserver.ThreadingTCPServer(('0.0.0.0', 15479), Bridge)
server.daemon_threads = True
server.serve_forever()
