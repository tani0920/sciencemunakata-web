# -*- coding: utf-8 -*-
"""下のページ（代表あいさつ・会員規約・個人情報の取り扱い）を作る。
ヘッダー・フッターをトップページと同じ形でそろえるため、文章はここに書いて、このスクリプトで HTML を書き出す。
使い方:  python3 _tools/build_pages.py   （WEBサイト フォルダで）
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C6.5 3 2 6.6 2 11c0 3.9 3.5 7.2 8.3 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.1.9c0 .3-.2 1 .9.5s5.9-3.5 8-6C21.3 14.3 22 12.7 22 11c0-4.4-4.5-8-10-8z"/></svg>'
WAVE = 'M0 30C240 0 480 0 720 30S1200 60 1440 30V60H0z'
FOOT = 'M0 60C240 20 480 20 720 60S1200 100 1440 60V120H0z'


def page(slug, title, en, icon, lead, chara, body, desc):
    B = '../'
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜サイエンス里山ラボ宗像</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.sciencemunakata.tech/{slug}/">
<meta property="og:site_name" content="サイエンス里山ラボ宗像">
<meta property="og:locale" content="ja_JP">
<meta property="og:type" content="article">
<meta property="og:url" content="https://www.sciencemunakata.tech/{slug}/">
<meta property="og:title" content="{title}｜サイエンス里山ラボ宗像">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.sciencemunakata.tech/assets/img/ogp.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{B}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{B}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&family=Zen+Maru+Gothic:wght@500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{B}assets/css/style.css?v=202611101254">
</head>
<body class="subpage" data-base="{B}">

<header class="site-header" id="top">
  <div class="header-inner">
    <a class="brand" href="{B}" aria-label="サイエンス里山ラボ宗像 トップへ">
      <picture>
        <source media="(max-width: 600px), (min-width: 961px) and (max-width: 1199px)" srcset="{B}assets/img/logo-color.webp">
        <img src="{B}assets/img/logo-line.webp" alt="サイエンス里山ラボ宗像" width="1400" height="128">
      </picture>
    </a>
    <nav class="gnav" id="gnav" aria-label="メインメニュー">
      <a href="{B}#news"><span class="nav-ic" data-icon="news"></span><span class="nav-tx">お知らせ</span></a>
      <a href="{B}#classes"><span class="nav-ic" data-icon="classes"></span><span class="nav-tx">授業</span></a>
      <a href="{B}#teachers"><span class="nav-ic" data-icon="teachers"></span><span class="nav-tx">先生</span></a>
      <a href="{B}#videos"><span class="nav-ic" data-icon="videos"></span><span class="nav-tx">動画</span></a>
      <a href="{B}#play"><span class="nav-ic" data-icon="play"></span><span class="nav-tx">あそぶ・まなぶ</span></a>
      <a href="{B}#join"><span class="nav-ic" data-icon="join"></span><span class="nav-tx">参加方法</span></a>
      <a href="{B}#contact"><span class="nav-ic" data-icon="contact"></span><span class="nav-tx">お問い合わせ</span></a>
      <span class="gnav-sub"><a href="{B}daihyo/">代表あいさつ</a><a href="{B}kaiinkiyaku/">会員規約</a><a href="{B}kojinjoho/">個人情報の取り扱い</a></span>
      <span class="gnav-sns js-sns-icons" aria-label="SNS"></span>
      <img class="gnav-chara" src="{B}assets/img/chara/pink-1.webp" alt="" aria-hidden="true">
    </nav>
    <button class="menu-btn" id="menuBtn" aria-controls="gnav" aria-expanded="false"><span></span><span></span><span></span><b>メニュー</b></button>
  </div>
</header>

<main>
  <section class="page-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="現在地"><a href="{B}">トップ</a><span aria-hidden="true">›</span><span>{title}</span></nav>
      <span class="sec-icon" data-icon="{icon}" aria-hidden="true"></span>
      <p class="sec-en">{en}</p>
      <h1>{title}</h1>
      {f'<p class="page-lead">{lead}</p>' if lead else ''}
    </div>
    <img class="page-chara" src="{B}assets/img/chara/{chara}.webp" alt="" aria-hidden="true">
    <svg class="wave-edge" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><g class="wave w4"><path d="{WAVE}"/><path transform="translate(1440 0)" d="{WAVE}"/></g></svg>
  </section>

  <div class="page-body">
    <div class="wrap narrow">
{body}
      <div class="page-cta reveal">
        <a class="btn btn-sub" href="{B}">← トップページへもどる</a>
        <a class="btn btn-line js-line" href="#" target="_blank" rel="noopener">{LINE_SVG}LINEで聞く・申し込む</a>
      </div>
    </div>
  </div>
</main>

<footer class="site-footer">
  <svg class="hills hills-foot" viewBox="0 0 1440 120" preserveAspectRatio="none" aria-hidden="true"><g class="wave w3"><path d="{FOOT}"/><path transform="translate(1440 0)" d="{FOOT}"/></g></svg>
  <div class="foot-inner">
    <a href="{B}"><img class="foot-logo" src="{B}assets/img/logo-white.webp" alt="サイエンス里山ラボ宗像" width="900" height="354"></a>
    <p class="foot-place">福岡県宗像市大穂の里山</p>
    <p class="foot-sns js-sns-icons" aria-label="SNS"></p>
    <ul class="foot-links">
      <li><a href="{B}daihyo/">代表あいさつ</a></li>
      <li><a href="{B}kaiinkiyaku/">会員規約</a></li>
      <li><a href="{B}kojinjoho/">個人情報の取り扱い</a></li>
    </ul>
    <p class="copy">© サイエンス里山ラボ宗像</p>
  </div>
</footer>

<div class="line-float" id="lineFloat">
  <img class="lf-chara" id="lfChara" src="{B}assets/img/chara/teal-5.webp" alt="" aria-hidden="true">
  <a class="lf-btn js-line" href="#" target="_blank" rel="noopener">
    {LINE_SVG}
    <span><small>授業の申し込みは</small>LINEで友だち追加</span>
  </a>
  <div class="lf-qr" aria-hidden="true">
    <img id="lfQr" alt="" width="120" height="120">
    <p>スマホで読みとってね<br><b id="lfId"></b></p>
  </div>
</div>

<script src="{B}assets/js/icons.js?v=202611101254"></script>
<script src="{B}assets/js/page.js?v=202611101254"></script>
</body>
</html>
'''


def write(slug, html):
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, 'index.html'), 'w', encoding='utf-8').write(html)
    print('書き出し', slug)


# ───────── 代表あいさつ ─────────
ACTS = [
    ('forenta 宗像エリア', '管理者', 'https://www.forenta.net/munakata'),
    ('むなかた自然栽培推進会', 'プロデュース支援', 'https://www.munakatasss.net/'),
    ('宗像大島 一日一組限定離島宿 minawa', 'プロデュース', 'http://minawa.jp/'),
    ('むなかたシェアラボ', '管理人', 'http://munakatasharelab.com/'),
    ('むなかたシェアハウス', '大家・管理人', 'http://munakatasharehouse.com/'),
]
acts = '\n'.join(f'''          <a class="act reveal" href="{u}" target="_blank" rel="noopener"><span class="act-role">{r}</span><b>{n}</b><span class="act-url">{u.split('//')[1].rstrip('/')} ↗</span></a>''' for n, r, u in ACTS)

daihyo = f'''      <section class="prof-card reveal">
        <figure class="prof-photo"><img src="../assets/img/daihyo.webp?v=2" alt="代表 谷口竜平と愛犬" width="600" height="750"></figure>
        <div class="prof-name">
          <p class="prof-role">サイエンス里山ラボ宗像 代表</p>
          <p class="prof-jp">谷口 竜平</p>
          <p class="prof-en">Taniguchi Ryohei</p>
          <p class="prof-meta"><span>1980年生まれ</span><span>福岡県宗像市出身</span></p>
        </div>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="heart"></span>宗像の里山で、子どもたちの「なぜ？」を育てたい</h2>
        <p>はじめまして。サイエンス里山ラボ宗像 代表の谷口竜平です。</p>
        <p>宗像で生まれ育ったわたしには、祖父母から受け継いだ家と、約7,200坪の里山があります。この里山を、子どもたちが遊びながら学べる場所にしたい。そんな思いから「サイエンス里山ラボ宗像」をはじめました。</p>
        <p>子どもたちは毎日の暮らしのなかで、たくさんの「なぜ？」に出会います。その「なぜ？」は、興味や好奇心の種です。仕事やプライベートで出会った大学の先生や、科学にかかわる専門家のみなさんのお話や活動はワクワクがいっぱいです。自分が感じたことを子どもたちともいっしょに体験したい。そんな想いからこの教室を始めました。自然の中で実験し、観察し、自分の手でつくってみる。そんな体験を通して、自分で疑問を見つけ、考え、学ぶ力を育ててほしいと思っています。</p>
        <p>授業のあとは、ぜひご家族で里山を楽しんでください。焚き火を囲んだり、虫をさがしたり。里山でお待ちしています。</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="person"></span>代表プロフィール</h2>
        <p>1980年生まれ。福岡県宗像市出身。事業企画・都市デザイン・建築設計・広告企画制作・販促プロモーションを行うクリエイティブオフィスなどを経て、2014年2月、個人事業主として開業。企業・団体、商品・サービスなどのミッション、ビジョンの整理・制作、事業の立ち上げ、ブランドづくり、コンセプトメイキング、事業戦略のサポート、企画・制作などのクライアントワークから自主事業などを、プロデューサー・ディレクター・デザイナーとして行う。</p>
        <p>地元宗像の祖父母から受け継いだ家と土地の有効活用事業として、約7,200坪の里山もシェアする「むなかたシェアハウス」、森林レンタルサービス「forenta 宗像エリア」を展開。ツリーハウスのある里山を遊びと学びのある場にするプロジェクトを模索中。</p>
        <p>2017年「宗像日本酒プロジェクト」の立ち上げに参加、その後「むなかた自然栽培推進会」へと進化し、プロデュースの側面で支援。2020年、宗像大島にて仲間と島づくり会社、合同会社「渡海屋」を設立（2023年2月役員辞職）。2020年春オープンの赤間駅前創業支援施設「fabbit 宗像」に地元サポーターとして協力。同年、宗像の観光拠点「街道の駅 赤馬館」企画・広報として参画（2023年3月末契約満了）。2021年冬、ローカルWEBメディア「宗像経済新聞」の創刊メンバーとして参加し、取材・編集や福岡県の事業に携わる。2023年10月には相続した山林を活用したキャンプ事業「forenta 宗像エリア」をスタート。その他に、一日一組限定離島宿、6次産業のブランディング、北九州市立大学にて文部科学省GP事業の企画広報担当、博多伝統工芸の商品開発プロジェクト、セルフリノベーション複合施設などのプロデュース。NPO法人福岡テンジン大学において企画力を有する人材育成、およびスタートアップ系ベンチャー企業、社会福祉関係などのデザインコミュニケーションに携わる。</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="work"></span>いまの活動</h2>
        <div class="act-grid">
{acts}
        </div>
        <h3 class="sub-h"><span class="h-ic sm" data-icon="star"></span>資格</h3>
        <ul class="hist">
          <li><span>2025</span>環境省認定制度 脱炭素アドバイザー ベーシック 2025#3</li>
        </ul>
        <h3 class="sub-h"><span class="h-ic sm" data-icon="history"></span>これまで</h3>
        <ul class="hist">
          <li><span>2010〜2016</span>福岡テンジン大学 理事・授業企画統括コーディネーターなど</li>
          <li><span>2012〜2014</span>文部科学省 大学間連携共同教育推進事業</li>
        </ul>
      </section>
'''
write('daihyo', page('daihyo', '代表あいさつ', 'MESSAGE', 'person', '', 'blue-5', daihyo,
                     'サイエンス里山ラボ宗像 代表・谷口竜平のあいさつとプロフィール。'))

# ───────── 会員規約 ─────────
ARTS = [
    ('第1条', '名称および所在地', ['本教室は「サイエンス里山ラボ宗像」と称し、福岡県宗像市大穂455 むなかたシェアラボに主たる事務所を置く。']),
    ('第2条', '入会の手続き', ['本教室に入会できる方は、定められた条件に該当し、本教室の趣旨に賛同し本規約を承諾した方とします。（以下「会員」といいます。）']),
    ('第3条', '授業内容、追加変更など', ['本教室は、自然の中で科学を学ぶサービスを提供する教室です。',
                              '教室の運営日は原則として教室が定める方法でホームページに掲載しているものとします。気象・災害・その他の理由により、教室の休校または内容変更を行う場合には、所定の方法により会員へ通知を行います。']),
    ('第4条', '会費等支払い', ['会員は、本教室の定める会費等を所定の方法で支払わなければなりません。会費等の種類、金額、支払い期限及び支払い方法等は本教室が定めるものとします。']),
    ('第5条', '会費の不返還', ['一旦入金した会費等は、理由の如何を問わず返還しないものとします。']),
    ('第6条', '退会', ['本教室は年度ごとの申込となります。期限内に更新の申出がない場合、自動的に退会したものとみなします。']),
    ('第7条', '欠席', ['欠席を希望する場合には、本教室の連絡ツールや授業前後などにて承ります。その際に、欠席日を御連絡ください。']),
    ('第8条', '規則の遵守および責任', ['会員は本教室が定める本規約・入会案内・その他の注意事項を守らねばなりません。',
                             '本教室内（駐車場含む）で発生した盗難・傷害・遺失物・その他の事故について、本教室は一切の責任を負わないものとします。また会員は事故の責任に帰すべき原因により、本教室または第三者に損害を与えた場合には、速やかにその賠償責任を果たさねばなりません。']),
    ('第9条', '会員資格の喪失', ['本教室は、会員が次の各号の一つに該当すると認めた場合は、会員資格の一時停止または除名をすることができます。',
                          ['本教室の定める会費・諸費用につき、2ヶ月以上滞納したとき。（除名の場合、除名以前の会費・諸費用は全て納入していただきます。）',
                           '本教室の所有物を故意に毀損したとき。', '本規約、その他本教室が定める規約に違反したとき。',
                           '本教室の名誉、信用を毀損し、または秩序を乱したとき。', '入会書類に虚偽を記載したことが判明したとき。',
                           '会員として品位を損なうと認められる非行があったとき。', '伝染病等他人に伝染・感染するおそれのある疾病に罹患したとき。',
                           '本教室の合理的な指示・指導に従わないとき。', 'その他本教室が、社会通念に照らし、本教室会員としてふさわしくないと認めたとき。']]),
    ('第10条', '教室運営', ['本教室は基本的に本教室が指定した講師陣にて授業を行いますが、講師の急病や不慮の事故などの止むを得ない事由により、代行講師への変更や教室休講になる場合があります。']),
    ('第11条', '傷害事故', ['授業受講中の傷害について授業中、講師の指示を無視した行動、また授業時間外の自主練習や遊びの中での事故の責任は負いかねます。']),
    ('第12条', '料金の変更', ['本教室は、本規約に基づいて会員が負担すべき諸費用を、社会情勢・経済状況の変動等を参考にして改定することができます。この場合、本教室は改定日の1ヶ月以上前までに本ホームページや連絡ツールにて会員に告知するものとします。']),
    ('第13条', '会場の変更', ['本教室は天候など必要に応じて会場の変更を行うことができます。変更の際は事前に連絡ツールなどで連絡いたします。']),
    ('第14条', '会場のアウトドア利用', ['会員とその家族は授業前後の時間、また本教室が定めた日の中でアウトドア利用ができます。利用する際は前日17時までに本教室へ連絡ツールにて事前連絡を必ず行うこと。']),
]
FIRE = ['焚き火やBBQなど火を扱う際は、周囲の枯葉などを除去し、焚き火台などを使用して直火は避け、延焼を防ぐ手立てを必ず講じてください。また、使用した薪、灰はきれいに始末して他利用者の迷惑にならないよう配慮ください。',
        'ゴミは燃やさないでください。',
        '火を取り扱う際は立木から離れた場所で行ってください。木の根などが燃焼すると腐食の原因になる場合があります。',
        '近くに水を用意し、危険な場合にはすぐに消火できる状態で焚き火を行ってください。',
        '火を使用している間は目を離さないでください。',
        '枯葉を使用しての焚き付けは枯葉が舞い上がると大変危険ですのでおやめください。',
        '乾燥注意報が発令されている時や強風の際は、火災の危険が高まりますので焚き火は極力お控えください。',
        '大量の薪や枝を燃やしたり、ガソリンなどの危険物を火に入れるようなことはおやめください。',
        '必要な手立てが講じられていない場合、会員除名する場合があります。',
        '万一、故意・重過失によって火災等を引き起こした場合には、損害賠償を負担していただきます。']


def paras(items, ordered=True):
    out = []
    for it in items:
        if isinstance(it, list):
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag} class="doc-list">' + ''.join(f'<li>{x}</li>' for x in it) + f'</{tag}>')
        else:
            out.append(f'<p>{it}</p>')
    return '\n          '.join(out)


toc = ''.join(f'<a href="#a{i}">{n}<small>{t}</small></a>' for i, (n, t, _) in enumerate(ARTS, 1)) + '<a href="#fire">火の取り扱い</a><a href="#fusoku">附則</a>'
arts = '\n'.join(f'''        <article class="art" id="a{i}">
          <h2><span class="art-no">{n}</span>{t}</h2>
          {paras(body)}
        </article>''' for i, (n, t, body) in enumerate(ARTS, 1))
kiyaku = f'''      <p class="doc-intro reveal">本利用規約（以下、「本規約」といいます）は、サイエンス里山ラボ宗像（以下、「運営者」といいます）が運営する教室（以下、「本教室」といいます）の利用条件を定めるものです。本教室を利用する場合、本規約に同意する必要があります。</p>
      <nav class="toc reveal" aria-label="目次">{toc}</nav>
      <section class="doc doc-arts reveal">
{arts}
      </section>
      <section class="fire-box reveal" id="fire">
        <h2><span class="h-ic" data-icon="fire"></span>火の取り扱いに関して<small>第14条　会場のアウトドア利用</small></h2>
        <ul class="check-list">{''.join(f'<li>{x}</li>' for x in FIRE)}</ul>
      </section>
      <section class="doc reveal" id="fusoku">
        <h2><span class="h-ic" data-icon="rule"></span>附則</h2>
        <p>本規約の改定及び変更は本教室により為されるものとし、その効力は当該改定及び変更時に在籍する全ての会員に及ぶものとします。なお、本教室が本規約の改定及び変更を行うときは改定日の原則1週間前までにその内容を本ホームページや連絡ツールにて会員に告知するものとします。</p>
        <ul class="dates"><li><span>施行</span>2024年10月20日</li><li><span>改定</span>2024年12月16日</li><li><span>改定</span>2025年4月2日</li></ul>
      </section>
'''
write('kaiinkiyaku', page('kaiinkiyaku', '会員規約', 'RULES', 'rule', 'サイエンス里山ラボ宗像 利用規約', 'teal-1', kiyaku,
                          'サイエンス里山ラボ宗像の会員規約（利用規約）。入会・会費・欠席・会場のアウトドア利用や火の取り扱いについて。'))

# ───────── 個人情報の取り扱い ─────────
SECS = [
    ('個人情報の取得について', ['当サイトでは、参加者から以下の個人情報を取得いたします。',
                         ['氏名', '連絡先（メールアドレス、電話番号など）', '住所', '生年月日', '性別', '参加理由・意見等のイベント参加に関連する情報'],
                         'これらの個人情報は、適切に管理し、以下の目的にのみ使用いたします。']),
    ('個人情報の利用目的', ['取得した個人情報は、以下の目的で利用させていただきます。',
                       ['授業に関する連絡・案内', '緊急時の対応', '授業参加に関する統計的な分析', '授業後のアンケート依頼や今後のイベント情報提供']]),
    ('個人情報の第三者提供について', ['取得した個人情報は、以下の場合を除き、第三者に提供することはありません。',
                            ['参加者の同意がある場合', '法令に基づく場合', '人の生命、身体または財産の保護のために必要であり、本人の同意を得ることが困難な場合']]),
    ('個人情報の管理', ['本教室では、参加者の個人情報を適切に管理し、不正アクセス、紛失、破壊、改ざん、漏えいなどを防止するために、必要な措置を講じます。']),
    ('個人情報の開示・訂正・削除について', ['参加者は、本教室に提供した自身の個人情報について、開示、訂正、削除を希望する場合は、以下の問い合わせ先までご連絡ください。合理的な範囲で速やかに対応いたします。']),
    ('問い合わせ先', ['個人情報に関するお問い合わせは、以下の連絡先までご連絡ください。',
                   '<span class="contact-line"><b>サイエンス里山ラボ宗像［担当：谷口］</b><br>サイエンス里山ラボの公式LINEのチャットにてご連絡ください。</span>',
                   '<span class="mail-box"><span class="mail-lead">LINEをお使いでない方はメールでも</span><img class="mail-img" src="../assets/img/contact-mail.webp" alt="メールアドレス（画像）" width="889" height="76"><span class="mail-btns"><button class="link-pill js-mail-send" type="button">メールを送る</button><button class="link-pill js-mail-copy" type="button">アドレスをコピー</button></span></span>']),
    ('規約の変更について', ['本規約は、法令の変更や当サイトの運営方針の変更に伴い、予告なく改定されることがあります。改定後の規約は公式ホームページ等でお知らせします。']),
    ('アクセス解析ツールについて', ['当サイトでは、サイトをより使いやすくするために、Google社のアクセス解析ツール「Googleアナリティクス」を利用しています。Googleアナリティクスはデータの収集のためにCookieを使用しています。このデータは匿名で収集されており、個人を特定するものではありません。',
                           'この機能はお使いのブラウザの設定でCookieを無効にすることで、収集を拒否することができます。くわしくは<a href="https://marketingplatform.google.com/about/analytics/terms/jp/" target="_blank" rel="noopener">Googleアナリティクス利用規約</a>、<a href="https://policies.google.com/technologies/partner-sites?hl=ja" target="_blank" rel="noopener">Googleのポリシーと規約</a>をご覧ください。']),
]
secs = '\n'.join(f'''        <article class="art" id="s{i}">
          <h2><span class="art-no">{i}</span>{t}</h2>
          {paras(body, ordered=False)}
        </article>''' for i, (t, body) in enumerate(SECS, 1))
toc2 = ''.join(f'<a href="#s{i}">{i}<small>{t}</small></a>' for i, (t, _) in enumerate(SECS, 1))
kojin = f'''      <p class="doc-intro reveal">本規約は、サイエンス里山ラボ宗像が運営する教室（以下、「本教室」といいます）の個人情報に関する規約です。</p>
      <nav class="toc reveal" aria-label="目次">{toc2}</nav>
      <section class="doc doc-arts reveal">
{secs}
      </section>
'''
write('kojinjoho', page('kojinjoho', '個人情報の取り扱い', 'PRIVACY', 'shield', '個人情報の取扱いに関する規約', 'pink-3', kojin,
                        'サイエンス里山ラボ宗像の個人情報の取り扱い（取得・利用目的・第三者提供・管理・問い合わせ先・アクセス解析）。'))

# ───────── お知らせ（中身は data/news.json から page.js が表示する） ─────────
news = '''      <div class="news-filter reveal" id="newsFilter" hidden></div>
      <ul class="news-list news-page reveal" id="newsPage"><li class="news-loading">よみこみ中…</li></ul>
'''
write('news', page('news', 'お知らせ', 'NEWS', 'news', 'サイエンス里山ラボ宗像からのお知らせ・イベント情報', 'teal-2', news,
                   'サイエンス里山ラボ宗像からのお知らせ一覧。授業・イベント・料金などの最新情報。'))

# ───────── ゲーム紹介：むなかた虫とり日記 ─────────
MUSHI_URL = 'https://tani0920.github.io/mushitori-rpg/'
GI = '../assets/img/games/mushitori/'
PLACES = [
    ('赤間の町', '家と虫具店。ここからスタート', 'モンシロチョウ、アブラゼミ'),
    ('赤間の田んぼ', '', 'バッタ、ナツアカネ、オオカマキリ'),
    ('釣川の河原', '', 'トンボ、アメンボ、夜はゲンジボタル'),
    ('宗像大社の森', 'スニーカーが必要', 'セミ、クワガタ、カブトムシ、タマムシ'),
    ('さつき松原', 'スニーカーが必要', 'クマゼミ、ハンミョウ、オニヤンマ'),
    ('城山', '登山ぐつが必要', 'ミヤマクワガタ、オオムラサキ、オオスズメバチ'),
    ('大島', '神湊で乗船チケットを買う', 'カラスアゲハ、オオクワガタ、伝説の虫…？'),
]
places = '\n'.join(f'''          <li class="g-place"><b>{n}</b>{f'<small>{c}</small>' if c else ''}<span>{b}</span></li>''' for n, c, b in PLACES)
STEPS = [
    ('map', '行き先をえらぶ', '朝6時に家を出て、宗像市マップから行きたい場所へ。朝・昼・夕方・夜で、出てくる虫がかわります。'),
    ('net', '弱らせて、あみでキャッチ', '草むらを歩くと虫が出てきます。HPをへらしすぎるとにげちゃうので、ちょうどいいところで「つかまえる」！'),
    ('shop', '道具をそろえる', 'つかまえた虫を虫具店で売って、もっといいあみや虫かご、遠くへ行けるくつを買おう。'),
    ('book', '図鑑をうめる', '夜9時には家に帰ってねる。14日目がおわったら、自由研究の昆虫図鑑を二学期に発表！'),
]
steps = '\n'.join(f'''          <li class="g-step reveal"><span class="s-no">{i}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (_, t, d) in enumerate(STEPS, 1))
SHOTS = [('s_field', '宗像の7つの場所で虫とり'), ('s_battle', 'そーっとキャッチ'), ('s_sumo', '虫ずもうで勝負'),
         ('s_both', 'タブレットでもスマホでも'), ('s_rest', '30分でひと休み')]
shots = '\n'.join(f'''          <figure class="g-shot"><img src="{GI}{f}.webp" alt="{c}" width="600" height="678" loading="lazy"><figcaption>{c}</figcaption></figure>''' for f, c in SHOTS)
REAL = [
    ('r_tablet', 'お子さまはタブレットで', '画面が大きいので、ボタンが押しやすく、ドット絵の虫もよく見えます。'),
    ('r_photo', 'スマホで本物の虫をとると、ゲームの特典', '外で昆虫採集をしているときに、スマホで本物の虫を撮影すると、AIが虫を見分けて、ゲームの中でどんぐりや道具などの特典がもらえます。'),
    ('r_card', '虫とりカードを、親のスマホから子どものタブレットへ', 'とった虫は「虫とりカード」になります。おうちの方のスマホからお子さまのタブレットへ送って、ゲームで開けて集められます。外あそびの楽しみが、家に帰ってからも続きます。'),
    ('r_dex', '図鑑は、ほんものの昆虫採集の参考に', '図鑑にのる虫には、実際の昆虫の情報（なかま・大きさ・いる場所・見られる時期・飼いかた）が入っています。虫とりに出かける前の下調べにも。'),
]
real = '\n'.join(f'''          <li class="g-point reveal"><img src="{GI}{f}.webp" alt="" width="600" height="678" loading="lazy"><div><h3>{t}</h3><p>{d}</p></div></li>''' for f, t, d in REAL)

mushitori = f'''      <section class="g-hero reveal">
        <figure class="g-hero-art"><img src="{GI}hero_tanbo.webp" alt="田んぼの向こうに海と大島が見える、夏の宗像" width="600" height="750"></figure>
        <div class="g-hero-text">
          <img class="g-logo" src="{GI}10_logo.webp" alt="むなかた虫とり日記" width="640" height="285">
          <p class="g-catch">宗像が舞台の<br>夏休み虫とりRPG</p>
          <ul class="g-tags"><li>無料</li><li>ダウンロードなし</li><li>お子さまはタブレットで</li></ul>
          <p class="g-play"><a class="btn btn-main" href="{MUSHI_URL}" target="_blank" rel="noopener">あそぶ ▶</a></p>
          <p class="g-note">iPhone・iPad は Safari で開いて「共有 → ホーム画面に追加」すると、アプリのように全画面で遊べます。</p>
        </div>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="play"></span>どんなゲーム？</h2>
        <p>夏休みのさいごの14日間（8月13日〜26日）。宿題を早めに終わらせた「ぼく」が、宗像じゅうを歩いて虫とりをします。つかまえた虫で<strong>自由研究の昆虫図鑑</strong>をつくって、二学期の発表でみんなをおどろかせよう！</p>
        <p>なつかしいドット絵のRPGです。宗像の田んぼや河原、宗像大社の森、大島など、身近な場所が舞台になっています。</p>
      </section>

      <section class="doc g-real reveal">
        <h2><span class="h-ic" data-icon="mountain"></span>ゲームから、本物の虫とりへ</h2>
        <figure class="g-real-art"><img src="{GI}r_family.webp?v=2" alt="お父さんと子どもが、木にとまったカブトムシをスマホで撮影している" width="900" height="767" loading="lazy"></figure>
        <p>ゲームの中だけでなく、外での昆虫採集もいっしょに楽しめるしかけがあります。おうちではタブレットでゲーム、外ではスマホで本物の虫とり。</p>
        <ul class="g-points">
{real}
        </ul>
        <p class="g-small">※ゲームの中で虫が出てくる場所は、ゲーム用に決めたものです。実際にその虫が見られる場所や時期とはちがうことがあります。</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="join"></span>あそびかた</h2>
        <ol class="g-steps">
{steps}
        </ol>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="pin"></span>宗像の7つの場所で虫とり</h2>
        <ul class="g-places">
{places}
        </ul>
        <p class="g-small">※ゲームに出てくる場所と虫の組み合わせはゲーム用のもので、実際にその場所にいる虫とはかぎりません。</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="classes"></span>31しゅるいの虫</h2>
        <figure class="g-bugs"><img src="{GI}09_bugs31_silhouette.webp" alt="ゲームに出てくる31しゅるいの虫のシルエット" width="720" height="720" loading="lazy"><figcaption>この虫、なーんだ？ どの虫かは、つかまえてからのおたのしみ！</figcaption></figure>
        <p>カブトムシ、クワガタ、セミ、トンボ、チョウ…。レア度★5の虫も。宗像の野山で見られる虫がたくさん出てきます。</p>
        <p class="g-small">※1しゅるいだけ、このゲームのための架空の昆虫がいます。ほかの30しゅるいは実在する昆虫です。</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="star"></span>虫ずもう と エンディング</h2>
        <p>近所の子と、つかまえた虫で<strong>虫ずもう</strong>。甲虫・チョウ・トンボ…タイプで作戦がかわります。</p>
        <p>エンディングは6しゅるい。図鑑のできばえで、二学期の発表の結果がかわります。めざせ「宗像市長賞」！</p>
      </section>

      <section class="doc reveal">
        <h2><span class="h-ic" data-icon="camera"></span>ゲームの画面</h2>
        <div class="g-shots">
{shots}
        </div>
      </section>

      <section class="doc g-family reveal">
        <h2><span class="h-ic" data-icon="family"></span>おうちの方へ</h2>
        <ul class="g-list">
          <li>30分あそぶと、10分の休けいになります。決めた時間の5分前に町のチャイム、1分前にヒグラシが鳴ってお知らせします。時間はおうちの方が決められます。</li>
          <li>虫の写真は、スマホ・タブレットの中だけでAIが判定します。写真が外に送られることはありません。</li>
          <li>位置情報は「スタンプの場所の近くか」を調べるだけで、保存も送信もしません。スタンプの前に「おうちの人といっしょに来た？」と確認します。</li>
          <li>ハチなど危ない虫の写真には、ごほうびが出ません。危ない虫には近づかないように声をかけてあげてください。</li>
          <li>ゲームのセーブは、遊んでいる端末のブラウザに保存されます。</li>
        </ul>
        <p class="g-play"><a class="btn btn-main" href="{MUSHI_URL}" target="_blank" rel="noopener">あそぶ ▶</a></p>
      </section>
'''
write('mushitori', page('mushitori', 'むなかた虫とり日記', 'GAME', 'play', '宗像が舞台の 夏休み虫とりRPG', 'teal-4', mushitori,
                        '宗像が舞台の夏休み虫とりRPG「むなかた虫とり日記」。宗像じゅうで31しゅるいの虫をつかまえて、自由研究の昆虫図鑑を完成させよう。スマホ・タブレットで無料、ダウンロードなし。'))

# 以前の Wix のアドレス（/blog）からお知らせページへ
blog = os.path.join(ROOT, 'blog')
os.makedirs(blog, exist_ok=True)
open(os.path.join(blog, 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>お知らせ｜サイエンス里山ラボ宗像</title>'
    '<link rel="canonical" href="https://www.sciencemunakata.tech/news/"><meta http-equiv="refresh" content="0; url=../news/">'
    '</head><body><p><a href="../news/">お知らせのページはこちらにうつりました</a></p></body></html>\n')

# 以前の Wix のアドレス（/代表自己紹介）から新しいページへ
old = os.path.join(ROOT, '代表自己紹介')
os.makedirs(old, exist_ok=True)
open(os.path.join(old, 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>代表あいさつ｜サイエンス里山ラボ宗像</title>'
    '<link rel="canonical" href="https://www.sciencemunakata.tech/daihyo/"><meta http-equiv="refresh" content="0; url=../daihyo/">'
    '</head><body><p><a href="../daihyo/">代表あいさつのページはこちらにうつりました</a></p></body></html>\n')
print('書き出し 代表自己紹介 → daihyo へ転送')
