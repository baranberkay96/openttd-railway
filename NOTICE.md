# Sources and licenses

This is an independent community template, with newly written Dockerfile, Python wrapper, tests, and documentation. No marketplace files or unlicensed template source were copied. No OpenTTD marketplace base or upstream template repository was provided in the assigned directory. The `164-horizon/template` package was consulted only for Railway schema conventions. The common `STANDARD.md` and `_tools/to_serialized.py` were read only.

Checked 2026-11-21 against official OpenTTD stable15.3 at commit `14ec60f248547d4d062a1160f0fc26d742319888`:

- [Official stable download/checksums](https://www.openttd.org/downloads/openttd-releases/15.3)
- [Official source archive](https://cdn.openttd.org/openttd-releases/15.3/openttd-15.3-source.tar.xz), SHA-256 `5ea21eea7d59c78a42071924ac18c6bc0116088f2e96b14cfee9369175973be7`.
- [Official multiplayer and game coordinator docs](https://github.com/OpenTTD/OpenTTD/tree/15.3/docs); directory_structure.md and readme.md; settings definitions `src/table/settings/network_settings.ini`, `network_private_settings.ini`, `network_secrets_settings.ini`, `gui_settings.ini`; `src/settings.cpp`, `src/fileio.cpp`, `src/video/dedicated_v.cpp`, `src/network/core/tcp_game.h`.
- [Official direct-IP TCP explanation](https://www.openttd.org/news/2021/09/26/new-multiplayer-experience). Some wiki pages still mention forwarding both protocols; current direct-IP gameplay uses TCP. UDP LAN discovery is not exposed by Railway.
- OpenTTD15.3 Linux generic amd64 release, SHA-256 `f49eb25d61b00f8f4d332fee02b530ad75552d1efb8f2bb01e7ca5e6540fe059`: GNU GPLv2, copyright OpenTTD developers. The unmodified release retains COPYING.md, CREDITS.md, readme licensing notes, bundled libraries and their notices. Corresponding source remains available from the official archive above; distribute it alongside the binary when required by GPLv2.
- [OpenGFX8.0 official release](https://www.openttd.org/downloads/opengfx-releases/8.0), SHA-256 `43a0c1dabf39cb865394f3a6cc36d4da5c10ecfaaf55652043104806810903be`: GNU GPLv2, copyright OpenGFX contributors listed in its readme. The official archive's license.txt, readme.txt, changelog and graphics remain together in `/opt/openttd/baseset/opengfx-8.0`.
- Marketplace icon: upstream OpenTTD `media/openttd.256.png` at the commit above, under the upstream GPLv2 license.
- Debian base packages retain their individual notices in `/usr/share/doc` in the image.

No Transport Tycoon Deluxe game files, commercial graphics, sound, music, or other proprietary assets are included. OpenGFX supplies all required base graphics. The server uses no NewGRFs or additional content by default.

Template-authored files: MIT, copyright (c)2026 Baran Berkay Barakcin; see LICENSE.
