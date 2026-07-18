#!/usr/bin/env python3
"""Build PrivGuide static pages with SEO, app websites, and multi-language support."""

from __future__ import annotations

import json
import re
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://privguide.example"  # replace with real domain when deploying
LANGS = ["en", "no", "es", "de", "fr"]
LANG_NAMES = {
    "en": "English",
    "no": "Norsk",
    "es": "Español",
    "de": "Deutsch",
    "fr": "Français",
}

# Public receiving addresses only — never put private keys here
DONATIONS = [
    {
        "id": "btc",
        "name": "Bitcoin",
        "ticker": "BTC",
        "address": "bc1qr2suucmufh36yay6g2wuhnema7fwmm549ug4ha",
        "uri": "bitcoin:bc1qr2suucmufh36yay6g2wuhnema7fwmm549ug4ha",
    },
    {
        "id": "xmr",
        "name": "Monero",
        "ticker": "XMR",
        "address": "46gac1uxB8i6rCcmb7t2VzUtogwPPp5yVBuxqVbS2YoDcFw9BZu2E5kBRngSZRtQPB5JzHw4paZHuGaeWZ89BUhYPiUB481",
        "uri": "monero:46gac1uxB8i6rCcmb7t2VzUtogwPPp5yVBuxqVbS2YoDcFw9BZu2E5kBRngSZRtQPB5JzHw4paZHuGaeWZ89BUhYPiUB481",
    },
    {
        "id": "evm",
        "name": "Ethereum / EVM",
        "ticker": "EVM",
        "address": "0x5e314E2bB8FfC67dD75629d104890B5feC520f1e",
        "uri": "ethereum:0x5e314E2bB8FfC67dD75629d104890B5feC520f1e",
    },
]

