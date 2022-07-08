==========
プロトコル
==========

次のような関数がある。

.. code-block:: python3

   def bait(duck):
       """アヒルを鳴かせます。"""
       duck.quack()  # アヒル (duck) がガーガー鳴く (quack)

この関数を動かしてみよう。

.. code-block:: python3

   >>> def bait(duck):
   ...     duck.quack()
   ... 
   >>> bait(10)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 2, in bait
   AttributeError: 'int' object has no attribute 'quack'

適当に ``bait(10)`` と呼び出してみたが、当然うまくいかない。

関数をよく見てみよう。 ``duck.quack()`` とは何だろうか？　これはメソッド呼び出しに見える。

ということで、まず ``quack`` という名前のメソッドを持ったクラスを作成してみよう。

.. code-block:: python3

   class Duck:
       def quack(self):
           print("Quack!")
 
このクラスのインスタンスは、 ``quack()`` メソッドを呼び出せる。

.. code-block:: python3

   >>> class Duck:
   ...     def quack(self):
   ...         print("Quack!")
   ... 
   >>> duck = Duck()
   >>> duck.quack()
   Quack!

このインスタンスを使えば、最初に示した関数を呼び出すことができそうだ。

.. code-block:: python3

   >>> def bait(duck):
   ...     duck.quack()
   ... 
   >>> class Duck:
   ...     def quack(self):
   ...         print("Quack!")
   ... 
   >>> duck = Duck()
   >>> bait(duck)
   Quack!

予想通り動いた。

ダック・タイピング
==================

ところで、ガーガー鳴くのはアヒルだけではない。カモもガーガー鳴く。

というより、アヒルはマガモを家禽として飼いならしたものであり、
英語ではどちらも duck と呼ばれる。
仕方がないので Kamo という名前で（アヒルではなく）カモを表すクラスを作ろう。

.. code-block:: python3

   class Kamo:
       def quack(self):
           print("quack!")

辞書によると、quack には「ぺちゃくちゃ・がやがやしゃべる」といった意味もあるようなので、
人間が quack することもあるかもしれない。

.. code-block:: python3

   class Person:
       def quack(self):
           print("quack?")

これらのクラスのインスタンスも、当然最初に示した ``bait()`` 関数の引数として渡すことができる。

.. code-block:: python3

   >>> # 宣言略

   >>> bait(Kamo())
   quack!
   >>> bait(Person())
   quack?

要するに、 ``quack()`` メソッドを持っているオブジェクトならなんでも ``bait()`` 関数に渡すことができる。

``duck.quack()`` というメソッド呼び出しがあったとき、
（予めオブジェクトの型を見るなどしてそのメソッド呼び出しが可能であるかどうかといったような確認はせずに）
Python は単にそういうメソッドを呼び出そうとする。
もしそのようなメソッドが呼び出せなかったら、単に失敗する（ ``AttributeError`` などの例外を投げる）。

このような挙動（スタイル）には名前が付いていて、 *ダック・タイピング* と呼ばれる。
「アヒルのように鳴くのであれば、それはアヒルだ」ということである。

.. note::

   一般的には「アヒルのように歩き、アヒルのように鳴くのなら、それはアヒルである（アヒルに違いない）」
   のように言われることが多い。

   一説によると、 `ダック・テスト`_ に由来するという。

.. _`ダック・テスト`: https://ja.wikipedia.org/wiki/ダック・テスト

.. note:: 

   特に静的型付け言語の経験等が少ない場合は、ダック・タイピングとは何であるのかが理解しにくいかもしれない。
   ここでは、ひとまず Python が上記のように動作するということを確認できればよい。

ダック・タイピングと型ヒント
============================

最初に示した関数を再掲する。

.. code-block:: python3

   def bait(duck):
       duck.quack()

Python は予めメソッド呼び出しが可能であるかどうかといった確認はしないので、
この関数の引数にどのようなオブジェクトが入ってこようが構いはしないのであった。

つまり、 ``duck.quack()`` というメソッド呼び出しが行われるときに初めて、
メソッドが実際に呼び出せるかどうかがわかる。

この挙動……つまりダック・タイピングには便利な点もあるが、困る点も存在する。

例えば、 ``quack()`` メソッドの呼び出しが失敗したら、プログラムはそこで停止してしまうかもしれない。
予め ``quack()`` メソッドが呼び出せないようなオブジェクトは
そもそも ``bait()`` 関数には渡せないようになっているほうが嬉しいだろう。

先程、 ``Duck`` というクラスを作成した。
もし引数 ``duck`` に ``Duck`` クラスのインスタンスを渡したいのであれば、次のように型ヒントを付けられる。
クラス名を型ヒントとして使用した場合、そのクラスのインスタンスを要求することになるということに注意しよう。

.. code-block:: python3

   def bait(duck: Duck) -> None:
       duck.quack()

型ヒントは「ヒント」なので、Python はこれを無視する。
しかし、mypy などの型チェッカーを用いれば、型があっていない場合にエラーを報告してくれる。

以下のコードを適当なファイル（ここでは ``main.py`` とした）に保存し、 mypy で検査してみよう。

