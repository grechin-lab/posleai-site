# posle.ai — состояние на 16.11.2026

Сделано:
- Сервер: Bridge 138.16.185.4 (VPN только на этом IP), сайт — Caddy на 109.172.85.123, файлы /srv/posle, сертификаты LE получены. DNS в Cloudflare (серое облачко).
- Hugo 0.154 установлен на сервере (apt). Каркас сайта собирается без ошибок: статьи, О проекте, llms.txt, llms-full.txt, .md-копии статей, schema.org, robots для ИИ, sitemap, RSS, поиск на JS.
- Редактор Decap CMS (static/admin) с editorial_workflow, вход через ops/oauth.py.

Осталось:
1. Пользователь: создать публичный репозиторий GitHub grechin-lab/posleai-site; добавить ~/.ssh/id_ed25519.pub в SSH-ключи GitHub; заменить GITHUB_USER в static/admin/config.yml; git push.
2. Пользователь: GitHub OAuth App (callback https://posle.ai/oauth/callback), Client ID/Secret положить в /etc/posle-oauth.env на сервере сам.
3. Сервер: клонировать репо в /opt/posle-site, systemd-сервис для ops/oauth.py, timer раз в минуту для ops/build.sh, в Caddyfile: reverse_proxy /oauth/* 127.0.0.1:8787, MIME text/markdown и text/plain; charset=utf-8.
4. GitHub: защита ветки main — обязательное одобрение владельца; агентство добавить как collaborator.