# Official websites for every recommended app
# Vassbrekke AS first-party products are listed first and tagged ours=True
APPS = [
    # —— Vassbrekke AS / VassDev (featured first) ——
    {
        "id": "privydeck",
        "cat": "ours",
        "icon": "🛡️",
        "tag": "Vassbrekke",
        "name": "PrivyDeck",
        "url": "https://privydeck.com",
        "host": "privydeck.com",
        "ours": True,
        "pills": [("ours", "Ours"), ("good", "Top pick"), ("", "Browser · Phone · Vault")],
    },
    {
        "id": "privbeacon",
        "cat": "ours",
        "icon": "📡",
        "tag": "Vassbrekke",
        "name": "PrivBeacon",
        "url": "https://www.privbeacon.com",
        "host": "privbeacon.com",
        "ours": True,
        "pills": [("ours", "Ours"), ("good", "Compliance"), ("", "16 law frameworks")],
    },
    {
        "id": "winprivacy",
        "cat": "ours",
        "icon": "🪟",
        "tag": "Vassbrekke",
        "name": "Windows 11 Privacy Tool",
        "url": "https://github.com/N0L0g1c/Windows-11-Privacy-Enhancing-tool-GUI-and-CLI",
        "host": "github.com · Windows Privacy Tool",
        "ours": True,
        "pills": [("ours", "Ours"), ("good", "Open source"), ("", "Windows 10/11 · GUI + CLI")],
    },
    {
        "id": "sechardening",
        "cat": "ours",
        "icon": "🔐",
        "tag": "Vassbrekke",
        "name": "Security Hardening",
        "url": "https://github.com/N0L0g1c/SecurityHardening",
        "host": "github.com/N0L0g1c/SecurityHardening",
        "ours": True,
        "pills": [("ours", "Ours"), ("", "Linux · Fresh install")],
    },
    # —— Community & third-party recommendations ——
    {
        "id": "signal",
        "cat": "messaging",
        "icon": "💬",
        "tag": "Messaging",
        "name": "Signal",
        "url": "https://signal.org",
        "host": "signal.org",
        "pills": [("good", "E2EE"), ("", "iOS · Android · Desktop")],
    },
    {
        "id": "session",
        "cat": "messaging",
        "icon": "🌑",
        "tag": "Messaging",
        "name": "Session",
        "url": "https://getsession.org",
        "host": "getsession.org",
        "pills": [("good", "No phone #"), ("", "Cross-platform")],
    },
    {
        "id": "element",
        "cat": "messaging",
        "icon": "⬡",
        "tag": "Messaging",
        "name": "Element (Matrix)",
        "url": "https://element.io",
        "host": "element.io",
        "pills": [("good", "Self-hostable"), ("", "Teams · Communities")],
    },
    {
        "id": "firefox",
        "cat": "browser",
        "icon": "🦊",
        "tag": "Browser",
        "name": "Firefox",
        "url": "https://www.mozilla.org/firefox/",
        "host": "mozilla.org/firefox",
        "pills": [("good", "Recommended"), ("", "Desktop · Mobile")],
    },
    {
        "id": "brave",
        "cat": "browser",
        "icon": "🦁",
        "tag": "Browser",
        "name": "Brave",
        "url": "https://brave.com",
        "host": "brave.com",
        "pills": [("", "Easy switch"), ("", "Desktop · Mobile")],
    },
    {
        "id": "tor",
        "cat": "browser",
        "icon": "🧅",
        "tag": "Browser",
        "name": "Tor Browser",
        "url": "https://www.torproject.org",
        "host": "torproject.org",
        "pills": [("good", "Anonymity"), ("", "Desktop · Android")],
    },
    {
        "id": "mullvad_browser",
        "cat": "browser",
        "icon": "🔒",
        "tag": "Browser",
        "name": "Mullvad Browser",
        "url": "https://mullvad.net/browser",
        "host": "mullvad.net/browser",
        "pills": [("", "Anti-fingerprint"), ("", "Desktop")],
    },
    {
        "id": "mullvad",
        "cat": "vpn",
        "icon": "🇸🇪",
        "tag": "VPN",
        "name": "Mullvad VPN",
        "url": "https://mullvad.net",
        "host": "mullvad.net",
        "pills": [("good", "Top pick"), ("", "All platforms")],
    },
    {
        "id": "protonvpn",
        "cat": "vpn",
        "icon": "🟣",
        "tag": "VPN",
        "name": "Proton VPN",
        "url": "https://protonvpn.com",
        "host": "protonvpn.com",
        "pills": [("", "Free tier"), ("", "All platforms")],
    },
    {
        "id": "ivpn",
        "cat": "vpn",
        "icon": "🛡️",
        "tag": "VPN",
        "name": "IVPN",
        "url": "https://www.ivpn.net",
        "host": "ivpn.net",
        "pills": [("", "No-logs"), ("", "Desktop · Mobile")],
    },
    {
        "id": "bitwarden",
        "cat": "passwords",
        "icon": "🔑",
        "tag": "Passwords",
        "name": "Bitwarden",
        "url": "https://bitwarden.com",
        "host": "bitwarden.com",
        "pills": [("good", "Best default"), ("", "All platforms")],
    },
    {
        "id": "keepassxc",
        "cat": "passwords",
        "icon": "🗄️",
        "tag": "Passwords",
        "name": "KeePassXC",
        "url": "https://keepassxc.org",
        "host": "keepassxc.org",
        "pills": [("good", "Local-first"), ("", "Desktop (+ mobile ports)")],
    },
    {
        "id": "protonpass",
        "cat": "passwords",
        "icon": "🔐",
        "tag": "Passwords",
        "name": "Proton Pass",
        "url": "https://proton.me/pass",
        "host": "proton.me/pass",
        "pills": [("", "Ecosystem"), ("", "All platforms")],
    },
    {
        "id": "protonmail",
        "cat": "email",
        "icon": "✉️",
        "tag": "Email",
        "name": "Proton Mail",
        "url": "https://proton.me/mail",
        "host": "proton.me/mail",
        "pills": [("good", "Popular"), ("", "Web · Apps")],
    },
    {
        "id": "tuta",
        "cat": "email",
        "icon": "🟢",
        "tag": "Email",
        "name": "Tuta (Tutanota)",
        "url": "https://tuta.com",
        "host": "tuta.com",
        "pills": [("", "Encrypted calendar"), ("", "Web · Apps")],
    },
    {
        "id": "thunderbird",
        "cat": "email",
        "icon": "🦅",
        "tag": "Email",
        "name": "Thunderbird",
        "url": "https://www.thunderbird.net",
        "host": "thunderbird.net",
        "pills": [("", "OpenPGP"), ("", "Desktop")],
    },
    {
        "id": "ddg",
        "cat": "search",
        "icon": "🦆",
        "tag": "Search",
        "name": "DuckDuckGo",
        "url": "https://duckduckgo.com",
        "host": "duckduckgo.com",
        "pills": [("", "Easy win"), ("", "Web · Apps")],
    },
    {
        "id": "bravesearch",
        "cat": "search",
        "icon": "🔍",
        "tag": "Search",
        "name": "Brave Search / Startpage",
        "url": "https://search.brave.com",
        "host": "search.brave.com",
        "url2": "https://www.startpage.com",
        "host2": "startpage.com",
        "pills": [("", "Google-quality options"), ("", "Web")],
    },
    {
        "id": "searxng",
        "cat": "search",
        "icon": "🧩",
        "tag": "Search",
        "name": "SearXNG",
        "url": "https://searxng.org",
        "host": "searxng.org",
        "pills": [("good", "Self-host"), ("", "Web")],
    },
    {
        "id": "protondrive",
        "cat": "storage",
        "icon": "☁️",
        "tag": "Storage",
        "name": "Proton Drive / Tresorit",
        "url": "https://proton.me/drive",
        "host": "proton.me/drive",
        "url2": "https://tresorit.com",
        "host2": "tresorit.com",
        "pills": [("", "E2EE cloud"), ("", "Cross-platform")],
    },
    {
        "id": "cryptomator",
        "cat": "storage",
        "icon": "🧊",
        "tag": "Storage",
        "name": "Cryptomator",
        "url": "https://cryptomator.org",
        "host": "cryptomator.org",
        "pills": [("good", "Works with any cloud"), ("", "Desktop · Mobile")],
    },
    {
        "id": "nextcloud",
        "cat": "storage",
        "icon": "🏠",
        "tag": "Storage",
        "name": "Nextcloud / Syncthing",
        "url": "https://nextcloud.com",
        "host": "nextcloud.com",
        "url2": "https://syncthing.net",
        "host2": "syncthing.net",
        "pills": [("", "Own the iron"), ("", "Self-host · P2P")],
    },
    {
        "id": "aegis",
        "cat": "auth",
        "icon": "📲",
        "tag": "2FA",
        "name": "Aegis Authenticator",
        "url": "https://getaegis.app",
        "host": "getaegis.app",
        "pills": [("good", "Android"), ("", "Offline")],
    },
    {
        "id": "enteauth",
        "cat": "auth",
        "icon": "🧬",
        "tag": "2FA",
        "name": "Ente Auth",
        "url": "https://ente.io/auth",
        "host": "ente.io/auth",
        "pills": [("", "Cross-platform"), ("", "Encrypted sync")],
    },
    {
        "id": "yubikey",
        "cat": "auth",
        "icon": "🔑",
        "tag": "Auth",
        "name": "YubiKey / hardware keys",
        "url": "https://www.yubico.com",
        "host": "yubico.com",
        "pills": [("good", "Phishing-resistant"), ("", "Hardware")],
    },
    {
        "id": "graphene",
        "cat": "os",
        "icon": "🟩",
        "tag": "Mobile OS",
        "name": "GrapheneOS",
        "url": "https://grapheneos.org",
        "host": "grapheneos.org",
        "pills": [("good", "Highest bar"), ("", "Pixel only")],
    },
    {
        "id": "linux",
        "cat": "os",
        "icon": "🐧",
        "tag": "Desktop OS",
        "name": "Linux (Fedora / Debian / Qubes)",
        "url": "https://fedoraproject.org",
        "host": "fedoraproject.org",
        "url2": "https://www.qubes-os.org",
        "host2": "qubes-os.org",
        "pills": [("", "Own your OS"), ("", "Desktop")],
    },
    {
        "id": "ios",
        "cat": "os",
        "icon": "🔵",
        "tag": "Mobile OS",
        "name": "iOS (hardened)",
        "url": "https://support.apple.com/guide/iphone/protect-your-web-browsing-iph01f4a43a5/ios",
        "host": "support.apple.com",
        "pills": [("", "Good baseline"), ("", "iPhone · iPad")],
    },
    {
        "id": "organicmaps",
        "cat": "extra",
        "icon": "🗺️",
        "tag": "Maps",
        "name": "Organic Maps / OsmAnd",
        "url": "https://organicmaps.app",
        "host": "organicmaps.app",
        "url2": "https://osmand.net",
        "host2": "osmand.net",
        "pills": [("", "Offline"), ("", "Mobile")],
    },
    {
        "id": "notes",
        "cat": "extra",
        "icon": "📝",
        "tag": "Notes",
        "name": "Standard Notes / Joplin",
        "url": "https://standardnotes.com",
        "host": "standardnotes.com",
        "url2": "https://joplinapp.org",
        "host2": "joplinapp.org",
        "pills": [("", "E2EE notes"), ("", "Cross-platform")],
    },
    {
        "id": "ublock",
        "cat": "extra",
        "icon": "🚫",
        "tag": "Blockers",
        "name": "uBlock Origin",
        "url": "https://ublockorigin.com",
        "host": "ublockorigin.com",
        "pills": [("good", "FOSS classic"), ("", "Browser extension")],
    },
    {
        "id": "rethinkdns",
        "cat": "extra",
        "icon": "🌐",
        "tag": "Blockers",
        "name": "RethinkDNS",
        "url": "https://rethinkdns.com",
        "host": "rethinkdns.com",
        "pills": [("", "DNS + firewall"), ("", "Android")],
    },
    {
        "id": "photos",
        "cat": "extra",
        "icon": "📸",
        "tag": "Photos",
        "name": "Ente Photos / Immich",
        "url": "https://ente.io",
        "host": "ente.io",
        "url2": "https://immich.app",
        "host2": "immich.app",
        "pills": [("", "E2EE or self-host"), ("", "Mobile · Server")],
    },
    {
        "id": "calling",
        "cat": "extra",
        "icon": "📞",
        "tag": "Calling",
        "name": "Signal calls · Jitsi",
        "url": "https://signal.org",
        "host": "signal.org",
        "url2": "https://jitsi.org",
        "host2": "jitsi.org",
        "pills": [("", "E2EE options"), ("", "Mobile · Desktop")],
    },
]


