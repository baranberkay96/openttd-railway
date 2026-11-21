# OpenTTD Railway composer specification

Create one repo-built **OpenTTD** service from `baranberkay96/openttd-railway`, root `/services/openttd`, Dockerfile builder. Attach one volume at `/data`. Enable TCP proxy to internal `3979`. Do not add a public HTTP domain. Set private healthcheck `/health`, `PORT=8080`, timeout 300 seconds, restart ALWAYS, one replica, deployment overlap 0 seconds, and draining 120 seconds. Use `template.json` for variables and generated `SERVER_PASSWORD`.

Pinned on 2026-11-21: OpenTTD **15.3** (latest stable; 16.0-RC1 is testing), free OpenGFX **8.0**, Debian bookworm-slim manifest digest. Both game and graphics release archives are verified by published SHA-256 during build. The OpenTTD binary is Linux amd64; Railway's build must target linux/amd64.

## Improvements over market templates

No `_market` or `_upstream` material was provided for this new app. The implementation was created from the official upstream sources and documentation. This template adds generated access passwords, TCP-only direct joins, disabled public announcements/relays/admin/RCON, a free graphics set with release checksums, a persistent saved world, timed checkpoints, graceful shutdown saves, non-root gameplay, one-world locking, and a private readiness check that validates the game protocol.

## Resource profile

One service; no database, cache, workers, or sidecars. Estimated small-world idle 0.08–0.20 GB RAM and 0.01–0.05 vCPU, typical 0.10–0.40 GB and 0.03–0.25 vCPU, depending on players/vehicles. A 1 GB volume adds $0.15/month. At RAM $10/GB-month and CPU $20/vCPU-month, approximate compute+1GB-volume cost is $1.15–$3.15 idle or $1.75–$9.15 typical; actual metering, egress and plan minimums apply. Trial's 1 GB RAM limit can run the default 256×256 map; Hobby recommended for continuing operation (5 GB volume allowance per service). Do not scale replicas.

## Verification checklist

- Build `docker build --platform linux/amd64 -t railway-openttd:15.3 services/openttd`.
- Run `python3 tests/integration.py` with Docker available; tests use a real matching client across a TCP-only forwarding container.
- On Railway, wait for private `/health` and ready log. Confirm only TCP3979 is publicly forwarded.
- Use matching15.3 client, connect directly to public hostname and assigned port, verify wrong password denied and correct password can create a company.
- Confirm no listener on admin3977, no public HTTP domain, `server_game_type=local`, relay never, and empty RCON/admin secrets.
- Check `/data/save/railway.sav` advances; redeploy and reconnect to the same world/company.
- Trigger graceful restart and verify saved-game restore log. Back up the volume privately before upgrades.

## Open questions

Local test results are in `VERIFICATION.md`. Railway public TCP proxy routing and plan resource metering require the parent's separate deployment verification; this package creates no Railway project and publishes nothing.
