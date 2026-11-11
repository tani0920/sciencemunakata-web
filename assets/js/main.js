/* サイエンス里山ラボ宗像  ─  データ（data/*.json）を読み込んで描画する */
(() => {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const CH = 'assets/img/chara/';
  const COLORS = ['blue', 'teal', 'pink'];
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const WD = ['日', '月', '火', '水', '木', '金', '土'];
  const pad = n => String(n).padStart(2, '0');
  const today = (() => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; })();
  const parseD = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
  const dayDiff = s => Math.round((parseD(s) - parseD(today)) / 864e5);
  const lineIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.3 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>';

  // 授業のジャンルアイコン（手描き風の線画）
  const { ICON_PATHS, SNS_ICON, UI_ICON } = window.SATO_ICONS;
  const catIcon = cat => `<svg class="ic" viewBox="0 0 48 48" aria-hidden="true">${ICON_PATHS[cat] || ICON_PATHS['かがく']}</svg>`;
  // 授業のアイキャッチ（LINE告知のタイトル入り画像）。なければ写真、それもなければアイコン
  const eyeHTML = (c, lazy = true) => {
    const src = c.eyecatch || c.photo;
    return src ? `<img src="${esc(src)}" alt="${esc(c.title)}"${lazy ? ' loading="lazy"' : ''}>` : `<div class="noimg">${catIcon(c.category)}</div>`;
  };

  // SNSアイコン

  // セクション・メニュー・料金などのアイコン（授業ジャンルと同じ手描き線画）
  const uiIcon = k => window.SATO_ICONS.icon(k);
  $$('[data-icon]').forEach(el => { el.innerHTML = uiIcon(el.dataset.icon); });

  // 画像を先読み（ポーズ切り替えでチラつかないように）
  COLORS.forEach(c => { for (let i = 1; i <= 5; i++) new Image().src = `${CH}${c}-${i}.webp`; });

  const load = f => fetch(`data/${f}.json`, { cache: 'no-cache' }).then(r => r.json());

  let SITE = {}, CLASSES = [], TEACHERS = [], NEWS = [], VIDEOS = [];
  Promise.all(['site', 'classes', 'teachers', 'news', 'videos', 'ruby'].map(load)).then(([s, c, t, n, v, r]) => {
    SITE = s; CLASSES = c; TEACHERS = t; NEWS = n; VIDEOS = v; setRuby(r); rubyStatic(); setAnalytics();
    setLinks(); renderSNS(); renderHero(); renderNext(); renderGallery(); renderNews(); renderClasses(); renderTeachers(); renderVideos(); renderGames();
    observeReveal(); watchLine();
  }).catch(err => {
    console.error(err);
    $('#nextCard').innerHTML = '<p>データを読み込めませんでした。時間をおいて再読み込みしてください。</p>';
  });

  const teacherOf = id => TEACHERS.find(t => t.id === id);
  const teacherLabel = c => { const t = teacherOf(c.teacher); return t ? `${t.org.split('\n')[0]}　${t.name} 先生` : (c.teacherText || ''); };
  const isPast = c => c.date < today;
  const statusOf = c => c.status === '中止' ? '中止' : isPast(c) ? '終了' : '';
  const fmtDate = s => { const d = parseD(s); return { y: d.getFullYear(), m: d.getMonth() + 1, d: d.getDate(), w: WD[d.getDay()] }; };
  const timeText = c => [c.reception && `受付 ${c.reception}〜`, c.start && `授業 ${c.start}〜${c.end || ''}`].filter(Boolean).join('　');
  const snsList = () => (SITE.sns || []).filter(s => s.url);
  const snsOf = id => snsList().find(s => s.id === id);

  function setLinks() {
    $$('.js-line').forEach(a => a.href = SITE.lineUrl);
    const yt = snsOf('youtube'); $$('.js-yt').forEach(a => yt ? a.href = yt.url : a.remove());
    // お問い合わせは公式LINEにまとめた（QRコードはパソコンで見ている人向け）
    $$('#lfQr, .js-line-qr').forEach(img => { if (SITE.lineQr) img.src = SITE.lineQr; });
    $$('#lfId, .js-line-id').forEach(el => { el.textContent = SITE.lineId || ''; });
  }

  /* ───── ふりがな（小学4年生以上で習う漢字に。子ども向けの部分だけ） ───── */
  let RUBY_RE = null, RUBY = {};
  function setRuby(dict) {
    RUBY = {};
    Object.keys(dict || {}).filter(k => !k.startsWith('_')).forEach(k => { RUBY[k] = dict[k]; });
    const keys = Object.keys(RUBY).sort((a, b) => b.length - a.length).map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    RUBY_RE = keys.length ? new RegExp(keys.join('|'), 'g') : null;
  }
  // すでにエスケープ済みの文字列に <ruby> を入れる
  const rb = html => !RUBY_RE ? html : html.replace(RUBY_RE, w => {
    const kanji = w.match(/^[\u4e00-\u9fff々]+/)[0], rest = w.slice(kanji.length);
    return `<ruby>${kanji}<rt>${RUBY[w]}</rt></ruby>${rest}`;
  });
  const er = t => rb(esc(t));
  // 授業の申し込み：LINEで開く申込画面（/apply/）。トークで申し込む今までの方法（記入欄つきの文面）も小さく並べて残す
  const applyUrl = c => `/apply/?c=${encodeURIComponent(c.id)}`;
  const talkUrl = c => SITE.lineId && window.SATO_APPLY ? window.SATO_APPLY.url(SITE.lineId, c) : SITE.lineUrl;
  const applyLinks = c => `<a class="btn btn-line" href="${esc(applyUrl(c))}" data-class="${esc(window.SATO_APPLY ? window.SATO_APPLY.label(c) : c.title)}">${lineIcon}LINEで申し込む</a>
    <p class="apply-hint">会員・参加したことのある方は、来る人をえらぶだけ。<br><a href="${esc(talkUrl(c))}" data-class="${esc(window.SATO_APPLY ? window.SATO_APPLY.label(c) : c.title)}" target="_blank" rel="noopener">トークで申し込む</a>こともできます</p>`;
  // ページに最初から書いてある見出しなど
  function rubyStatic() {
    $$('.hero-copy .hero-badge, .hero-lead, .sec-head h2, .gal-head b, #classes .sec-lead, #play .sec-lead, .gnav a, .venn .vl').forEach(el => {
      const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      const nodes = []; while (walk.nextNode()) nodes.push(walk.currentNode);
      nodes.forEach(n => {
        if (n.parentElement.closest('rt, ruby, svg')) return;
        const html = rb(esc(n.nodeValue));
        if (html === esc(n.nodeValue)) return;
        const span = document.createElement('span'); span.innerHTML = html; n.replaceWith(...span.childNodes);
      });
    });
  }

  /* ───── アクセス解析（Google アナリティクス）：site.json の gaId を入れたら動く ───── */
  function setAnalytics() {
    const id = SITE.gaId; if (!id || !/^G-[A-Z0-9]+$/.test(id)) return;
    const s = document.createElement('script'); s.async = true; s.src = `https://www.googletagmanager.com/gtag/js?id=${id}`;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', id, isMe() ? { traffic_type: 'internal' } : {});
    // 押されたボタンを記録：授業の申し込み（apply_class）／入会フォーム（join_form）／LINEの友だち追加・問い合わせ（line_click）
    document.addEventListener('click', e => {
      const a = e.target.closest('a'); if (!a) return;
      const h = a.getAttribute('href') || '';
      if (h.includes('/apply/')) gtag('event', 'apply_class', { class_title: a.dataset.class || '', method: 'app' });
      else if (h.includes('oaMessage')) gtag('event', 'apply_class', { class_title: a.dataset.class || '', method: 'talk' });
      else if (/forms\.gle|docs\.google\.com\/forms/.test(h)) gtag('event', 'join_form');
      else if (a.matches('.js-line, .btn-line, .lf-btn')) gtag('event', 'line_click');
    });
  }
  // 自分（運営側）のアクセスは数えない：?me=1 を付けて一度ひらく か 管理画面をひらいた端末は「内部」になる（?me=0 で解除）
  function isMe() {
    try {
      const q = new URLSearchParams(location.search).get('me');
      if (q === '1') localStorage.setItem('sato_me', '1');
      if (q === '0') localStorage.removeItem('sato_me');
      return localStorage.getItem('sato_me') === '1';
    } catch (e) { return false; }
  }

  /* ───── SNS（メニューの下・フッター・Instagramの帯） ───── */
  function renderSNS() {
    const list = snsList();
    $$('.js-sns-icons').forEach(box => {
      box.innerHTML = list.map(s => `<a class="sns-ic sns-${esc(s.id)}" href="${esc(s.url)}" target="_blank" rel="noopener" aria-label="${esc(s.label)}" title="${esc(s.label)}">${SNS_ICON[s.id] || ''}</a>`).join('');
    });
    const ig = snsOf('instagram'), band = $('#snsBand');
    if (!band) return;
    if (!ig) { band.hidden = true; return; }
    const others = list.filter(s => s.id !== 'instagram' && s.id !== 'facebook');
    band.innerHTML = `<a class="ig-card" href="${esc(ig.url)}" target="_blank" rel="noopener">
        <span class="ig-icon">${SNS_ICON.instagram}</span>
        <span class="ig-text"><small>もっと見たい人は</small><b>Instagram で、授業のようすを発信中！</b><em>@${esc(ig.url.replace(/\/$/, '').split('/').pop())} をフォロー →</em></span>
        <img class="ig-chara" src="${CH}pink-2.webp" alt="">
      </a>
      ${others.length ? `<p class="sns-others">${others.map(s => `<a class="sns-pill sns-${esc(s.id)}" href="${esc(s.url)}" target="_blank" rel="noopener">${SNS_ICON[s.id] || ''}${esc(s.label)}${s.note ? `<small>${esc(s.note)}</small>` : ''}</a>`).join('')}</p>` : ''}`;
  }

  /* ───── ヒーローの写真：数秒ごとにふわっと切り替わる ───── */
  function renderHero() {
    const list = SITE.hero || [], box = $('#heroSlides'), dots = $('#heroDots');
    if (list.length < 2) return;
    box.innerHTML = list.map((s, i) => `<img class="slide${i ? '' : ' on'}" src="${esc(s.src)}" alt="${esc(s.alt)}" width="1200" height="960"${s.pos ? ` style="object-position:${esc(s.pos)}"` : ''}${i ? ' loading="lazy"' : ' fetchpriority="high"'}>`).join('');   // pos：写真ごとに見せる位置（例 "50% 25%"）
    dots.innerHTML = list.map((_, i) => `<span class="${i ? '' : 'on'}"></span>`).join('');
    const imgs = $$('.slide', box), ds = $$('span', dots);
    let cur = 0;
    // 2枚目以降も先に読み込んで展開しておく（初めて切り替わるときに引っかからないように）
    const ready = imgs.map(img => { img.loading = 'eager'; return img.decode ? img.decode().catch(() => {}) : Promise.resolve(); });
    const go = async n => {
      const next = (n + imgs.length) % imgs.length;
      await ready[next];
      imgs[cur].classList.remove('on'); ds[cur].classList.remove('on');
      cur = next;
      imgs[cur].classList.add('on'); ds[cur].classList.add('on');
    };
    setInterval(() => { if (!document.hidden) go(cur + 1); }, reduceMotion ? 9000 : 5000);
  }

  /* ───── つぎの授業 ───── */
  function renderNext() {
    const up = CLASSES.filter(c => !isPast(c) && c.status !== '中止').sort((a, b) => a.date.localeCompare(b.date));
    const el = $('#nextCard');
    if (!up.length) {
      el.classList.add('next-empty');
      el.innerHTML = `<span class="next-label">つぎの授業</span>
        <div class="next-body"><h3>つぎの授業はただいま準備中！</h3><p class="sub">決まったらLINEでいちばんにお知らせします。</p></div>
        <div class="next-side"><a class="btn btn-line" href="${esc(SITE.lineUrl)}" target="_blank" rel="noopener">${lineIcon}友だち追加</a></div>
        <img class="next-chara" src="${CH}pink-5.webp" alt="">`;
      return;
    }
    const c = up[0], d = fmtDate(c.date), n = dayDiff(c.date);
    el.dataset.cat = c.category;
    el.innerHTML = `<span class="next-label">つぎの授業</span>
      <button class="next-photo" data-open="${esc(c.id)}" aria-label="${esc(c.title)} のくわしい内容"><span class="np-img">${eyeHTML(c, false)}</span></button>
      <div class="next-body">
        <span class="cc-cat">${catIcon(c.category)}${esc(c.category)}</span>
        <p class="next-date">${d.y}年 <b>${d.m}</b>月<b>${d.d}</b>日（${d.w}）</p>
        <h3>${er(c.title)}</h3>${c.subtitle ? `<p class="sub">${er(c.subtitle)}</p>` : ''}
        <p class="next-meta"><span>🕐 ${esc(timeText(c))}</span><span>👩‍🔬 ${esc(teacherLabel(c))}</span></p>
      </div>
      <div class="next-side">
        <p class="countdown">${n === 0 ? '<b>きょう</b>！' : `あと<b>${n}</b>日`}</p>
        ${applyLinks(c)}
        <p style="margin:10px 0 0"><a href="#" data-open="${esc(c.id)}">くわしく見る →</a></p>
      </div>
      <img class="next-chara" src="${CH}pink-5.webp" alt="">`;
    $$('[data-open]', el).forEach(b => b.addEventListener('click', e => { e.preventDefault(); openClass(c.id); }));
  }

  /* ───── お知らせ ───── */
  function renderNews() {
    const list = [...NEWS].sort((a, b) => b.date.localeCompare(a.date));
    // トップには新しい3件だけ。ぜんぶはお知らせページ（news/）で
    $('#newsList').innerHTML = list.length ? list.slice(0, 3).map(n => window.SATO_NEWS.html(n)).join('')
      : '<li style="padding:20px;text-align:center">いまお知らせはありません</li>';
    const more = $('#newsMore');
    if (more) { more.hidden = false; $('a', more).innerHTML = `お知らせをもっと見る（ぜんぶで${list.length}件）→`; }
  }

  /* ───── 授業のようす（写真が流れる） ───── */
  function renderGallery() {
    // 授業の動画から切り出した場面（scene）があればそれを、なければ授業の写真を出す
    const items = CLASSES.filter(c => (c.scene || (c.photo && c.photoType === 'photo')) && isPast(c))
      .sort((a, b) => b.date.localeCompare(a.date));
    const track = $('#galTrack'); if (!track) return;
    if (!items.length) { track.closest('.gal-viewport').hidden = true; return; }
    const one = items.map((c, i) => `<button class="polaroid" data-open="${esc(c.id)}" style="--rot:${[-3, 2, -1.5, 3, -2.5, 1.5][i % 6]}deg">
      <img src="${esc(c.scene || c.photo)}" alt="${esc(c.title)} のようす" loading="lazy"><span>${er(c.title)}</span></button>`).join('');
    track.innerHTML = one + one.replace(/alt="[^"]*"/g, 'alt="" aria-hidden="true"').replace(/<button /g, '<button tabindex="-1" ');

    // ゆっくり自動で流れる。指（マウス）で横にすべらせると、そのぶん速く送れる。はなすとまた自動に戻る
    const vp = track.closest('.gal-viewport');
    // 自動の位置は pos に小数で持つ（スマホで1pxずつ動かすと丸められて止まることがあるため）
    let paused = false, resumeAt = 0, dragging = false, moved = 0, startX = 0, startLeft = 0;
    let pos = 0, lastSet = null, speed = 1;
    const half = () => track.scrollWidth / 2;
    const wrap = () => {
      const h = half(); if (!h) return;
      if (vp.scrollLeft >= h) vp.scrollLeft -= h; else if (vp.scrollLeft <= 0) vp.scrollLeft += h; else return;
      pos = vp.scrollLeft; lastSet = vp.scrollLeft;
    };
    // 指やマウスで動かしている間は止める。はなして約1秒したら、ゆっくり加速しながら自動に戻る
    const hold = (ms = 1000) => { paused = true; resumeAt = performance.now() + ms; speed = 0; };
    vp.addEventListener('touchstart', () => hold(Infinity), { passive: true });
    vp.addEventListener('touchend', () => hold(1000), { passive: true });
    vp.addEventListener('touchcancel', () => hold(1000), { passive: true });
    vp.addEventListener('wheel', () => hold(1000), { passive: true });
    vp.addEventListener('scroll', () => {
      // 自動で動かした以外の動き（指をはなした後の慣性スクロールなど）があれば、その間も待つ
      if (lastSet !== null && Math.abs(vp.scrollLeft - lastSet) > 3 && resumeAt !== Infinity) hold(900);
      wrap();
    }, { passive: true });
    vp.addEventListener('pointerdown', e => {
      if (e.pointerType !== 'mouse') return;
      dragging = true; moved = 0; startX = e.clientX; startLeft = vp.scrollLeft; hold();
    });
    addEventListener('pointermove', e => {
      if (!dragging) return;
      moved = Math.max(moved, Math.abs(e.clientX - startX));
      vp.scrollLeft = startLeft - (e.clientX - startX); hold();
    });
    addEventListener('pointerup', () => { dragging = false; });
    vp.addEventListener('mouseleave', () => { dragging = false; });
    track.addEventListener('click', e => {
      if (moved > 6) { moved = 0; e.preventDefault(); return; }   // ドラッグしただけのときは開かない
      const b = e.target.closest('[data-open]'); if (b) openClass(b.dataset.open);
    });
    vp.scrollLeft = 1; pos = 1; lastSet = vp.scrollLeft;
    if (reduceMotion) return;
    let last = performance.now();
    const tick = now => {
      const dt = Math.min(50, now - last); last = now;
      if (paused && now > resumeAt) { paused = false; pos = vp.scrollLeft; }
      if (!paused && !document.hidden) {
        speed = Math.min(1, speed + dt / 900);   // 再開するときはふわっと加速
        pos += dt * .045 * speed;                // 1秒で約45px、左へ流れる
        vp.scrollLeft = pos; lastSet = vp.scrollLeft;
        wrap();
      }
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ───── 授業 ─────
     これから：大きいカード
     これまで：小さいカード（年とジャンルでしぼれる）。はじめは8件、「もっと見る」で8件ずつ */
  const PAGE = 8;
  let tab = 'upcoming', year = '', cat = '', shown = PAGE;
  function renderClasses() {
    const up = CLASSES.filter(c => !isPast(c)).sort((a, b) => a.date.localeCompare(b.date));
    const past = CLASSES.filter(isPast).sort((a, b) => b.date.localeCompare(a.date));
    $('#cntUp').textContent = up.length; $('#cntPast').textContent = past.length;
    if (!up.length && tab === 'upcoming' && !renderClasses.done) tab = 'past';
    renderClasses.done = true;
    $$('.tab').forEach(b => { const on = b.dataset.tab === tab; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });

    const grid = $('#classGrid'), filter = $('#pastFilter'), more = $('#classMore');
    grid.classList.toggle('is-past', tab === 'past');

    if (tab === 'upcoming') {
      filter.hidden = true; more.hidden = true;
      grid.innerHTML = up.length ? up.map(bigCard).join('')
        : `<div class="class-empty"><img src="${CH}teal-2.webp" alt="">つぎの授業はただいま準備中です。<br>決まったらLINEでいちばんにお知らせします！</div>`;
      observeReveal(); return;
    }

    const years = [...new Set(past.map(c => c.date.slice(0, 4)))];
    const cats = [...new Set(past.map(c => c.category))];
    filter.hidden = false;
    filter.innerHTML = `<div class="chips" aria-label="年でしぼる">${[['', 'ぜんぶの年']].concat(years.map(y => [y, `${y}年`]))
        .map(([v, l]) => `<button class="chip-y${year === v ? ' on' : ''}" data-year="${v}">${l}</button>`).join('')}</div>
      <div class="chips" aria-label="ジャンルでしぼる">${[`<button class="cat${cat ? '' : ' on'}" data-cat-f="">ぜんぶ</button>`]
        .concat(cats.map(x => `<button class="cat${cat === x ? ' on' : ''}" data-cat-f="${esc(x)}">${catIcon(x)}${esc(x)}</button>`)).join('')}</div>`;

    const list = past.filter(c => (!year || c.date.startsWith(year)) && (!cat || c.category === cat));
    grid.innerHTML = list.length ? list.slice(0, shown).map(miniCard).join('')
      : '<div class="class-empty">この条件の授業はありません</div>';
    const rest = list.length - shown;
    more.hidden = rest <= 0;
    if (rest > 0) $('button', more).textContent = `もっと見る（あと${rest}件）`;
    observeReveal();
  }
  function bigCard(c) {
    const d = fmtDate(c.date), st = statusOf(c);
    return `<button class="class-card reveal" data-cat="${esc(c.category)}" data-open="${esc(c.id)}">
      <div class="cc-photo">${eyeHTML(c)}<span class="cc-icon" title="${esc(c.category)}">${catIcon(c.category)}</span></div>
      <div class="cc-top"><div class="cc-date"><span class="cc-year">${d.y}年</span>${d.m}<small>月</small>${d.d}<small>日（${d.w}）</small></div><span class="cc-cat">${esc(c.category)}</span></div>
      <div class="cc-body">
        <div class="cc-title">${er(c.title)}</div>${c.subtitle ? `<p class="cc-sub">${er(c.subtitle)}</p>` : ''}
        <p class="cc-teacher">${esc(teacherLabel(c))}</p>
        <div class="cc-foot">${!st ? '<span class="tag">申し込み受付中</span>' : ''}</div>
      </div>
    </button>`;
  }
  function miniCard(c) {
    const d = fmtDate(c.date), st = statusOf(c);
    return `<button class="mini-card reveal" data-cat="${esc(c.category)}" data-open="${esc(c.id)}">
      <span class="mc-img">${eyeHTML(c)}${c.videoId ? '<span class="mc-video" title="動画あり">▶</span>' : ''}${st === '中止' ? '<span class="mc-cancel">中止</span>' : ''}</span>
      <span class="mc-date"><span class="mc-ic">${catIcon(c.category)}</span>${d.y}.${d.m}.${d.d}</span>
      <span class="mc-title">${er(c.title)}</span>
    </button>`;
  }
  document.addEventListener('click', e => {
    const t = e.target.closest('.tab'); if (t) { tab = t.dataset.tab; year = ''; cat = ''; shown = PAGE; renderClasses(); return; }
    const y = e.target.closest('[data-year]'); if (y) { year = y.dataset.year; shown = PAGE; renderClasses(); return; }
    const f = e.target.closest('[data-cat-f]'); if (f) { cat = f.dataset.catF; shown = PAGE; renderClasses(); return; }
    if (e.target.closest('#classMore button')) { shown += PAGE; renderClasses(); return; }
    const o = e.target.closest('.class-card[data-open], .mini-card[data-open]'); if (o) openClass(o.dataset.open);
  });

  const modal = $('#classModal');
  function openClass(id) {
    const c = CLASSES.find(x => x.id === id); if (!c) return;
    const d = fmtDate(c.date), st = statusOf(c), t = teacherOf(c.teacher);
    // 授業のようす：授業の動画から切り出した写真（shots）。まだないものは、これまでの写真
    const photos = c.shots?.length ? c.shots : [c.photoType === 'photo' ? c.photo : ''].concat(c.gallery || []).filter(Boolean);
    const gal = photos.map(g => `<img src="${esc(g)}" alt="" loading="lazy">`).join('');
    $('#classModalBody').innerHTML = `<div data-cat="${esc(c.category)}">
      <div class="md-cover">${eyeHTML(c, false)}</div>
      <div class="md-top"><span class="cc-cat">${catIcon(c.category)}${esc(c.category)}</span>${st ? ` <span class="tag">${st === '中止' ? '中止になりました' : 'おわった授業'}</span>` : ''}
        <h3>${er(c.title)}</h3>${c.subtitle ? `<p class="sub">${er(c.subtitle)}</p>` : ''}</div>
      <div class="md-body">
        <dl class="md-meta"><dt>日にち</dt><dd>${d.y}年${d.m}月${d.d}日（${d.w}）</dd>
          ${timeText(c) ? `<dt>時間</dt><dd>${esc(timeText(c))}</dd>` : ''}
          <dt>先生</dt><dd>${esc(teacherLabel(c))}</dd></dl>
        ${c.videoId ? ytHTML(c.videoId, c.title, c.videoShort) + '<div style="height:18px"></div>' : ''}
        <p>${er(c.description)}</p>
        ${gal ? `<p class="md-sub">授業のようす</p><div class="md-gallery">${gal}</div>` : ''}
        ${c.notes?.length ? `<ul class="md-notes">${c.notes.map(n => `<li>${er(n)}</li>`).join('')}</ul>` : ''}
        ${t ? `<div class="md-teacher">${t.photo ? `<img src="${esc(t.photo)}" alt="">` : ''}<p><b>${esc(t.name)} 先生</b><br>${esc(t.bio)}</p></div>` : ''}
        ${!st ? `<div class="md-cta">${applyLinks(c)}</div>` : ''}
      </div></div>`;
    modal.showModal();
    $('#classModalBody').scrollTop = 0;
  }
  modal.addEventListener('click', e => { if (e.target === modal || e.target.closest('[data-close]')) modal.close(); });
  modal.addEventListener('close', () => { $('#classModalBody').innerHTML = ''; });

  /* ───── 先生（2列。最近授業をした先生から順に6人、のこりは「ほかの先生」で開く） ───── */
  const T_FIRST = 6;
  function renderTeachers() {
    const last = id => CLASSES.filter(c => c.teacher === id && c.status !== '中止').map(c => c.date).sort().pop() || '';
    const list = [...TEACHERS].sort((a, b) => last(b.id).localeCompare(last(a.id)));
    $('#teacherGrid').innerHTML = list.map((t, i) => {
      const n = CLASSES.filter(c => c.teacher === t.id && c.status !== '中止').length;
      const initial = t.name.replace(/\s.*/, '').slice(0, 1);
      return `<article class="teacher reveal${i >= T_FIRST ? ' is-more' : ''}${t.links?.length ? ' has-links' : ''}" style="--n:${t.links?.length || 0}">
        <div class="avatar">${t.photo ? `<img src="${esc(t.photo)}" alt="${esc(t.name)} 先生" loading="lazy">` : esc(initial)}</div>
        ${t.links?.length ? `<p class="t-links">${t.links.map(l => {
          const k = /instagram/i.test(l.label) ? 'instagram' : /facebook/i.test(l.label) ? 'facebook' : /youtube/i.test(l.label) ? 'youtube' : '';
          return `<a class="sns-ic${k ? ' sns-' + k : ''}" href="${esc(l.url)}" target="_blank" rel="noopener" aria-label="${esc(t.name)} 先生の${esc(l.label)}" title="${esc(l.label)}">${k ? SNS_ICON[k] : uiIcon('link')}</a>`;
        }).join('')}</p>` : ''}
        <div class="t-info">
          <span class="t-field">${esc(t.field)}</span>${n ? `<span class="t-count">授業 ${n}回</span>` : ''}
          <p class="t-name">${esc(t.name)}<small>先生</small></p>
          <p class="t-org">${esc(t.org)}</p>
          <details><summary>プロフィール</summary><p class="t-bio">${esc(t.bio)}</p></details>
        </div>
      </article>`;
    }).join('');
    const rest = list.length - T_FIRST, more = $('#teacherMore'), btn = $('button', more);
    if (rest <= 0) return;
    more.hidden = false;
    const label = open => open ? '先生の一覧をとじる' : `ほかの先生も見る（あと${rest}人）`;
    btn.textContent = label(false);
    btn.addEventListener('click', () => {
      const open = $('#teacherGrid').classList.toggle('show-all');
      btn.textContent = label(open); btn.setAttribute('aria-expanded', open);
      if (open) observeReveal(); else $('#teachers').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  /* ───── 動画（クリックするまでYouTubeを読み込まない） ───── */
  const thumb = id => `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
  function ytHTML(id, title, short) {
    return `<div class="yt${short ? ' is-short' : ''}" data-yt="${esc(id)}" role="button" tabindex="0" aria-label="${esc(title)} を再生" style="background-image:url('${thumb(id)}')"><span class="yt-play"></span></div>`;
  }
  function playYT(box) {
    const id = box.dataset.yt;
    box.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0&playsinline=1" title="YouTube" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
    box.style.backgroundImage = 'none';
  }
  document.addEventListener('click', e => { const b = e.target.closest('.yt[data-yt]'); if (b && !b.querySelector('iframe')) playYT(b); });
  document.addEventListener('keydown', e => { const b = e.target.closest?.('.yt[data-yt]'); if (b && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); playYT(b); } });

  function renderVideos() {
    const fromClasses = CLASSES.filter(c => c.videoId).sort((a, b) => b.date.localeCompare(a.date))
      .map(c => ({ id: c.videoId, title: c.title, short: !!c.videoShort, date: c.date }));
    const all = fromClasses.filter(v => !v.short).concat(VIDEOS.filter(v => !v.short), fromClasses.filter(v => v.short), VIDEOS.filter(v => v.short));
    if (!all.length) { $('#videos').hidden = true; return; }
    const show = (v, auto) => {
      $('#player').innerHTML = ytHTML(v.id, v.title, v.short) + `<p class="player-title">${esc(v.title)}${v.date ? `<small style="opacity:.7;margin-left:.6em">${v.date.replace(/-/g, '.')}</small>` : ''}</p>`;
      if (auto) playYT($('#player .yt'));
      $$('.vthumb').forEach(b => b.classList.toggle('on', b.dataset.v === v.id));
    };
    $('#vlist').innerHTML = all.map(v => `<button class="vthumb" data-v="${esc(v.id)}"><div class="th" style="background-image:url('${thumb(v.id)}')"></div><span>${esc(v.title)}</span></button>`).join('');
    $('#vlist').addEventListener('click', e => { const b = e.target.closest('.vthumb'); if (b) { show(all.find(v => v.id === b.dataset.v), true); $('#player').scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' }); } });
    show(all[0], false);
  }

  /* ───── あそぶ ───── */
  function renderGames() {
    $('#gameGrid').innerHTML = (SITE.games || []).map(g => {
      const open = g.status === 'open' && g.url;
      const visual = g.image ? `<span class="g-img"><img src="${esc(g.image)}" alt="${esc(g.title)} のタイトル画面" loading="lazy"></span>`
        : `<span class="g-img g-chara-box"><img class="g-chara" src="${CH}${esc(g.chara || 'blue-1')}.webp" alt=""></span>`;
      return `<article class="game reveal${open ? '' : ' soon'}">
        <span class="ribbon">${open ? 'あそべる！' : 'じゅんび中'}</span>
        ${g.badge ? `<span class="g-badge">${uiIcon('star')}${er(g.badge)}</span>` : ''}
        ${open ? `<a href="${esc(g.url)}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">${visual}</a>` : visual}
        <div class="g-body"><h3>${er(g.title)}</h3><p>${er(g.desc)}</p>
        <div class="g-btns">${g.page ? `<a class="btn btn-sub g-info" href="${esc(g.page)}">ゲームの内容</a>` : ''}
        ${open ? `<a class="btn btn-main" href="${esc(g.url)}" target="_blank" rel="noopener">あそぶ ▶</a>` : '<span class="btn">もうすぐ公開</span>'}</div></div>
      </article>`;
    }).join('');
  }

  /* ───── スクロールで出てくる／見出しキャラがポーズを変える ───── */
  let io;
  function observeReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) { $$('.reveal').forEach(el => el.classList.add('in')); return; }
    io = io || new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in'); io.unobserve(e.target);
      const ch = e.target.querySelector?.('.sec-chara'); if (ch) flip(ch, ch.dataset.color, 4);
    }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal:not(.in)').forEach(el => io.observe(el));
  }
  function flip(img, color, times) {
    if (reduceMotion) return;
    let i = 0; const start = Math.floor(Math.random() * 5);
    const t = setInterval(() => { img.src = `${CH}${color}-${((start + i) % 5) + 1}.webp`; if (++i > times) clearInterval(t); }, 160);
  }
  observeReveal();

  /* ───── ヒーローのキャラ：ポーズがぱらぱら変わる・さわるとくるっと回る ───── */
  const hero = $('#heroChara'), heroImg = $('#heroCharaImg'), speech = $('#speech');
  let pose = 1, color = 0;
  if (!reduceMotion) setInterval(() => { pose = pose % 5 + 1; heroImg.src = `${CH}${COLORS[color]}-${pose}.webp`; }, 4500);
  const setWord = w => {
    const img = w === 'なぜ？';
    speech.classList.toggle('speech-img', img);
    speech.innerHTML = img ? '<img src="assets/img/naze-bubble.webp" alt="なぜ？">' : esc(w);
  };
  setWord('なぜ？');
  // スマホでは吹き出しをキャラクターの中に入れて、頭の上に出す（パソコンはキャッチコピーの横）
  const mqSp = matchMedia('(max-width: 860px)');
  const placeSpeech = () => (mqSp.matches ? hero : hero.parentElement).appendChild(speech);
  placeSpeech();
  mqSp.addEventListener('change', placeSpeech);
  const WORDS = ['なぜ？', 'ふしぎ！', 'やってみよう！', 'みつけた！', 'なるほど！', 'どうして？'];
  hero.addEventListener('click', () => {
    color = (color + 1) % 3;
    heroImg.src = `${CH}${COLORS[color]}-${pose}.webp`;
    setWord(WORDS[Math.floor(Math.random() * WORDS.length)]);
    hero.classList.remove('spin'); void hero.offsetWidth; hero.classList.add('spin');
  });
  hero.addEventListener('animationend', () => hero.classList.remove('spin'));

  /* ───── 追いかけてくるLINEボタン ───── */
  const lf = $('#lineFloat'), lfChara = $('#lfChara');
  let lastY = 0, lfPose = 5;
  addEventListener('scroll', () => {
    const y = scrollY;
    if (!reduceMotion && Math.abs(y - lastY) > 140) { lfPose = lfPose % 5 + 1; lfChara.src = `${CH}teal-${lfPose}.webp`; lastY = y; }
  }, { passive: true });
  // ページ内の大きなLINEボタンが見えているときは重ならないように隠す
  const visible = new Set();
  const lio = new IntersectionObserver(es => {
    es.forEach(e => e.isIntersecting ? visible.add(e.target) : visible.delete(e.target));
    lf.classList.toggle('hide', visible.size > 0);
  }, { threshold: .5 });
  function watchLine() { $$('.btn-line').forEach(b => lio.observe(b)); }
  watchLine();

  /* ───── スマホのメニュー ───── */
  const btn = $('#menuBtn'), nav = $('#gnav');
  btn.addEventListener('click', () => { const o = !nav.classList.contains('open'); nav.classList.toggle('open', o); btn.setAttribute('aria-expanded', o); document.body.classList.toggle('menu-open', o); });
  nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', false); document.body.classList.remove('menu-open'); } });

  /* ───── いま見ているセクションのメニューに下線を出す ───── */
  const navLinks = $$('.gnav > a[href^="#"]');
  const secs = navLinks.map(a => $(a.getAttribute('href'))).filter(Boolean);
  const markCurrent = () => {
    const line = innerHeight * .35;   // 画面の上から35%の位置にあるセクションを「いま」とする
    let cur = null;
    secs.forEach(s => { if (s.getBoundingClientRect().top <= line) cur = s; });
    // いちばん下まで来たら最後のセクション
    if (innerHeight + scrollY >= document.documentElement.scrollHeight - 4) cur = secs[secs.length - 1];
    // つぎの授業・授業ふうけいなど、メニューにないところでは前のセクションの続きにしない
    if (cur && cur.getBoundingClientRect().bottom < line) cur = null;
    navLinks.forEach(a => {
      const on = !!cur && a.getAttribute('href') === `#${cur.id}`;
      a.classList.toggle('is-current', on);
      on ? a.setAttribute('aria-current', 'location') : a.removeAttribute('aria-current');
    });
  };
  let spyRaf = 0;
  addEventListener('scroll', () => { if (!spyRaf) spyRaf = requestAnimationFrame(() => { spyRaf = 0; markCurrent(); }); }, { passive: true });
  addEventListener('resize', markCurrent);
  markCurrent();
})();
