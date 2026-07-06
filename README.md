# RAPTOR Hub

Pagina indice con tutti i repository pubblici di [Giorgiogoldoni](https://github.com/Giorgiogoldoni), ordinati alfabeticamente. Ogni card apre la pagina GitHub Pages del repository in una nuova scheda.

## Struttura

- `index.html` — pagina statica, legge `data/repos.json`
- `data/repos.json` — elenco repository, rigenerato automaticamente
- `scripts/fetch_repos.py` — script che interroga l'API pubblica di GitHub e rigenera `data/repos.json`
- `.github/workflows/update.yml` — GitHub Action: gira ogni notte alle 03:00 UTC + trigger manuale dal tab **Actions**

## Setup dopo il primo upload

1. Vai su **Settings → Pages** del repo e attiva GitHub Pages (branch `main`, cartella `/`).
2. Vai su **Settings → Actions → General** e assicurati che "Workflow permissions" sia impostato su **Read and write permissions** (serve per il commit automatico di `repos.json`).
3. La pagina sarà disponibile su `https://giorgiogoldoni.github.io/hub/`.

## Aggiungere/rimuovere repository

Non serve modificare nulla a mano: ogni nuovo repository pubblico che crei comparirà automaticamente nell'elenco dopo il prossimo run della Action (o subito, lanciandola manualmente da Actions → "Aggiorna elenco repository" → Run workflow).

Per escludere permanentemente un repo dall'elenco, aggiungi il suo nome al set `EXCLUDE` in `scripts/fetch_repos.py`.
