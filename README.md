# plr-public

PLR（Personal Life Repository）の公開する資料です。PLR の系のオントロジーと、AI 用のプロンプトを置いています。

## 中身

```
ontology/Ontology.xlsx            系のオントロジー（正本）。シートは1枚
ontology/Ontology.csv             Ontology.xlsx を CSV にしたもの（差分を読むため）
ontology/Profile.xlsx             プロフィールのオントロジー（人・氏名・住所・健康など。正本）。シートは1枚
ontology/Profile.csv              Profile.xlsx を CSV にしたもの
ontology/spreadsheet_format.md    スプレッドシートによるオントロジーとスタイルシートの書き方
prompts/GDdef.md                  グラフ文書の定義（ノードと関係の種類）
prompts/GDconv.md                 文章をグラフ文書に変換する手順
prompts/GDgen.md                  目的（問い・課題・相談など）に沿ってグラフ文書を作る手順
prompts/GDmod.txt                 グラフ文書に新しいノードとリンクを足して問いに答える指示
prompts/TEXTgen.txt               グラフ文書と検索結果をもとに問いに文章で答える指示
tools/xlsx_to_csv.py              xlsx の最初のシートを CSV にする
```

## オントロジー

`ontology/Ontology.xlsx`（系のオントロジー）と `ontology/Profile.xlsx`（プロフィールのオントロジー）が正本です。

ダウンロードせずに見るには、[ontology/README.md](ontology/README.md) のリンクから開きます。

### 書き方

スプレッドシートでオントロジーとスタイルシートを書く書き方は、`ontology/spreadsheet_format.md` にあります。

- クラス・属性・データタイプ・ラベルの書き方、オントロジーの限定、制約、タイムラインなどのスタイルシートを、構文規則と例で定めている
- `Ontology.xlsx` の最初のセルが指している Google ドキュメントを Markdown にしたものである
- 元の文書では、未実装の部分を青字で示していた。Markdown では色が失われているので、未実装かどうかは、変換した結果（CI の成果物）で確かめる

### 直すとき

1. `ontology/` の xlsx を直す
2. CSV を作り直す：`python3 tools/xlsx_to_csv.py ontology/Ontology.xlsx > ontology/Ontology.csv`（Profile も同じ）
3. 両方をコミットして、プルリクエストを出す

プルリクエストでは、CI が次を確かめます（`.github/workflows/check.yml`）。

- 各 CSV が xlsx から作ったものと同じか
- [osspublish](https://gitlab.com/assemblogue/osspublish) の `cto.pl`・`cts.pl` で JSON-LD に変換できるか。変換した JSON-LD は、CI の成果物（ontology-jsonld）としてダウンロードできる

### PLR に配置する

osspublish の `osscon-all.jar` で配置します（使い方は osspublish の readme.md）。

```
java -jar osscon-all.jar ontology/Ontology.xlsx
java -jar osscon-all.jar ontology/Profile.xlsx
```

配置するのは、タグを付けたコミットの xlsx にします。

## プロンプト

`prompts/` のプロンプトは、グラフ文書（ノードと、種類の付いたリンクで文章の内容を表すもの）を扱う AI に渡すものです。`GDdef.md` が定義で、ほかはそれと一緒に渡します。

## ライセンス

[CC BY 4.0](LICENSE)（Creative Commons Attribution 4.0 International）
