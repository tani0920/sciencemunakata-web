# サイエンス里山ラボ宗像 WEBサイト（リニューアル版）

Wix から GitHub Pages へ移すための新しいサイト。HTML／CSS／JS だけで動く（PHP・WordPress なし）。

## フォルダ

| 場所 | 中身 |
|---|---|
| `index.html` | トップページ（1ページにすべてのセクション） |
| `assets/css/style.css` | デザイン（色・フォント・アニメーション） |
| `assets/js/main.js` | `data/` を読み込んで、授業・先生・お知らせ・動画を表示する |
| `assets/img/chara/` | ロゴのキャラクター 5ポーズ × 3色（青 blue／水色 teal／ピンク pink） |
| `data/classes.json` | 授業（日付が過ぎると自動で「おわり」になる。`status: "中止"` で中止表示） |
| `data/teachers.json` | 先生（`photo` に画像パスを入れると写真が出る） |
| `data/news.json` | お知らせ（`date`・`category`・`title`・`body`（空行で段落）・`images`・`links`）。トップには新しい3件、`news/` にぜんぶ表示。写真は `assets/img/news/` |
| `data/videos.json` | 授業以外の動画（授業の動画は `classes.json` の `videoId` に入れる） |
| `data/site.json` | LINE（申し込み・お問い合わせはLINEに一本化）・SNS・ヒーロー写真・ゲームの一覧・GA測定ID |

| `assets/img/classes/` | 授業の写真（`{授業id}.webp` が表紙 800×600、`-2`,`-3` は「授業のようす」用） |
| `assets/img/teachers/` | 先生の写真（360×360） |

授業のアイキャッチ：`eyecatch`（LINE・Instagram告知のタイトル入り画像。`{授業id}-eye.webp` 640×800 の縦長 4:5＝Instagramの縦位置。これから作る告知画像も 4:5（1080×1350）で作れば、そのまま使える。9:16 は上下を少し切る、正方形はぼかした背景で4:5に収める）。

ヒーローの写真：`site.json` の `hero`（5秒ごとに切り替わる。`assets/img/hero/` に 1200×960）。ABOUTの4つの写真は `assets/img/about/1〜4.webp`。カード・つぎの授業・詳細画面の上に使う。

SNS：`site.json` の `sns`。URLが空のものは表示しない（TikTokを始めたら `url` を入れるだけでメニュー・フッター・Instagramの帯の下に出る）。Instagramは「授業のようす」の下に大きな帯で出す。

授業データの写真まわり：`photo`（表紙）、`photoType`（`photo`＝実際の写真／`illust`＝告知用イラスト。イラストには「イメージ」と小さく表示し、流れる写真ギャラリーには出さない）、`gallery`（詳細画面に出す追加の写真）。写真がない授業はジャンルのアイコンを表示する。

写真の元：`授業の記録と動画/サムネール/` と `授業の記録と動画/<日付>…/` の静止画・当日写真、先生は `03企画/各授業プログラム/`・`04制作/000_sozai/` など。瀧下先生の写真は Wix のサイトから（許可済み）。

ふりがな：`data/ruby.json`（ことば → よみ）。小学1〜3年で習わない漢字に、子ども向けの部分（ヒーロー・見出し・メニュー・授業のタイトルと内容・ゲーム）だけ自動で付く。料金や先生プロフィールなど保護者向けの部分には付けない。新しい授業で4年生以上の漢字を使ったら、ここに1行足す。

素材の出どころ：キャラとロゴは `04制作/ロゴ/☆サイエンス里山ラボ宗像_ロゴイラスト_納品データ.ai` から切り出し。

## 下のページ（代表あいさつ・会員規約・個人情報の取り扱い）

- `news/`（お知らせ一覧。中身は `data/news.json` から自動で表示）・`daihyo/`・`kaiinkiyaku/`・`kojinjoho/` の `index.html`。昔の `/blog` は `news/` へ転送。アドレスは Wix のときと同じ `/kaiinkiyaku`・`/kojinjoho`（代表は `/daihyo/`。昔の `/代表自己紹介` は自動で転送）。
- 文章は `_tools/build_pages.py` に書いてある。直したら `python3 _tools/build_pages.py` で3ページを書き出し直す（ヘッダー・フッターもトップとそろう）。
- 共通の部品：`assets/js/icons.js`（アイコン。トップと共通）、`assets/js/page.js`（メニュー・SNS・LINEボタン・目次）。

## 公開（GitHub Pages）と管理画面

