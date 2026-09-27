# ROX GROUP s.r.o. — návrh webu a loga

Statický web (5 stránek: Domů, Služby, O nás, Kontakt, Logo manuál). Struktura podle molvergroup.cz.

- Úpravy: `src/layout.html`, `src/pages/*.html`, `src/style.css`, `src/main.js`
- Telefon a e-mail: konstanty `PHONE` / `EMAIL` v `build.py`
- `python3 build.py` → vygeneruje stránky, zkopíruje assety, přidá `?v=` hashe (cache busting)
- Logo: `brand/make_logo.py` generuje SVG z písma Archivo (OFL); PNG exporty v `brand/png/`
- Fotky: Unsplash (licence Unsplash, komerční použití zdarma) — zdroje v `brand/unsplash-credits.json`
