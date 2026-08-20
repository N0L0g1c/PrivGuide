"""Render PrivGuide trust / methodology / conflicts pages."""

from __future__ import annotations

import json
from html import escape as esc
from typing import Callable

CORRECTIONS_URL = "https://github.com/Vassbrekke/PrivGuide/issues"
DISCUSSIONS_URL = "https://github.com/Vassbrekke/PrivGuide/discussions"
COMPANY_URL = "https://www.vassbrekke.no"


def _section(title: str, body_html: str, sid: str) -> str:
    return f'''        <section class="trust-block" id="{sid}">
          <h2>{title}</h2>
          {body_html}
        </section>'''


def render_trust_page(
    lang: str,
    tr: dict,
    *,
    site_url: str,
    t: Callable,
    path_for: Callable,
    hreflang_links: Callable,
    asset_prefix: Callable,
    langs: list[str],
    lang_names: dict[str, str],
) -> str:
    # Pages live at /trust/ or /{lang}/trust/ — assets are two levels up for non-en
    if lang == "en":
        css = "../css/styles.css"
        js_main = "../js/main.js"
        home = "../index.html"
        icon = "../assets/favicon.svg"
    else:
        css = "../../css/styles.css"
        js_main = "../../js/main.js"
        home = "../index.html"
        icon = "../../assets/favicon.svg"
    trust_home = "index.html"

    title = t(tr, lang, "trust_page.meta_title")
    description = t(tr, lang, "trust_page.meta_description")
    canonical = f"{site_url}{path_for(lang)}trust/"
    og_locale = {
        "en": "en_US",
        "no": "nb_NO",
        "es": "es_ES",
        "de": "de_DE",
        "fr": "fr_FR",
    }[lang]

    switcher_opts = []
    for l in langs:
        if lang == "en":
            # From /trust/ → /trust/ or /no/trust/
            href = "index.html" if l == "en" else f"../{l}/trust/index.html"
        else:
            # From /no/trust/ → /trust/ or /es/trust/
            href = "../../trust/index.html" if l == "en" else f"../../{l}/trust/index.html"
        active = " active" if l == lang else ""
        switcher_opts.append(
            f'<a href="{href}" hreflang="{l}" lang="{l}" class="lang-option{active}" '
            f'data-lang="{l}" role="option" aria-selected="{str(l == lang).lower()}">{lang_names[l]}</a>'
        )

    def paras(key: str, n: int) -> str:
        return "\n".join(
            f"          <p>{t(tr, lang, f'{key}.{i}')}</p>" for i in range(1, n + 1)
        )

    def bullets(key: str, n: int) -> str:
        items = "\n".join(
            f"            <li>{t(tr, lang, f'{key}.{i}')}</li>" for i in range(1, n + 1)
        )
        return f"          <ul class=\"trust-list\">\n{items}\n          </ul>"

    def changelog() -> str:
        items = []
        for i in range(1, 6):
            date = t(tr, lang, f"trust_page.changelog.e{i}.date")
            text = t(tr, lang, f"trust_page.changelog.e{i}.text")
            items.append(f"            <li><time datetime=\"{esc(date)}\">{esc(date)}</time> — {text}</li>")
        return f"          <ul class=\"trust-changelog\">\n{chr(10).join(items)}\n          </ul>"

    ownership = (
        paras("trust_page.ownership", 3)
        + f'\n          <p class="trust-meta"><strong>{t(tr, lang, "trust_page.org_label")}</strong> '
        f'<a href="{COMPANY_URL}" target="_blank" rel="noopener noreferrer">Vassbrekke AS</a>'
        f' · Haugesund, Norway'
        f' · <a href="{COMPANY_URL}" target="_blank" rel="noopener noreferrer">vassbrekke.no</a>'
        f' · <a href="mailto:contact@vassbrekke.no">contact@vassbrekke.no</a></p>'
        + "\n"
        + bullets("trust_page.roles", 4)
    )

    conflicts = paras("trust_page.conflicts", 4) + "\n" + bullets("trust_page.conflict_rules", 5)
    methodology = paras("trust_page.methodology", 2) + "\n" + bullets("trust_page.criteria", 6)
    transparency = paras("trust_page.transparency", 3) + "\n" + bullets("trust_page.collect", 5)
    corrections = (
        paras("trust_page.corrections", 2)
        + f'\n          <p><a class="btn btn-primary btn-sm" href="{CORRECTIONS_URL}" '
        f'target="_blank" rel="noopener noreferrer">{t(tr, lang, "trust_page.corrections_cta")} ↗</a></p>'
    )

    blocks = [
        _section(t(tr, lang, "trust_page.ownership_title"), ownership, "ownership"),
        _section(t(tr, lang, "trust_page.conflicts_title"), conflicts, "conflicts"),
        _section(t(tr, lang, "trust_page.methodology_title"), methodology, "methodology"),
        _section(t(tr, lang, "trust_page.transparency_title"), transparency, "transparency"),
        _section(t(tr, lang, "trust_page.changelog_title"), changelog(), "changelog"),
        _section(t(tr, lang, "trust_page.corrections_title"), corrections, "corrections"),
    ]

    webpage_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": "PrivGuide", "url": site_url},
        "publisher": {
            "@type": "Organization",
            "name": "Vassbrekke AS",
            "url": COMPANY_URL,
        },
    }

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="author" content="PrivGuide / Vassbrekke AS" />
  <meta name="robots" content="index, follow" />
  <meta name="theme-color" content="#05010d" />
  <meta name="color-scheme" content="dark" />
  <meta name="referrer" content="no-referrer" />
  <link rel="canonical" href="{canonical}" />
  <link rel="alternate" hreflang="en" href="{site_url}/trust/" />
  <link rel="alternate" hreflang="no" href="{site_url}/no/trust/" />
  <link rel="alternate" hreflang="es" href="{site_url}/es/trust/" />
  <link rel="alternate" hreflang="de" href="{site_url}/de/trust/" />
  <link rel="alternate" hreflang="fr" href="{site_url}/fr/trust/" />
  <link rel="alternate" hreflang="x-default" href="{site_url}/trust/" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="PrivGuide" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="{og_locale}" />
  <meta property="og:image" content="{site_url}/assets/og-cover.svg" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="{icon}" type="image/svg+xml" />
  <link rel="stylesheet" href="{css}" />
  <script type="application/ld+json">
{json.dumps(webpage_ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body data-lang="{lang}" class="trust-page">
  <div class="cursor" id="cursor" aria-hidden="true"></div>
  <div class="cursor-dot" id="cursorDot" aria-hidden="true"></div>
  <a class="skip-link" href="#main">{t(tr, lang, "a11y.skip")}</a>
  <div class="bg-grid" aria-hidden="true"></div>
  <div class="bg-glow" aria-hidden="true"></div>

  <header class="site-header" id="top">
    <nav class="nav container" aria-label="Primary">
      <a href="{home}" class="logo">
        <span class="logo-mark" aria-hidden="true">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <path d="M16 3L5 8v8c0 7.2 4.7 13.9 11 15.5C22.3 29.9 27 23.2 27 16V8L16 3z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M12 16.5l2.5 2.5L20 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
        <span class="logo-text">Priv<span>Guide</span></span>
      </a>
      <ul class="nav-links" id="navLinks">
        <li><a href="{home}#apps">{t(tr, lang, "nav.apps")}</a></li>
        <li><a href="{trust_home}" class="is-current">{t(tr, lang, "nav.trust")}</a></li>
        <li><a href="{home}#life">{t(tr, lang, "nav.life")}</a></li>
        <li><a href="{home}#phone">{t(tr, lang, "nav.phone")}</a></li>
        <li><a href="{home}#desktop">{t(tr, lang, "nav.desktop")}</a></li>
        <li><a href="{home}#paths">{t(tr, lang, "nav.paths")}</a></li>
        <li><a href="{home}#donate">{t(tr, lang, "donate.nav")}</a></li>
        <li><a href="{home}#checklist" class="nav-cta">{t(tr, lang, "nav.checklist")}</a></li>
      </ul>
      <div class="nav-right">
        <div class="lang-switcher" role="navigation" aria-label="{t(tr, lang, "nav.language")}">
          <button type="button" class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false">
            <span class="lang-globe" aria-hidden="true">🌐</span>
            <span class="lang-btn-label">{lang_names[lang]}</span>
            <span class="lang-chevron" aria-hidden="true">▾</span>
          </button>
          <div class="lang-menu" id="langMenu" role="listbox" hidden>
            {"".join(switcher_opts)}
          </div>
        </div>
        <button class="nav-toggle" id="navToggle" aria-label="{t(tr, lang, "a11y.menu_open")}" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
  </header>

  <main id="main" class="trust-main">
    <div class="container narrow trust-wrap">
      <header class="section-head trust-hero-head">
        <p class="eyebrow">{t(tr, lang, "trust_page.eyebrow")}</p>
        <h1>{t(tr, lang, "trust_page.title")}</h1>
        <p class="section-lead">{t(tr, lang, "trust_page.lead")}</p>
        <nav class="trust-toc" aria-label="{t(tr, lang, "trust_page.toc_aria")}">
          <a href="#ownership">{t(tr, lang, "trust_page.ownership_title")}</a>
          <a href="#conflicts">{t(tr, lang, "trust_page.conflicts_title")}</a>
          <a href="#methodology">{t(tr, lang, "trust_page.methodology_title")}</a>
          <a href="#transparency">{t(tr, lang, "trust_page.transparency_title")}</a>
          <a href="#changelog">{t(tr, lang, "trust_page.changelog_title")}</a>
          <a href="#corrections">{t(tr, lang, "trust_page.corrections_title")}</a>
        </nav>
      </header>
{chr(10).join(blocks)}
      <p class="trust-back"><a href="{home}">← {t(tr, lang, "trust_page.back")}</a></p>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container footer-owner">
      <p>
        <strong>{t(tr, lang, "footer.owned_by")}</strong>
        <a href="{COMPANY_URL}" target="_blank" rel="noopener noreferrer">www.vassbrekke.no</a>
        · <a href="https://privydeck.com" target="_blank" rel="noopener noreferrer">privydeck.com</a>
        · <a href="https://www.privbeacon.com" target="_blank" rel="noopener noreferrer">privbeacon.com</a>
      </p>
    </div>
    <div class="container footer-grid">
      <div>
        <a href="{home}" class="logo">
          <span class="logo-mark" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 32 32" fill="none">
              <path d="M16 3L5 8v8c0 7.2 4.7 13.9 11 15.5C22.3 29.9 27 23.2 27 16V8L16 3z" stroke="currentColor" stroke-width="2" fill="none"/>
              <path d="M12 16.5l2.5 2.5L20 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span class="logo-text">Priv<span>Guide</span></span>
        </a>
        <p class="footer-tag">{t(tr, lang, "footer.tag")}</p>
      </div>
      <div>
        <h4>{t(tr, lang, "footer.explore")}</h4>
        <ul>
          <li><a href="{home}#apps">{t(tr, lang, "nav.apps")}</a></li>
          <li><a href="{trust_home}">{t(tr, lang, "footer.trust")}</a></li>
          <li><a href="{home}#life">{t(tr, lang, "nav.life")}</a></li>
          <li><a href="{home}#phone">{t(tr, lang, "nav.phone")}</a></li>
          <li><a href="{home}#desktop">{t(tr, lang, "nav.desktop")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t(tr, lang, "footer.start")}</h4>
        <ul>
          <li><a href="{home}#paths">{t(tr, lang, "nav.paths")}</a></li>
          <li><a href="{home}#checklist">{t(tr, lang, "nav.checklist")}</a></li>
          <li><a href="{home}#faq">{t(tr, lang, "faq.title")}</a></li>
          <li><a href="{CORRECTIONS_URL}" target="_blank" rel="noopener noreferrer">{t(tr, lang, "footer.issues")}</a></li>
          <li><a href="{DISCUSSIONS_URL}" target="_blank" rel="noopener noreferrer">{t(tr, lang, "footer.discussions")}</a></li>
          <li><a href="{home}#donate">{t(tr, lang, "donate.nav")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t(tr, lang, "footer.disclaimer_title")}</h4>
        <p class="footer-fine">{t(tr, lang, "footer.disclaimer")}</p>
      </div>
    </div>
    <div class="container footer-bottom">
      <div class="footer-bottom-meta">
        <p>© <span id="year"></span> <a href="{COMPANY_URL}" target="_blank" rel="noopener noreferrer">Vassbrekke AS</a> · PrivGuide · {t(tr, lang, "footer.built")}</p>
        <p class="footer-privacy">{t(tr, lang, "footer.privacy")}</p>
      </div>
      <!-- PrivBeacon Certified Private Badge -->
      <a class="privbeacon-badge" href="https://privbeacon.com/verify/cmsp6uvg00005zqdcg2zwvx6z" target="_blank" rel="noopener noreferrer">
        <img src="https://privbeacon.com/api/badge/png?siteId=cmsp6uvg00005zqdcg2zwvx6z" alt="PrivBeacon Certified Private — Score 99/100" width="168" height="54" />
      </a>
    </div>
  </footer>
  <script src="{js_main}" defer></script>
</body>
</html>
'''
    return html
