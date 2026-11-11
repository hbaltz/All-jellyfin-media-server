#!/bin/sh
# Watchdog for qBittorrent behind Gluetun. qBittorrent only listens on the addresses that exist when its
# port is applied: if it starts before WireGuard is up, or the VPN reconnects, it stops listening on the
# VPN IP and every transfer drops to 0. Checks every minute and re-applies the port only when that
# listener is missing (qbit-port-sync.sh switches the port to 0 first, re-setting the same port is a no-op).
set -- $(echo "${WIREGUARD_ADDR%%/*}" | tr . ' ')
VPN_HEX=$(printf '%02X%02X%02X%02X' "$4" "$3" "$2" "$1")   # /proc/net/tcp writes IPv4 as little-endian hex
while true; do
  p=$(cat /tmp/gluetun/forwarded_port 2>/dev/null)
  if [ -n "$p" ] && ! grep -q " $VPN_HEX:$(printf '%04X' "$p") 00000000:0000 0A" /proc/net/tcp; then
    echo "$(date '+%F %T') qBittorrent is not listening on ${WIREGUARD_ADDR%%/*}:$p, re-applying the port"
    sh /qbit-port-sync.sh
  fi
  sleep 60
done
