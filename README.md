# Python 研修

HTML 形式で閲覧できます: https://aizulab.github.io/python-training/

## 概要

[株式会社会津ラボ](https://www.aizulab.com/) において、社内研修に使用されている資料です。Python を利用して API サーバーを構築することを目標としています。

講義形式で使用されることを想定しているため、独習には少し難しいかもしれません。

## ビルド

[Sphinx](https://www.sphinx-doc.org) を利用して HTML 形式や EPUB 形式で出力できます。LaTeX 形式経由で PDF としても出力できます。

### 例: HTML 形式で出力

1. Sphinx をインストールし、`sphinx-build` コマンドが使える状態にする
2. 日本語対応（空白除去）のための拡張モジュール [sphinxcontrib-trimblank](https://pypi.org/project/sphinxcontrib-trimblank/) をインストールする
3. このリポジトリのルートディレクトリで `sphinx-build -M html source build` コマンドを実行
4. `build/html` ディレクトリに HTML 形式で出力されていることを確認（例えば、`index.html` を開いてみる）

Sphinx のインストール方法については https://www.sphinx-doc.org/ja/master/usage/installation.html などを参照してください。

## サンプルリポジトリ

まだありません。

## 練習問題の解答

（まだ）ありません。

## Contribution

誤りや不適切な内容の報告は、Issue を利用してください。

## ライセンス

[CC0-1.0](LICENSE)

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)