def load_translations() -> dict:
    path = ROOT / "locales" / "translations.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def t(translations: dict, lang: str, key: str) -> str:
    node = translations.get(lang) or translations["en"]
    parts = key.split(".")
    cur = node
    for p in parts:
        if not isinstance(cur, dict) or p not in cur:
            # fallback en
            cur = translations["en"]
            for p2 in parts:
                cur = cur[p2]
            return str(cur)
        cur = cur[p]
    return str(cur)


def path_for(lang: str) -> str:
    return f"/{lang}/" if lang != "en" else "/"


def asset_prefix(lang: str) -> str:
    return ".." if lang != "en" else "."


def hreflang_links(lang: str) -> str:
    lines = []
    for l in LANGS:
        href = f"{SITE_URL}{path_for(l)}"
        lines.append(f'  <link rel="alternate" hreflang="{l}" href="{href}" />')
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/" />')
    return "\n".join(lines)


def lang_switcher(lang: str, prefix: str) -> str:
    opts = []
    for l in LANGS:
        href = f"{prefix}/{l}/index.html" if False else (
            f"{prefix}/index.html" if l == "en" else f"{prefix}/{l}/index.html"
        )
        # prefix is "." for en page in root? We'll put en at root as index.html and also en/index.html
        if l == "en":
            href = f"{prefix}/index.html" if prefix == "." else "../index.html"
        else:
            href = f"{l}/index.html" if prefix == "." else f"../{l}/index.html"
        selected = " selected" if l == lang else ""
        active = " class=\"lang-option active\"" if l == lang else " class=\"lang-option\""
        opts.append(
            f'<a href="{href}" hreflang="{l}" lang="{l}"{active} data-lang="{l}">{LANG_NAMES[l]}</a>'
        )
    return (
        '<div class="lang-switcher" role="navigation" aria-label="Language">'
        '<button type="button" class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false">'
        f'<span class="lang-btn-label">{LANG_NAMES[lang]}</span><span class="lang-chevron" aria-hidden="true">▾</span>'
        "</button>"
        f'<div class="lang-menu" id="langMenu" role="listbox" hidden>{"".join(opts)}</div>'
        "</div>"
    )


def app_card_html(app: dict, tr: dict, lang: str) -> str:
    desc = t(tr, lang, f"apps.{app['id']}.desc")
    why = t(tr, lang, f"apps.{app['id']}.why")
    use_when = t(tr, lang, "apps.use_when")
    pills = []
    for kind, label in app["pills"]:
        # Localize built-in pill labels where we have translations
        if kind == "ours":
            label = t(tr, lang, "apps.ours_pill")
            cls = "pill pill-ours"
        elif kind == "good":
            cls = "pill pill-good"
        else:
            cls = "pill"
        pills.append(f'<span class="{cls}">{label}</span>')
    pills_html = "".join(pills)
    links = (
        f'<a class="app-site" href="{app["url"]}" target="_blank" rel="noopener noreferrer" '
        f'title="{app["name"]}">{app["host"]} ↗</a>'
    )
    if app.get("url2"):
        links += (
            f'<a class="app-site app-site-secondary" href="{app["url2"]}" target="_blank" '
            f'rel="noopener noreferrer">{app["host2"]} ↗</a>'
        )
    ours_class = " app-card-ours" if app.get("ours") else ""
    publisher = ""
    author_meta = ""
    if app.get("ours"):
        publisher = (
            f'<p class="app-publisher">{t(tr, lang, "apps.by_vassbrekke")} · '
            f'<a href="https://www.vassbrekke.no" target="_blank" rel="noopener noreferrer">vassbrekke.no</a></p>'
        )
        author_meta = '<meta itemprop="author" content="Vassbrekke AS" />'
    return f'''          <article class="app-card{ours_class}" data-cat="{app["cat"]}" itemscope itemtype="https://schema.org/SoftwareApplication">
            <div class="app-top">
              <span class="app-icon" aria-hidden="true">{app["icon"]}</span>
              <span class="app-tag">{app["tag"]}</span>
            </div>
            <h3 itemprop="name">{app["name"]}</h3>
            {publisher}
            <p itemprop="description">{desc}</p>
            <div class="app-meta">{pills_html}</div>
            <div class="app-links">{links}</div>
            <meta itemprop="url" content="{app["url"]}" />
            <meta itemprop="applicationCategory" content="SecurityApplication" />
            {author_meta}
            <p class="app-why"><strong>{use_when}</strong> {why}</p>
          </article>'''


def checklist_items(tr: dict, lang: str, group: str, ids: list[str]) -> str:
    lines = []
    for i in ids:
        text = t(tr, lang, f"checklist.items.{i}")
        lines.append(
            f'            <label class="check-item"><input type="checkbox" data-id="{i}" /> {text}</label>'
        )
    return "\n".join(lines)


