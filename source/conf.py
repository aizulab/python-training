# Sphinx の設定ファイル。
# See: https://www.sphinx-doc.org/en/master/usage/configuration.html

project = 'Python 研修'
author = 's.suzuka'

# Copyright を表示しない
html_show_copyright = False

# 言語設定
language = 'ja'

# 無視するファイルやディレクトリの設定
exclude_patterns = []

# HTML 出力時のテーマ
html_theme = 'alabaster'

# 拡張モジュールの設定
extensions = ['sphinxcontrib.trimblank']

# sphinxcontrib.trimblank 拡張モジュールの設定
# HTML 出力の場合に日本語と半角英数字の間の空白を維持する
trimblank_keep_alnum_blank = ['html', 'singlehtml']