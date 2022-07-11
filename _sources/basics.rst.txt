========
基本文法
========

Python の基本文法について概説する。

コメント
========

Python のコメントは ``#`` で始まる。

.. code-block:: python3

   >>> x = 2  # x は 2 です

通常、上記のように ``#`` の前に文字がある場合は半角スペース２つ、
また ``#`` の後ろには半角スペース１つを入れる。

変数
====

変数の定義・変数への値の代入には、単に ``=`` を使う。
変数名には通常小文字のスネークケース (snake_case) を用いる。

.. code-block:: python3

   >>> some_value = 10
   >>> print(some_value)
   10

   >>> some_value = "Hello"
   >>> print(some_value)
   Hello

変数の定義には *型ヒント（型アノテーション）* を付けることもできる。

.. code-block:: python3

   >>> some_value: int = 10
   >>> print(some_value)
   10

   >>> some_value = "Hello"
   >>> print(some_value)
   Hello

上の例からもわかるように、型ヒントは単に「ヒント」であり、Python は基本的に実行時にはこれを無視する。
mypy 等の型チェッカーや VSCode 等の IDE などでは、この型ヒントを利用して静的型検査や自動補完を行うことができる。

.. note::

   mypy 等の型チェッカーは変数の型を推論してくれるため、
   通常変数に型ヒントをつけることは少ない。

   以下の例では、 ``some_value`` 変数の値が整数 ( ``int`` ) か文字列 ( ``str`` ) の
   どちらでもよいことを明示するために ``Union`` を使用して型ヒントを付けている。

   .. code-block:: python3

      from typing import Union  # Union の使用にはこの宣言が必要

      some_value: Union[int, str] = 10

      some_value = "Hello"

   なお、Python 3.10 からは ``Union`` の代わりに ``|`` が使える。

   .. code-block:: python3

      some_value: int | str = 10

      some_value = "Hello"

定数
====

変更不可能な定数のようなものを宣言する構文は存在しないが、
通例大文字のスネークケース (SNAKE_CASE) で宣言された変数は固定値として扱う。

型ヒントを利用する場合は、 ``Final`` を利用することで固定値であることを宣言できる
（繰り返すが、基本的に実行時には無視される）。

.. code-block:: python3

   from typing import Final  # Final の使用にはこの宣言が必要

   SOME_VALUE: Final[int] = 10

   SOME_VALUE = 11  # 実行はできるが、型チェッカーは文句を言うだろう

基本的な型
==========

Python の組み込み型のうち、基本的なものを紹介する。

- ``int``: 整数
- ``float``: 浮動小数点数
- ``str``: 文字列
- ``bytes``: バイト列
- ``bool``: 真偽値
- ``list``: リスト
- ``tuple``: タプル
- ``set``: 集合
- ``dict``: 辞書

なお、型は ``type()`` 組み込み関数で調べることができる。

.. code-block:: python3

   >>> x = 10
   >>> type(x)
   <class 'int'>

   >>> type("Hello")
   <class 'str'>

   >>> type([1,2,3])
   <class 'list'>

組み込み型の詳細については `組み込み型についてのドキュメント`_ を参照されたい。

.. _`組み込み型についてのドキュメント`: https://docs.python.org/ja/3/library/stdtypes.html

int と float
------------

``int`` は整数、 ``float`` は浮動小数点数を表す。

``float`` は通常倍精度であり、つまり C 言語での ``double`` に相当する。

.. code-block:: python3

   >>> x: int = 10
   >>> y: float = 3.1

   >>> x + y
   13.1
   >>> x - y
   6.9
   >>> x * y
   31.0
   >>> x / y
   3.225806451612903
   >>> x // y  # 結果が整数になる除算
   3.0
   >>> x % y  # 剰余
   0.6999999999999997
   >>> x ** y  # x の y 乗
   1258.9254117941675

   >>> x += 1  # ++, -- はない
   >>> x
   11

   >>> x >= 0
   True
   >>> 0 < x < 5  # (0 < x) and (x < 5) と同じ（但し x が１度のみ評価される）
   False

   # 2 進数、8 進数、16 進数
   >>> 0b11111111 == 0o377 == 0xFF == 255
   True