def donate_cards_html(tr: dict, lang: str) -> str:
    copy_label = t(tr, lang, "donate.copy")
    open_wallet = t(tr, lang, "donate.open_wallet")
    cards = []
    for coin in DONATIONS:
        addr_esc = esc(coin["address"], quote=True)
        name_esc = esc(coin["name"], quote=True)
        ticker_esc = esc(coin["ticker"], quote=True)
        uri_esc = esc(coin["uri"], quote=True)
        note = t(tr, lang, f"donate.{coin['id']}.note")
        cards.append(
            f'''          <article class="donate-card" data-reveal>
            <div class="donate-card-top">
              <span class="donate-ticker">{ticker_esc}</span>
              <h3>{name_esc}</h3>
            </div>
            <p class="donate-note">{esc(note)}</p>
            <code class="donate-address" translate="no">{addr_esc}</code>
            <div class="donate-actions">
              <button type="button" class="btn btn-primary donate-copy" data-copy="{addr_esc}">
                {esc(copy_label)}
              </button>
              <a class="btn btn-ghost" href="{uri_esc}">{esc(open_wallet)}</a>
            </div>
          </article>'''
        )
    return "\n".join(cards)


def render_page(lang: str, tr: dict) -> str:
    prefix = asset_prefix(lang)
    # Asset paths
    if lang == "en":
        css = "css/styles.css"
        js_main = "js/main.js"
        js_i18n = "js/i18n.js"
        # en lives at root
        home_href = "#top"
        path_prefix = ""
    else:
        css = "../css/styles.css"
        js_main = "../js/main.js"
        js_i18n = "../js/i18n.js"
        home_href = "#top"
        path_prefix = "../"

    title = t(tr, lang, "meta.title")
    description = t(tr, lang, "meta.description")
    keywords = t(tr, lang, "meta.keywords")
    og_locale = {
        "en": "en_US",
        "no": "nb_NO",
        "es": "es_ES",
        "de": "de_DE",
        "fr": "fr_FR",
    }[lang]
    canonical = f"{SITE_URL}{path_for(lang)}"

    # Build app cards
    cards = "\n\n".join(app_card_html(a, tr, lang) for a in APPS)

    # Filters
    filters = [
        ("all", t(tr, lang, "filters.all")),
        ("ours", t(tr, lang, "filters.ours")),
        ("messaging", t(tr, lang, "filters.messaging")),
        ("browser", t(tr, lang, "filters.browser")),
        ("vpn", t(tr, lang, "filters.vpn")),
        ("passwords", t(tr, lang, "filters.passwords")),
        ("email", t(tr, lang, "filters.email")),
        ("search", t(tr, lang, "filters.search")),
        ("storage", t(tr, lang, "filters.storage")),
        ("auth", t(tr, lang, "filters.auth")),
        ("os", t(tr, lang, "filters.os")),
        ("extra", t(tr, lang, "filters.extra")),
    ]
    filter_btns = []
    for i, (fid, label) in enumerate(filters):
        active = " active" if i == 0 else ""
        sel = "true" if i == 0 else "false"
        filter_btns.append(
            f'          <button class="filter-btn{active}" data-filter="{fid}" role="tab" aria-selected="{sel}">{label}</button>'
        )

    # FAQ JSON-LD
    faq_entities = []
    for i in range(1, 7):
        faq_entities.append(
            {
                "@type": "Question",
                "name": t(tr, lang, f"faq.q{i}"),
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": t(tr, lang, f"faq.a{i}"),
                },
            }
        )

    app_list_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": t(tr, lang, "apps.title"),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "SoftwareApplication",
                    "name": a["name"],
                    "url": a["url"],
                    "applicationCategory": "SecurityApplication",
                    "operatingSystem": "Android, iOS, Windows, macOS, Linux",
                    "description": t(tr, lang, f"apps.{a['id']}.desc"),
                },
            }
            for i, a in enumerate(APPS)
        ],
    }

    website_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "PrivGuide",
        "url": canonical,
        "description": description,
        "inLanguage": lang,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{canonical}#apps",
            "query-input": "required name=search_term_string",
        },
    }

    webpage_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": "PrivGuide", "url": SITE_URL},
        "publisher": {
            "@type": "Organization",
            "name": "Vassbrekke AS",
            "url": "https://www.vassbrekke.no",
            "sameAs": [
                "https://www.vassbrekke.no",
                "https://privydeck.com",
                "https://www.privbeacon.com",
            ],
        },
        "copyrightHolder": {
            "@type": "Organization",
            "name": "Vassbrekke AS",
            "url": "https://www.vassbrekke.no",
        },
        "about": {
            "@type": "Thing",
            "name": "Digital privacy",
            "description": "Personal privacy apps, phone hardening, desktop security, and everyday privacy habits",
        },
        "primaryImageOfPage": f"{SITE_URL}/assets/og-cover.svg",
    }

    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities,
    }

    howto_ld = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": t(tr, lang, "checklist.title"),
        "description": t(tr, lang, "checklist.lead"),
        "step": [
            {
                "@type": "HowToStep",
                "position": i + 1,
                "name": t(tr, lang, f"checklist.items.c{i+1}")[:80],
                "text": t(tr, lang, f"checklist.items.c{i+1}"),
            }
            for i in range(6)
        ],
    }

    def jld(obj: dict) -> str:
        return json.dumps(obj, ensure_ascii=False, indent=2)

    # Lang switcher paths relative to current page
    switcher_opts = []
    for l in LANGS:
        if lang == "en":
            href = "index.html" if l == "en" else f"{l}/index.html"
        else:
            href = "../index.html" if l == "en" else f"../{l}/index.html"
        active = " active" if l == lang else ""
        switcher_opts.append(
            f'<a href="{href}" hreflang="{l}" lang="{l}" class="lang-option{active}" data-lang="{l}" role="option" aria-selected="{str(l==lang).lower()}">{LANG_NAMES[l]}</a>'
        )
    switcher = f'''      <div class="lang-switcher" role="navigation" aria-label="{t(tr, lang, "nav.language")}">
        <button type="button" class="lang-btn" id="langBtn" aria-haspopup="listbox" aria-expanded="false">
          <span class="lang-globe" aria-hidden="true">🌐</span>
          <span class="lang-btn-label">{LANG_NAMES[lang]}</span>
          <span class="lang-chevron" aria-hidden="true">▾</span>
        </button>
        <div class="lang-menu" id="langMenu" role="listbox" hidden>
          {"".join(switcher_opts)}
        </div>
      </div>'''

    # Helper for multi-line list items
    def lis(key_prefix: str, n: int) -> str:
        return "\n".join(
            f"              <li>{t(tr, lang, f'{key_prefix}.{i}')}</li>" for i in range(1, n + 1)
        )

    def steps(key_prefix: str, n: int) -> str:
        out = []
        for i in range(1, n + 1):
            raw = t(tr, lang, f"{key_prefix}.{i}")
            # bold first sentence fragment before colon if present
            if ":" in raw[:80]:
                head, rest = raw.split(":", 1)
                out.append(f"                  <li><strong>{head}:</strong>{rest}</li>")
            else:
                out.append(f"                  <li>{raw}</li>")
        return "\n".join(out)

    faq_html = []
    for i in range(1, 7):
        faq_html.append(
            f'''          <details class="faq-item">
            <summary>{t(tr, lang, f"faq.q{i}")}</summary>
            <p>{t(tr, lang, f"faq.a{i}")}</p>
          </details>'''
        )

    principles = []
    for i in range(1, 7):
        principles.append(
            f'''          <article class="principle">
            <h3>{t(tr, lang, f"principles.p{i}.title")}</h3>
            <p>{t(tr, lang, f"principles.p{i}.body")}</p>
          </article>'''
        )

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="author" content="PrivGuide" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow" />
  <meta name="theme-color" content="#05010d" />
  <meta name="color-scheme" content="dark" />
  <meta name="referrer" content="no-referrer" />
  <meta name="format-detection" content="telephone=no" />
  <link rel="canonical" href="{canonical}" />
{hreflang_links(lang)}

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="PrivGuide" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:locale" content="{og_locale}" />
  <meta property="og:image" content="{SITE_URL}/assets/og-cover.svg" />
  <meta property="og:image:alt" content="PrivGuide — privacy apps and personal privacy guide" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />
  <meta name="twitter:image" content="{SITE_URL}/assets/og-cover.svg" />

  <link rel="icon" href="{prefix}/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="{prefix}/assets/favicon.svg" />
  <link rel="manifest" href="{prefix}/site.webmanifest" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@400;500;600;700&family=Orbitron:wght@500;600;700;800&family=Share+Tech+Mono&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{css}" />

  <script type="application/ld+json">
{jld(website_ld)}
  </script>
  <script type="application/ld+json">
{jld(webpage_ld)}
  </script>
  <script type="application/ld+json">
{jld(app_list_ld)}
  </script>
  <script type="application/ld+json">
{jld(faq_ld)}
  </script>
  <script type="application/ld+json">
{jld(howto_ld)}
  </script>
