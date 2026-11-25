# -*- coding: utf-8 -*-
import json, os, shutil, html
from PIL import Image
from content import *

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
BROCHURE = "rr-exports-product-brochure.pdf"
T.update({
 "added": ("In enquiry ✓", "في الاستفسار ✓"), "remove": ("Remove", "إزالة"), "copied": ("Copied", "تم النسخ"),
 "err_req": ("Please fill in the highlighted fields.", "يرجى تعبئة الحقول المحدّدة."),
 "err_prod": ("Choose at least one bottle.", "اختر زجاجة واحدة على الأقل."),
 "err_contact": ("Add a valid email or WhatsApp number.", "أضف بريداً إلكترونياً أو رقم واتساب صحيحاً."),
 "f_contact": ("Email or WhatsApp number", "البريد الإلكتروني أو رقم واتساب"),
 "f_pick": ("Which bottles?", "ما الزجاجات المطلوبة؟"),
 "f_more": ("More options: colours, logo, packaging, shipping, message", "خيارات إضافية: الألوان والشعار والتغليف والشحن والرسالة"),
 "pl_h1": ("Private label collapsible silicone bottles", "زجاجات سيليكون قابلة للطي بعلامة خاصة"),
 "pl_lead": ("Launch a bottle range under your own brand. We print your logo, match your colours and pack every bottle retail-ready — starting at 300 pieces per model.",
             "أطلق تشكيلة زجاجات تحمل علامتك الخاصة. نطبع شعارك ونطابق ألوانك ونغلّف كل زجاجة جاهزة للبيع — بدءاً من 300 قطعة لكل طراز."),
 "pick_bottle": ("Pick a bottle to brand", "اختر زجاجة لتحمل علامتك"),
 "steps_more": ("See the full ordering process", "اطّلع على خطوات الطلب كاملة"),
 "order_lead": ("No surprises: you approve the artwork, photos and specifications before bulk production starts, and see photos of your goods before they ship.",
                "بلا مفاجآت: تعتمد التصميم والصور والمواصفات قبل بدء الإنتاج بالجملة، وترى صور بضاعتك قبل شحنها."),
 "all_products": ("All products", "كل المنتجات"),
})
ESC = lambda s: html.escape(s, quote=True)

IMGDIM = {}
for f in os.listdir(os.path.join(ROOT, "photos")):
    IMGDIM[f[:-4]] = Image.open(os.path.join(ROOT, "photos", f)).size

ICON = {
 "box": '<path d="M3 7l9-4 9 4-9 4-9-4zM3 7v10l9 4 9-4V7M12 11v10"/>',
 "palette": '<path d="M12 3a9 9 0 100 18c1 0 1.5-.8 1.5-1.6 0-1-.8-1.4-.8-2.4s.8-1.6 1.8-1.6H17a4 4 0 004-4c0-4.7-4-8.4-9-8.4z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15" cy="7.5" r="1.2"/>',
 "check": '<path d="M12 3l2.5 1.8 3 .2 1 2.9 2.3 2-1 2.9 1 2.9-2.3 2-1 2.9-3 .2L12 21l-2.5-1.8-3-.2-1-2.9-2.3-2 1-2.9-1-2.9 2.3-2 1-2.9 3-.2z"/><path d="M8.5 12l2.3 2.3 4.7-4.6"/>',
 "flask": '<path d="M9 3h6M10 3v6l-5.5 9.5A1.7 1.7 0 006 21h12a1.7 1.7 0 001.5-2.5L14 9V3M7.5 15h9"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
 "ship": '<path d="M3 16l2 5h14l2-5H3zM5 16V9h14v7M12 9V3M8 6h8"/>',
 "bag": '<path d="M5 8h14l-1 13H6L5 8zM9 8a3 3 0 016 0"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "x": '<path d="M6 6l12 12M18 6L6 18"/>',
 "cube": '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9L12 3zM12 12l8-4.5M12 12v9M12 12L4 7.5"/>',
 "mail": '<path d="M3 6h18v12H3zM3 7l9 7 9-7"/>',
 "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 006 6L16 13l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/>',
 "pin": '<path d="M12 21s-7-6.2-7-12a7 7 0 0114 0c0 5.8-7 12-7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "wa": '<path d="M4 20l1.3-4A8 8 0 1112 20a8 8 0 01-4-1.1L4 20z"/><path d="M9 9.5c0 2.8 2.7 5.5 5.5 5.5l1-1.5-2-1-1 .8c-.9-.4-1.9-1.4-2.3-2.3l.8-1-1-2L9 9.5z"/>',
}
def ic(n, cls="ic"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICON[n]}</svg>'

PROD = {p["id"]: p for p in PRODUCTS}
CARD_IMG = {"cb01": "origami-foldable-silicone-bottle-600ml-custom-logo", "cb02": "flip-straw-silicone-bottle-colours",
            "cb03": "roll-up-silicone-bottle-backpack-clip", "cb04": "telescopic-collapsible-sports-bottle-760ml-colours"}
