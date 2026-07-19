# PrivGuide — Ultimate Privacy Landing Page

**Hosted and owned by [Vassbrekke AS](https://www.vassbrekke.no)** — makers of [PrivyDeck](https://privydeck.com) and [PrivBeacon](https://www.privbeacon.com).

> We build privacy tools. This guide exists so you’re not stuck with only ours.

Trust / conflicts / methodology: [`/trust/`](https://www.privguide.com/trust/) · Corrections: [GitHub issues](https://github.com/N0L0g1c/PrivGuide/issues)

A multi-language, SEO-optimized privacy guide that helps people:

- **Find the best privacy apps** with official website links (independent tools first; Ours labeled)
- **Protect personal privacy** in everyday life
- **Harden phones** (Android & iOS)
- **Harden desktops/laptops** (Windows, macOS, Linux)
- **Follow leveled paths** and an interactive checklist (saved locally only)
- **Read ownership, conflicts, and methodology** on the Trust page

## Languages

| Code | Language | Path |
|------|----------|------|
| `en` | English | `/` (`index.html`) |
| `no` | Norsk | `/no/` |
| `es` | Español | `/es/` |
| `de` | Deutsch | `/de/` |
| `fr` | Français | `/fr/` |

Each language has **fully rendered static HTML** (not client-only translation) so search engines can index every version. `hreflang` tags and `sitemap.xml` connect them.

## Quick start

```bash
cd ~/Projects/PrivacyGuide
python3 -m http.server 8080
# English:  http://localhost:8080/
# Norwegian: http://localhost:8080/no/
```

## SEO features

- Unique `<title>`, meta description, and keywords per language
- Canonical URLs + `hreflang` (en, no, es, de, fr, x-default)
- Open Graph + Twitter Card tags
- JSON-LD: `WebSite`, `WebPage`, `ItemList` (apps), `FAQPage`, `HowTo`
- `robots.txt` + `sitemap.xml` with alternate language links
- Semantic HTML, skip link, schema.org on app cards
- `site.webmanifest` + favicon / OG image

`SITE_URL` is set to `https://www.privguide.com` in `scripts/build_site.py`.

## Rebuild pages after content changes

```bash
# Edit locales/translations.json and/or scripts/build_site.py (apps + URLs)
python3 scripts/build_site.py
```

This regenerates:

- `index.html` and `no|es|de|fr/index.html`
- `sitemap.xml`, `robots.txt`, `site.webmanifest`
- `assets/favicon.svg`, `assets/og-cover.svg`

## App websites & Vassbrekke products

**Independent tools are listed first.** First-party products are tagged **Ours**, show a publisher line, and appear after community recommendations (also under the Ours filter):

| Product | URL |
|---------|-----|
| PrivyDeck | https://privydeck.com |
| PrivBeacon | https://www.privbeacon.com |
| Windows 11 Privacy Tool | GitHub (VassDev) |
| Security Hardening | GitHub (VassDev) |

Plus community tools (Signal, Bitwarden, Mullvad, Firefox, uBlock Origin, …) with official links. No affiliate parameters.

App metadata lives in `scripts/build_site.py` (`APPS` list). Descriptions live in `locales/translations.json`. Trust copy lives under `trust_page` in the same file.

## Structure

```
PrivacyGuide/
├── index.html              # English (default)
├── no|es|de|fr/index.html  # Translated pages
├── css/styles.css
├── js/main.js
├── locales/translations.json
├── scripts/build_site.py
├── robots.txt
├── sitemap.xml
├── site.webmanifest
└── assets/
```

## Privacy of this site

- No analytics, ads, or third-party trackers (except optional Google Fonts CDN)
- Checklist progress stays in `localStorage` only
- Language preference remembered locally when the user picks a language

To remove Google Fonts entirely, self-host DM Sans / JetBrains Mono and drop the Google CSS link from the build template.

## License

Educational use. Listed tools are trademarks of their owners — no affiliation implied.