- リポジトリ：https://github.com/tani0920/sciencemunakata-web （public、`main` ブランチの直下をそのまま公開）
- 仮のアドレス：https://tani0920.github.io/sciencemunakata-web/ （ドメイン切り替え後は https://www.sciencemunakata.tech/ ）
- このフォルダ（OneDrive）がそのまま作業コピー。`.git` は OneDrive の外（`~/.git-repos/sciencemunakata-web`）に置いている（同期で壊れないように）。`_tools/src/`（元の絵・差し替え前の写真）は公開しない（`.gitignore`）。
- **管理画面**：`/admin/`（https://tani0920.github.io/sciencemunakata-web/admin/ ）。お知らせ・授業・先生・動画をフォームで追加・編集・削除。写真は端末の中で縮小して WebP にする（お知らせ 長辺1400／授業の表紙 800×600・告知画像 640×800・ようす 長辺1200／先生 360×360）。保存すると画像と JSON を1回のコミットで GitHub に書き込み、1〜2分で反映。
  - カギ：GitHub の fine-grained personal access token（このリポジトリだけ・Contents を Read and write）。端末のブラウザ（localStorage）にだけ保存。
  - 保存のたびに最新の JSON を読み直してから変更を当てるので、2台で同時に触っても上書き事故は起きにくい。
  - **管理画面で更新すると、GitHub のほうが新しくなる。手元（このフォルダ）で直す前に必ず `git pull` する。**

## 更新のしかた（手で直すとき）

- 授業を足す：`classes.json` に1件追加。並び順は気にしなくてよい（日付で自動並べ替え）。
- 動画を足す：YouTube の動画ID（`watch?v=` のあとの11文字）を、その授業の `videoId` に入れる。**限定公開の道順動画は入れない。**

## 動かし方（手元で見る）

`fetch` で JSON を読むので、ファイルをダブルクリックでは表示されない。ローカルサーバーか GitHub Pages で開く。

## まだのこと

- [x] 更新用の管理画面（`/admin/`）
- [x] GitHub Pages に公開（仮のアドレス）
- [x] ドメイン切り替え（2026-11-10。ネームサーバーを Wix → ムームーDNS。下の「DNS」） → ムームードメインで sciencemunakata.tech を切り替え（Google のメール設定 MX・SPF・確認TXT・DMARC を残す）
- [ ] 里山ラボ サイエンスアプリ（会員コード・1つおためし）

## DNS（2026-11-10 に Wix からムームーDNSへ移した）
- ドメインの契約：ムームードメイン。ネームサーバー：ムームーDNS（dns01/dns02.muumuu-domain.com）。設定は「ムームーDNS → 変更 → カスタム設定 → 設定2」。
- 入っているレコード：A ×4（185.199.108〜111.153＝GitHub Pages）／CNAME www → tani0920.github.io／MX ×5（aspmx.l.google.com 10、alt1〜alt4 20〜50）／TXT SPF `v=spf1 include:_spf.google.com ~all`／TXT google-site-verification／TXT _dmarc `v=DMARC1; p=none`
- Wix のメルマガ用（s1・s2・sel1._domainkey、sg）は移していない（Wix のメール配信は使わない）。
- **メール（Google Workspace）は Wix 経由の契約（年払い、次回 2027-08-11）。Wix のプレミアムプランを止めても、こちらは解約しない。**
- GitHub Pages の独自ドメイン：www.sciencemunakata.tech（リポジトリの `CNAME` ファイル）。

## 公開するときにいっしょにやること（Google アナリティクス／サーチコンソール）

1. **Google アナリティクス（GA4）**：analytics.google.com でプロパティ「サイエンス里山ラボ宗像」を作り、ウェブのデータストリーム（`https://www.sciencemunakata.tech`）を追加 → 出てくる測定ID（`G-XXXXXXX`）を `data/site.json` の `gaId` に入れる。入れたら自動で計測が始まる（LINEボタンが押された回数も `line_click` として数える）。空のあいだは何も読み込まない。
2. **Google サーチコンソール**：「ドメイン」プロパティで `sciencemunakata.tech` を登録 → 表示される `google-site-verification=…` を、ムームードメインのDNSに TXT で追加（ドメインの切り替えと同じ画面で一緒にできる）。登録できたら `https://www.sciencemunakata.tech/sitemap.xml` を送信。
   - いまのDNSには Google Workspace 用の確認TXTがすでにある。同じGoogleアカウントなら、サーチコンソールの確認がそのまま通ることもある。
3. アクセス解析を入れるので、「個人情報の取り扱い」ページにアクセス解析（Cookie）を使う旨を一文足す。
4. `robots.txt`・`sitemap.xml`・`index.html` の canonical は `https://www.sciencemunakata.tech/` で用意済み（www なしにするなら3か所を直す）。