.. code-block:: python3

   class Duck:
       def quack(self) -> None:
           print("Quack!")

   def bait(duck: Duck) -> None:
       duck.quack()

   bait("あひる")

.. code-block:: shell

   $ mypy main.py
   main.py:8: error: Argument 1 to "bait" has incompatible type "str"; expected "Duck"
   Found 1 error in 1 file (checked 1 source file)

型チェッカーを用いることにより、 ``Duck`` クラスのインスタンスではないオブジェクトを
``bait()`` 関数に渡そうとすることを防ぐことができるようになった。

ところで、この関数に ``Kamo`` クラスのインスタンスを渡すとどうなるだろうか。
``Kamo`` クラスも ``quack()`` メソッドを持っているのだから、
``bait()`` 関数に渡すことができてほしい。
しかし、 ``Kamo`` クラスと ``Duck`` クラスは別物であるので、
当然 mypy は型があっていないといったエラーを報告してくる。

.. code-block:: python3

   class Duck:
       def quack(self) -> None:
           print("Quack!")

   class Kamo:
       def quack(self) -> None:
           print("quack!")

   def bait(duck: Duck) -> None:
       duck.quack()

   bait(Duck())  # 12 行目: OK!
   bait(Kamo())  # 13 行目: NG

.. code-block:: shell

   $ mypy main.py
   main.py:13: error: Argument 1 to "bait" has incompatible type "Kamo"; expected "Duck"
   Found 1 error in 1 file (checked 1 source file)

このような場合、 *プロトコルクラス（プロトコル）* を用いることができる。

プロトコル
==========

プロトコルは `typing 標準モジュール`_ の `Protocol` クラスを用いて定義できる。

.. _`typing 標準モジュール`: https://docs.python.org/ja/3/library/typing.html

.. code-block:: python3

   from typing import Protocol

   class Quackable(Protocol):
       """アヒルのように鳴くことができるプロトコル。"""

       def quack(self) -> None:
           """ガーガー鳴きます。"""
           ...

``bait()`` 関数の引数の型ヒントを上で定義した ``Quackable`` に変更すると、
（ ``Quackable.quack()`` と同じ型シグネチャを持つ） ``quack()`` メソッドを持つクラスのインスタンスであれば
何でも ``bait()`` 関数に渡すことができるようになる。

.. code-block:: python3

   from typing import Protocol

   class Quackable(Protocol):
       def quack(self) -> None:
           ...

   class Duck:
       def quack(self) -> None:
           print("Quack!")

   class Kamo:
       def quack(self) -> None:
           print("quack!")

   class Person:
       def quack(self) -> None:
           print("quack?")

   def bait(q: Quackable) -> None:
       q.quack()

   bait(Duck())
   bait(Kamo())
   bait(Person())

.. code-block:: shell

   $ mypy main.py
   Success: no issues found in 1 source file

個々のクラス (``Duck``, ``Kamo``, ``Person``) は、 ``Quackable`` であると宣言する必要がない。
ただ ``quack(self) -> None`` メソッドを持ってさえいれば ``Quackable`` であると見做される。
これは *structural subtyping（構造的部分型）* 、静的ダック・タイピングなどとも呼ばれる。

.. note:: 

   TypeScript や Go 言語での interface 等は同じように構造的部分型を実現している。
   一方、Java の interface 等では明示的な宣言をしない限り部分型であるとは見做されない。
   これは *nominal subtyping（名前的部分型、公称的部分型、公称型）* と呼ばれる。

練習問題
========

1. プロトコルクラスと似たものに、 *抽象クラス* がある。
   Python で抽象クラスを使う方法を調べよ。
   また、プロトコルと抽象クラスの違いについて調べよ。

2. ユーザーを永続化する、つまり ``User`` クラスのインスタンスを保存したり取り出したりするための
   ``UserRepository`` プロトコルを作成せよ。
   ``UserRepository`` には以下のメソッドを用意せよ。

   * ``get(self, user_id: str) -> User``: ユーザーを取得する。
   * ``put(self, user: User) -> None``: ユーザーを保存する。
   * ``delete(self, user_id: str) -> None``: ユーザーを削除する。

3. ``put`` メソッドでは何もせず、 ``get`` メソッドでは適当なユーザーを返すだけ、といったように
   データベースを使用しない仮の ``UserRepository`` である ``DummyUserRepository`` を実装せよ。

4. Amazon DynamoDB を用いた ``DynamoUserRepository`` を実装せよ。
   実装には、AWS 公式の SDK である Boto3_ や
   サードパーティライブラリの PynamoDB_ などが使用できる。
   テストを書く場合、AWS サービスをモックしてくれる moto_ ライブラリが使用できる。
   また、 `DynamoDB Local`_ を使用するとローカルにテスト用の DynamoDB を構築することもできる。

5. *Repository パターン* について調べよ。

6. *Active Record パターン* について調べよ。
   また、Repository パターンと Active Record パターンのメリット・デメリットについて考察せよ。

.. _Boto3: https://github.com/boto/boto3 
.. _PynamoDB: https://github.com/pynamodb/PynamoDB
.. _moto: https://github.com/spulec/moto
.. _`DynamoDB Local`: https://docs.aws.amazon.com/ja_jp/amazondynamodb/latest/developerguide/DynamoDBLocal.html
