#!/bin/bash
# Копия на сервере: /usr/local/bin/posle-build (пользователь posle-build, таймер раз в минуту).
# Правки здесь на сервер сами НЕ попадают — копировать вручную.
# Забирает изменения из GitHub и, если они есть, пересобирает сайт в /srv/posle.
set -euo pipefail
SRC=/opt/posle-site
cd "$SRC"
OLD=$(git rev-parse HEAD)
git fetch -q origin main
git reset -q --hard origin/main
NEW=$(git rev-parse HEAD)
if [ "$OLD" != "$NEW" ] || [ ! -f /srv/posle/index.html ] || [ "${1:-}" = "--force" ]; then
  rm -rf /var/tmp/posle-build/out
  hugo --minify --quiet -d /var/tmp/posle-build/out
  rsync -a --delete /var/tmp/posle-build/out/ /srv/posle/
  # IndexNow: сообщить Bing и Яндексу, что сайт обновился (ключ — static/182fc47aa8e448758027a001fb947a24.txt)
  KEY=182fc47aa8e448758027a001fb947a24
  URLS=$(grep -o '<loc>[^<]*</loc>' /srv/posle/sitemap.xml | sed 's/<[^>]*>//g; s/.*/"&"/' | paste -sd, - || true)
  curl -s -o /dev/null -m 20 -X POST https://api.indexnow.org/indexnow \
    -H 'Content-Type: application/json; charset=utf-8' \
    -d "{\"host\":\"posle.ai\",\"key\":\"$KEY\",\"keyLocation\":\"https://posle.ai/$KEY.txt\",\"urlList\":[$URLS]}" || true
  echo "built $NEW"
fi
