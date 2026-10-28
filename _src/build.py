#!/usr/bin/env python3
"""Builds the La Roda site from _src/ into the repository root.

    python3 _src/build.py

Page bodies live in _src/pages/<lang>/<page>.html: a few `key: value` lines,
a `---` line, then the HTML that goes between the main menu and the footer.
Everything shared (head, language bar, ticker, header, menu, footer) is
generated here, so the three languages stay in sync. Commit the generated
HTML: GitHub Pages serves it as-is and ignores _src/.
"""
import datetime
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_src'
SITE = 'https://laroda.bike'
YEAR = datetime.date.today().year
OG_IMAGE = SITE + '/assets/og.png'

LANGS = ['ca', 'es', 'en']
PAGES = ['home', 'experiences', 'store', 'workshop', 'contact', 'legal']
MENU = ['experiences', 'store', 'workshop', 'contact']

SLUGS = {
    'ca': {'home': 'index.html', 'experiences': 'experiencies.html', 'store': 'botiga.html',
           'workshop': 'taller.html', 'contact': 'contacte.html', 'legal': 'avis-legal.html'},
    'es': {'home': 'index.html', 'experiences': 'experiencias.html', 'store': 'tienda.html',
           'workshop': 'taller.html', 'contact': 'contacto.html', 'legal': 'aviso-legal.html'},
    'en': {'home': 'index.html', 'experiences': 'experiences.html', 'store': 'store.html',
           'workshop': 'workshop.html', 'contact': 'contact.html', 'legal': 'legal.html'},
}

UI = {
    'ca': {'name': 'Català', 'locale': 'ca_ES', 'nav_main': 'Principal', 'nav_lang': 'Idioma',
           'nav_foot': 'Peu de pàgina', 'kicker': 'Experiències en bici · Botiga · Taller',
           'notice': 'Botiga i taller: obrim el gener de 2027',
           'labels': {'experiences': 'Experiències', 'store': 'Botiga', 'workshop': 'Taller',
                      'contact': 'Contacte', 'legal': 'Avís legal i privacitat'}},
    'es': {'name': 'Español', 'locale': 'es_ES', 'nav_main': 'Principal', 'nav_lang': 'Idioma',
           'nav_foot': 'Pie de página', 'kicker': 'Experiencias en bici · Tienda · Taller',
           'notice': 'Tienda y taller: abrimos en enero de 2027',
           'labels': {'experiences': 'Experiencias', 'store': 'Tienda', 'workshop': 'Taller',
                      'contact': 'Contacto', 'legal': 'Aviso legal y privacidad'}},
    'en': {'name': 'English', 'locale': 'en_GB', 'nav_main': 'Main', 'nav_lang': 'Language',
           'nav_foot': 'Footer', 'kicker': 'Bike experiences · Store · Workshop',
           'notice': 'Store & workshop opening January 2027',
           'labels': {'experiences': 'Experiences', 'store': 'Store', 'workshop': 'Workshop',
                      'contact': 'Contact', 'legal': 'Legal & privacy'}},
}

FONTS_HEAD = '''<link rel="preload" href="{a}fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a}fonts/space-mono-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{r}favicon.ico" sizes="32x32">
<link rel="icon" href="{a}icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{a}apple-touch-icon.png">
<link rel="stylesheet" href="{a}laroda.css">'''

CURRENT = ' aria-current="page"'
STRIPES = '<div class="stripes" aria-hidden="true"><i></i><i></i><i></i></div>'


def esc(s):
    return html.escape(s, quote=True)


def url(lang, page):
    slug = SLUGS[lang][page]
    return f'{SITE}/{lang}/' + ('' if slug == 'index.html' else slug)


def read_page(lang, page):
    meta, body = (SRC / 'pages' / lang / f'{page}.html').read_text().split('\n---\n', 1)
    fm = dict(line.split(': ', 1) for line in meta.splitlines() if line.strip())
    return fm, body.rstrip('\n')


def social(title, description, page_url, lang):
    others = [UI[l]['locale'] for l in LANGS if l != lang]
    lines = [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="La Roda">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(description)}">',
        f'<meta property="og:url" content="{page_url}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="La Roda · Santa Coloma de Queralt">',
        f'<meta property="og:locale" content="{UI[lang]["locale"]}">',
        *[f'<meta property="og:locale:alternate" content="{o}">' for o in others],
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    return '\n'.join(lines)


