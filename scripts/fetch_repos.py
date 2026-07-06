#!/usr/bin/env python3
"""
RAPTOR Hub - genera data/repos.json leggendo l'elenco pubblico
dei repository GitHub di Giorgiogoldoni.

Eseguito nightly + manualmente via GitHub Actions.
Non richiede token: i repository sono pubblici.
"""
import json
import urllib.request
from datetime import datetime, timezone

USER = "Giorgiogoldoni"
API_URL = f"https://api.github.com/users/{USER}/repos?per_page=100&sort=name&direction=asc&type=owner"
OUT_PATH = "data/repos.json"

# Repo da escludere dall'hub (superati / duplicati / non pertinenti)
EXCLUDE = set()  # attualmente vuoto: mostriamo tutti i repo pubblici


def fetch_all_repos():
    repos = []
    page = 1
    while True:
        url = f"{API_URL}&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "raptor-hub"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            batch = json.loads(resp.read().decode("utf-8"))
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def main():
    raw = fetch_all_repos()

    items = []
    for r in raw:
        name = r["name"]
        if name in EXCLUDE:
            continue
        if r.get("private"):
            continue
        if r.get("fork"):
            continue
        items.append({
            "name": name,
            "description": r.get("description") or "",
            "url": f"https://giorgiogoldoni.github.io/{name}/",
            "repo_url": r.get("html_url"),
            "has_pages": bool(r.get("has_pages")),
            "updated_at": r.get("updated_at"),
        })

    # ordine alfabetico case-insensitive
    items.sort(key=lambda x: x["name"].lower())

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "repos": items,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Scritti {len(items)} repository in {OUT_PATH}")


if __name__ == "__main__":
    main()
