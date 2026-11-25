R&R Exports website - how to edit
- All text (English + Arabic) lives in content.py. Photos are in photos/.
- After editing, run:  python build.py   (needs Python 3 + Pillow). It rebuilds the site into out/.
- Upload everything outside this source/ folder to your host (Vercel, Netlify, cPanel...).
- The domain is set to https://rrexportsinternational.com in content.py (BASE) - canonical URLs, sitemap and hreflang use it.
- After going live: submit sitemap.xml in Google Search Console and Bing Webmaster Tools.
