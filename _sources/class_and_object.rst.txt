====================
クラスとオブジェクト
====================

オブジェクト
============

*オブジェクト* は、簡単に言うと *属性* を持つデータである。

たとえば、JavaScript にはオブジェクトリテラル記法が存在し、　``{}`` でオブジェクトを作成できる。

.. code-block:: javascript

   > const obj = {}

   > obj
   {}

   > obj.name = "Kent Beck" // オブジェクトに name 属性を追加

   > obj.name // オブジェクトの name 属性を参照
   'Kent Beck'

   > obj
   { name: 'Kent Beck' }

.. note:: 

   Python では、実際には *ほとんどすべてがオブジェクト* であるが、ここでは深入りしない。
   例えば、int 型の数値はオブジェクトである。

   .. code-block:: python3

      >>> isinstance(1, object)
      True

   それどころか、int 型それ自体もオブジェクトである。

   .. code-block:: python3

      >>> isinstance(int, object)
      True

クラス
======

Python には JavaScript のオブジェクトリテラルのようなものは存在しない。
Python は *クラスベースオブジェクト指向* であり、通常 *クラス* を利用してオブジェクトを作成する。

まず、クラスを定義する。
クラス名には通常アッパーキャメルケース (UpperCamelCase) を用いる。

.. code-block:: python3

   class SoftwareEngineer:
       pass

クラス名に ``()`` をつけて "呼び出す" と、クラスからオブジェクトが作成される。

.. code-block:: python3

   >>> class SoftwareEngineer:
   ...     pass
   ... 
   >>> se = SoftwareEngineer()  # クラスからオブジェクトを作成

   >>> se.name = "Robert C. Martin"  # オブジェクトに name 属性を追加
   >>> se.name  # オブジェクトの name 属性を参照
   'Robert C. Martin'

   >>> se.name = "Martin Fowler"  # オブジェクトの name 属性を変更
   >>> se.name
   'Martin Fowler'

クラスから作成されたオブジェクトのことを *インスタンス* ともいう。

.. note:: 

   もしインスタンスを格納する変数やインスタンスを受け取る引数に型ヒントをつけたい場合、
   クラス名を使用する。

   .. code-block:: python3

      se: SoftwareEngineer = SoftwareEngineer()


      def fire(incompetent: SoftwareEngineer) -> None:
          ...

属性に型ヒントをつける
----------------------

属性に型ヒントをつけたい場合は、以下のようにする。

.. code-block:: python3

   class SoftwareEngineer:
       name: str

後述する ``__init__()`` メソッドで属性を設定する場合、通常明示的に型を指定する必要はない。

.. code-block:: python3

   class SoftwareEngineer:
       def __init__(self) -> None:
           self.name = "John Doe"


   se = SoftwareEngineer()
   se.name = "Eric Evans"  # se は name 属性を持ち、型は str だろう...

メソッド
========

*メソッド* は、クラス本体の中で定義された関数である。
メソッドの第一引数は特殊な引数であり、通常 ``self`` という名前にする。

``self`` 引数については後述する。
ひとまず、メソッドの定義時には ``self`` が必要で、
メソッドを呼び出すときには不要だということを覚えておこう。

.. code-block:: python3

   class Greeting:
       """いろいろな挨拶をするクラスです。"""

       def hello(self) -> None:
           """Hello! と挨拶します。"""
           print("Hello!")

       def hi(self) -> None:
           """Hi! と挨拶します。"""
           print("Hi!")

       def greet(self, phrase: str) -> None:
           """好きなフレーズで挨拶します。"""
           print(f"{phrase}!")

.. note::

   ``self`` 引数には通常型ヒントをつけなくてよいが、
   あえてつけるとしたら以下のようになる。

   .. code-block:: python3

      # 現在のところ、クラス内からのクラス名の参照には制限があり、この記述が必要
      from __future__ import annotations

      
      class Greeting:
          """いろいろな挨拶をするクラスです。"""
      
          def hello(self: Greeting) -> None:
              """Hello! と挨拶します。"""
              print("Hello!")

メソッドは通常の関数と異なり、以下のようにインスタンスの属性として呼び出す。
即ち、まずクラスからインスタンスを作成し、そのインスタンスを利用してメソッドを呼び出す。