</head>
<body data-lang="{lang}">
  <div class="page-loader" id="pageLoader" aria-hidden="true">
    <div class="loader-inner">
      <div class="loader-brand">PRIVGUIDE</div>
      <div class="loader-bar"><div class="loader-fill" id="loaderFill"></div></div>
      <div class="loader-pct" id="loaderPct">0%</div>
      <div class="loader-tag">jacking in…</div>
    </div>
  </div>
  <div class="cursor" id="cursor" aria-hidden="true"></div>
  <div class="cursor-dot" id="cursorDot" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
  <canvas id="fx-canvas" aria-hidden="true"></canvas>
  <div class="spotlight" aria-hidden="true"></div>
  <div class="scanlines" aria-hidden="true"></div>

  <a class="skip-link" href="#main">{t(tr, lang, "a11y.skip")}</a>
  <div class="bg-grid" aria-hidden="true"></div>
  <div class="bg-glow" aria-hidden="true"></div>

  <nav class="section-nav" aria-label="Sections">
    <a href="#top" class="is-active"><span>Top</span></a>
    <a href="#paths"><span>Paths</span></a>
    <a href="#apps"><span>Apps</span></a>
    <a href="#life"><span>Life</span></a>
    <a href="#phone"><span>Phone</span></a>
    <a href="#desktop"><span>Desktop</span></a>
    <a href="#checklist"><span>List</span></a>
  </nav>

  <header class="site-header" id="top">
    <nav class="nav container" aria-label="Primary">
      <a href="{home_href}" class="logo">
        <span class="logo-mark" aria-hidden="true">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <path d="M16 3L5 8v8c0 7.2 4.7 13.9 11 15.5C22.3 29.9 27 23.2 27 16V8L16 3z" stroke="currentColor" stroke-width="2" fill="none"/>
            <path d="M12 16.5l2.5 2.5L20 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </span>
        <span class="logo-text">Priv<span>Guide</span></span>
      </a>
      <ul class="nav-links" id="navLinks">
        <li><a href="#apps">{t(tr, lang, "nav.apps")}</a></li>
        <li><a href="#life">{t(tr, lang, "nav.life")}</a></li>
        <li><a href="#phone">{t(tr, lang, "nav.phone")}</a></li>
        <li><a href="#desktop">{t(tr, lang, "nav.desktop")}</a></li>
        <li><a href="#paths">{t(tr, lang, "nav.paths")}</a></li>
        <li><a href="#checklist" class="nav-cta">{t(tr, lang, "nav.checklist")}</a></li>
      </ul>
      <div class="nav-right">
{switcher}
        <button class="nav-toggle" id="navToggle" aria-label="{t(tr, lang, "a11y.menu_open")}" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
  </header>

  <main id="main">
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy" data-reveal="left">
          <p class="eyebrow">
            <span class="pulse"></span>
            {t(tr, lang, "hero.eyebrow")}
          </p>
          <h1>
            <span class="line">{t(tr, lang, "hero.h1a")}</span>
            <span class="line gradient-text">{t(tr, lang, "hero.h1b")}</span>
          </h1>
          <p class="hero-lead">{t(tr, lang, "hero.lead")}</p>
          <div class="hero-actions">
            <a href="#apps" class="btn btn-primary">{t(tr, lang, "hero.cta_apps")}</a>
            <a href="#paths" class="btn btn-ghost">{t(tr, lang, "hero.cta_path")}</a>
          </div>
          <ul class="hero-stats" role="list">
            <li><strong>40+</strong><span>{t(tr, lang, "hero.stat_tools")}</span></li>
            <li><strong>3</strong><span>{t(tr, lang, "hero.stat_levels")}</span></li>
            <li><strong>0</strong><span>{t(tr, lang, "hero.stat_trackers")}</span></li>
          </ul>
        </div>
        <div class="hero-card" aria-hidden="true" data-reveal="right">
          <div class="terminal">
            <div class="terminal-bar">
              <span></span><span></span><span></span>
              <em>privacy-stack.sh</em>
            </div>
            <pre class="terminal-body"><code><span class="cmt"># Everyday privacy stack · Vassbrekke</span>
