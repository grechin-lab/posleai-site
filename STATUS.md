# posle.ai — состояние на 16.11.2026

Работает:
- Сайт https://posle.ai на Bridge-VPS (Caddy на 109.172.85.123; VPN xray только на 138.16.185.4). DNS в Cloudflare, облачко серое.
- Репозиторий github.com/grechin-lab/posleai-site (публичный). Ветка main защищена: нужен PR с одобрением, владелец может обходить.
- Сервер раз в минуту тянет main и собирает Hugo (таймер posle-build, пользователь posle-build, скрипт /usr/local/bin/posle-build) в /srv/posle.
- Редактор https://posle.ai/admin/ (Decap CMS, editorial_workflow), вход через GitHub OAuth App "posle.ai CMS"; сервис posle-oauth (/usr/local/lib/posle-oauth.py, секреты /etc/posle-oauth.env).
- LLM-слой: llms.txt, llms-full.txt, index.md у каждой статьи, schema.org, robots для ИИ, sitemap, RSS.

Важно: ops/*.sh|py в репо — только образцы; серверные копии обновлять вручную.

Дальше:
- Пригласить агентство (Collaborators → Write), проверить, что без одобрения не публикуется.
- Дизайн по референсам, тексты главной и «О проекте», удалить пример статьи.
