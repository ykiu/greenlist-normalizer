# Green List Normalizer

[Green List](http://www.rdplants.org/gl/) を json 形式に整形し、オプショナルで Species IO [開発中] に取り込みます。

## 変換前

これが:

|ID20160207|雑種・品種|新リスト和名|和名異名|GreenList学名|APG科番号|APG科和名|APG科名|固有|新エングラー科和名|
|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|
|1039.0||ジュンサイ||Brasenia schreberi J.F.Gmel.|3.0|ジュンサイ科|Cabombaceae||スイレン科|
|1040.0||オニバス||Euryale ferox Salisb.|4.0|スイレン科|Nymphaeaceae||スイレン科|
|1041.0||コウホネ||Nuphar japonica DC.|4.0|スイレン科|Nymphaeaceae||スイレン科|

## 変換後

こうなる:

### taxa.json

```json
{
  "taxa": [
    {
      "path": "/cabombaceae/",
      "sort_key": 0,
      "common_names": [{ "name": "ジュンサイ科" }],
      "scientific_names": [{ "name": "Cabombaceae" }]
    },
    {
      "path": "/cabombaceae/brasenia/",
      "sort_key": 0,
      "common_names": [],
      "scientific_names": [{ "name": "Brasenia" }]
    },
    {
      "path": "/cabombaceae/brasenia/brasenia_schreberi/",
      "sort_key": 0,
      "common_names": [{ "name": "ジュンサイ" }],
      "scientific_names": [{ "name": "Brasenia schreberi J.F.Gmel." }]
    },
    {
      "path": "/nymphaeaceae/",
      "sort_key": 1,
      "common_names": [{ "name": "スイレン科" }],
      "scientific_names": [{ "name": "Nymphaeaceae" }]
    },
    {
      "path": "/nymphaeaceae/euryale/",
      "sort_key": 0,
      "common_names": [],
      "scientific_names": [{ "name": "Euryale" }]
    },
    {
      "path": "/nymphaeaceae/euryale/euryale_ferox/",
      "sort_key": 0,
      "common_names": [{ "name": "オニバス" }],
      "scientific_names": [{ "name": "Euryale ferox Salisb." }]
    },
    {
      "path": "/nymphaeaceae/nuphar/",
      "sort_key": 1,
      "common_names": [],
      "scientific_names": [{ "name": "Nuphar" }]
    },
    {
      "path": "/nymphaeaceae/nuphar/nuphar_japonica/",
      "sort_key": 0,
      "common_names": [{ "name": "コウホネ" }],
      "scientific_names": [{ "name": "Nuphar japonica DC." }]
    }
  ]
}
```

## 機能

- GreenList の CSV ファイルを JSON 形式に変換
- ファイルパス形式で階層構造を表現
    - 門 (シダ植物門、裸子植物門、被子植物門)、科、属、種 (種内分類を含む) ごとに階層が作られます。
- Species IO [開発中] へのアップロード。

## インストール

### 要件

下記のツール類は事前にインストールしてください。

- Git
- [Make](https://ja.wikipedia.org/wiki/Make)
- Python 3.7
- Pipenv

### 手順

上記要件が整っていることを確認した上で、コマンドラインで下記を実行してください。

```
$ git clone https://github.com/ykiu/greenlist-normalizer.git
```

## 使用方法

まず、Green List を Web からダウンロードします。

```
$ make downloads
```

次に、ダウンロードした Green List を整形します。

```
$ make normalizations
```

変換後のファイルは、`normalizations/` に生成されます。

変換後のファイルは Species IO にアップロードすることができます。

```
$ pipenv run python -c "import uploader; uploader.upload('https://species.appspot.com/rest/taxonomy_versions/', '<Taxonomy ID>', '<JWT>')"
```