NAV = [("home", "nav_home"), ("products", "nav_products"), ("private", "nav_private"), ("order", "nav_order"), ("about", "nav_about"), ("contact", "nav_contact")]

class Ctx:
    def __init__(s, L): s.L = L; s.ar = L == 1; s.A = "../assets/" if s.ar else "assets/"
    def t(s, k): return T[k][s.L]
    def x(s, pair): return pair[s.L]
    def url(s, f, lang=None):
        ar = s.ar if lang is None else lang == 1
        path = ("ar/" if ar else "") + ("" if f == "index.html" else f)
        return f"{BASE}/{path}"
    def img(s, name, alt, cls="", lazy=True, sizes=None, extra=""):
        w, h = IMGDIM[name]
        return (f'<img src="{s.A}img/{name}.jpg" width="{w}" height="{h}" alt="{ESC(alt)}"'
                f'{" loading=\"lazy\" decoding=\"async\"" if lazy else " fetchpriority=\"high\""}'
                f'{f" class=\"{cls}\"" if cls else ""}{extra}>')

def pname(c, p): return f'{c.x(p["name"])} · {c.x((p["cap"], p["cap"].replace("ml", "مل")))}'

# ---------- components ----------
def viewer(c, models, label):
    p0 = models[0]
    chips = ""
    if len(models) > 1:
        chips = '<div class="chips" role="group" aria-label="%s">' % c.t("model") + "".join(
            f'<button type="button" class="mchip" data-m="{p["model"]}" data-c="{p["color"]}" aria-pressed="{"true" if i == 0 else "false"}">{p["code"]}</button>'
            for i, p in enumerate(models)) + "</div>"
    sws = "".join(
        f'<div class="sws" data-for="{p["model"]}" role="group" aria-label="{c.t("colour")}"{"" if i == 0 else " hidden"}>' + "".join(
            f'<button type="button" class="sw" data-c="{h}" style="--c:{h}" aria-label="{ESC(col[c.L])}" title="{ESC(col[c.L])}"{" aria-pressed=\"true\"" if h == p["color"] else ""}></button>'
            for col in p["colours"] for h in [col[2]]) + "</div>" for i, p in enumerate(models))
    return (f'<div class="stage"><div class="viewer" data-model="{p0["model"]}" data-color="{p0["color"]}" role="img" aria-label="{ESC(label)}">'
            f'<div class="disc" aria-hidden="true"></div></div>'
            f'<div class="vctl">{chips}{sws}<label class="foldl"><span>{c.t("fold_lbl")}</span><input class="foldr" type="range" min="0" max="100" value="0"></label></div>'
            f'<p class="hint">{c.t("drag")}</p></div>')

def card(c, p, h="h3"):
    im = CARD_IMG[p["id"]]; alt = dict((n, a) for n, a in p["imgs"]).get(im, p["imgs"][0][1])
    return f'''<article class="pc">
<a class="pcimg" href="{p["slug"]}.html" tabindex="-1" aria-hidden="true">{c.img(im, c.x(alt))}</a>
<div class="pcb"><p class="tagrow"><span class="code">{p["code"]}</span><span class="badge">{c.x(p["badge"])}</span></p>
<{h}><a href="{p["slug"]}.html">{pname(c, p)}</a></{h}>
<p>{c.x(p["desc"])}</p>
<dl class="mini"><div><dt>{c.t("th_cap")}</dt><dd>{c.x((p["cap"], p["cap"].replace("ml", "مل")))}</dd></div><div><dt>{c.t("th_moq")}</dt><dd>{c.x(p["moq"])}</dd></div><div><dt>{c.t("th_prod")}</dt><dd>{c.x(p["prod"])}</dd></div></dl>
<div class="pcact"><a class="btn sm" href="{p["slug"]}.html">{c.t("view")}</a><button type="button" class="btn ghost sm addbtn" data-id="{p["id"]}">{c.t("add")}</button></div></div></article>'''

def grid(c, prods, h="h3"): return '<div class="pgrid">' + "".join(card(c, p, h) for p in prods) + "</div>"

VIDEOS = {
 "cb01": ("origami-foldable-bottle-demo", 520, 604, ("Origami bottle: unpacking, unfolding and carry strap", "زجاجة الأوريغامي: إخراجها من العبوة وفتحها وحزام الحمل")),
 "cb02": ("flip-straw-bottle-demo", 1280, 720, ("Flip-straw bottle: colours, straw lid and roll-up", "زجاجة الشفّاط القلّاب: الألوان وغطاء الشفّاط وطريقة اللف")),
}
def videos(c, ids, band="soft"):
    ids = [i for i in ids if i in VIDEOS]
    if not ids: return ""
    base = c.A + "video/"
    figs = "".join(f'<figure style="--ar:{w / h:.4f}"><video controls muted playsinline preload="none" width="{w}" height="{h}" poster="{base}{n}.jpg" aria-label="{ESC(c.x(t))}"><source src="{base}{n}.mp4" type="video/mp4"></video><figcaption>{c.x(t)}</figcaption></figure>' for n, w, h, t in (VIDEOS[i] for i in ids))
    title = c.x(("See it in action", "شاهد المنتج على الطبيعة"))
    return f'<section class="band {band}"><div class="wrap"><div class="shead"><h2>{title}</h2></div><div class="vids">{figs}</div></div></section>'

