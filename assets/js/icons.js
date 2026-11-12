/* サイエンス里山ラボ宗像  ─  アイコン（手描き風の線画）。どのページからも使う */
(() => {
  const ICON_PATHS = {
    'いきもの': '<path d="M24 14v24"/><path d="M24 21c-4-8-16-10-16-2 0 6 8 8 16 6"/><path d="M24 21c4-8 16-10 16-2 0 6-8 8-16 6"/><path d="M24 27c-4 0-12 2-10 8 2 4 8 2 10-4"/><path d="M24 27c4 0 12 2 10 8-2 4-8 2-10-4"/><path d="M22 13l-3-6M26 13l3-6"/>',
    'しょくぶつ': '<path d="M24 42V22"/><path d="M24 27c0-8-6-12-14-12 0 8 6 12 14 12z"/><path d="M24 22c0-7 5-11 13-11 0 7-5 11-13 11z"/><path d="M13 42h22"/>',
    'かがく': '<path d="M18 6h12M21 6v12L10 38a4 4 0 0 0 3.5 6h21a4 4 0 0 0 3.5-6L27 18V6"/><path d="M14 32h20"/><circle cx="21" cy="38" r="2"/><circle cx="28" cy="36" r="1.6"/>',
    'でんき': '<path d="M27 4L12 27h10l-3 17 17-25H25z"/>',
    '火・エネルギー': '<path d="M24 44c-8 0-13-5-13-12 0-8 7-11 8-20 5 3 7 8 6 12 2-1 3-3 3-5 4 4 7 8 7 13 0 7-5 12-11 12z"/><path d="M24 44c-3 0-5-2-5-5 0-3 3-5 4-8 3 2 6 5 6 8s-2 5-5 5z"/>',
    'ものづくり': '<path d="M8 40l17-17"/><path d="M22 14l8-8 12 12-8 8z"/><path d="M26 18l4 4"/><path d="M6 42l4-4"/>',
    'アート': '<path d="M24 6C13 6 5 14 5 23c0 8 6 13 12 13 4 0 4 3 3 5-1 3 1 4 4 4 11 0 19-9 19-20S35 6 24 6z"/><circle cx="15" cy="21" r="2.6"/><circle cx="23" cy="13" r="2.6"/><circle cx="32" cy="16" r="2.6"/><circle cx="35" cy="25" r="2.6"/>',
    'おと・ひかり': '<path d="M18 36V11l20-5v26"/><path d="M18 17l20-5"/><circle cx="13" cy="36" r="5"/><circle cx="33" cy="32" r="5"/>',
    'からだ・ちから': '<path d="M24 44V28"/><path d="M24 30c-10 0-15-5-15-11 0-5 4-8 8-8 1-4 4-7 7-7s6 3 7 7c4 0 8 3 8 8 0 6-5 11-15 11z"/><path d="M24 35l-6-4M24 33l5-4"/>',
    'ロボット・AI': '<rect x="10" y="15" width="28" height="22" rx="7"/><path d="M24 15V9"/><circle cx="24" cy="7" r="2.6"/><circle cx="18" cy="25" r="2.6"/><circle cx="30" cy="25" r="2.6"/><path d="M19 31h10M6 23v6M42 23v6"/>',
  };
  const SNS_ICON = {
    instagram: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5.5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="17.4" cy="6.6" r="1.4" fill="currentColor"/></svg>',
    youtube: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="5" width="20" height="14" rx="4.5" fill="currentColor"/><path d="M10 9l5.5 3-5.5 3z" fill="#fff"/></svg>',
    tiktok: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 3h3c.3 2.2 1.7 3.6 4 3.9v3c-1.5 0-2.9-.4-4-1.2V15a6 6 0 1 1-6-6v3.1A2.9 2.9 0 1 0 14 15z" fill="currentColor"/></svg>',
    facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.3-1.4 1.5-1.4h1.4V5.1c-.3 0-1.1-.1-2.1-.1-2.1 0-3.6 1.3-3.6 3.7V11H8.4v3h2.3v7z" fill="currentColor"/></svg>',
  };
  const UI_ICON = {
    news: '<path d="M8 20v8h6l14 8V12l-14 8z"/><path d="M15 28l3 10h5l-2-10"/><path d="M34 18c2.5 2.5 2.5 9.5 0 12M38.5 14c5 5 5 15 0 20"/>',
    about: '<circle cx="20" cy="20" r="12"/><path d="M29 29l11 11"/><path d="M15 25c0-6 4-9 10-9 0 6-4 9-10 9z"/>',
    classes: null,
    teachers: '<path d="M4 18l20-9 20 9-20 9z"/><path d="M12 22v9c0 3 6 6 12 6s12-3 12-6v-9"/><path d="M44 18v12"/>',
    videos: '<rect x="5" y="10" width="38" height="28" rx="7"/><path d="M20 18l10 6-10 6z"/>',
    play: '<path d="M14 16h20a9 9 0 0 1 9 9v4a6 6 0 0 1-10 4l-3-3H18l-3 3a6 6 0 0 1-10-4v-4a9 9 0 0 1 9-9z"/><path d="M14 22v8M10 26h8"/><circle cx="32" cy="24" r="2.2"/><circle cx="36" cy="29" r="2.2"/>',
    join: '<path d="M6 14h36v7a3.5 3.5 0 0 0 0 6v7H6v-7a3.5 3.5 0 0 0 0-6z"/><path d="M30 16v3M30 23v3M30 30v2"/>',
    contact: '<rect x="5" y="11" width="38" height="26" rx="6"/><path d="M8 15l16 11 16-11"/>',
    camera: '<rect x="5" y="15" width="38" height="25" rx="7"/><path d="M16 15l3-6h10l3 6"/><circle cx="24" cy="27" r="7"/>',
    star: '<path d="M24 5l5.6 12.2 13.4 1.5-10 9 2.8 13.3L24 34.3 12.2 41l2.8-13.3-10-9 13.4-1.5z"/>',
    ticket: '<path d="M6 14h36v7a3.5 3.5 0 0 0 0 6v7H6v-7a3.5 3.5 0 0 0 0-6z"/><path d="M30 16v3M30 23v3M30 30v2"/>',
    kid: '<circle cx="24" cy="13" r="7"/><path d="M11 42c0-9 6-16 13-16s13 7 13 16"/>',
    calendar: '<rect x="6" y="10" width="36" height="32" rx="6"/><path d="M6 19h36M16 6v8M32 6v8"/><circle cx="16" cy="28" r="2.2"/><circle cx="24" cy="28" r="2.2"/><circle cx="32" cy="28" r="2.2"/>',
    pin: '<path d="M24 44s14-13 14-24a14 14 0 0 0-28 0c0 11 14 24 14 24z"/><circle cx="24" cy="20" r="5"/>',
    family: '<circle cx="16" cy="13" r="5.5"/><circle cx="33" cy="18" r="4.5"/><path d="M6 41c0-9 4-15 10-15s10 6 10 15M26 41c0-7 3-12 7-12s8 5 8 12"/>',
    line: '<path d="M24 8C13 8 5 15 5 23c0 7 6 13 15 15 1 .3 1 1 .8 2l-.4 2c0 .5.4 1 1.5.4 2-1 11-7 15-11 2.5-2.6 3.6-5.4 3.6-8.4C43 15 35 8 24 8z"/>',
    chat: '<path d="M8 10h32a4 4 0 0 1 4 4v16a4 4 0 0 1-4 4H22l-9 7v-7H8a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z"/><path d="M14 20h20M14 26h12"/>',
    mountain: '<path d="M4 40l14-22 8 12 6-8 12 18z"/><circle cx="35" cy="11" r="4"/>',
    link: '<path d="M20 28l8-8"/><path d="M22 14l3-3a8 8 0 0 1 11 11l-3 3"/><path d="M26 34l-3 3a8 8 0 0 1-11-11l3-3"/>',
    person: '<circle cx="24" cy="15" r="8"/><path d="M8 42c0-10 7-17 16-17s16 7 16 17"/>',
    heart: '<path d="M24 41S6 30 6 18a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 12-18 23-18 23z"/>',
    rule: '<rect x="9" y="7" width="30" height="36" rx="5"/><path d="M17 4h14v7H17z"/><path d="M16 21h16M16 28h16M16 35h10"/>',
    shield: '<path d="M24 5l16 6v11c0 11-7 18-16 21-9-3-16-10-16-21V11z"/><rect x="17" y="21" width="14" height="11" rx="2.5"/><path d="M20 21v-3a4 4 0 0 1 8 0v3"/>',
    fire: '<path d="M24 44c-8 0-13-5-13-12 0-8 7-11 8-20 5 3 7 8 6 12 2-1 3-3 3-5 4 4 7 8 7 13 0 7-5 12-11 12z"/><path d="M24 44c-3 0-5-2-5-5 0-3 3-5 4-8 3 2 6 5 6 8s-2 5-5 5z"/>',
    home: '<path d="M6 22L24 7l18 15"/><path d="M11 18v22h26V18"/><path d="M20 40V29h8v11"/>',
    work: '<rect x="5" y="15" width="38" height="25" rx="5"/><path d="M17 15v-4a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v4M5 26h38"/>',
    history: '<circle cx="24" cy="24" r="17"/><path d="M24 14v10l7 5"/>',
    free: '<path d="M24 6a18 18 0 1 1-.01 0z"/><path d="M17 13l7 10 7-10M24 23v13M18 26h12M18 31h12"/>',
    browser: '<rect x="5" y="9" width="38" height="30" rx="5"/><path d="M5 17h38M10 13h1M14 13h1"/><path d="M20 23v11l9-5.5z"/>',
    tablet: '<rect x="10" y="5" width="28" height="38" rx="5"/><path d="M20 37h8"/>',
  };
  UI_ICON.classes = ICON_PATHS['かがく'];
  // GPTでつくった絵のアイコン（assets/img/icons/<名前>.webp）。ここにない名前は線画を使う
  const IMG_ICONS = ['news', 'classes', 'teachers', 'videos', 'play', 'join', 'contact', 'about', 'camera',
    'star', 'ticket', 'kid', 'calendar', 'pin', 'family', 'line', 'chat', 'mountain',
    'person', 'heart', 'work', 'history', 'rule', 'shield', 'fire', 'home', 'link', 'art'];
  const icon = (k, base = '') => IMG_ICONS.includes(k)
    ? `<img class="ic ic-img" src="${base}assets/img/icons/${k}.webp" alt="" aria-hidden="true">`
    : `<svg class="ic" viewBox="0 0 48 48" aria-hidden="true">${UI_ICON[k] || ''}</svg>`;
  window.SATO_ICONS = { ICON_PATHS, SNS_ICON, UI_ICON, icon };

  // お知らせ1件分のHTML（トップとお知らせページで共通）。base は下のページなら '../'
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const pad = n => String(n).padStart(2, '0');
  const isNew = s => { const [y, m, d] = s.split('-').map(Number); return (Date.now() - new Date(y, m - 1, d)) / 864e5 <= 30; };
  const href = (u, base) => /^(https?:|mailto:)/.test(u) ? u : base + u;
  window.SATO_NEWS = {
    html(n, base = '', open = false) {
      const [y, m, d] = n.date.split('-');
      const paras = esc(n.body || '').split(/\n{2,}/).map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
      // 写真は見るだけ（押しても何も起きない）
      const imgs = (n.images || []).map(src => `<span class="news-img"><img src="${esc(base + src)}" alt="${esc(n.title)}" loading="lazy"></span>`).join('');
      const links = (n.links || []).map(l => {
        const u = href(l.url, base), ext = /^https?:/.test(l.url);
        return `<a class="link-pill" href="${esc(u)}"${ext ? ' target="_blank" rel="noopener"' : ''}>${esc(l.label)} ${ext ? '↗' : '→'}</a>`;
      }).join('');
      return `<li class="news-item" id="n-${esc(n.id)}"><details${open ? ' open' : ''}><summary>
        <span class="news-date">${y}.${m}.${d}</span>${n.category ? `<span class="news-cat">${esc(n.category)}</span>` : ''}
        <span class="news-title">${esc(n.title)}${isNew(n.date) ? '<span class="news-new">NEW</span>' : ''}</span></summary>
        <div class="news-body${imgs ? ' has-img' : ''}">${imgs ? `<div class="news-imgs">${imgs}</div>` : ''}<div class="news-text">${paras}${links ? `<p class="news-links">${links}</p>` : ''}</div></div></details></li>`;
    },
  };

  // メールアドレス：迷惑メール対策のため、ページには文字で書かず（表示は画像）、
  // ボタンを押したときだけ組み立てる
  const mail = () => ['moc.liamg', 'atakanumecneics'].map(s => [...s].reverse().join('')).reverse().join('@');
  document.addEventListener('click', e => {
    const send = e.target.closest('.js-mail-send');
    if (send) { location.href = 'mailto:' + mail() + '?subject=' + encodeURIComponent('サイエンス里山ラボ宗像へのお問い合わせ'); return; }
    const copy = e.target.closest('.js-mail-copy');
    if (copy) {
      const done = () => { const t = copy.textContent; copy.textContent = 'コピーしました！'; setTimeout(() => { copy.textContent = t; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(mail()).then(done, () => prompt('メールアドレス', mail()));
      else prompt('メールアドレス', mail());
    }
  });
})();
