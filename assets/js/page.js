/* サイエンス里山ラボ宗像  ─  下のページ（代表あいさつ・会員規約・個人情報）用。
   メニュー・アイコン・SNS・追いかけてくるLINEボタン・スクロールで出てくる動き */
(() => {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const BASE = document.body.dataset.base || '';
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const { SNS_ICON, UI_ICON } = window.SATO_ICONS;
  const uiIcon = k => window.SATO_ICONS.icon(k, BASE);
  $$('[data-icon]').forEach(el => { el.innerHTML = uiIcon(el.dataset.icon); });

  fetch(`${BASE}data/site.json`, { cache: 'no-cache' }).then(r => r.json()).then(SITE => {
    $$('.js-line').forEach(a => a.href = SITE.lineUrl);
    const qr = $('#lfQr'); if (qr && SITE.lineQr) qr.src = SITE.lineQr;
    const id = $('#lfId'); if (id) id.textContent = SITE.lineId || '';
    const list = (SITE.sns || []).filter(s => s.url);
    $$('.js-sns-icons').forEach(box => {
      box.innerHTML = list.map(s => `<a class="sns-ic sns-${esc(s.id)}" href="${esc(s.url)}" target="_blank" rel="noopener" aria-label="${esc(s.label)}" title="${esc(s.label)}">${SNS_ICON[s.id] || ''}</a>`).join('');
    });
    const ga = SITE.gaId;
    if (ga && /^G-[A-Z0-9]+$/.test(ga)) {
      const s = document.createElement('script'); s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${ga}`; document.head.appendChild(s);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
      gtag('js', new Date()); gtag('config', ga);
      document.addEventListener('click', e => { if (e.target.closest('.js-line, .btn-line, .lf-btn')) gtag('event', 'line_click'); });
    }
    watchLine();
  }).catch(err => console.error(err));

  // お知らせページ：data/news.json をぜんぶ表示（はじめから開いた状態）。種類でしぼれる
  const newsBox = $('#newsPage');
  if (newsBox) {
    fetch(`${BASE}data/news.json`, { cache: 'no-cache' }).then(r => r.json()).then(list => {
      list = [...list].sort((a, b) => b.date.localeCompare(a.date));
      let cat = '';
      const cats = [...new Set(list.map(n => n.category).filter(Boolean))];
      const filter = $('#newsFilter');
      const draw = () => {
        const shown = list.filter(n => !cat || n.category === cat);
        newsBox.innerHTML = shown.length ? shown.map(n => window.SATO_NEWS.html(n, BASE, true)).join('')
          : '<li class="news-loading">いまお知らせはありません</li>';
        if (cats.length > 1) {
          filter.hidden = false;
          filter.innerHTML = [['', `ぜんぶ（${list.length}）`]].concat(cats.map(c => [c, c]))
            .map(([v, l]) => `<button class="chip-y${cat === v ? ' on' : ''}" data-ncat="${esc(v)}" type="button">${esc(l)}</button>`).join('');
        }
      };
      filter.addEventListener('click', e => { const b = e.target.closest('[data-ncat]'); if (b) { cat = b.dataset.ncat; draw(); } });
      draw();
      // トップから「#n-○○」で来たら、その記事までスクロール
      if (location.hash) { const t = document.getElementById(location.hash.slice(1)); if (t) setTimeout(() => t.scrollIntoView({ block: 'start' }), 50); }
    }).catch(() => { newsBox.innerHTML = '<li class="news-loading">お知らせを読みこめませんでした</li>'; });
  }

  // スクロールで出てくる
  if (reduceMotion || !('IntersectionObserver' in window)) $$('.reveal').forEach(el => el.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }),
      { threshold: .1, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal').forEach(el => io.observe(el));
  }

  // 追いかけてくるLINEボタン（ページ内のLINEボタンが見えているときは隠す）
  const lf = $('#lineFloat'), lfChara = $('#lfChara');
  let lastY = 0, pose = 5;
  addEventListener('scroll', () => {
    if (!reduceMotion && Math.abs(scrollY - lastY) > 140) { pose = pose % 5 + 1; lfChara.src = `${BASE}assets/img/chara/teal-${pose}.webp`; lastY = scrollY; }
  }, { passive: true });
  const visible = new Set();
  const lio = new IntersectionObserver(es => {
    es.forEach(e => e.isIntersecting ? visible.add(e.target) : visible.delete(e.target));
    lf.classList.toggle('hide', visible.size > 0);
  }, { threshold: .5 });
  function watchLine() { $$('.btn-line').forEach(b => lio.observe(b)); }

  // 目次：いま読んでいるところに色をつける
  const toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    const tio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      toc.forEach(a => a.classList.toggle('on', a.getAttribute('href') === `#${e.target.id}`));
    }), { rootMargin: '-30% 0px -60% 0px' });
    toc.forEach(a => { const t = $(a.getAttribute('href')); if (t) tio.observe(t); });
  }

  // スマホのメニュー
  const btn = $('#menuBtn'), nav = $('#gnav');
  btn.addEventListener('click', () => { const o = !nav.classList.contains('open'); nav.classList.toggle('open', o); btn.setAttribute('aria-expanded', o); document.body.classList.toggle('menu-open', o); });
  nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', false); document.body.classList.remove('menu-open'); } });
})();
