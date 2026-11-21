# Deploy and Host OpenTTD with Railway

Host a private OpenTTD 15.3 transport simulation world with a generated game password, persistent saves, and direct connections through Railway's TCP proxy. This community template includes the free OpenGFX 8.0 graphics set. Friends can build railways, run competing transport companies, or cooperate without purchasing or uploading Transport Tycoon Deluxe assets.

## About Hosting OpenTTD

OpenTTD is an open source transport management game. This deployment runs one dedicated server with a 256×256 world, pauses when no active players remain, saves a checkpoint every minute, and saves before graceful shutdown. It restores the newest saved game after a redeploy. Railway provides TCP forwarding for gameplay, but no public UDP; use a direct connection to the proxy hostname and assigned port. Public discovery, invite codes, relay connections, admin networking, and remote console are disabled. The server password controls game access; share it only with invited players. Install OpenTTD 15.3 on each player's computer.

## Common Use Cases

- Run a persistent transport world for friends.
- Build a shared railway company cooperatively.
- Compete with separate transport companies.
- Learn OpenTTD multiplayer using free graphics and matching clients.

## Dependencies for OpenTTD Hosting

- One Railway service and one persistent volume mounted at `/data`.
- A public Railway TCP proxy forwarding to port `3979`.
- Matching OpenTTD 15.3 clients, available free from the official website.
- Hobby plan recommended for an always-on world; the default small world fits Trial's 1 GB service limit.

### Deployment Dependencies

- [OpenTTD downloads](https://www.openttd.org/downloads/openttd-releases/15.3)
- [OpenGFX downloads](https://www.openttd.org/downloads/opengfx-releases/8.0)
- [Official multiplayer manual](https://github.com/OpenTTD/OpenTTD/blob/15.3/docs/multiplayer.md)
- [Direct-IP TCP support](https://www.openttd.org/news/2021/09/26/new-multiplayer-experience)
- [Railway TCP proxy documentation](https://docs.railway.com/guides/tcp-proxy)

### Implementation Details

| Service | Purpose | Storage | Public access |
| --- | --- | --- | --- |
| OpenTTD | Dedicated game and private readiness endpoint | `/data` | TCP proxy → 3979 |

After deployment:

1. Copy the TCP proxy hostname and **assigned public port** from Railway's Networking settings. It is usually different from 3979.
2. Reveal `SERVER_PASSWORD` in Railway variables.
3. Open the OpenTTD **15.3** client console and enter `connect {proxy-hostname}:{proxy-port}`. Enter the generated password when prompted. Alternatively launch `openttd -n {proxy-hostname}:{proxy-port} -p {password}`.
4. Create a company or join as a spectator. Install OpenGFX on your own client if needed; it is already included on the server.

The multiplayer server list can display the server as local/unlisted because announcements are deliberately disabled. Always connect directly. No browser dashboard is exposed; Railway's private `/health` probe validates an OpenTTD game-info response over TCP.

`SERVER_NAME`, `MAX_CLIENTS` (2–64), and `SAVE_INTERVAL_SECONDS` (10–3600) configure the server. Defaults are 16 clients and 60 seconds. Use a password containing 16–32 ASCII letters, numbers, `_`, or `-`. Invalid optional values revert to defaults; an invalid password retains the previous one or locks access with a random password until you set a valid value. Configuration files are managed at startup.

Use one replica. Workers and horizontal replicas are not appropriate for one game world. Make private backups of `/data` before upgrades. Saves are in `/data/save`; startup restores the newest `.sav` there, including native autosave and exit saves. Stop the service before restoring a backup. Upgrades require changing the pinned game artifact and SHA-256 in the Dockerfile, testing with matching clients, and backing up the volume; newer saves may not load in older releases.

The free OpenGFX set is included; sound/music are unnecessary for a headless server. No proprietary Transport Tycoon Deluxe files are distributed. OpenTTD and OpenGFX licenses and third-party notices remain in the image. The default world needs modest CPU and memory, but larger worlds, many vehicles, and additional players increase usage.

### Why Deploy OpenTTD on Railway?

Railway gives a private OpenTTD world persistent storage, a stable TCP endpoint, deployment logs, generated secrets, and straightforward redeployments. Keep the world small initially, monitor resource usage, and keep volume backups before changing versions.