<span class="cmd">blockers</span>   → PrivyDeck
<span class="cmd">messenger</span>  → Signal / Session
<span class="cmd">browser</span>    → Firefox (+ uBlock)
<span class="cmd">search</span>     → DuckDuckGo / Brave
<span class="cmd">passwords</span>  → Bitwarden
<span class="cmd">email</span>      → Proton Mail
<span class="cmd">vpn</span>        → Mullvad / Proton
<span class="ok">✓</span> {t(tr, lang, "hero.terminal_ok")}</code></pre>
          </div>
        </div>
      </div>
    </section>

    <section class="trust-strip" aria-label="{t(tr, lang, "trust.aria")}">
      <div class="container trust-grid">
        <div class="trust-item" data-reveal data-reveal-delay="1">
          <span class="trust-icon">🛡️</span>
          <div>
            <strong>{t(tr, lang, "trust.1.title")}</strong>
            <p>{t(tr, lang, "trust.1.body")}</p>
          </div>
        </div>
        <div class="trust-item" data-reveal data-reveal-delay="2">
          <span class="trust-icon">📱</span>
          <div>
            <strong>{t(tr, lang, "trust.2.title")}</strong>
            <p>{t(tr, lang, "trust.2.body")}</p>
          </div>
        </div>
        <div class="trust-item" data-reveal data-reveal-delay="3">
          <span class="trust-icon">🌍</span>
          <div>
            <strong>{t(tr, lang, "trust.3.title")}</strong>
            <p>{t(tr, lang, "trust.3.body")}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="paths">
      <div class="container">
        <header class="section-head" data-reveal>
          <p class="eyebrow">{t(tr, lang, "paths.eyebrow")}</p>
          <h2>{t(tr, lang, "paths.title")}</h2>
          <p class="section-lead">{t(tr, lang, "paths.lead")}</p>
        </header>
        <div class="path-grid">
          <article class="path-card path-beginner" data-level="01" data-reveal data-reveal-delay="1">
            <div class="path-badge">{t(tr, lang, "paths.l1.badge")}</div>
            <h3>{t(tr, lang, "paths.l1.title")}</h3>
            <p>{t(tr, lang, "paths.l1.body")}</p>
            <ul>
{lis("paths.l1", 5)}
            </ul>
            <a href="#checklist" class="path-link" data-level="beginner">{t(tr, lang, "paths.l1.cta")}</a>
          </article>
          <article class="path-card path-solid featured" data-level="02" data-reveal data-reveal-delay="2">
            <div class="path-badge">{t(tr, lang, "paths.l2.badge")}</div>
            <h3>{t(tr, lang, "paths.l2.title")}</h3>
            <p>{t(tr, lang, "paths.l2.body")}</p>
            <ul>
{lis("paths.l2", 5)}
            </ul>
            <a href="#apps" class="path-link" data-level="solid">{t(tr, lang, "paths.l2.cta")}</a>
          </article>
          <article class="path-card path-advanced" data-level="03" data-reveal data-reveal-delay="3">
            <div class="path-badge">{t(tr, lang, "paths.l3.badge")}</div>
            <h3>{t(tr, lang, "paths.l3.title")}</h3>
            <p>{t(tr, lang, "paths.l3.body")}</p>
            <ul>
{lis("paths.l3", 5)}
            </ul>
            <a href="#phone" class="path-link" data-level="advanced">{t(tr, lang, "paths.l3.cta")}</a>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="apps">
      <div class="container">
        <header class="section-head" data-reveal>
          <p class="eyebrow">{t(tr, lang, "apps.eyebrow")}</p>
          <h2>{t(tr, lang, "apps.title")}</h2>
          <p class="section-lead">{t(tr, lang, "apps.lead")}</p>
        </header>

        <aside class="ours-banner" id="vassbrekke" data-reveal="scale">
          <div class="ours-banner-copy">
            <p class="ours-banner-label">{t(tr, lang, "ours.badge")}</p>
            <h3>{t(tr, lang, "ours.title")}</h3>
            <p>{t(tr, lang, "ours.body")}</p>
            <div class="ours-banner-links">
              <a class="btn btn-primary btn-sm" href="https://privydeck.com" target="_blank" rel="noopener noreferrer">PrivyDeck ↗</a>
              <a class="btn btn-ghost btn-sm" href="https://www.privbeacon.com" target="_blank" rel="noopener noreferrer">PrivBeacon ↗</a>
              <a class="btn btn-ghost btn-sm" href="https://www.vassbrekke.no" target="_blank" rel="noopener noreferrer">vassbrekke.no ↗</a>
            </div>
          </div>
        </aside>

        <div class="filter-bar" role="tablist" aria-label="{t(tr, lang, "filters.aria")}">
{chr(10).join(filter_btns)}
        </div>

        <div class="app-grid" id="appGrid">
{cards}
        </div>

        <p class="apps-note">{t(tr, lang, "apps.note")}</p>
      </div>
    </section>

    <section class="section" id="life">
      <div class="container">
        <header class="section-head" data-reveal>
          <p class="eyebrow">{t(tr, lang, "life.eyebrow")}</p>
          <h2>{t(tr, lang, "life.title")}</h2>
          <p class="section-lead">{t(tr, lang, "life.lead")}</p>
        </header>
        <div class="life-grid">
          <article class="life-card" data-reveal data-reveal-delay="1">
            <div class="life-num">01</div>
            <h3>{t(tr, lang, "life.1.title")}</h3>
            <ul>
{lis("life.1", 5)}
            </ul>
          </article>
          <article class="life-card" data-reveal data-reveal-delay="2">
            <div class="life-num">02</div>
            <h3>{t(tr, lang, "life.2.title")}</h3>
            <ul>
{lis("life.2", 5)}
            </ul>
          </article>
          <article class="life-card" data-reveal data-reveal-delay="3">
            <div class="life-num">03</div>
            <h3>{t(tr, lang, "life.3.title")}</h3>
            <ul>
{lis("life.3", 5)}
            </ul>
          </article>
          <article class="life-card" data-reveal data-reveal-delay="4">
            <div class="life-num">04</div>
            <h3>{t(tr, lang, "life.4.title")}</h3>
            <ul>
{lis("life.4", 5)}
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="phone">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "phone.eyebrow")}</p>
          <h2>{t(tr, lang, "phone.title")}</h2>
          <p class="section-lead">{t(tr, lang, "phone.lead")}</p>
        </header>

        <div class="platform-tabs" role="tablist" aria-label="{t(tr, lang, "phone.tabs_aria")}">
          <button class="platform-tab active" data-platform="android" role="tab" aria-selected="true">Android</button>
          <button class="platform-tab" data-platform="ios" role="tab" aria-selected="false">iOS</button>
        </div>

        <div class="platform-panels">
          <div class="platform-panel active" id="panel-android" role="tabpanel">
            <div class="split">
              <div>
                <h3>{t(tr, lang, "phone.android.title")}</h3>
                <ol class="step-list">
{steps("phone.android", 10)}
                </ol>
              </div>
              <aside class="callout">
                <h4>{t(tr, lang, "phone.android.stack")}</h4>
                <ul>
                  <li>PrivyDeck · Signal · Bitwarden</li>
                  <li>Aegis · Firefox / Vanadium</li>
                  <li>Organic Maps · Proton Mail</li>
                  <li>Mullvad / Proton VPN</li>
                  <li>NewPipe / LibreTube</li>
                </ul>
                <p class="callout-note">{t(tr, lang, "phone.android.note")}</p>
              </aside>
            </div>
          </div>

          <div class="platform-panel" id="panel-ios" role="tabpanel" hidden>
            <div class="split">
              <div>
                <h3>{t(tr, lang, "phone.ios.title")}</h3>
                <ol class="step-list">
{steps("phone.ios", 10)}
                </ol>
              </div>
              <aside class="callout">
                <h4>{t(tr, lang, "phone.ios.stack")}</h4>
                <ul>
                  <li>PrivyDeck · Signal · Bitwarden</li>
                  <li>Ente Auth · Firefox / Brave</li>
                  <li>Proton Mail · Organic Maps</li>
                  <li>Mullvad / Proton VPN</li>
                  <li>Lockdown Mode when needed</li>
                </ul>
                <p class="callout-note">{t(tr, lang, "phone.ios.note")}</p>
              </aside>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="desktop">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "desktop.eyebrow")}</p>
          <h2>{t(tr, lang, "desktop.title")}</h2>
          <p class="section-lead">{t(tr, lang, "desktop.lead")}</p>
        </header>

        <div class="desktop-grid">
          <article class="desk-card">
            <h3><span>🪟</span> Windows</h3>
            <ul>
{lis("desktop.windows", 7)}
            </ul>
          </article>
          <article class="desk-card">
            <h3><span></span> macOS</h3>
            <ul>
{lis("desktop.macos", 7)}
            </ul>
          </article>
          <article class="desk-card">
            <h3><span>🐧</span> Linux</h3>
            <ul>
{lis("desktop.linux", 7)}
            </ul>
          </article>
        </div>

        <div class="desk-universal">
          <h3>{t(tr, lang, "desktop.universal_title")}</h3>
          <div class="universal-grid">
            <div class="u-item"><strong>{t(tr, lang, "desktop.u1.title")}</strong><p>{t(tr, lang, "desktop.u1.body")}</p></div>
            <div class="u-item"><strong>{t(tr, lang, "desktop.u2.title")}</strong><p>{t(tr, lang, "desktop.u2.body")}</p></div>
            <div class="u-item"><strong>{t(tr, lang, "desktop.u3.title")}</strong><p>{t(tr, lang, "desktop.u3.body")}</p></div>
            <div class="u-item"><strong>{t(tr, lang, "desktop.u4.title")}</strong><p>{t(tr, lang, "desktop.u4.body")}</p></div>
            <div class="u-item"><strong>{t(tr, lang, "desktop.u5.title")}</strong><p>{t(tr, lang, "desktop.u5.body")}</p></div>
            <div class="u-item"><strong>{t(tr, lang, "desktop.u6.title")}</strong><p>{t(tr, lang, "desktop.u6.body")}</p></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="checklist">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "checklist.eyebrow")}</p>
          <h2>{t(tr, lang, "checklist.title")}</h2>
          <p class="section-lead">{t(tr, lang, "checklist.lead")}</p>
        </header>

        <div class="checklist-toolbar">
          <div class="progress-wrap">
            <div class="progress-bar" id="progressBar" style="width: 0%"></div>
          </div>
          <p class="progress-label"><span id="progressText">0</span>% {t(tr, lang, "checklist.complete")} · <span id="progressCount">0 / 0</span></p>
          <button type="button" class="btn btn-ghost btn-sm" id="resetChecklist" data-confirm="{t(tr, lang, "checklist.reset_confirm")}">{t(tr, lang, "checklist.reset")}</button>
        </div>

        <div class="checklist-groups" id="checklist">
          <div class="check-group" data-level="beginner">
            <h3>{t(tr, lang, "checklist.g1")}</h3>
{checklist_items(tr, lang, "g1", [f"c{i}" for i in range(1, 7)])}
          </div>
          <div class="check-group" data-level="solid">
            <h3>{t(tr, lang, "checklist.g2")}</h3>
{checklist_items(tr, lang, "g2", [f"c{i}" for i in range(7, 13)])}
          </div>
          <div class="check-group" data-level="advanced">
            <h3>{t(tr, lang, "checklist.g3")}</h3>
{checklist_items(tr, lang, "g3", [f"c{i}" for i in range(13, 19)])}
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="principles">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "principles.eyebrow")}</p>
          <h2>{t(tr, lang, "principles.title")}</h2>
        </header>
        <div class="principles-grid">
{chr(10).join(principles)}
        </div>
      </div>
    </section>

    <section class="section section-alt" id="faq">
      <div class="container narrow">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "faq.eyebrow")}</p>
          <h2>{t(tr, lang, "faq.title")}</h2>
        </header>
        <div class="faq-list">
{chr(10).join(faq_html)}
        </div>
      </div>
    </section>

    <section class="section" id="donate" data-copied="{esc(t(tr, lang, "donate.copied"), quote=True)}">
      <div class="container">
        <header class="section-head">
          <p class="eyebrow">{t(tr, lang, "donate.eyebrow")}</p>
          <h2>{t(tr, lang, "donate.title")}</h2>
          <p class="section-lead">{t(tr, lang, "donate.lead")}</p>
        </header>
        <div class="donate-grid">
{donate_cards_html(tr, lang)}
        </div>
        <p class="donate-foot" data-reveal>{t(tr, lang, "donate.foot")}</p>
      </div>
    </section>

    <section class="cta-section">
      <div class="container cta-inner" data-reveal="scale">
        <h2>{t(tr, lang, "cta.title")}</h2>
        <p>{t(tr, lang, "cta.body")}</p>
        <div class="hero-actions">
          <a href="#paths" class="btn btn-primary">{t(tr, lang, "cta.paths")}</a>
          <a href="#apps" class="btn btn-ghost">{t(tr, lang, "cta.apps")}</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-owner">
      <p>
        <strong>{t(tr, lang, "footer.owned_by")}</strong>
        <a href="https://www.vassbrekke.no" target="_blank" rel="noopener noreferrer">www.vassbrekke.no</a>
        · <a href="https://privydeck.com" target="_blank" rel="noopener noreferrer">privydeck.com</a>
        · <a href="https://www.privbeacon.com" target="_blank" rel="noopener noreferrer">privbeacon.com</a>
      </p>
    </div>
    <div class="container footer-grid">
      <div>
        <a href="{home_href}" class="logo">
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
          <li><a href="#apps">{t(tr, lang, "nav.apps")}</a></li>
          <li><a href="#vassbrekke">{t(tr, lang, "filters.ours")}</a></li>
          <li><a href="#life">{t(tr, lang, "nav.life")}</a></li>
          <li><a href="#phone">{t(tr, lang, "nav.phone")}</a></li>
          <li><a href="#desktop">{t(tr, lang, "nav.desktop")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t(tr, lang, "footer.start")}</h4>
        <ul>
          <li><a href="#paths">{t(tr, lang, "nav.paths")}</a></li>
          <li><a href="#checklist">{t(tr, lang, "nav.checklist")}</a></li>
          <li><a href="#faq">{t(tr, lang, "faq.title")}</a></li>
          <li><a href="#principles">{t(tr, lang, "principles.eyebrow")}</a></li>
          <li><a href="#donate">{t(tr, lang, "donate.nav")}</a></li>
        </ul>
      </div>
      <div>
        <h4>{t(tr, lang, "footer.disclaimer_title")}</h4>
        <p class="footer-fine">{t(tr, lang, "footer.disclaimer")}</p>
      </div>
    </div>
    <div class="container footer-bottom">
      <p>© <span id="year"></span> <a href="https://www.vassbrekke.no" target="_blank" rel="noopener noreferrer">Vassbrekke AS</a> · PrivGuide · {t(tr, lang, "footer.built")}</p>
      <p class="footer-privacy">{t(tr, lang, "footer.privacy")}</p>
    </div>
  </footer>

  <script src="{js_main}" defer></script>
