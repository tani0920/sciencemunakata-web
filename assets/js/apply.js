/* 授業の申し込み文面：記入欄つきの文が入った状態で公式LINEのトークを開く
   サイトの「LINEで申し込む」（main.js）で使う。LINEリッチメニューの「申し込む」も同じ文（授業名なし）。
   項目名は里山ラボアプリの読み取り（parseLineApplication）と合わせている。変えるときはアプリも直す。 */
window.SATO_APPLY = (() => {
  const WD = '日月火水木金土';
  const label = c => {
    if (!c) return '';
    const [y, m, d] = c.date.split('-').map(Number);
    return `${m}/${d}（${WD[new Date(y, m - 1, d).getDay()]}）${c.title}`;
  };
  // LINEのリッチメニューの「申し込む」は、この文（授業名なし）を入れたリンクを直接使う。
  // リンクの上限が1000文字なので、項目を増やすときは文字数に注意（いまは授業名なしで961文字）。
  const text = c => ['🌱授業の申し込み',
    `📅授業：${label(c)}`,
    '👤保護者のお名前：',
    '🧒お子さまのお名前・学年：',
    '👪いっしょに来るご家族：',
    '※会員の方は👤と👪だけでOK',
    '',
    '🔰はじめての方は',
    '🏠お住まい（町名まで）：',
    '💡参加のきっかけ：',
    '🔍知ったところ：'].join('\n');
  const url = (lineId, c) => `https://line.me/R/oaMessage/${encodeURIComponent(lineId)}/?${encodeURIComponent(text(c))}`;
  return { label, text, url };
})();