def range_table(c):
    rows = "".join(f'<tr><td><a href="{p["slug"]}.html"><b>{p["code"]}</b></a></td><td>{c.x(p["style"])}</td><td class="nw">{c.x((p["cap"], p["cap"].replace("ml", "مل")))}</td><td class="nw">{c.x(p["moq"])}</td><td class="nw">{c.x(p["prod"])}</td><td><span class="ok">✓ {c.t("lab_ok")}</span><small>{c.t("lab_sub")}</small></td></tr>' for p in PRODUCTS)
    return f'<div class="tablewrap"><table class="stack rt"><thead><tr><th>{c.t("th_model")}</th><th>{c.t("th_style")}</th><th>{c.t("th_cap")}</th><th>{c.t("th_moq")}</th><th>{c.t("th_prod")}</th><th>{c.t("th_lab")}</th></tr></thead><tbody>{rows}</tbody></table></div>'

def steps(c):
    return '<ol class="steps">' + "".join(f'<li><span class="sn">{i+1}</span><div><h3>{c.x(a)}</h3><p>{c.x(b)}</p></div></li>' for i, (a, b) in enumerate(STEPS)) + "</ol>"

def terms(c):
    return '<dl class="terms">' + "".join(f'<div><dt>{c.x(a)}</dt><dd>{c.x(b)}</dd></div>' for a, b in TERMS) + "</dl>"

def faq(c):
    return '<div class="faq">' + "".join(f'<details{" open" if i == 0 else ""}><summary>{c.x(q)}</summary><p>{c.x(a)}</p></details>' for i, (q, a) in enumerate(FAQ)) + "</div>"

def why(c):
    return '<div class="why">' + "".join(f'<div class="wi">{ic(n, "ic big")}<h3>{c.x(a)}</h3><p>{c.x(b)}</p></div>' for n, a, b in WHY) + "</div>"

def sell(c):
    return '<div class="sell">' + "".join(f'<div><h3>{c.x(a)}</h3><p>{c.x(b)}</p></div>' for a, b in SELL) + "</div>"

def serve(c): return '<ul class="serve">' + "".join(f"<li>{c.x(s)}</li>" for s in SERVE) + "</ul>"

def plist(c): return '<ul class="pl">' + "".join(f'<li><b>{c.x(a)}</b> — {c.x(b)}</li>' for a, b in PL) + "</ul>"

def quality(c):
    return '<div class="qual">' + "".join(f'<div><h3>{c.x(a)}</h3><p>{c.x(b)}</p></div>' for a, b in QUAL) + "</div>"

