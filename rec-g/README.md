# 🥚 REC-G｜RSS Egg Collection Garden

あちこちのSNSやブログで産んだ卵（記事・投稿）を、一つの庭に集める仕組み。
記事は引っ越さない。それぞれの場所に置いたまま、**表紙と目次だけ**をここに並べる。

人が書くのは、テキスト二枚だけ。

| ファイル | 書くこと |
|---|---|
| `eggs.txt` | 卵の一覧。ふだん見ているページのURLを一行に一つ |
| `shelves.txt` | 棚割り。どの卵をどの棚に並べるか（なくてもよい） |

あとは仕入れ係（GitHub Actions）が一日二回、卵を集めて `garden.json` と `feed.xml` を作る。
ページ（`index.html`）は、新着順・棚ごと・ぜんぶ（題名順）の三つの引き方で見せる。

## はじめかた

1. このリポジトリの「Use this template」→「Create a new repository」で写す（公開 Public にする）
2. 写した先の Settings → Pages で、Branch を `main`・`/ (root)` にして Save
3. `eggs.txt` を開いて鉛筆マークで編集し、自分のページのURLを書いて「Commit changes」
4. Actions タブで「Collect eggs」が動き終わったら、`https://あなたの名前.github.io/リポジトリ名/` に庭ができている

棚を分けたくなったら `shelves.txt` を同じように書き換える。それだけ。

## 自動で RSS を見つける場所

note（アカウント・マガジン）、Bluesky、Medium、Substack は住所から直接。
はてなブログ、YouTube、WordPress など、ページに RSS の印があるところはページから探す。
X と Instagram は RSS を出していないので、集められない。

## 巣立ち

この庭の本体はテキスト二枚。どこへ引っ越すときも、二枚を持って出ればいい。
CHIC TEC の私書箱で温めた庭も、巣立つときは二枚を自分の REC-G に写す。

---
REC-G は [DyXis](https://ittekiou.github.io/dyxis/) の仲間。文章は CC BY-SA 4.0、コードは MIT。
