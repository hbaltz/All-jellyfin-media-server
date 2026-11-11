#!/bin/sh
# Boot-time updater: pull newer images; if any container would change, back up the
# configs first (Jellyfin and the *arrs migrate their databases on upgrade), then recreate.
# Installed with:  @reboot <path>/update-stack.sh >> $HOME/backups/update-stack.log 2>&1
cd "$(dirname "$0")" || exit 1
F=tailscale-docker-compose.yaml
COMMON_PATH=$(sed -n 's/^COMMON_PATH=//p' .env)
BACKUPS=$HOME/backups
echo "== $(date '+%F %T') update-stack"

# cron fires before the network is fully up at boot: wait (max ~10 min) for Docker Hub.
for i in $(seq 20); do docker pull -q alpine:3 >/dev/null 2>&1 && break; sleep 30; done
docker compose -f "$F" pull -q --ignore-pull-failures

# A container needs recreating when its image is not the freshly pulled one.
changed=$(docker compose -f "$F" ps -aq | while read -r c; do
  [ "$(docker inspect -f '{{.Image}}' "$c")" = "$(docker image inspect -f '{{.Id}}' "$(docker inspect -f '{{.Config.Image}}' "$c")" 2>/dev/null)" ] ||
    docker inspect -f '{{.Name}}' "$c"
done)

if [ -n "$changed" ]; then
  echo "new images for:" $changed
  docker compose -f "$F" stop            # consistent SQLite copies
  mkdir -p "$BACKUPS"
  if ! docker run --rm -e OWNER="$(id -u):$(id -g)" -v "$COMMON_PATH":/src:ro -v "$BACKUPS":/dst alpine:3 sh -c '
    tar -cf /dst/stack-$(date +%F_%H%M).tar --exclude=configs/jellyfin/cache -C /src configs scripts &&
    chown "$OWNER" /dst/stack-*.tar &&
    ls -1t /dst/stack-*.tar | tail -n +4 | xargs -r rm -f'; then
    echo "backup FAILED: restarting the old containers without upgrading"
    docker compose -f "$F" up -d --no-recreate
    exit 1
  fi
  echo "backup ok (keeping the 3 newest)"
fi

docker compose -f "$F" up -d --remove-orphans
docker image prune -f >/dev/null
echo "== $(date '+%F %T') done"
