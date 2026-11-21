# Local verification — 2026-11-21

- `docker build --platform linux/amd64 -t railway-openttd:15.3 services/openttd`: **PASS**. Both official release archive SHA-256 checks pass. Final image is 84,184,276 bytes unpacked (about80 MiB), far below Railway's4GB compressed cap.
- `python3 -m py_compile services/openttd/server.py tests/*.py`: **PASS**.
- `python3 tests/integration.py`: **PASS**, exit0. The test builds a matching unmodified15.3 game client with SDL's dummy display. A named client starts without an interactive first-run name dialog.
- Client and server are on **two separate internal Docker networks**. A Python proxy bridges onlyTCP15479→3979; it has noUDP socket. No public Docker ports, coordinator, relay or internet path is available to the isolated client.
- Wrong password: server error received; client never becomesACTIVE.
- Correct password: real client reports encrypted authentication, complete map transfer, ACTIVE status, frame ACKs, and creates company1.
- Timed snapshot: `/data/save/railway.sav` modification time advances.
- Graceful `docker stop -t120`: upstream dedicatedSIGTERM save creates exit.sav; server exits0 with noOOM. Restart loads saved game rather than generating a new world. TCP game-info confirms company count and world date/ticks persisted. A real client reconnects and ACKs frames.
- AdminTCP3977: connection refused. RCON/adminpasswords and authorized keys are empty. Public discovery and relays disabled.
- Test server runs with Docker`--init`,512MiB RAM and1vCPU limits. Measured after restart/client join: **46.43MiB /512MiB**, CPU2.25% at the sampled instant; earlier paused server was60.16MiB/0.25%. Workload/map complexity affects usage.
- Supervisor and game run asUID10001 after volume initialization (confirmed with`docker top`).
- Invalid password/name/client-count/save-interval inputs and a health-port collision: **PASS**, service becomes ready; generated locked password remains unchanged after restart.
- Official commit-pinned icon downloaded successfully (HTTP200).

The integration harness removes its own containers, networks, and named volume in`finally`. Test helpers are not copied into the production image. No GitHub repository, Railway project, deployment or marketplace listing was created by these local tests.

Railway-specific public proxy routing, private readiness probes and billing still need the parent's separate deployment verification. This report does not claim a cloud deployment test.
