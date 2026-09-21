#!/bin/bash
# ~/scan/lib holds OpenSSL 1.1 on arm64, where the upstream binary needs it.
# It is empty or absent elsewhere, so the export is harmless.
export LD_LIBRARY_PATH="$HOME/scan/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
COOKIE="$(/opt/sandboxd/sbin/wsenv token request --domain=endpoint --print=cookie)"
exec "$HOME/scan/lonkero" scan --cookie "$COOKIE" --insecure "$@"
