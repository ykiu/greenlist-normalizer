# Green List Normalizer

[Green List](http://www.rdplants.org/gl/) を整形し、Species IO [開発中] に取り込みます。

## 変換前

これが:

|ID20160207|雑種・品種|新リスト和名|和名異名|GreenList学名|APG科番号|APG科和名|APG科名|固有|新エングラー科和名|
|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|
|1039.0||ジュンサイ||Brasenia schreberi J.F.Gmel.|3.0|ジュンサイ科|Cabombaceae||スイレン科|
|1040.0||オニバス||Euryale ferox Salisb.|4.0|スイレン科|Nymphaeaceae||スイレン科|
|1041.0||コウホネ||Nuphar japonica DC.|4.0|スイレン科|Nymphaeaceae||スイレン科|

## 変換後

こうなる:

### taxa.csv

|parent_key|key|sort_key|
|:-|:-|:-|
|plants|cabombaceae|0|
|cabombaceae|brasenia|0|
|brasenia|brasenia_schreberi|0|
|plants|nymphaeaceae|1|
|nymphaeaceae|euryale|0|
|euryale|euryale_ferox|0|
|nymphaeaceae|nuphar|1|
|nuphar|nuphar_japonica|0|

### common_names.csv

|taxon_key|name|
|:-|:-|
|cabombaceae|ジュンサイ科|
|brasenia_schreberi|ジュンサイ|
|nymphaeaceae|スイレン科|
|euryale_ferox|オニバス|
|nuphar_japonica|コウホネ|


### scientific_names.csv

|taxon_key|name|
|:-|:-|
|cabombaceae|Cabombaceae|
|brasenia|Brasenia|
|brasenia_schreberi|Brasenia schreberi J.F.Gmel.|
|nymphaeaceae|Nymphaeaceae|
|euryale|Euryale|
|euryale_ferox|Euryale ferox Salisb.|
|nuphar|Nuphar|
|nuphar_japonica|Nuphar japonica DC.|

## 機能

- 各分類群の URL-safe な ID を学名に基づいて自動生成。
    - e.g. Brasenia schreberi J.F.Gmel. -> brasenia_schreberi
- [隣接リスト方式](https://ja.wikipedia.org/wiki/%E9%9A%A3%E6%8E%A5%E3%83%AA%E3%82%B9%E3%83%88)で分類体系の木構造を表現。
    - 門 (シダ植物門、裸子植物門、被子植物門)、科、属、種 (種内分類を含む) がノード。
- 分類群と名前の一対多関係を[正規化](https://ja.wikipedia.org/wiki/%E9%96%A2%E4%BF%82%E3%81%AE%E6%AD%A3%E8%A6%8F%E5%8C%96)。
- Species IO へのアップロード。

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
$ make normalization
```

変換後のファイルは、`normalizations/` に生成されます。

最後に、変換後のファイルを Species IO にアップロードします。

```
$ pipenv run python -c "import uploader; uploader.upload('https://species.appspot.com/rest/taxonomy_versions/', '<User ID>', '<JWT>')"
```
