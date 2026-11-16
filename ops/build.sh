#!/bin/bash
# Запускается на сервере раз в минуту (systemd timer posle-build).
# Забирает изменения из GitHub и, если они есть, пересобирает сайт в /srv/posle.
set -euo pipefail
SRC=/opt/posle-site
cd "$SRC"
OLD=$(git rev-parse HEAD)
git fetch -q origin main
git reset -q --hard origin/main
NEW=$(git rev-parse HEAD)
if [ "$OLD" != "$NEW" ] || [ ! -f /srv/posle/index.html ] || [ "${1:-}" = "--force" ]; then
  rm -rf /tmp/posle-build
  hugo --minify --quiet -d /tmp/posle-build
  rsync -a --delete /tmp/posle-build/ /srv/posle/
  echo "built $NEW"
fi
