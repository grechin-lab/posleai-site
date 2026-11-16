#!/usr/bin/env python3
# Копия на сервере: /usr/local/lib/posle-oauth.py. Правки здесь на сервер сами НЕ попадают.
"""Мини-сервер входа через GitHub для Decap CMS (только стандартная библиотека).
Слушает 127.0.0.1:8787, Caddy проксирует на него /oauth/*.
Секреты берёт из окружения: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET (файл /etc/posle-oauth.env)."""
import json, os, secrets, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

CID = os.environ["GITHUB_CLIENT_ID"]
SECRET = os.environ["GITHUB_CLIENT_SECRET"]
ORIGIN = "https://posle.ai"
STATES = set()

PAGE = """<!doctype html><meta charset=utf-8><body><script>
(function(){var msg=%s;
function recv(e){if(e.origin!==%s)return;window.opener.postMessage(msg,e.origin);window.removeEventListener("message",recv)}
window.addEventListener("message",recv,false);window.opener.postMessage("authorizing:github","*");})();
</script>Вход выполняется…</body>"""


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8", headers=None):
        b = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/oauth/auth":
            st = secrets.token_urlsafe(24)
            STATES.add(st)
            loc = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(
                {"client_id": CID, "scope": "public_repo,read:user", "state": st,
                 "redirect_uri": ORIGIN + "/oauth/callback"})
            return self._send(302, "", headers={"Location": loc})
        if u.path == "/oauth/callback":
            st = (q.get("state") or [""])[0]
            if st not in STATES:
                return self._send(400, "bad state")
            STATES.discard(st)
            data = urllib.parse.urlencode({"client_id": CID, "client_secret": SECRET,
                                           "code": (q.get("code") or [""])[0]}).encode()
            req = urllib.request.Request("https://github.com/login/oauth/access_token", data=data,
                                         headers={"Accept": "application/json"})
            try:
                tok = json.load(urllib.request.urlopen(req, timeout=15)).get("access_token")
            except Exception:
                tok = None
            if tok:
                msg = "authorization:github:success:" + json.dumps({"token": tok, "provider": "github"})
            else:
                msg = "authorization:github:error:" + json.dumps({"message": "login failed"})
            return self._send(200, PAGE % (json.dumps(msg), json.dumps(ORIGIN)))
        self._send(404, "not found")

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("127.0.0.1", 8787), H).serve_forever()
