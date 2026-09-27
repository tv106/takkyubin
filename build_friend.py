#!/usr/bin/env python3
"""Construit web/friend.html (page d'un ami, 100 % statique) à partir des sources Apps Script.

    python3 web/build_friend.py

La page lit ses données par l'API JSON du script (aucune page Google affichée) :
elle fonctionne donc aussi dans le navigateur intégré d'Instagram.
"""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / 'apps-script' / 'src'
OUT = Path(__file__).resolve().parent / 'friend.html'
config = (SRC / 'Config.js').read_text()
deployment = re.search(r"DEPLOYMENT_ID = '([^']+)'", config).group(1)
api_url = f'https://script.google.com/macros/s/{deployment}/exec'

style = (SRC / 'Style.html').read_text()
common = (SRC / 'Common.html').read_text()
common = common.replace('const KEY = <?!= JSON.stringify(key) ?>;', "const KEY = new URLSearchParams(location.search).get('f') || '';")
common = common.replace('const API_URL = <?!= JSON.stringify(WEBAPP_URL) ?>;', f"const API_URL = '{api_url}';")
common = common.replace('let INITIAL = <?!= initial ?>;', 'let INITIAL = null;')
assert '<?' not in common, 'modèle non remplacé dans Common.html'

page = (SRC / 'Friend.html').read_text()
head = '''<title>Ma box · Takkyubin</title>
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Ma box">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="favicon.png">
<link rel="manifest" href="manifest.webmanifest?v=3">
<script>
  // Icône d'écran d'accueil : elle rouvre cette page avec le lien personnel.
  (function () {
    var base = location.origin + location.pathname.replace(/[^/]*$/, '');
    var start = location.href;
    var m = { name: 'Ma box', short_name: 'Ma box', lang: 'fr', display: 'standalone', start_url: start, scope: base,
      background_color: '#F2F3F6', theme_color: '#F2F3F6',
      icons: [{ src: base + 'icon-192.png', sizes: '192x192', type: 'image/png' }, { src: base + 'icon-512.png', sizes: '512x512', type: 'image/png' }] };
    document.addEventListener('DOMContentLoaded', function () {
      document.querySelector('link[rel=manifest]').href = 'data:application/manifest+json,' + encodeURIComponent(JSON.stringify(m));
    });
  })();
</script>
'''
page = page.replace("<?!= include_('Style') ?>", head + style)
page = page.replace("<?!= include_('Common', { key: key, initial: initial }) ?>", common)
page = page.replace('<base target="_blank">', '<base target="_blank">')
assert '<?' not in page, 'modèle non remplacé dans Friend.html'
OUT.write_text('<!-- Généré par build_friend.py depuis apps-script/src : ne pas modifier à la main. -->\n' + page)
print('friend.html :', len(page), 'caractères')
