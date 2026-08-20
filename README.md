# PrivGuide

Public website: **[https://www.privguide.com](https://www.privguide.com)**

A multi-language privacy guide covering recommended apps, everyday privacy practices, and hardening paths for phones and desktops. Independent tools are listed first; first-party products from the publisher are labeled **Ours**.

## Ownership & hosting

PrivGuide is **owned and hosted by [Vassbrekke AS](https://www.vassbrekke.no)** (Haugesund, Norway), makers of [PrivyDeck](https://privydeck.com) and [PrivBeacon](https://www.privbeacon.com). Source lives in the **[Vassbrekke/PrivGuide](https://github.com/Vassbrekke/PrivGuide)** repository.

Copyright: **Vassbrekke AS** — see [`LICENSE`](LICENSE) (MIT).

Trust, conflicts of interest, and methodology: [privguide.com/trust](https://www.privguide.com/trust/)

## Issues & corrections

Report problems, suggest corrections, or request content changes via **[GitHub issues](https://github.com/Vassbrekke/PrivGuide/issues)**. Questions and ideas: **[GitHub Discussions](https://github.com/Vassbrekke/PrivGuide/discussions)**.

Company contact: [vassbrekke.no](https://www.vassbrekke.no) · [contact@vassbrekke.no](mailto:contact@vassbrekke.no)

## What the site covers

- Curated privacy apps with official website links (no affiliate parameters)
- Everyday personal privacy guidance
- Phone hardening (Android & iOS)
- Desktop/laptop hardening (Windows, macOS, Linux)
- Leveled paths and an interactive checklist (progress stored in the browser only)
- Ownership and editorial disclosures on the Trust page

## Languages

| Code | Language | Live path |
|------|----------|-----------|
| `en` | English | [/](https://www.privguide.com/) |
| `no` | Norsk | [/no/](https://www.privguide.com/no/) |
| `es` | Español | [/es/](https://www.privguide.com/es/) |
| `de` | Deutsch | [/de/](https://www.privguide.com/de/) |
| `fr` | Français | [/fr/](https://www.privguide.com/fr/) |

Each language is fully rendered static HTML (not client-only translation) so search engines can index every version. `hreflang` tags and `sitemap.xml` connect the locales.

## How the project is built

The site is a static HTML/CSS/JS publication. Page content is generated from `locales/translations.json` and `scripts/build_site.py`, which produce:

- `index.html` and `no|es|de|fr/index.html` (plus matching `/trust/` pages)
- `sitemap.xml`, `robots.txt`, `site.webmanifest`
- Assets under `assets/`

Production URL (`SITE_URL`) is `https://www.privguide.com`.

### SEO & discoverability

- Unique `<title>`, meta description, and keywords per language
- Canonical URLs + `hreflang` (en, no, es, de, fr, x-default)
- Open Graph + Twitter Card tags
- JSON-LD (`WebSite`, `WebPage`, `ItemList`, `FAQPage`, `HowTo`)
- Semantic HTML and schema.org markup on app cards

### Repository layout

```
PrivacyGuide/
├── index.html              # English (default)
├── no|es|de|fr/            # Translated pages (+ trust/)
├── css/styles.css
├── js/main.js
├── locales/translations.json
├── scripts/build_site.py
├── trust/                  # English Trust page
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── LICENSE
└── assets/
```

App metadata lives in `scripts/build_site.py` (`APPS`). Descriptions and Trust copy live in `locales/translations.json`.

## Privacy of this site

- No analytics, ads, or third-party trackers
- Checklist progress stays in `localStorage` only
- Language preference is remembered locally when chosen
- System font stacks only (no third-party font CDN)

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Vassbrekke AS.

Listed tools and brands are trademarks of their respective owners — no affiliation implied unless marked **Ours**.