数値を扱う組み込み型には、他に複素数を扱う ``complex`` 型がある（練習問題を参照）。

str
---

``str`` は文字列型である。
文字列はシングルクォート ( ``'`` ) もしくはダブルクォート (``"``) で記述できる（文字列リテラル）。

.. code-block:: python3

   >>> s1: str = "Hello"
   >>> s2 = 'Hi'

   # "" の中では " を、'' の中では ' をエスケープする必要がある
   >>> "You'll say \"Now!\""
   'You\'ll say "Now!"'

   # 8 進数表記、16 進数表記
   >>> "\110\111" == "\x48\x49" == "HI" 
   True

   # 16 進数表記 (16 bit)、16 進数表記 (32 bit)
   >>> "\u0048\u0049" == "\U00000048\U00000049" == "HI" 
   True

三連引用符 ( ``'''`` または ``""""`` ) で囲まれた文字列リテラルは、複数行に跨って書くことができる。
この記法はよく docstring の記述にも用いられる（後述）。

.. code-block:: python3

   >>> ff = """𝑭𝑰𝑵𝑨𝑳𝑭𝑨𝑵𝑻
   ... 𝑨𝑺𝒀"""

   >>> ff
   '𝑭𝑰𝑵𝑨𝑳𝑭𝑨𝑵𝑻\n𝑨𝑺𝒀'

   >>> print(ff)
   𝑭𝑰𝑵𝑨𝑳𝑭𝑨𝑵𝑻
   𝑨𝑺𝒀

文字列リテラルの頭に ``f`` か ``F`` をつけるフォーマット済み文字列リテラル (f-string) を用いると、
文字列中に ``{}`` を用いて式を埋め込むこともできる。

.. code-block:: python3

   >>> from math import gamma
   >>> x_min = 1.4616321449683622

   >>> f"Γ({x_min}) ≈ {gamma(x_min)}"
   'Γ(1.4616321449683622) ≈ 0.8856031944108889'

この他にも f-string では様々な書式指定が可能である。
詳細については `Python チュートリアル 7. 入力と出力`_ 等を参照されたい。

.. _`Python チュートリアル 7. 入力と出力`: https://docs.python.org/ja/3.8/tutorial/inputoutput.html

bytes
-----

``bytes`` はバイト列を扱う型である。
文字列リテラルの頭に ``b`` をつけると bytes リテラルとなる。

.. code-block:: python3

   >>> b1: bytes = bytes([65, 66, 67, 68])
   >>> b2 = b'ABCD'
   >>> b3 = b"\x41\x42\x43\x44"

   >>> b1 == b2 == b3
   True

   >>> b1.hex()
   '41424344'

   >>> b1.decode()
   'ABCD'

他に可変なバイト列を扱う ``bytearray`` 型や、メモリビューを扱う ``memoryview`` 型がある。

bool
----

``bool`` は真偽値であり、 ``True`` か ``False`` である。大文字始まりなので注意。

.. code-block:: python3

   >>> b1: bool = True
   >>> b2 = False

   >>> not b1
   False
   >>> b1 and b2
   False
   >>> b1 or b2
   True

list と tuple
=============

TODO

set と dict
===========

TODO

制御構文
========

Python の制御構文は、コロン ( ``:`` ) とインデント（通常は半角スペース４文字）を用いるのが特徴である。

if 文
-----

.. code-block:: python3

   if x % 15 == 0:
       print("FizzBuzz")
   elif x % 3 == 0:
       print("Fizz")
   elif x % 5 == 0:
       print("Buzz")
   else:
       print(x)

while 文
--------

.. code-block:: python3

   x = 27

   while True:
       print(x)

       if x == 1:
           break

       if x % 2 == 0:
           x //= 2
           continue

       x = x * 3 + 1

for 文
------

``for`` 文は、シーケンス（例えばリストや文字列）に対して反復処理を行う。

.. code-block:: python3

   >>> for season in ["весна", "літо", "осінь", "зима"]:
   ...     print(season)
   ... 
   весна
   літо
   осінь
   зима

   >>> for season in "春夏秋冬":
   ...     print(season)
   ... 
   春
   夏
   秋
   冬


``range()`` 組み込み関数と共に用いることで、数列に対して反復処理を行うことができる。

.. code-block:: python3

   >>> for i in range(5):
   ...     print(i)
   ... 
   0
   1
   2
   3
   4

pass 文
-------

``pass`` 文は、何もしない。

例えば、Python では次のように本体のない関数を宣言することはできない。

.. code-block:: python3

   # NG: 本体が必要
   def let_it_go() -> None:

このような場合に ``pass`` 文を用いることができる。

.. code-block:: python3

   # OK
   def let_it_go() -> None:
      pass

また、 ``pass`` 文の代わりに Ellipsis ( ``...`` ) が用いられることもある。

.. code-block:: python3

   # OK
   def let_it_go() -> None:
      ...

.. note::

   後述する docstring を用いる場合は ``pass`` 等は不要になる。

   .. code-block:: python3

      # OK
      def let_it_go() -> None:
          """何もしません。"""

match 文
--------

Python 3.10 以降で使用可能。

.. code-block:: python3

   match TODO

``match`` 文の詳細な動作については、練習問題とする。

関数
====

関数名には通常スネークケース (snake_case) を用いる。

.. code-block:: python3

   def is_palindrome(s):
       return s == s[::-1]

型ヒントを書く場合、以下のようになる。

.. code-block:: python3

   def is_palindrome(s: str) -> bool:
       return s == s[::-1]

.. caution::

   mypy 等の型チェッカーは型ヒントのついていない関数については型チェックを行わず、
   また引数や戻り値の型推論もしてくれない（``Any`` 型等になる）ため、
   型ヒントを用いる場合、関数には常に型ヒントをつけるのがよい。

``return`` 文の引数に何も指定しなかった場合や、 
``return`` 文のない関数が正常に終了したときには ``None`` が返される。
そのため、このような場合戻り値の型ヒントは ``None`` となる。

.. code-block:: python3

   >>> def intone() -> None:
   ...     print("仏説摩訶般若波羅蜜多心経...")
   ... 
   >>> result = intone()
   仏説摩訶般若波羅蜜多心経...

   >>> result is None
   True

Docstring
---------

関数、クラス、モジュールの先頭には、文字列リテラルで説明文を記述できる (docstring)。

.. code-block:: python3

   def is_palindrome(s: str) -> bool:
       """文字列が回分なら True, そうでなければ False を返します。"""
       return s == s[::-1]

Docstring の内容は ``help()`` 組み込み関数を使用することでも閲覧できる。

.. code-block:: python3

   >>> def is_palindrome(s: str) -> bool:
   ...     """文字列が回分なら True, そうでなければ False を返します。"""
   ...     return s == s[::-1]
   ... 
   >>> help(is_palindrome)

   Help on function is_palindrome in module __main__:

   is_palindrome(s: str) -> bool
       文字列が回分なら True, そうでなければ False を返します。

.. note::

   公開する関数、クラス、モジュールに常にドキュメントを記述するのは良い習慣である。

   Docstring には自由に文字列を記述できるが、 
   reStructuredText スタイル、Google スタイル、NumPy スタイルなどの
   様々な記述スタイルも存在する（練習問題）。

None
====

TODO

Truthy と Falsy
===============

TODO: bool のところで説明する？

型ヒントあれこれ
================

TODO: Optional, Union, Any, Literal とか

例外
====

TODO

表明
====

TODO

練習問題
========

1. ``complex`` 組み込み型について調べよ。
2. `decimal 標準モジュール`_ で提供される ``Decimal`` 型（クラス）について調べよ。
3. ``match`` 文の動作について調べよ。
4. Docstring の記述には reStructuredText スタイル、Google スタイル、NumPy スタイルなど
   様々なスタイルが存在する。これらのスタイルについて調べよ。

.. _`decimal 標準モジュール`: https://docs.python.org/ja/3/library/decimal.html