</body>
</html>
'''
    # Fix asset paths that used {prefix}/ incorrectly for en
    if lang == "en":
        html = html.replace('href="./assets/', 'href="assets/')
        html = html.replace('href="./site.webmanifest"', 'href="site.webmanifest"')
        # prefix was "." so "./assets" - let me check
        html = html.replace(f'href="{prefix}/assets/', 'href="assets/')
        html = html.replace(f'href="{prefix}/site.webmanifest"', 'href="site.webmanifest"')
    else:
        html = html.replace(f'href="{prefix}/assets/', 'href="../assets/')
        html = html.replace(f'href="{prefix}/site.webmanifest"', 'href="../site.webmanifest"')

    return html


def write_sitemap() -> None:
    urls = []
    for lang in LANGS:
        loc = f"{SITE_URL}{path_for(lang)}"
        alts = "\n".join(
            f'      <xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}{path_for(l)}"/>'
            for l in LANGS
        )
        alts += f'\n      <xhtml:link rel="alternate" hreflang="x-default" href="{SITE_URL}/"/>'
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if lang == "en" else "0.9"}</priority>
{alts}
  </url>"""
        )
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{chr(10).join(urls)}
</urlset>
'''
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots() -> None:
    (ROOT / "robots.txt").write_text(
        f"""# PrivGuide
User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
""",
        encoding="utf-8",
    )