.. code-block:: python3

   >>> class Greeting:
   ...     def hello(self) -> None:
   ...         print("Hello!")
   ...     def hi(self) -> None:
   ...         print("Hi!")
   ...     def greet(self, phrase: str) -> None:
   ...         print(f"{phrase}!")
   ... 
   >>> greeting = Greeting()

   >>> greeting.hello()
   Hello!

   >>> greeting.hi()
   Hi!

   >>> greeting.greet("irankarapte")
   irankarapte!

``greet()`` メソッドは ``self`` と ``phrase`` の２つの引数を持っているが、
メソッド呼び出し時は ``self`` を無視して ``phrase`` のみ指定していることに注意しよう。

次に、インスタンスを作らずに ``クラス名.メソッド名()`` としても呼び出せないことを確認してみよう。

.. code-block:: python3

   >>> Greeting.hello()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: hello() missing 1 required positional argument: 'self'

   >>> Greeting().hello()  # これはインスタンスを作成しているので OK 
   Hello!

"hello() には 'self' 引数が必要だ" という不可解なエラーが発生しているが、
これを理解するためにはまず ``self`` 引数について理解する必要がある。

.. note::

   ``クラス名.メソッド名()`` のようにして呼び出せるような特殊なメソッドも存在する。

   TODO: インスタンスメソッドとクラスメソッド、static method について

self 引数
=========

メソッドの第一引数には、謎の ``self`` を指定する決まりであった。
この ``self`` 引数は、メソッドを呼び出したインスタンスを受け取る。

実験してみよう。

.. code-block:: python3

   class Organism:
       """生物を表すクラスです。
       
       generic_name は属名、specific_name は種名です。
       """

       generic_name: str
       specific_name: str

       def binomen(self) -> str:
           """二名法での学名を返します。"""
           return f"{self.generic_name} {self.specific_name}"


   org = Organism()
   org.generic_name = "Canis"
   org.specific_name = "lupus"

   binomen = org.binomen()
   print(binomen)  # Canis lupus

``org.binomen()`` のようにメソッドを呼び出すと、
``binomen()`` メソッドの ``self`` には「このメソッドを呼び出したインスタンス」、
つまり ``org`` が渡される。

そのため、 ``binomen()`` メソッド内部から
``self.generic_name`` のような形でインスタンスに設定された属性にアクセスできるのである。

.. note::

   実は、上記の ``org.binomen()`` は ``Organism.binomen(org)`` と書くこともできる。

   インスタンスメソッドを ``クラス名.メソッド名()`` のように呼び出すときは、
   明示的に ``self`` 引数を渡さなければならない。
   そのため、 ``Organism.binomen()`` としてメソッドを呼び出そうとすると
   引数が足りないというエラーが出る。

   .. code-block:: python3

      >>> Organism.binomen()
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      TypeError: binomen() missing 1 required positional argument: 'self'

   ただし、通常インスタンスメソッドをこのように呼び出す必要はない。

``self`` 引数を利用すれば、メソッド内から同じクラスの別のメソッドにアクセスすることもできる。
メソッドは、インスタンスの属性として呼び出すからである。

   .. code-block:: python3

      class Greeting:
          """いろいろな挨拶をするクラスです。"""
      
          def hello(self) -> None:
              """Hello! と挨拶します。"""
              self.greet("Hello")
      
          def hi(self) -> None:
              """Hi! と挨拶します。"""
              self.greet("Hi")
      
          def greet(self, phrase: str) -> None:
              """好きなフレーズで挨拶します。"""
              print(f"{phrase}!")

__init__ メソッド
=================

TODO

練習問題
========

1. ``user.py`` というファイルを作成し、その中に ``User`` クラスを作成せよ。
2. ``User`` クラスに ``name`` 属性（文字列）を追加せよ。
   ``name`` 属性は、コンストラクタ経由で初期化できるようにせよ。
   即ち、以下が動作するようにせよ。

   .. code-block:: python3

      >>> user = User("Ada Lovelace")
      >>> user.name
      'Ada Lovelace'

      >>> user.name = "Grace Hopper"
      >>> user.name
      'Grace Hopper'

3. *プロトタイプベースオブジェクト指向* について調べよ。
4. 本章で登場した人名について調べよ。