def jsonld(description):
    hours = [
        (['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], '09:30', '13:30'),
        (['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], '16:30', '20:00'),
        (['Saturday'], '10:00', '14:00'),
    ]
    data = {
        '@context': 'https://schema.org',
        '@type': 'BicycleStore',
        '@id': SITE + '/#store',
        'name': 'La Roda',
        'description': description,
        'url': SITE + '/',
        'image': OG_IMAGE,
        'logo': SITE + '/assets/apple-touch-icon.png',
        'telephone': '+34666668086',
        'email': 'hola@laroda.bike',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Santa Coloma de Queralt',
                    'postalCode': '43420', 'addressRegion': 'Tarragona', 'addressCountry': 'ES'},
        'areaServed': 'Catalonia',
        'sameAs': ['https://instagram.com/larodabike'],
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': d, 'opens': o, 'closes': c,
             'validFrom': '2027-01-01'} for d, o, c in hours],
    }
    return ('<script type="application/ld+json">\n'
            + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>')


def build_page(lang, page, ticker):
    fm, body = read_page(lang, page)
    ui, slugs = UI[lang], SLUGS[lang]
    title, description = fm['title'], fm['description']
    page_url = url(lang, page)

    alternates = '\n'.join(
        [f'<link rel="alternate" hreflang="{l}" href="{url(l, page)}">' for l in LANGS]
        + [f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'])
    langbar = ''.join(
        f'<a href="{slugs[page] if l == lang else f"../{l}/{SLUGS[l][page]}"}" hreflang="{l}" '
        f'lang="{l}" data-lang="{l}"{CURRENT if l == lang else ""}>{UI[l]["name"]}</a>'
        for l in LANGS)
    menu = ''.join(
        f'<a href="{slugs[k]}"{CURRENT if k == page else ""}>'
        f'<b>{n:02d}</b>{ui["labels"][k]}</a>' for n, k in enumerate(MENU, 1))
    footer_nav = ''.join(f'<a href="{slugs[k]}">{ui["labels"][k]}</a>' for k in MENU + ['legal'])

    if page == 'home':
        header = (f'<div class="kicker"><span>{ui["kicker"]}</span><span>Santa Coloma de Queralt</span></div>\n'
                  '<h1 class="display">La Roda</h1>')
    else:
        h1 = fm.get('h1', ui['labels'][page])
        crumb = f'{MENU.index(page) + 1:02d} / {h1}' if page in MENU else h1
        header = (f'<div class="kicker"><a href="index.html">&larr; La Roda</a><span>{crumb}</span></div>\n'
                  f'<h1 class="display sub">{h1}</h1>')

    head_extra = '\n' + jsonld(description) if page == 'home' else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{page_url}">
{alternates}
{social(title, description, page_url, lang)}
{FONTS_HEAD.format(a='../assets/', r='../')}{head_extra}
</head>
<body>
<div class="langbar"><div class="wrap"><p class="notice">{ui["notice"]}</p><nav aria-label="{ui["nav_lang"]}">{langbar}</nav></div></div>
<div class="ticker" aria-hidden="true"><span>{ticker}</span><span>{ticker}</span></div>

<header><div class="wrap">
{header}
{STRIPES}
</div></header>

<div class="wrap">
<nav class="menu" aria-label="{ui["nav_main"]}">
{menu}
</nav>

{body}
</div>

<footer><div class="wrap"><a href="index.html">© {YEAR} La Roda · Santa Coloma de Queralt</a><nav aria-label="{ui["nav_foot"]}">{footer_nav}</nav></div></footer>
<script src="../assets/laroda.js"></script>
</body>
</html>
'''


def language_links(prefix):
    return ''.join(f'<a href="{prefix}{l}/index.html" hreflang="{l}" lang="{l}" data-lang="{l}">{UI[l]["name"]}</a>'
                   for l in LANGS)


def build_root():
    title = 'La Roda'
    description = ('La Roda: experiències en bici, botiga i taller a Santa Coloma de Queralt. '
                   'Bike experiences, store and workshop in Catalonia.')
    alternates = '\n'.join(
        [f'<link rel="alternate" hreflang="{l}" href="{url(l, "home")}">' for l in LANGS]
        + [f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'])
    return f'''<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{SITE}/">
{alternates}
{social(title, description, SITE + '/', 'ca')}
{FONTS_HEAD.format(a='assets/', r='')}
<script>
(function(){{
  var l;
  try{{l=localStorage.getItem('laroda-lang')}}catch(e){{}}
  if(l!=='ca'&&l!=='es'&&l!=='en'){{
    l='en';
    var prefs=navigator.languages||[navigator.language||''];
    for(var i=0;i<prefs.length;i++){{
      if(/^(ca|oc)\\b/i.test(prefs[i])){{l='ca';break}}
      if(/^(es|gl|eu)\\b/i.test(prefs[i])){{l='es';break}}
      if(/^en\\b/i.test(prefs[i])){{l='en';break}}
    }}
  }}
  location.replace(l+'/index.html');
}})();
</script>
</head>
<body>
<header><div class="wrap">
<h1 class="display">La Roda</h1>
{STRIPES}
</div></header>
<div class="wrap"><nav class="menu" aria-label="Idioma / Idioma / Language">
{language_links('')}
</nav></div>
<script src="assets/laroda.js"></script>
</body>
</html>
'''


def build_404():
    # Served for any missing path at any depth, so every URL is root-relative.
    return f'''<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>404 · La Roda</title>
{FONTS_HEAD.format(a='/assets/', r='/')}
</head>
<body>
<header><div class="wrap">
<div class="kicker"><a href="/">&larr; La Roda</a><span>404</span></div>
<h1 class="display sub">404</h1>
{STRIPES}
</div></header>
<div class="wrap">
<nav class="menu" aria-label="Idioma / Idioma / Language">
{language_links('/')}
</nav>
<div class="intro">
<h2 class="display">Fora de ruta.</h2>
<div><p lang="ca">Aquesta pàgina no existeix.</p><p lang="es">Esta página no existe.</p><p lang="en">This page doesn’t exist.</p></div>
</div>
</div>
<script src="/assets/laroda.js"></script>
</body>
</html>
'''


def build_sitemap():
    entries = []
    for page in PAGES:
        alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{url(l, page)}"/>' for l in LANGS)
        for lang in LANGS:
            entries.append(f'  <url>\n    <loc>{url(lang, page)}</loc>{alts}\n  </url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(entries) + '\n</urlset>\n')


def main():
    for lang in LANGS:
        ticker = (SRC / 'ticker' / f'{lang}.html').read_text().strip()
        (ROOT / lang).mkdir(exist_ok=True)
        for page in PAGES:
            (ROOT / lang / SLUGS[lang][page]).write_text(build_page(lang, page, ticker))
    (ROOT / 'index.html').write_text(build_root())
    (ROOT / '404.html').write_text(build_404())
    (ROOT / 'sitemap.xml').write_text(build_sitemap())
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print(f'Built {len(LANGS) * len(PAGES)} pages + index.html, 404.html, sitemap.xml, robots.txt')


if __name__ == '__main__':
    main()