def write_manifest(tr: dict) -> None:
    manifest = {
        "name": "PrivGuide — Privacy Guide",
        "short_name": "PrivGuide",
        "description": t(tr, "en", "meta.description"),
        "start_url": "/",
        "display": "standalone",
        "background_color": "#070b14",
        "theme_color": "#0a0f1a",
        "lang": "en",
        "icons": [
            {
                "src": "assets/favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            }
        ],
    }
    (ROOT / "site.webmanifest").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_favicon() -> None:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none">
  <rect width="32" height="32" rx="8" fill="#05010d"/>
  <path d="M16 4L6 8.5v7.5c0 6.5 4.3 12.5 10 14 5.7-1.5 10-7.5 10-14V8.5L16 4z" stroke="#00f5ff" stroke-width="2"/>
  <path d="M12 16.2l2.6 2.6L20.5 13" stroke="#ff2d95" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
    (ROOT / "assets" / "favicon.svg").write_text(svg, encoding="utf-8")
    og = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="50%" stop-color="#ff2d95"/>
      <stop offset="100%" stop-color="#b24bff"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="#05010d"/>
  <circle cx="950" cy="120" r="220" fill="#ff2d95" opacity="0.15"/>
  <circle cx="200" cy="500" r="260" fill="#00f5ff" opacity="0.1"/>
  <text x="80" y="280" font-family="Orbitron,system-ui,sans-serif" font-size="72" font-weight="700" fill="#f3e9ff">PrivGuide</text>
  <text x="80" y="360" font-family="system-ui,sans-serif" font-size="36" fill="url(#g)">Best privacy apps · Phone · Desktop · Life</text>
  <text x="80" y="430" font-family="system-ui,sans-serif" font-size="24" fill="#b8a4d4">Cyber privacy map · Vassbrekke AS</text>
</svg>
'''
    (ROOT / "assets" / "og-cover.svg").write_text(og, encoding="utf-8")


def main() -> None:
    tr = load_translations()
    for lang in LANGS:
        html = render_page(lang, tr)
        if lang == "en":
            out = ROOT / "index.html"
        else:
            out_dir = ROOT / lang
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / "index.html"
        out.write_text(html, encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")

    write_sitemap()
    write_robots()
    write_manifest(tr)
    write_favicon()
    print("Wrote sitemap.xml, robots.txt, site.webmanifest, assets")


if __name__ == "__main__":
    main()