def brochure(c, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return f'<a{attr} href="{c.A}{BROCHURE}" target="_blank" rel="noopener">{c.t("brochure")}</a>'

def cta(c):
    return f'''<section class="band cta"><div class="wrap ctain"><div><h2>{c.t("cta_t")}</h2><p>{c.t("cta_p")}</p></div>
<div class="ctab"><a class="btn pri qopen" href="contact.html">{c.t("quote")}</a><a class="btn light" href="https://wa.me/{PHONE_RAW}" rel="noopener" target="_blank">{ic("wa")} WhatsApp</a>{brochure(c, "btn light")}</div></div></section>'''

def form(c):
    rows = ""
    for p in PRODUCTS:
        opts = ["300", "500", "1,000", "2,000", "5,000+"] if p["minq"] == 300 else ["1,000", "2,000", "5,000", "10,000+"]
        o = "".join(f'<option>{v}</option>' for v in opts)
        rows += f'''<div class="prow"><label class="pchk"><input type="checkbox" name="p" value="{p["id"]}">{c.img(CARD_IMG[p["id"]], "", "pthumb")}<span><b>{p["code"]}</b><small>{c.x(p["style"])}</small></span></label>
<select name="q_{p["id"]}" aria-label="{c.t("f_qty")} {p["code"]}">{o}</select></div>'''
    def select(name, label, opts):
        o = '<option value="">—</option>' + "".join(f'<option value="{v}">{c.t(k)}</option>' for v, k in opts)
        return f'<label class="fld"><span>{c.t(label)}</span><select name="{name}">{o}</select></label>'
    biz = '<option value="">—</option>' + "".join(f'<option value="{ESC(b[0])}">{c.x(b)}</option>' for b in BIZ)
    r = f'<abbr title="{c.t("req")}">*</abbr>'
    return f'''<div class="formwrap"><form class="qform" novalidate>
<fieldset><legend>{c.t("f_pick")}</legend><div class="plist">{rows}</div><p class="err" data-err="p" hidden>{c.t("err_prod")}</p></fieldset>
<div class="fgrid three">
<label class="fld"><span>{c.t("f_name")} {r}</span><input name="name" required autocomplete="name"></label>
<label class="fld"><span>{c.t("f_contact")} {r}</span><input name="contact" required autocomplete="email" dir="ltr"></label>
<label class="fld"><span>{c.t("f_country")} {r}</span><input name="country" required autocomplete="country-name"></label></div>
<p class="err" data-err="contact" hidden>{c.t("err_contact")}</p>
<details class="more-opts"><summary>{c.t("f_more")}</summary><div class="fgrid">
<label class="fld"><span>{c.t("f_company")}</span><input name="company" autocomplete="organization"></label>
<label class="fld"><span>{c.t("f_biz")}</span><select name="biz">{biz}</select></label>
<label class="fld"><span>{c.t("f_cols")}</span><input name="colours" placeholder="{c.t("f_cols_ph")}" autocomplete="off"></label>
{select("logo", "f_logo", [("Yes", "yes"), ("No", "no"), ("Not sure", "notsure")])}
{select("pack", "f_pack", [("OPP bag", "pack1"), ("Custom colour box", "pack2")])}
{select("ship", "f_ship", [("Not sure", "notsure"), ("Sea", "sea"), ("Air", "air"), ("Courier", "courier")])}
<label class="chk wide"><input type="checkbox" name="samples"> {c.t("f_samples")}</label>
<label class="fld wide"><span>{c.t("f_msg")}</span><textarea name="msg" rows="3" placeholder="{c.t("f_msg_ph")}"></textarea></label></div></details>
<div class="fsub"><p class="formerr" role="alert" hidden>{c.t("err_req")}</p>
<button class="btn pri" type="submit" value="wa">{ic("wa")} {c.t("wa")}</button><button class="btn ghost" type="submit" value="mail">{ic("mail")} {c.t("mail")}</button>
<p class="note">{c.t("f_note")}</p></div></form>
<div class="done" hidden tabindex="-1"><h3>{c.t("done_t")}</h3><p>{c.t("done_p")}</p>
<div class="doneact"><a class="btn pri wab" href="#" target="_blank" rel="noopener">{ic("wa")} {c.t("wa")}</a><a class="btn mailb" href="#">{ic("mail")} {c.t("mail")}</a><button type="button" class="btn ghost copyb">{c.t("copy")}</button></div>
<p class="small" dir="ltr">{EMAIL} · WhatsApp {PHONE}</p><pre class="msg" dir="auto"></pre><button type="button" class="linkb editb">{c.t("edit")}</button></div></div>'''

def crumbs(c, items):
    lis = "".join(f'<li><a href="{f}">{n}</a></li>' if f else f'<li aria-current="page">{n}</li>' for n, f in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

# ---------- JSON-LD ----------
def org_ld(c):
    return {"@type": "Organization", "@id": BASE + "/#org", "name": ORG, "alternateName": ALT_NAMES, "url": BASE + "/",
            "description": T["foot_p"][0], "areaServed": ["India", "United Arab Emirates", "United States", "Worldwide"],
            "knowsAbout": [p["full"][0] for p in PRODUCTS],
            "logo": BASE + "/assets/img/rr-exports-international-logo.jpg", "email": EMAIL, "telephone": PHONE,
            "address": {"@type": "PostalAddress", "addressLocality": "Surendranagar", "addressRegion": "Gujarat", "addressCountry": "IN"},
            "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "email": EMAIL, "contactType": "sales"}}
def crumb_ld(c, items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": c.url(f)} for i, (n, f) in enumerate(items)]}
def faq_ld(c):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": c.x(q), "acceptedAnswer": {"@type": "Answer", "text": c.x(a)}} for q, a in FAQ]}
def product_ld(c, p):
    return {"@type": "Product", "@id": c.url(p["slug"] + ".html") + "#product", "name": c.x(p["full"]), "sku": p["code"], "mpn": p["code"], "alternateName": [f'RR Exports {p["code"]}', f'R&R Exports {c.x(p["name"])}'],
            "description": c.x(p["desc"]), "brand": {"@type": "Brand", "name": ORG}, "manufacturer": {"@id": BASE + "/#org"},
            "category": "Collapsible silicone water bottles", "material": "Silicone",
            "image": [f'{BASE}/assets/img/{n}.jpg' for n, _ in p["imgs"]], "color": [col[0] for col in p["colours"]],
            "additionalProperty": [{"@type": "PropertyValue", "name": SPEC_L[k][0], "value": en} for k, en, _ in p["specs"] if k not in ("price",)]}

# ---------- page shell ----------
def page(c, key, body, ld=(), viewer_on=False, og_img="og-image.jpg", pid=""):
    f, title, desc = PAGES[key] if key in PAGES else key
    lang = "ar" if c.ar else "en"
    other = "../" + f if c.ar else "ar/" + f
    if c.ar and f == "index.html": other = "../index.html"
    navh = "".join(f'<a href="{PAGES[k][0]}"{" aria-current=\"page\"" if PAGES.get(k, (0,))[0] == f else ""}>{c.t(lbl)}</a>' for k, lbl in NAV)
    graph = {"@context": "https://schema.org", "@graph": [org_ld(c)] + list(ld)}
    rrjs = {"lang": lang, "contact": "contact.html", "wa": PHONE_RAW, "email": EMAIL,
            "lead": [f"https://formsubmit.co/ajax/{e}" for e in LEAD_EMAILS],
            "products": [{"id": p["id"], "code": p["code"], "name": c.x(p["name"]), "url": p["slug"] + ".html", "img": f'{c.A}img/{CARD_IMG[p["id"]]}.jpg'} for p in PRODUCTS],
            "s": {k: c.t(k) for k in ("add", "added", "remove", "copied", "err_req")}}
    prods_f = "".join(f'<li><a href="{p["slug"]}.html">{c.x(p["name"])}</a></li>' for p in PRODUCTS)
    comp_f = "".join(f'<li><a href="{PAGES[k][0]}">{c.t(l)}</a></li>' for k, l in NAV[2:5])
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{"rtl" if c.ar else "ltr"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ESC(c.x(title))}</title>
<meta name="description" content="{ESC(c.x(desc))}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{ORG}">
<meta name="geo.region" content="IN-GJ">
<meta name="geo.placename" content="Surendranagar, Gujarat, India">
<link rel="canonical" href="{c.url(f)}">
<link rel="alternate" hreflang="en" href="{c.url(f, 0)}">
<link rel="alternate" hreflang="ar" href="{c.url(f, 1)}">
<link rel="alternate" hreflang="x-default" href="{c.url(f, 0)}">
<meta property="og:type" content="{"product" if og_img != "og-image.jpg" else "website"}">
<meta property="og:site_name" content="{ORG}">
<meta property="og:title" content="{ESC(c.x(title))}">
<meta property="og:description" content="{ESC(c.x(desc))}">
<meta property="og:url" content="{c.url(f)}">
<meta property="og:image" content="{BASE}/assets/img/{og_img}">
<meta property="og:locale" content="{"ar_AE" if c.ar else "en_US"}">
<meta property="og:locale:alternate" content="{"en_US" if c.ar else "ar_AE"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b5a58">
<link rel="icon" href="{c.A}img/rr-exports-international-logo.jpg">
<link rel="apple-touch-icon" href="{c.A}img/rr-exports-international-logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{c.A}style.css">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>
<body data-product="{pid}">
<a class="skip" href="#main">{c.t("skip")}</a>
<header class="hd"><div class="wrap hdin">
<a class="brand" href="index.html"><img src="{c.A}img/rr-exports-international-logo.jpg" width="44" height="44" alt="{ORG} (RR Exports) logo"><span><b>R&amp;R Exports</b><small>{c.t("tagline")}</small></span></a>
<nav class="nav" id="nav" aria-label="Main">{navh}<a class="lang m" href="{other}" hreflang="{"en" if c.ar else "ar"}" lang="{"en" if c.ar else "ar"}">{c.t("lang_other")}</a></nav>
<div class="hdact"><a class="lang d" href="{other}" hreflang="{"en" if c.ar else "ar"}" lang="{"en" if c.ar else "ar"}">{c.t("lang_other")}</a>
<button type="button" class="enqbtn" aria-label="{c.t("enq_list")}">{ic("bag")}<span class="cnt">0</span></button>
<a class="btn pri sm qbtn qopen" href="contact.html">{c.t("quote")}</a>
<button type="button" class="menub" aria-expanded="false" aria-controls="nav" aria-label="{c.t("menu")}">{ic("menu")}</button></div></div></header>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap ftg">
<div><a class="brand" href="index.html"><img src="{c.A}img/rr-exports-international-logo.jpg" width="44" height="44" alt="" loading="lazy"><span><b>R&amp;R Exports</b><small>INTERNATIONAL</small></span></a><p>{c.t("foot_p")}</p><p>{c.t("foot_aka")}</p></div>
<div><h2>{c.t("foot_products")}</h2><ul>{prods_f}</ul></div>
<div><h2>{c.t("foot_company")}</h2><ul>{comp_f}<li><a href="contact.html">{c.t("nav_contact")}</a></li><li>{brochure(c)}</li></ul></div>
<div><h2>{c.t("foot_contact")}</h2><ul class="ftc"><li>{ic("mail")}<a href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a></li><li>{ic("phone")}<a href="tel:+{PHONE_RAW}" dir="ltr">{PHONE}</a></li><li>{ic("pin")}<span>{c.t("addr")}</span></li></ul></div>
</div><div class="wrap ftb"><span>© 2026 {ORG}</span><a href="{other}" hreflang="{"en" if c.ar else "ar"}">{c.t("lang_other")}</a></div></footer>
<aside class="drawer" hidden aria-labelledby="dtitle"><div class="dscrim" data-close></div><div class="dpanel" role="dialog" aria-modal="true" aria-labelledby="dtitle">
<div class="dhead"><h2 id="dtitle">{c.t("enq_list")}</h2><button type="button" class="iconb" data-close aria-label="{c.t("close")}">{ic("x")}</button></div>
<ul class="dlist"></ul><p class="dempty">{c.t("d_empty")}</p><a class="btn pri dgo qopen" href="contact.html">{c.t("d_go")}</a></div></aside>
<dialog class="qmodal" aria-labelledby="qtitle">
<div class="dhead"><h2 id="qtitle">{c.t("f_t")}</h2><button type="button" class="iconb qclose" aria-label="{c.t("close")}">{ic("x")}</button></div>
<div class="qbody">{form(c)}</div></dialog>
<a class="btn pri qfloat qopen" href="contact.html">{c.t("quote")}</a>
<a class="wafloat" href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener" aria-label="{c.t("wa_float")}">{ic("wa")}</a>
<script>window.RR={json.dumps(rrjs, ensure_ascii=False)}</script>
{'<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" defer></script>' if viewer_on else ""}
<script src="{c.A}site.js" defer></script>
</body>
</html>'''

# ---------- pages ----------
def home(c):
    stats = "".join(f'<div class="stat"><b>{c.t(a)}</b><span>{c.t(b)}</span></div>' for a, b in [("st1a", "st1b"), ("st2a", "st2b"), ("st3a", "st3b"), ("st4a", "st4b")])
    order2 = [PROD["cb02"], PROD["cb01"], PROD["cb03"], PROD["cb04"]]
    body = f'''<section class="hero"><div class="wrap herog">
<div class="herot"><p class="eyebrow">{c.t("eyebrow")}</p><h1>{c.t("h1")}</h1><p class="lead">{c.t("hero_p")}</p>
<div class="btns"><a class="btn pri qopen" href="contact.html">{c.t("quote")}</a><a class="btn light" href="products.html">{c.t("see_range")}</a><a class="btn ghost" href="#range">{c.t("all_btn")}</a></div></div>
{viewer(c, order2, c.t("eyebrow"))}
</div><div class="wrap"><div class="stats">{stats}</div></div></section>
<section class="band" id="range"><div class="wrap"><div class="shead"><p class="eyebrow">{c.t("range_eyebrow")}</p><h2>{c.t("range_t")}</h2><p>{c.t("range_p")}</p></div>{grid(c, PRODUCTS)}</div></section>
{videos(c, ["cb01", "cb02"])}
<section class="band teal"><div class="wrap split"><div><h2>{c.t("sell_t")}</h2>{sell(c)}<h3 class="sub">{c.t("serve_t")}</h3>{serve(c)}</div>
<figure class="ph">{c.img("collapsible-silicone-bottle-lifestyle", c.x(("Flip-straw collapsible bottles rolled up in several colours", "زجاجات بشفّاط قلّاب ملفوفة بعدة ألوان")))}</figure></div></section>
<section class="band"><div class="wrap split rev"><figure class="ph white">{c.img("private-label-custom-print-bottle", c.x(("Collapsible bottle with an all-over custom printed pattern", "زجاجة قابلة للطي بنقشة مطبوعة مخصّصة")))}</figure>
<div><p class="eyebrow">{c.t("pl_eyebrow")}</p><h2>{c.t("pl_t")}</h2><p>{c.t("pl_p")}</p>{plist(c)}<a class="btn" href="private-label.html">{c.t("pl_more")}</a></div></div></section>
<section class="band soft"><div class="wrap"><div class="shead"><h2>{c.t("compare")}</h2></div>{range_table(c)}</div></section>
<section class="band"><div class="wrap"><div class="shead"><p class="eyebrow">{c.t("order_eyebrow")}</p><h2>{c.t("order_t")}</h2></div>{steps(c)}<p><a class="more" href="how-to-order.html">{c.t("steps_more")} →</a></p></div></section>
<section class="band soft"><div class="wrap narrow"><h2>{c.t("faq_t")}</h2>{faq(c)}</div></section>
{cta(c)}'''
    ld = [{"@type": "WebSite", "@id": BASE + "/#site", "url": c.url("index.html"), "name": ORG, "alternateName": ALT_NAMES, "inLanguage": "ar" if c.ar else "en", "publisher": {"@id": BASE + "/#org"}}, faq_ld(c),
          {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": c.url(p["slug"] + ".html"), "name": c.x(p["full"])} for i, p in enumerate(PRODUCTS)]}]
    return page(c, "home", body, ld, viewer_on=True)

def products(c):
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_products"), "")]
    body = f'''<section class="band phead"><div class="wrap">{crumbs(c, items)}<h1>{c.t("p_t")}</h1><p class="lead">{c.t("p_p")}</p><div class="btns">{brochure(c, "btn ghost")}</div></div></section>
<section class="band"><div class="wrap">{grid(c, PRODUCTS, "h2")}</div></section>
<section class="band soft"><div class="wrap"><div class="shead"><h2>{c.t("compare")}</h2><p>{c.t("range_p")}</p></div>{range_table(c)}</div></section>
<section class="band"><div class="wrap"><h2>{c.t("serve_t")}</h2>{serve(c)}</div></section>{cta(c)}'''
    return page(c, "products", body, [crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "products.html")])])

def product(c, p):
    f = p["slug"] + ".html"
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_products"), "products.html"), (c.x(p["name"]), "")]
    thumbs = f'<button type="button" class="th on" data-3d aria-label="{c.t("view3d")}">{ic("cube")}<span>{c.t("view3d")}</span></button>' + "".join(
        f'<button type="button" class="th" data-src="{c.A}img/{n}.jpg" data-alt="{ESC(c.x(a))}">{c.img(n, c.x(a))}</button>' for n, a in p["imgs"])
    sw = "".join(f'<li><span class="dot" style="--c:{h}"></span>{ESC(col[c.L])}</li>' for col in p["colours"] for h in [col[2]])
    feats = "".join(f'<li><h3>{c.x(a)}</h3><p>{c.x(b)}</p></li>' for a, b in p["feats"])
    specs = "".join(f'<tr><th scope="row">{SPEC_L[k][c.L]}</th><td>{en if not c.ar else ar}</td></tr>' for k, en, ar in p["specs"])
    others = [q for q in PRODUCTS if q["id"] != p["id"]]
    first = p["imgs"][0]
    body = f'''<section class="band pp"><div class="wrap">{crumbs(c, items)}<div class="ppg">
<div class="media"><div class="mview">{viewer(c, [p], c.x(p["full"]) + " — 3D")}</div>
<figure class="mphoto" hidden>{c.img(first[0], c.x(first[1]), "mimg", lazy=False)}</figure>
<div class="thumbs" role="group" aria-label="{c.t("view3d")}">{thumbs}</div></div>
<div class="info"><p class="tagrow"><span class="code">{p["code"]}</span><span class="badge">{c.x(p["badge"])}</span></p>
<h1>{c.x(p["full"])}</h1><p class="lead">{c.x(p["desc"])}</p>
<dl class="mini big"><div><dt>{c.t("th_cap")}</dt><dd>{c.x((p["cap"], p["cap"].replace("ml", "مل")))}</dd></div><div><dt>{c.t("th_moq")}</dt><dd>{c.x(p["moq"])}</dd></div><div><dt>{c.t("th_prod")}</dt><dd>{c.x(p["prod"])}</dd></div></dl>
<h2 class="h4">{c.t("colours_avail")}</h2><ul class="cols">{sw}<li class="anyc">+ {c.t("colours_more")}</li></ul>
<div class="btns"><a class="btn pri qopen" href="contact.html" data-id="{p["id"]}">{c.t("enquire")}</a><button type="button" class="btn ghost addbtn" data-id="{p["id"]}">{c.t("add")}</button></div>
<div class="labcard">{ic("flask", "ic big")}<div><h2 class="h4">{c.t("lab")}</h2><p>{c.x(p["lab"])}</p></div></div></div></div></div></section>
{videos(c, [p["id"]], "")}
<section class="band soft"><div class="wrap split top"><div><h2>{c.t("features")}</h2><ul class="feats">{feats}</ul></div>
<div><h2>{c.t("specs")}</h2><table class="spec"><tbody>{specs}</tbody></table><p class="ideal"><b>{c.t("ideal")}:</b> {c.x(p["ideal"])}</p></div></div></section>
<section class="band soft"><div class="wrap"><h2>{c.t("more")}</h2>{grid(c, others)}</div></section>{cta(c)}'''
    key = (f, (p["full"][0] + " – Custom Logo, Wholesale | R&R Exports", p["full"][1] + " – بشعارك وبالجملة | آر آند آر"), p["meta"])
    ld = [product_ld(c, p), crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "products.html"), (items[2][0], f)])]
    return page(c, key, body, ld, viewer_on=True, og_img=first[0] + ".jpg", pid=p["id"])

def private(c):
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_private"), "")]
    body = f'''<section class="band phead"><div class="wrap">{crumbs(c, items)}<div class="split"><div><p class="eyebrow">{c.t("pl_eyebrow")}</p><h1>{c.t("pl_h1")}</h1><p class="lead">{c.t("pl_lead")}</p>{plist(c)}
<div class="btns"><a class="btn pri qopen" href="contact.html">{c.t("quote")}</a></div></div>
<figure class="ph white">{c.img("private-label-custom-print-bottle", c.x(("Private label collapsible bottle with custom all-over print and logo details", "زجاجة قابلة للطي بعلامة خاصة مع طباعة مخصّصة وتفاصيل الشعار")), lazy=False)}</figure></div></div></section>
<section class="band soft"><div class="wrap"><h2>{c.t("q_t")}</h2>{quality(c)}</div></section>
<section class="band"><div class="wrap"><h2>{c.t("pick_bottle")}</h2>{grid(c, PRODUCTS)}</div></section>
<section class="band soft"><div class="wrap"><h2>{c.t("order_t")}</h2>{steps(c)}</div></section>{cta(c)}'''
    return page(c, "private", body, [crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "private-label.html")])])

def order(c):
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_order"), "")]
    body = f'''<section class="band phead"><div class="wrap">{crumbs(c, items)}<p class="eyebrow">{c.t("order_eyebrow")}</p><h1>{c.t("order_t")}</h1><p class="lead">{c.t("order_lead")}</p></div></section>
<section class="band"><div class="wrap">{steps(c)}</div></section>
<section class="band soft"><div class="wrap"><h2>{c.t("terms_t")}</h2>{terms(c)}</div></section>
<section class="band"><div class="wrap"><h2>{c.t("q_t")}</h2>{quality(c)}</div></section>
<section class="band soft"><div class="wrap narrow"><h2>{c.t("faq_t")}</h2>{faq(c)}</div></section>{cta(c)}'''
    return page(c, "order", body, [faq_ld(c), crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "how-to-order.html")])])

def about(c):
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_about"), "")]
    body = f'''<section class="band phead"><div class="wrap">{crumbs(c, items)}<div class="split"><div><p class="eyebrow">{c.t("who_eyebrow")}</p><h1>{c.t("who_t")}</h1><p class="lead">{c.t("who_p1")}</p><p>{c.t("who_p2")}</p><p>{c.t("aka")}</p></div>
<figure class="ph">{c.img("collapsible-silicone-bottle-lifestyle", c.x(("Rolled-up flip-straw silicone bottles in several colours", "زجاجات سيليكون ملفوفة بعدة ألوان")), lazy=False)}</figure></div></div></section>
<section class="band"><div class="wrap"><h2>{c.t("why_t")}</h2>{why(c)}</div></section>
<section class="band teal"><div class="wrap"><h2>{c.t("sell_t")}</h2>{sell(c)}<h3 class="sub">{c.t("serve_t")}</h3>{serve(c)}</div></section>
<section class="band"><div class="wrap"><h2>{c.t("q_t")}</h2>{quality(c)}</div></section>{cta(c)}'''
    return page(c, "about", body, [crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "about.html")])])

def contact(c):
    items = [(c.t("crumb_home"), "index.html"), (c.t("nav_contact"), "")]
    body = f'''<section class="band phead"><div class="wrap">{crumbs(c, items)}<h1>{c.t("c_t")}</h1><p class="lead">{c.t("c_p")}</p>
<div class="btns"><button type="button" class="btn pri qopen">{c.t("quote")}</button>{brochure(c, "btn ghost")}</div>
<ul class="ccards"><li>{ic("mail", "ic big")}<span>{c.t("email_l")}</span><a href="mailto:{EMAIL}" dir="ltr">{EMAIL}</a></li>
<li>{ic("wa", "ic big")}<span>{c.t("phone_l")}</span><a href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener" dir="ltr">{PHONE}</a></li>
<li>{ic("pin", "ic big")}<span>{c.t("addr_l")}</span><b>{c.t("addr")}</b></li></ul></div></section>'''
    return page(c, "contact", body, [crumb_ld(c, [(items[0][0], "index.html"), (items[1][0], "contact.html")]),
                 {"@type": "ContactPage", "url": c.url("contact.html"), "about": {"@id": BASE + "/#org"}}])

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "img")); os.makedirs(os.path.join(OUT, "ar"))
    for f in os.listdir(os.path.join(ROOT, "photos")): shutil.copy(os.path.join(ROOT, "photos", f), os.path.join(OUT, "assets", "img", f))
    # Open Graph image 1200x630
    im = Image.open(os.path.join(ROOT, "photos", "flip-straw-collapsible-bottle-colours-sizes.jpg"))
    og = Image.new("RGB", (1200, 630), (255, 255, 255)); r = min(1160 / im.width, 600 / im.height)
    im2 = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS); og.paste(im2, ((1200 - im2.width) // 2, (630 - im2.height) // 2))
    og.save(os.path.join(OUT, "assets", "img", "og-image.jpg"), quality=85)
    for a in ("style.css", "site.js"): shutil.copy(os.path.join(ROOT, a), os.path.join(OUT, "assets", a))
    shutil.copytree(os.path.join(ROOT, "videos"), os.path.join(OUT, "assets", "video"))
    shutil.copy(os.path.join(ROOT, "brochure", BROCHURE), os.path.join(OUT, "assets", BROCHURE))
    urls = []
    for L in (0, 1):
        c = Ctx(L); d = os.path.join(OUT, "ar") if L else OUT
        out = {"index.html": home(c), "products.html": products(c), "private-label.html": private(c), "how-to-order.html": order(c),
               "about.html": about(c), "contact.html": contact(c)}
        for p in PRODUCTS: out[p["slug"] + ".html"] = product(c, p)
        for f, h in out.items():
            open(os.path.join(d, f), "w", encoding="utf-8").write(h)
            if L == 0: urls.append(f)
    c0, c1 = Ctx(0), Ctx(1)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for f in urls:
        imgs = "".join(f'<image:image><image:loc>{BASE}/assets/img/{n}.jpg</image:loc></image:image>' for p in PRODUCTS if p["slug"] + ".html" == f for n, _ in p["imgs"])
        for c in (c0, c1):
            sm.append(f'<url><loc>{c.url(f)}</loc><lastmod>2026-11-26</lastmod>'
                      f'<xhtml:link rel="alternate" hreflang="en" href="{c0.url(f)}"/><xhtml:link rel="alternate" hreflang="ar" href="{c1.url(f)}"/>'
                      f'<xhtml:link rel="alternate" hreflang="x-default" href="{c0.url(f)}"/>{imgs}</url>')
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    print("built", len(urls) * 2, "pages")

if __name__ == "__main__": build()
