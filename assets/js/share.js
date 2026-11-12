/* サイエンス里山ラボ宗像  ─  シェアボタン
   <div class="share-box" data-share-text="シェアするときの文"></div> の中にボタンをつくる。
   シェアするURLは、そのページの canonical（?me=1 などが付かないように） */
(() => {
  'use strict';
  const SVG = {
    share: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12M7.5 7.5 12 3l4.5 4.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M8 11H6.5A1.5 1.5 0 0 0 5 12.5v7A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5v-7a1.5 1.5 0 0 0-1.5-1.5H16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    line: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.3 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>',
    x: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.77zm-1.08 16.18h1.7L7.4 4.73H5.58z"/></svg>',
    facebook: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5.02 3.66 9.18 8.44 9.94v-7.03H7.9v-2.91h2.54V9.84c0-2.52 1.49-3.91 3.78-3.91 1.1 0 2.24.2 2.24.2v2.47h-1.26c-1.24 0-1.63.78-1.63 1.57v1.89h2.78l-.44 2.91h-2.34V22c4.78-.76 8.43-4.92 8.43-9.94z"/></svg>',
    link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
  };
  const canon = document.querySelector('link[rel="canonical"]');
  const url = canon ? canon.href : location.origin + location.pathname;
  const enc = encodeURIComponent;
  const track = m => { if (window.gtag) gtag('event', 'share', { method: m, content_type: 'page', item_id: location.pathname }); };

  document.querySelectorAll('.share-box').forEach(box => {
    const text = box.dataset.shareText || document.title;
    const lead = box.dataset.shareLead || '';
    const a = (k, label, href) => `<a class="share-btn sh-${k}" href="${href}" target="_blank" rel="noopener" data-m="${k}">${SVG[k]}<span>${label}</span></a>`;
    box.innerHTML = `${lead ? `<p class="share-lead">${lead}</p>` : ''}<div class="share-btns">
      ${navigator.share ? `<button class="share-btn sh-share" type="button" data-m="native">${SVG.share}<span>シェアする</span></button>` : ''}
      ${a('line', 'LINE', `https://social-plugins.line.me/lineit/share?url=${enc(url)}&text=${enc(text)}`)}
      ${a('x', 'X', `https://x.com/intent/post?text=${enc(text)}&url=${enc(url)}`)}
      ${a('facebook', 'Facebook', `https://www.facebook.com/sharer/sharer.php?u=${enc(url)}`)}
      <button class="share-btn sh-copy" type="button" data-m="copy">${SVG.link}<span>リンクをコピー</span></button>
    </div>`;
    box.addEventListener('click', async e => {
      const b = e.target.closest('.share-btn'); if (!b) return;
      track(b.dataset.m);
      if (b.dataset.m === 'native') {
        try { await navigator.share({ title: document.title, text, url }); } catch (err) {}
      } else if (b.dataset.m === 'copy') {
        const sp = b.querySelector('span');
        try { await navigator.clipboard.writeText(url); sp.textContent = 'コピーしました！'; }
        catch (err) {  // 古いブラウザ：見えない入力欄に入れてコピー
          const t = Object.assign(document.createElement('textarea'), { value: url }); t.style.cssText = 'position:fixed;opacity:0';
          document.body.appendChild(t); t.select(); const ok = document.execCommand('copy'); t.remove();
          sp.textContent = ok ? 'コピーしました！' : url;
        }
        setTimeout(() => { sp.textContent = 'リンクをコピー'; }, 2000);
      }
    });
  });
})();
