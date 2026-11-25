/* R&R Exports — site behaviour: menu, enquiry list, quote popup, gallery, 3D bottle viewer */
(function () {
  const RR = window.RR || { products: [], s: {} };
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const KEY = 'rr_enquiry';
  const store = {
    get() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } },
    set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) {} }
  };
  let basket = store.get().filter(id => RR.products.some(p => p.id === id));

  /* ---------- mobile menu ---------- */
  const menuB = $('.menub'), nav = $('#nav');
  if (menuB && nav) menuB.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuB.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  /* ---------- enquiry list ---------- */
  const drawer = $('.drawer'), list = $('.dlist'), empty = $('.dempty'), go = $('.dgo');
  function syncBasket() {
    store.set(basket);
    $$('.cnt').forEach(c => { c.textContent = basket.length; c.dataset.n = basket.length; });
    $$('.addbtn').forEach(b => {
      const on = basket.includes(b.dataset.id);
      b.classList.toggle('on', on);
      b.textContent = on ? RR.s.added : RR.s.add;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (!list) return;
    list.innerHTML = '';
    basket.forEach(id => {
      const p = RR.products.find(x => x.id === id); if (!p) return;
      const li = document.createElement('li');
      const img = document.createElement('img'); img.src = p.img; img.alt = ''; img.width = 56; img.height = 56;
      const a = document.createElement('a'); a.href = p.url; a.textContent = p.code + ' · ' + p.name;
      const rm = document.createElement('button'); rm.type = 'button'; rm.textContent = RR.s.remove;
      rm.addEventListener('click', () => { basket = basket.filter(x => x !== id); syncBasket(); });
      li.append(img, a, rm); list.appendChild(li);
    });
    empty.hidden = basket.length > 0; go.hidden = basket.length === 0;
  }
  $$('.addbtn').forEach(b => b.addEventListener('click', () => {
    const id = b.dataset.id;
    basket = basket.includes(id) ? basket.filter(x => x !== id) : basket.concat(id);
    syncBasket();
  }));
  let lastFocus = null;
  function openDrawer() { lastFocus = document.activeElement; drawer.hidden = false; $('.dpanel .iconb').focus(); document.body.style.overflow = 'hidden'; }
  function closeDrawer() { drawer.hidden = true; document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }
  $$('.enqbtn').forEach(b => b.addEventListener('click', openDrawer));
  if (drawer) {
    $$('[data-close]', drawer).forEach(el => el.addEventListener('click', closeDrawer));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !drawer.hidden) closeDrawer(); });
  }
  syncBasket();

  /* ---------- quote popup ---------- */
  function markRow(cb) { const r = cb.closest('.prow'); r.classList.toggle('sel', cb.checked); $('select', r).disabled = !cb.checked; }
  const modal = $('.qmodal');
  if (modal) {
    const form = $('.qform', modal), done = $('.done', modal), body = $('.qbody', modal);
    const boxes = $$('input[name=p]', form);
    boxes.forEach(cb => { markRow(cb); cb.addEventListener('change', () => markRow(cb)); });
    // remember contact details for next time
    const DK = 'rr_contact';
    try {
      const d = JSON.parse(localStorage.getItem(DK) || '{}');
      d.contact = d.contact || d.email || d.phone;
      ['name', 'company', 'contact', 'country'].forEach(k => { if (d[k]) form.elements[k].value = d[k]; });
    } catch (e) {}

    function openQuote(id) {
      if (drawer && !drawer.hidden) closeDrawer();
      const want = basket.concat(id || document.body.dataset.product || []);
      boxes.forEach(cb => { if (want.includes(cb.value)) cb.checked = true; markRow(cb); });
      done.hidden = true; form.hidden = false;
      if (!modal.open) modal.showModal();
      document.body.style.overflow = 'hidden'; body.scrollTop = 0;
    }
    $$('.qopen').forEach(b => b.addEventListener('click', e => {
      if (!modal.showModal) return;
      e.preventDefault(); openQuote(b.dataset.id);
    }));
    $('.qclose', modal).addEventListener('click', () => modal.close());
    modal.addEventListener('click', e => { if (e.target === modal) modal.close(); });
    modal.addEventListener('close', () => { document.body.style.overflow = ''; });
    if (location.hash === '#enquire' && modal.showModal) openQuote();

    const sentLeads = new Set();
    form.addEventListener('submit', e => {
      e.preventDefault();
      const via = e.submitter ? e.submitter.value : 'wa';
      const f = form.elements;
      const get = n => f[n].value.trim();
      let ok = true;
      $$('.bad', form).forEach(el => el.classList.remove('bad'));
      $$('.err', form).forEach(el => el.hidden = true);
      const chosen = boxes.filter(cb => cb.checked).map(cb => cb.value);
      if (!chosen.length) { ok = false; $('[data-err=p]', form).hidden = false; }
      ['name', 'country'].forEach(k => { if (!get(k)) { ok = false; f[k].classList.add('bad'); } });
      const contact = get('contact'), isEmail = contact.includes('@');
      if (!(isEmail ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact) : contact.replace(/\D/g, '').length >= 7)) {
        ok = false; f.contact.classList.add('bad'); $('[data-err=contact]', form).hidden = false;
      }
      $('.formerr', form).hidden = ok;
      if (!ok) { const bad = $('.bad, .err:not([hidden])', form); if (bad) bad.scrollIntoView({ block: 'center', behavior: 'smooth' }); return; }
      try { localStorage.setItem(DK, JSON.stringify({ name: get('name'), company: get('company'), contact, country: get('country') })); } catch (err) {}

      const lines = ['Quote request — collapsible silicone bottles', ''];
      chosen.forEach(id => {
        const p = RR.products.find(x => x.id === id);
        lines.push('• ' + p.code + ' ' + p.name + ' — qty ' + get('q_' + id));
      });
      if (get('colours')) lines.push('Colours: ' + get('colours'));
      [['Logo printing', 'logo'], ['Packaging', 'pack'], ['Shipping', 'ship']].forEach(([label, k]) => { if (get(k)) lines.push(label + ': ' + get(k)); });
      if (f.samples.checked) lines.push('Samples first: Yes');
      lines.push('');
      lines.push('Name: ' + get('name'));
      if (get('company')) lines.push('Company: ' + get('company'));
      if (get('biz')) lines.push('Business: ' + get('biz'));
      lines.push('Destination: ' + get('country'));
      lines.push((isEmail ? 'Email: ' : 'Phone/WhatsApp: ') + contact);
      if (get('msg')) lines.push('', 'Message: ' + get('msg'));
      lines.push('', '(Sent from the ' + (RR.lang === 'ar' ? 'Arabic' : 'English') + ' website)');
      const text = lines.join('\n');
      const subj = 'Quote request: ' + chosen.map(id => RR.products.find(x => x.id === id).code).join(', ') + ' — ' + (get('company') || get('name'));
      const waUrl = 'https://wa.me/' + RR.wa + '?text=' + encodeURIComponent(text);
      const mailUrl = 'mailto:' + RR.email + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(text);
      $('.msg', done).textContent = text;
      $('.wab', done).href = waUrl;
      $('.mailb', done).href = mailUrl;
      form.hidden = true; done.hidden = false; body.scrollTop = 0; done.focus();
      // background copy to our inboxes, so the enquiry is kept even if it is never sent from WhatsApp / email
      const channel = via === 'mail' ? 'Email' : 'WhatsApp';
      const data = {
        _subject: 'Website enquiry (clicked Send on ' + channel + '): ' + get('name') + ', ' + get('country'),
        _template: 'box',
        'Clicked': 'Send on ' + channel + ' (not confirmed that the visitor sent it)',
        'Name': get('name'), 'Contact': contact, 'Country': get('country'),
        'Enquiry': text, 'Page': location.href, 'Time': new Date().toString()
      };
      if (isEmail) data._replyto = contact;
      // one request per inbox, so a problem with one does not stop the others
      (RR.lead || []).forEach(url => {
        const key = url + channel + text;
        if (sentLeads.has(key)) return;
        sentLeads.add(key);
        // keepalive: the request completes even if the page is left; a failure never blocks the visitor
        const retry = () => sentLeads.delete(key);
        fetch(url, { method: 'POST', keepalive: true, headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) })
          .then(r => r.json()).then(r => { if (String(r.success) !== 'true') retry(); }).catch(retry);
      });
      if (via === 'mail') location.href = mailUrl; else window.open(waUrl, '_blank', 'noopener');

      const cp = $('.copyb', done), label = cp.dataset.label || (cp.dataset.label = cp.textContent);
      function selectPre() { const r = document.createRange(); r.selectNodeContents($('.msg', done)); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); }
      cp.onclick = () => {
        const fin = () => { cp.textContent = RR.s.copied; setTimeout(() => cp.textContent = label, 1600); };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(fin, selectPre);
        else selectPre();
      };
      $('.editb', done).onclick = () => { done.hidden = true; form.hidden = false; body.scrollTop = 0; };
    });
  }

  /* ---------- product gallery ---------- */
  const media = $('.media');
  if (media) {
    const mview = $('.mview', media), mphoto = $('.mphoto', media), mimg = $('.mimg', media);
    $$('.th', media).forEach(t => t.addEventListener('click', () => {
      $$('.th', media).forEach(x => x.classList.remove('on')); t.classList.add('on');
      if (t.hasAttribute('data-3d') && V.ok) { mview.hidden = false; mphoto.hidden = true; V.resume(); }
      else {
        const src = t.dataset.src || $('img', $$('.th[data-src]', media)[0]).src;
        mimg.src = src; mimg.alt = t.dataset.alt || ''; mview.hidden = true; mphoto.hidden = false; V.pause();
      }
    }));
  }

  /* ---------- 3D bottle viewer (three.js) ---------- */
  const V = { ok: false, pause() {}, resume() {} };
  const host = $('.viewer');
  function fallback() {
    if (!host) return;
    const stage = host.closest('.stage');
    if (media) { // product page: show the photo instead
      $('.mview', media).hidden = true; $('.mphoto', media).hidden = false;
      const t3 = $('.th[data-3d]', media); if (t3) t3.remove();
      const first = $('.th', media); if (first) first.classList.add('on');
      return;
    }
    const im = document.createElement('img');
    im.className = 'fbimg'; im.alt = ''; im.src = (RR.products.find(p => p.id === 'cb02') || RR.products[0]).img;
    host.appendChild(im);
    $$('.vctl, .hint', stage).forEach(el => el.hidden = true);
  }
  function start() {
    if (!host) return;
    if (!window.THREE) return fallback();
    const THREE = window.THREE;
    let R;
    try { R = new THREE.WebGLRenderer({ antialias: true, alpha: true }); } catch (e) { return fallback(); }
    if (!R.getContext()) return fallback();
    V.ok = true;
    const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
    R.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); R.outputEncoding = THREE.sRGBEncoding;
    R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
    const S = new THREE.Scene();
    const C = new THREE.PerspectiveCamera(28, 1, 0.1, 60);
    // photo-studio reflections: a dim room with a few softboxes
    (function studio() {
      const room = new THREE.Scene();
      room.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), new THREE.MeshBasicMaterial({ color: new THREE.Color(.36, .39, .39), side: THREE.BackSide })));
      const box = (w, h, x, y, z, i) => {
        const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(i, i, i), side: THREE.DoubleSide }));
        m.position.set(x, y, z); m.lookAt(0, 0, 0); room.add(m);
      };
      box(3, 8, -7, 2, 4, 2.2); box(1.6, 8, 7, 1, 1, 1.5); box(8, 4, 0, 8, 1, 1.8); box(5, 5, 2, 1, -8, .9);
      const pm = new THREE.PMREMGenerator(R);
      S.environment = pm.fromScene(room, 0.04).texture; pm.dispose();
    })();
    S.add(new THREE.HemisphereLight(0xffffff, 0x9fc3bb, 0.28));
    const key = new THREE.DirectionalLight(0xffffff, 0.66); key.position.set(2.6, 5, 3.4); key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024); key.shadow.radius = 4; key.shadow.bias = -0.0004; key.shadow.normalBias = 0.015;
    Object.assign(key.shadow.camera, { left: -1.8, right: 1.8, top: 3, bottom: -1 }); S.add(key);
    const rim = new THREE.DirectionalLight(0xe8fbf6, 0.45); rim.position.set(-4, 2.5, -3); S.add(rim);
    // floor: cast shadow plus a soft contact shadow
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(8, 8), new THREE.ShadowMaterial({ opacity: 0.1 }));
    floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; S.add(floor);
    const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
    const sc = canvas(128, 128), g2 = sc.getContext('2d'), gr = g2.createRadialGradient(64, 64, 4, 64, 64, 64);
    gr.addColorStop(0, 'rgba(8,63,62,.42)'); gr.addColorStop(1, 'rgba(8,63,62,0)'); g2.fillStyle = gr; g2.fillRect(0, 0, 128, 128);
    const shadow = new THREE.Mesh(new THREE.PlaneGeometry(1.7, 1.7), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.002; S.add(shadow);
    host.appendChild(R.domElement);
    const disc = $('.disc', host); if (disc) disc.remove();

    /* materials */
    const grain = (() => { // fine silicone texture
      const c = canvas(256, 256), x = c.getContext('2d'), d = x.createImageData(256, 256);
      for (let i = 0; i < d.data.length; i += 4) { const v = 110 + Math.random() * 36; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
      x.putImageData(d, 0, 0);
      const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(5, 4); return t;
    })();
    const mat = (c, o) => {
      const m = new THREE.MeshPhysicalMaterial(Object.assign({ color: c, metalness: 0, envMapIntensity: 0.75 }, o));
      m.color.convertSRGBToLinear(); return m;
    };
    const silicone = c => mat(c, { roughness: 0.5, clearcoat: 0.18, clearcoatRoughness: 0.45, bumpMap: grain, bumpScale: 0.0022 });
    const plastic = c => mat(c, { roughness: 0.3, clearcoat: 0.55, clearcoatRoughness: 0.2 });
    const clear = () => mat(0xb9ccd2, { roughness: 0.04, clearcoat: 1, clearcoatRoughness: 0.03, transparent: true, opacity: 0.38, depthWrite: false, envMapIntensity: 1.5 });
    // tag a mesh so it follows the chosen colour: body, shade (darker) or tint (paler)
    const as = (tag, mesh) => { mesh.userData[tag] = 1; return mesh; };

    /* geometry helpers */
    const TAU = Math.PI * 2;
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    const smooth = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
    const sp = (v, n) => Math.sign(v) * Math.pow(Math.abs(v), 2 / n); // superellipse: n = 2 round, higher = squarer
    const sq = (a, n) => Math.pow(Math.pow(Math.abs(Math.sin(a)), n) + Math.pow(Math.abs(Math.cos(a)), n), -1 / n);
    const interp = (tab, y) => {
      if (y <= tab[0][0]) return tab[0].slice(1);
      for (let i = 1; i < tab.length; i++) if (y <= tab[i][0]) {
        const a = tab[i - 1], b = tab[i], t = (y - a[0]) / (b[0] - a[0] || 1);
        return a.slice(1).map((v, k) => v + (b[k + 1] - v) * t);
      }
      return tab[tab.length - 1].slice(1);
    };
    // surface around the Y axis; fn(u, v, fold) -> [x, y, z], u = 0 faces the camera
    function surf(nu, nv, fn, material, u0 = 0, u1 = 1) {
      const geo = new THREE.BufferGeometry(), pos = new Float32Array((nu + 1) * (nv + 1) * 3), uv = [], idx = [], whole = u1 - u0 === 1;
      for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++) uv.push(i / nu, j / nv);
      for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) { const a = j * (nu + 1) + i, b = a + 1, c = a + nu + 1; idx.push(a, b, c, b, c + 1, c); }
      geo.setIndex(idx); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
      const mesh = new THREE.Mesh(geo, material);
      mesh.userData.update = f => {
        let k = 0;
        for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++) { const p = fn(u0 + (u1 - u0) * i / nu, j / nv, f); pos[k++] = p[0]; pos[k++] = p[1]; pos[k++] = p[2]; }
        geo.attributes.position.needsUpdate = true; geo.computeVertexNormals();
        if (whole) { // hide the seam
          const n = geo.attributes.normal, a = new THREE.Vector3(), b = new THREE.Vector3();
          for (let j = 0; j <= nv; j++) { const l = j * (nu + 1), r = l + nu; a.fromBufferAttribute(n, l).add(b.fromBufferAttribute(n, r)).normalize(); n.setXYZ(l, a.x, a.y, a.z); n.setXYZ(r, a.x, a.y, a.z); }
        }
        geo.computeBoundingSphere();
      };
      mesh.userData.update(0);
      return mesh;
    }
    // turned part with rounded edges; ridges > 0 gives a knurled grip
    function turned(r, h, material, { bevel = 0.025, ridges = 0, depth = 0.008, rTop = r, n = 2, d = 1 } = {}) {
      const b = Math.min(bevel, h / 2);
      const prof = [[0, 0], [r - b, 0], [r - b * .3, b * .3], [r, b], [rTop, h - b], [rTop - b * .3, h - b * .3], [rTop - b, h], [0, h]];
      // each profile edge gets its own vertices so flat tops stay crisp
      const geo = surf(ridges ? ridges * 6 : 64, (prof.length - 1) * 3, (u, v) => {
        const s = Math.min(v * (prof.length - 1), prof.length - 1 - 1e-6), j = Math.floor(s), t = s - j, a = u * TAU;
        const y = prof[j][1] + (prof[j + 1][1] - prof[j][1]) * t;
        let rad = prof[j][0] + (prof[j + 1][0] - prof[j][0]) * t;
        if (ridges && y > b * .5 && y < h - b * .5 && rad > r * .6) rad += depth * (smooth(-.4, .4, Math.cos(u * ridges * TAU)) - .5);
        const k = rad * sq(a, n);
        return [k * Math.sin(a), y, k * Math.cos(a) * d];
      }, material);
      return geo;
    }
    const tube = (pts, r, material, seg = 90) => new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))), seg, r, 12, false), material);
    const ball = (r, material) => new THREE.Mesh(new THREE.SphereGeometry(r, 16, 12), material);
    const at = (o, x, y, z) => { o.position.set(x, y, z); return o; };
    // "YOUR LOGO" print that wraps onto a body surface
    function logo(fn, u0, u1, v0, v1, vertical, lift = 1.012) {
      const c = canvas(vertical ? 128 : 512, vertical ? 512 : 128), x = c.getContext('2d');
      x.translate(c.width / 2, c.height / 2); if (vertical) x.rotate(-Math.PI / 2);
      x.fillStyle = '#fff'; x.textAlign = 'center'; x.textBaseline = 'middle';
      x.font = '700 70px "Space Grotesk", Inter, sans-serif'; x.fillText('YOUR LOGO', 0, 0, 480);
      const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.anisotropy = R.capabilities.getMaxAnisotropy();
      const m = new THREE.MeshStandardMaterial({ map: t, transparent: true, opacity: 0.78, roughness: 0.45, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4 });
      return as('print', surf(64, 64, (u, v, f) => { const p = fn(u, v0 + (v1 - v0) * v, f); return [p[0] * lift, p[1], p[2] * lift]; }, m, u0, u1));
    }
    // body defined by a [height, halfWidth, halfDepth] table
    const loft = (tab, n, H, extra) => (u, v, f) => {
      const y0 = v < .05 ? 0 : (v - .05) / .95 * H, a = u * TAU;
      let [w, d] = interp(tab, y0);
      if (v < .05) { w *= v / .05; d *= v / .05; }
      const e = extra ? extra(u, y0, f, a) : { k: 1, y: y0 };
      const k = e.k * sq(a, n);
      return [w * k * Math.sin(a), e.y, d * k * Math.cos(a)];
    };
    // soft walls roll into stacked folds when collapsed
    const rolled = (H, squash, folds) => (u, y, f, a) => {
      const t = y / H, soft = smooth(0, .1, t) * (1 - smooth(.86, .98, t));
      const wave = Math.pow(Math.abs(Math.sin(t * Math.PI * folds)), .6);
      return { k: 1 + f * soft * (.2 * wave - .04) + f * soft * .025 * Math.sin(a * 3 + t * 22), y: y * (1 - squash * f) };
    };

    const BUILD = {
      cb01(c) { // origami foldable: creased square-round body, knurled screw lid, carry strap
        const g = new THREE.Group(), H = 1.68, levels = [.07, .55, 1.03, 1.48];
        const tab = [[0, .32, .32], [.035, .37, .37], [.1, .385, .385], [.55, .36, .36], [.8, .33, .33], [1.03, .355, .355], [1.32, .385, .385], [1.46, .375, .375], [1.56, .3, .3], [1.62, .22, .22], [H, .2, .2]];
        const crease = (u, y, f) => {
          let ridge = 0, pleat = 0;
          const turn = ((u * 4 + .5) % 1 + 1) % 1;
          const across = .5 + .5 * Math.tan((turn - .5) * Math.PI / 2);
          for (let i = 0; i < levels.length - 1; i++) if (y >= levels[i] && y <= levels[i + 1]) {
            const t = (y - levels[i]) / (levels[i + 1] - levels[i]);
            const dist = Math.min(Math.abs(across - t), Math.abs(across - (1 - t)), Math.min(t, 1 - t) * 1.1);
            ridge = Math.exp(-Math.pow(dist / .022, 2)); pleat = Math.sin(t * Math.PI) * (i % 2 ? 1 : -.6);
          }
          return { k: 1 + .024 * ridge - .018 * Math.abs(pleat) * (1 - ridge) + f * .17 * pleat, y: y * (1 - .68 * f) };
        };
        const fn = loft(tab, 4.6, H, crease);
        g.add(as('body', surf(256, 240, fn, silicone(c))));
        g.add(logo(fn, -.1, .1, .25, .36, false, 1.035));
        const top = new THREE.Group();
        top.add(as('tint', turned(.285, .13, silicone(c), { ridges: 36, depth: .014 })));
        top.add(at(as('body', turned(.215, .03, plastic(c))), 0, .125, 0));
        top.add(at(as('body', turned(.14, .17, plastic(c), { ridges: 12, depth: .016, bevel: .04 })), 0, .15, 0));
        top.add(at(as('body', turned(.147, .035, plastic(c))), 0, .15, 0));
        const lug = as('body', new THREE.Mesh(new THREE.TorusGeometry(.062, .02, 12, 32), silicone(c))); lug.position.set(.19, .25, 0); lug.rotation.x = -.25; top.add(lug);
        const strap = as('body', tube([[.24, .08, .03], [.43, -.02, .08], [.47, -.36, .1], [.485, -.66, .05], [.47, -.72, -.02], [.45, -.62, -.08], [.435, -.3, -.09], [.4, -.02, -.07], [.24, .08, -.04]], .016, silicone(c)));
        top.add(strap); g.add(top);
        g.userData.fold = f => { top.position.y = H * (1 - .68 * f); strap.scale.y = 1 - .5 * f; strap.position.x = f * .06; };
        return g;
      },
      cb02(c) { // flip-straw: soft square body, grey lid, screw spout, clear straw cover, handle
        const g = new THREE.Group(), H = 1.52;
        const tab = [[0, .31, .29], [.03, .355, .335], [.09, .375, .355], [.7, .362, .342], [1.35, .375, .355], [H - .04, .372, .352], [H, .35, .33]];
        const fn = loft(tab, 5, H, rolled(H, .56, 5));
        g.add(as('body', surf(128, 150, fn, silicone(c))));
        const print = logo(fn, -.05, .05, .12, .62, true); g.add(print);
        const top = new THREE.Group(), grey = () => plastic(0xc3c9cd);
        top.add(at(turned(.392, .045, plastic(0xaab1b6), { n: 5, d: .945 }), 0, -.02, 0));
        top.add(at(turned(.384, .2, grey(), { n: 5, d: .945, bevel: .045 }), 0, .03, 0));
        top.add(at(turned(.135, .05, grey()), -.15, .22, 0));
        top.add(at(as('shade', turned(.152, .11, plastic(c), { ridges: 30, depth: .011 })), -.15, .265, 0));
        top.add(at(as('shade', turned(.105, .025, plastic(c))), -.15, .372, 0));
        top.add(at(turned(.145, .05, grey(), { n: 6, d: .95 }), .165, .22, 0));
        top.add(at(turned(.029, .19, plastic(0xf6f7f7)), .165, .265, 0));
        top.add(at(as('shade', turned(.052, .035, plastic(c))), .165, .265, 0));
        const cover = turned(.142, .25, clear(), { n: 5, d: .92, bevel: .05 }); cover.renderOrder = 2; top.add(at(cover, .165, .265, 0));
        const latch = as('shade', turned(.082, .045, plastic(c), { n: 5, d: 1.05, bevel: .018 })); latch.rotation.x = Math.PI / 2; top.add(at(latch, .165, .15, .34));
        const dot = turned(.042, .018, grey()); dot.rotation.x = Math.PI / 2; top.add(at(dot, .165, .15, .385));
        const pin = turned(.027, .014, plastic(0xeef1f2)); pin.rotation.x = Math.PI / 2; top.add(at(pin, .165, .15, .401));
        [-1, 1].forEach(s => { const peg = turned(.048, .05, plastic(0xaab1b6)); peg.rotation.z = -s * Math.PI / 2; top.add(at(peg, s * .37, .12, 0)); });
        const handle = as('body', tube([[-.415, .12, 0], [-.425, .34, 0], [-.35, .57, 0], [-.16, .66, 0], [0, .675, 0], [.16, .66, 0], [.35, .57, 0], [.425, .34, 0], [.415, .12, 0]], .027, silicone(c)));
        handle.rotation.x = -.12; handle.position.z = -.015; top.add(handle);
        g.add(top);
        const strap = as('shade', surf(96, 2, (u, v) => { const a = u * TAU; return [.425 * sp(Math.sin(a), 4), .27 + v * .05 + .11 * Math.sin(a), .41 * sp(Math.cos(a), 4)]; }, silicone(c)));
        strap.material.side = THREE.DoubleSide; g.add(strap);
        g.userData.fold = f => { top.position.y = H * (1 - .56 * f); strap.visible = f > .65; print.visible = f < .35; };
        return g;
      },
      cb03(c) { // squeeze & roll-up: tapered flask, collar, stacked spout, roll-up strap
        const g = new THREE.Group(), H = 1.56;
        const tab = [[0, .26, .14], [.035, .31, .185], [.12, .335, .215], [.55, .355, .225], [1.0, .385, .235], [1.28, .42, .24], [1.42, .415, .235], [H, .385, .22]];
        const squash = rolled(H, .6, 4);
        const fn = loft(tab, 3.4, H, (u, y, f, a) => {
          const e = squash(u, y, f, a), x = Math.sin(a), front = Math.cos(a), edge = .1 * (1 - x * x * 4);
          const panel = (1 - smooth(.34, .52, Math.abs(x))) * smooth(.07, .1, y) * (1 - smooth(.34 + edge, .4 + edge, y));
          e.k *= 1 - .09 * panel * (front > 0 ? 1 : 0) * (1 - f);
          return e;
        });
        g.add(as('body', surf(144, 160, fn, silicone(c))));
        g.add(logo(fn, -.11, .11, .73, .82));
        const top = new THREE.Group();
        top.add(at(as('shade', turned(.4, .15, plastic(c), { n: 4, d: .6, bevel: .04, rTop: .385 })), 0, -.01, 0));
        top.add(at(as('shade', turned(.36, .035, plastic(c), { n: 4, d: .6 })), 0, .145, 0));
        [-1, 1].forEach(s => { const peg = turned(.042, .055, plastic(0xd9dde0)); peg.rotation.z = -s * Math.PI / 2; top.add(at(peg, s * .39, .065, 0)); });
        top.add(at(as('shade', turned(.17, .06, plastic(c))), 0, .175, 0));
        top.add(at(as('body', turned(.145, .17, plastic(c), { ridges: 28, depth: .009 })), 0, .23, 0));
        top.add(at(as('shade', turned(.152, .035, plastic(c))), 0, .395, 0));
        top.add(at(as('body', turned(.088, .12, plastic(c), { rTop: .075 })), 0, .425, 0));
        top.add(at(as('shade', turned(.1, .085, plastic(c), { ridges: 18, depth: .009 })), 0, .54, 0));
        top.add(as('body', tube([[-.15, .2, 0], [-.27, .3, 0], [-.25, .45, 0], [-.15, .5, 0], [-.09, .47, 0]], .017, silicone(c))));
        g.add(top);
        const strap = new THREE.Group();
        [-1, 1].forEach(s => strap.add(as('body', tube([[s * .2, .14, .31], [s * .09, .38, .32], [-s * .06, .66, .29], [-s * .13, .86, .1]], .028, silicone(c), 40))));
        g.add(strap);
        g.userData.fold = f => { top.position.y = H * (1 - .6 * f); strap.visible = f > .7; };
        return g;
      },
      cb04(c) { // telescopic: diamond-faceted rings, striped collar, black dual lid, handle
        const g = new THREE.Group(), N = 4, h = .34, y0 = .17;
        const black = () => plastic(0x1d1f22);
        g.add(as('shade', turned(.385, .18, silicone(c), { bevel: .05 })));
        const body = (u, v, f) => {
          const s = Math.min(N - 1e-6, v * N), i = Math.floor(s), t = s - i, a = u * TAU;
          let r;
          if (t < .2) r = .315 + .055 * smooth(0, .2, t);
          else if (t > .82) r = .37 - .055 * smooth(.82, 1, t);
          else {
            const q = (t - .2) / .62, p = ((u * 8) % 1 + 1) % 1;
            r = .37 + .05 * Math.min(1, 2.6 * Math.min(p, 1 - p, q, 1 - q)) - .016 * Math.max(0, 1 - Math.abs(Math.abs(p - .5) - Math.abs(q - .5)) * 10);
          }
          r *= 1 + (i % 2 ? -.04 : .05) * f;
          return [r * Math.sin(a), y0 + (i + t) * h * (1 - .68 * f), r * Math.cos(a)];
        };
        const skin = silicone(c); skin.flatShading = true;
        g.add(as('body', surf(192, N * 44, body, skin)));
        g.add(logo((u, v) => { const a = u * TAU, r = .392; return [r * Math.sin(a), v, r * Math.cos(a)]; }, -.1, .1, .045, .135));
        const top = new THREE.Group();
        top.add(turned(.365, .26, plastic(0xf1f3f3), { bevel: .03 }));
        [.055, .105, .155].forEach(y => top.add(at(as('body', turned(.374, .022, plastic(c), { bevel: .008 })), 0, y, 0)));
        top.add(at(turned(.372, .055, black()), 0, .25, 0));
        top.add(at(turned(.345, .17, black(), { rTop: .31, bevel: .05 }), 0, .3, 0));
        top.add(at(turned(.1, .17, black(), { rTop: .085, ridges: 20, depth: .006 }), .1, .46, 0));
        top.add(at(turned(.094, .05, black()), .1, .62, 0));
        top.add(at(as('body', turned(.065, .15, plastic(c), { n: 4 })), -.17, .45, 0));
        const flip = as('body', turned(.07, .045, plastic(c), { n: 4, d: 2.1 })); flip.rotation.z = .16; top.add(at(flip, -.15, .6, 0));
        top.add(as('body', tube([[.31, .38, 0], [.46, .36, 0], [.52, .22, 0], [.5, .02, 0], [.43, -.04, 0], [.36, .03, 0]], .042, plastic(c))));
        top.add(at(ball(.055, plastic(0xcfd4d6)), .34, .39, 0));
        g.add(top);
        g.userData.fold = f => { top.position.y = y0 + N * h * (1 - .68 * f) - .01; };
        return g;
      }
    };
    const st = { m: host.dataset.model, col: host.dataset.color, f: 0, tf: 0, ry: -0.45, v: 0, drag: false, px: 0, auto: !RM && !!$('.chips'), touched: false, run: true };
    let G = null, shown = -1;
    function fold(f) {
      if (Math.abs(f - shown) < 0.002) return;
      shown = f; G.traverse(o => { if (o.userData.update) o.userData.update(f); }); G.userData.fold(f);
    }
    function build() {
      if (G) {
        S.remove(G);
        G.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) { if (o.userData.print) o.material.map.dispose(); o.material.dispose(); } });
      }
      G = BUILD[st.m](st.col);
      G.traverse(o => { if (o.isMesh && !o.userData.print && !o.material.transparent) o.castShadow = o.receiveShadow = true; });
      S.add(G); setColor(st.col); shown = -1; fold(st.f);
    }
    function setColor(c) {
      st.col = c;
      const base0 = new THREE.Color(c), hsl = {}; base0.getHSL(hsl); const base = base0.clone().convertSRGBToLinear();
      const dark = new THREE.Color().setHSL(hsl.h, Math.min(1, hsl.s * 1.05), Math.max(0.08, hsl.l * (hsl.l > .8 ? .84 : .76))).convertSRGBToLinear();
      const pale = base0.clone().lerp(new THREE.Color(0xffffff), .45).convertSRGBToLinear();
      const ink = base0.r * .3 + base0.g * .59 + base0.b * .11 > .6 ? 0x1d2b2c : 0xffffff;
      G.traverse(o => {
        const u = o.userData;
        if (u.body) o.material.color.copy(base);
        if (u.shade) o.material.color.copy(dark);
        if (u.tint) o.material.color.copy(pale);
        if (u.print) o.material.color.set(ink).convertSRGBToLinear();
      });
    }
    build();
    function size() {
      const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return;
      R.setSize(w, h, false); C.aspect = w / h;
      const d = 5.5 * Math.max(1, 0.8 / C.aspect);
      C.position.set(0, 1.55, d); C.lookAt(0, 1.1, 0); C.updateProjectionMatrix();
    }
    const ro = new ResizeObserver(size); ro.observe(host); size();
    // controls
    const stage = host.closest('.stage'), slider = $('.foldr', stage);
    const stopAuto = () => { st.auto = false; st.touched = true; };
    if (slider) slider.addEventListener('input', () => { stopAuto(); st.tf = slider.value / 100; });
    $$('.sw', stage).forEach(b => b.addEventListener('click', () => {
      $$('.sw', b.parentElement).forEach(x => x.removeAttribute('aria-pressed')); b.setAttribute('aria-pressed', 'true'); setColor(b.dataset.c);
    }));
    $$('.mchip', stage).forEach(b => b.addEventListener('click', () => {
      stopAuto();
      $$('.mchip', stage).forEach(x => x.setAttribute('aria-pressed', 'false')); b.setAttribute('aria-pressed', 'true');
      st.m = b.dataset.m;
      const set = $$('.sws', stage); set.forEach(s => s.hidden = s.dataset.for !== st.m);
      const active = $('.sws[data-for="' + st.m + '"] .sw[aria-pressed=true]', stage) || $('.sws[data-for="' + st.m + '"] .sw', stage);
      st.col = active ? active.dataset.c : b.dataset.c; st.ry = -0.45; st.v = 0; build();
    }));
    const cv = R.domElement;
    cv.addEventListener('pointerdown', e => { st.drag = true; st.px = e.clientX; st.v = 0; stopAuto(); try { cv.setPointerCapture(e.pointerId); } catch (_) {} });
    cv.addEventListener('pointermove', e => { if (!st.drag) return; const dx = e.clientX - st.px; st.px = e.clientX; const dir = document.dir === 'rtl' ? 1 : 1; st.ry += dx * 0.011 * dir; st.v = dx * 0.0009; });
    const up = () => { st.drag = false; }; cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    let visible = true;
    const io = new IntersectionObserver(es => { visible = es[0].isIntersecting; }); io.observe(host);
    let t0 = performance.now(), raf = 0;
    function loop(now) {
      raf = requestAnimationFrame(loop);
      if (!visible || !st.run) return;
      const t = (now - t0) / 1000;
      if (st.auto) { st.tf = (Math.sin(t * 0.9 - 1.2) > 0.25) ? 1 : 0; if (slider) slider.value = Math.round(st.f * 100); }
      st.f += (st.tf - st.f) * 0.09;
      fold(st.f);
      if (!st.drag) { st.ry += st.v + (RM ? 0 : 0.0035); st.v *= 0.94; }
      G.rotation.y = st.ry;
      G.position.y = RM ? 0 : Math.sin(t * 1.4) * 0.025;
      shadow.scale.setScalar(1 + st.f * 0.15);
      R.render(S, C);
    }
    raf = requestAnimationFrame(loop);
    V.pause = () => { st.run = false; }; V.resume = () => { st.run = true; size(); };
  }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();