### アクセス解析の設定（2026-11-10 済み）
- プロパティ「サイエンス里山ラボ宗像 WEBサイト」（ID 563459915、測定ID G-EYWX2Y198N）。データ保持は14か月。サーチコンソール（sciencemunakata.tech）とリンク済み。
- サイトが送るイベント：`apply_class`（授業の「LINEで申し込む」。`class_title` に授業名 → カスタムディメンション「申し込みされた授業」）、`join_form`（入会フォーム）、`line_click`（友だち追加・問い合わせなどそのほかのLINEボタン）。
- キーイベント：`apply_class` と `join_form` を、最初のデータが届いたあと（管理 → イベント の一覧に出てから）☆でキーイベントにする。
- 運営側の閲覧は数えない：`?me=1` を付けてサイトを一度ひらく か 管理画面をひらいた端末は `traffic_type=internal` になり、データフィルタ「Internal Traffic」（有効）で除かれる。`?me=0` で解除。http→https に変わると端末の記憶が別になるので、https化のあとにもう一度 `?me=1` でひらく。
- LINEからのリンクには `utm_source=line`（リッチメニュー `utm_medium=richmenu`／プロフィール `utm_medium=profile`）を付けている。

## 絵のアイコン・3つの輪・「なぜ？」の吹き出し（GPTでつくった絵）
- 元の絵（白背景）は `_tools/src/gpt/` にある。アイコンは3×3で9個ずつ並んだシートが3枚。
- `python3 _tools/cut_gpt.py` で背景を透明にして切り出す。
  - アイコン → `assets/img/icons/<名前>.webp`
  - 3つの輪 → `assets/img/about-venn.webp`
  - 吹き出し → `assets/img/naze-bubble.webp`
  - OneDriveへの書き込みが止まるときは、別のフォルダを引数に渡して書き出し、あとでコピーする。
- どの名前を絵のアイコンにするかは `assets/js/icons.js` の `IMG_ICONS` で決める。ここにない名前は、今までどおり線画で表示される。
- 3つの輪の「自然・科学・アート」の札は画像ではなく文字。位置は style.css の `.vl-nature` などで調整する。
- 「なぜ？」は絵の吹き出しで出す。キャラクターをさわって出るほかの言葉（ふしぎ！など）は、今までどおり文字の吹き出し。

## 「授業ふうけい」の写真（scene）
- classes.json の `scene` に入れた写真が、「授業ふうけい」に流れる。なければ `photo` が使われる。
- `scene` は、授業の動画からその授業の内容に合う場面を切り出した 800×600 の画像（`assets/img/classes/<id>-scene.webp`）。

## SEO・OGP
- トップの `<head>` には、description、keywords、OGP（SNSでシェアしたときの表示）、構造化データ（JSON-LD）を入れている。
- 下のページの `<head>` は、`_tools/build_pages.py` がページごとの説明文で作る。
- OGP画像は `assets/img/ogp.jpg`（1200×630）。作り直すときは `python3 _tools/make_ogp.py` を実行する。フォントはMacに入っているG丸ゴを使う。
- 「里山ラボって？」の吹き出しは、形だけを左右反転したもの（文字はそのまま）。`python3 _tools/flip_bubble.py` で作る。
- 公開したあと、Facebookのシェアデバッガーなどで表示を確かめる。
- 授業の詳細の「授業のようす」には `shots`（動画から切り出した写真を3枚以上）を出す。`shots` がない授業は、これまでの `photo` / `gallery` を出す。
- 授業カードの画像は、告知用のアイキャッチ（`eyecatch`）のまま。

## ヒーローの写真を差し替えるとき
- `assets/img/hero/1〜5.webp`（1200×960・5:4）を置きかえ、`data/site.json` の `hero[].alt` も直す
- 同じファイル名だとブラウザが古い画像を出すので、`hero[].src` の末尾の `?v=…` を新しい日時にする（例 `assets/img/hero/5.webp?v=202611101040`）
- 写真ごとに見せる位置を変えたいときは `hero[].pos`（例 `"50% 25%"`）。楕円で顔や手元が切れるときに使う
- 前の写真は `_tools/src/hero_old/`、ABOUT の写真は `_tools/src/about_old/` に保管

## ゲームの紹介ページ（あそぶ・まなぶ）
- `data/site.json` の `games[].page` に下層ページのアドレス（例 `mushitori/`）を書くと、カードに「ゲームの内容」ボタンが出る
- ページの中身は `_tools/build_pages.py` の「ゲーム紹介：むなかた虫とり日記」に書いてある。新しいゲームを出すときは、ここをまねて追加し `python3 _tools/build_pages.py`
- 画像は `assets/img/games/mushitori/`（ゲームの `sns/screens/` のスクショを 420px 幅に縮めたもの）。`sitemap.xml` にも追加する
