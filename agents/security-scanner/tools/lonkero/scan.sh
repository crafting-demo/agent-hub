#!/bin/bash
COOKIE="$(/opt/sandboxd/sbin/wsenv token request --domain=endpoint --print=cookie)"
exec "$HOME/scan/lonkero" scan --cookie "$COOKIE" --insecure "$@"
