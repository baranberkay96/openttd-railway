"""Launch the unmodified matching game client with SDL dummy display."""
import os
from pathlib import Path

Path('/data/openttd.cfg').write_text('[version]\nini_version = 7\n')
Path('/data/private.cfg').write_text('[network]\nclient_name = TCP Proof\nuse_relay_service = never\nparticipate_survey = no\n')
os.execv('/opt/openttd/openttd', ['/opt/openttd/openttd', '-c', '/data/openttd.cfg', '-v', 'sdl', '-b', '8bpp-optimized', '-s', 'null', '-m', 'null', '-n', os.environ.get('TEST_ADDRESS', 'bridge:15479'), '-p', os.environ['TEST_PASSWORD'], '-d', 'net=9'])
