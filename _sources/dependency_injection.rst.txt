====================
Dependency Injection
====================

不安定なテスト
==============

以下のスクリプトは、生年月日から年齢を計算するものである。

.. code-block:: python3
  
   from datetime import date
   
   
   def calc_age(date_of_birth: date) -> int:
       """生年月日から年齢を計算します。
   
       Args:
           date_of_birth: 生年月日。
   
       Returns:
           年齢。
       """
       today = date.today()
       deltayear = today.year - date_of_birth.year
   
       if (today.month, today.day) <= (date_of_birth.month, date_of_birth.day):
           deltayear -= 1
   
       return deltayear
   
   
   if __name__ == "__main__":  # スクリプトとして実行されたときのみ、以下を実行
       import sys
   
       # スクリプトの第一引数を date に変換して calc_age を呼ぶ
       age = calc_age(date.fromisoformat(sys.argv[1]))
       print(age)

たとえば上記のスクリプトを ``calc_age.py`` として保存して、以下のように実行できる。

.. code-block:: shell

   $ python3 calc_age.py 1994-03-30  # 私の誕生日
   28

実は、このなかの ``calc_age()`` 関数にはバグがある。
テストをしっかり書いておけば、
ユーザーからクレームが来る前にバグに気づくことができただろう。

今からでも遅くない。 ``calc_age()`` 関数のテストを書いてみよう。

テストを書くときのコツは、エッジケース、つまり境界値を意識することだ。
今日が 2022 年 7 月 6 日だとすると、

- 2000 年 7 月 5 日生まれの場合 → 22 歳
- 2000 年 7 月 6 日生まれの場合 → 22 歳（今日が誕生日！）
- 2000 年 7 月 7 日生まれの場合 → 21 歳

となるはずだ。

.. note::

   *満年齢* は厳密には誕生日前日の午後 12 時（24 時）に加算される。
   そのため、7 月 7 日生まれの人は 7 月 6 日の午後 12 時に満年齢で 22 歳となる。
   つまり、7 月 6 日の時点で満 22 歳となってしまうわけだが、
   今回はこれを無視し、日本での通常の感覚における年齢計算（誕生日に年齢が加算される）とする。

テストは以下のようになった
（ここでは別ファイルにテストを書いている）。

.. code-block:: python3
  
   from datetime import date

   from calc_age import calc_age


   def test_calc_age() -> None:
       """calc_age() 関数のテスト。"""

       assert calc_age(date(2000, 7, 5)) == 22
       assert calc_age(date(2000, 7, 6)) == 22
       assert calc_age(date(2000, 7, 7)) == 21

2022 年 7 月 6 日時点でのテスト結果は以下の通り。

.. code-block:: python3

       def test_calc_age() -> None:
           """calc_age() 関数のテスト。"""
       
           assert calc_age(date(2000, 7, 5)) == 22
   >       assert calc_age(date(2000, 7, 6)) == 22
   E       assert 21 == 22
   E        +  where 21 = calc_age(datetime.date(2000, 7, 6))
   E        +    where datetime.date(2000, 7, 6) = date(2000, 7, 6)
   
   test_calc_age.py:10: AssertionError

``calc_age(date(2000, 7, 6))`` の結果が ``22`` ではなくて ``21`` になっている。
やはり境界にバグが潜んでいたようだ。となると、比較演算子 ``<=`` のあたりが怪しい。
修正してみよう。

.. code-block:: python3

   def calc_age(date_of_birth: date) -> int:
       """略"""
       today = date.today()
       deltayear = today.year - date_of_birth.year
   
       if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
           deltayear -= 1
   
       return deltayear

テストが通ることを確認してみる。

.. code-block:: python3

   (前略)

   test_calc_age.py .                                  [100%]
   
   ==================== 1 passed in 0.01s ====================

一件落着だ。コードをチェックインして家に帰ろう。

しかし明日、出勤して誰かがテストを走らせてみると……どうなるかはおわかりだろう。

.. code-block:: python3

       def test_calc_age() -> None:
           """calc_age() 関数のテスト。"""
       
           assert calc_age(date(2000, 7, 5)) == 22
           assert calc_age(date(2000, 7, 6)) == 22
   >       assert calc_age(date(2000, 7, 7)) == 21
   E       assert 22 == 21
   E        +  where 22 = calc_age(datetime.date(2000, 7, 7))
   E        +    where datetime.date(2000, 7, 7) = date(2000, 7, 7)

   test_calc_age.py:11: AssertionError

*不安定なテスト (flaky test)* ……
つまり、その時の状況や運によって成功したりしなかったりするテストは **危険** だ。

なにか重大なバグが潜んでいるかもしれないにも関わらず、
運良くテストが通った日には見過ごされてしまう。

あるいは、テストを実行するたびにイライラさせられ、
ついにはコメントアウトされてしまう。

不安定なテストの原因は様々だが、主にテストが何か不安定なものに *依存* しているときに発生する。

- テストが他のテストに依存している：例えば、他のテストで生成・削除されたデータを使用している
- テストが現在日時に依存している
- テストが乱数に依存している
- テストが外部サービスやネットワークに依存している

今回の場合は、テストが現在日時に依存していることが問題だ。

テストしやすいコード
====================

前述の ``calc_age()`` 関数は、
現在日時に依存しているため本質的にテストしにくい関数だった。

テストしやすくするためには、
``calc_age()`` 関数がそもそも現在日時に依存していなければよい。

.. code-block:: python3

   from datetime import date
   
   
   def calc_age_at(d: date, date_of_birth: date) -> int:
       """生年月日から、ある日付時点での年齢を計算します。
   
       Args:
           d: この日付時点での年齢を計算します。
           date_of_birth: 生年月日。
   
       Returns:
           年齢。
       """
       deltayear = d.year - date_of_birth.year
   
       if (d.month, d.day) < (date_of_birth.month, date_of_birth.day):
           deltayear -= 1
   
       return deltayear
   
   
   if __name__ == "__main__":
       import sys
   
       age = calc_age_at(date.today(), date.fromisoformat(sys.argv[1]))
       print(age)

新しい ``calc_age_at()`` 関数は、内部で ``date.today()`` を使用していない。
代わりに、呼び出し時に第１引数に ``date.today()`` を渡している。

``calc_age_at()`` 関数は現在日時に依存していないので、テストしやすい。

.. code-block:: python3

   from datetime import date
   
   from calc_age import calc_age_at
   
   
   def test_calc_age_at() -> None:
       """calc_age_at() 関数のテスト。"""
   
       today = date(2022, 7, 6)
       assert calc_age_at(today, date(2000, 7, 5)) == 22
       assert calc_age_at(today, date(2000, 7, 6)) == 22
       assert calc_age_at(today, date(2000, 7, 7)) == 21

また、副作用として ``calc_age_at()`` 関数では
「特定の日時における年齢」も計算できるようにもなっている。

.. note::
   
   日時のテストに便利な FreezeGun_ というサードパーティライブラリを用いると、
   もとの ``calc_age()`` 関数のままでも壊れないテストを書くことができる。

   .. code-block:: python3

      from datetime import date
      
      from freezegun import freeze_time
      
      from calc_age import calc_age
      
      
      @freeze_time("2022-07-06")  # 日付を 2022/07/06 に固定
      def test_calc_age() -> None:
          """calc_age() 関数のテスト。"""
      
          assert calc_age(date(2000, 7, 5)) == 22
          assert calc_age(date(2000, 7, 6)) == 22
          assert calc_age(date(2000, 7, 7)) == 21

.. _FreezeGun: https://github.com/spulec/freezegun

.. note::

   より一般に、 `unittest.mock 標準モジュール`_ の ``patch()`` デコレータや、
   pytest の ``monkeypatch`` フィクスチャなどを用いて
   プログラムの一部分をテスト中のみ書き換えてテストすることもできる（ *モンキーパッチ* ）。

   .. code-block:: python3

      from datetime import date
      from unittest.mock import MagicMock, patch
      
      from calc_age import calc_age
      
      
      # calc_age.py 内の date をモック（偽物）に変更
      @patch("calc_age.date")
      def test_calc_age(mock_date: MagicMock) -> None:
          """calc_age() 関数のテスト。"""
      
          # モックになった calc_age.py 内の date の today() メソッドを
          # 常に date(2022, 7, 6) を返すように設定
          mock_date.today = lambda: date(2022, 7, 6)
      
          assert calc_age(date(2000, 7, 5)) == 22
          assert calc_age(date(2000, 7, 6)) == 22
          assert calc_age(date(2000, 7, 7)) == 21

.. _`unittest.mock 標準モジュール`: https://docs.python.org/ja/3/library/unittest.mock.html

Dependency Injection
====================

不安定なものに依存したコードはテストしにくい。
しかし、通常コードというのは不安定なもの（乱数、日時、外部サービス、etc.）に依存するものである。

そこで、先程は依存する不安定なものを関数の外部から引数で渡すことで、
関数をテストしやすい状態にした。
これは *Dependency Injection（DI；依存性の注入）* と呼ばれる。

クラスの場合は、コンストラクタ経由で依存性を注入することもできる。

次の ``Dice`` クラスはサイコロを表すクラスであるが、内部で乱数を使用している。

.. code-block:: python3

   from random import Random
   
   
   class Dice:
       """サイコロを表すクラス。
   
       Args:
           number_of_sides: 面の数。デフォルトは６です。
       """
   
       def __init__(self, number_of_sides: int = 6) -> None:
           self.number_of_sides = number_of_sides
   
       def max_in(self, n: int) -> int:
           """サイコロを n 回振って、そのうちの最大の出目を返します。
   
           Args:
               n: サイコロを振る回数。
   
           Returns:
               最大の出目。
           """
           random = Random()
           return max(
               random.randint(1, self.number_of_sides) for _ in range(n)
           )


   if __name__ == "__main__":
       dice = Dice(100)
       print(dice.max_in(10))

`random 標準モジュール`_ で提供されている ``Random`` クラスの
``randint(a, b)`` メソッドは、 ``a <= N <= b`` であるようなランダムな整数 ``N`` を返す。

.. note:: 

   ``randint(a, b)`` は `random 標準モジュール`_ の関数としても提供されている。

   .. code-block:: python3

      >>> from random import randint
      >>> randint(0, 100)
      65

.. _`random 標準モジュール`: https://docs.python.org/ja/3/library/random.html


このクラスをテストしやすいように変更してみよう。
即ち、依存している ``Random`` クラスのインスタンスを外部から注入する。

.. code-block:: python3

   from random import Random
   
   
   class Dice:
       """サイコロを表すクラス。
   
       Args:
           random: 乱数を生成するために用いる、Random クラスのインスタンス。
           number_of_sides: 面の数。デフォルトは６です。
       """
   
       def __init__(self, random: Random, number_of_sides: int = 6) -> None:
           self.random = random
           self.number_of_sides = number_of_sides
   
       def max_in(self, n: int) -> int:
           """サイコロを n 回振って、そのうちの最大の出目を返します。
   
           Args:
               n: サイコロを振る回数。
   
           Returns:
               最大の出目。
           """
           return max(
               self.random.randint(1, self.number_of_sides) for _ in range(n)
           )
   
   
   if __name__ == "__main__":
       dice = Dice(Random(), 100)
       print(dice.max_in(10))

すると、テストは以下のように書ける。

.. code-block:: python3

   from typing import Any
   
   from dice import Dice
   
   
   def test_max_in() -> None:
       """max_in() メソッドのテスト。"""
   
       class MockRandom:  # 関数内でもクラスは定義できる
           def __init__(self) -> None:
               self.randints = iter([83, 98, 56, 81, 28])
   
           def randint(self, a: int, b: int) -> int:
               # randint(1, 100) として呼ばれていることをテスト
               assert a == 1
               assert b == 100
   
               # 呼び出された順に 83, 98, 56, 81, 28 を返す
               return next(self.randints)
   
       random: Any = MockRandom()
       d = Dice(random, 100)
   
       assert d.max_in(5) == 98

上記のテストでは、 ``randint()`` メソッドが固定値を返すような "偽物の" ``Random`` クラスである
``MockRandom`` クラスを用意してテストを行っている。

``MockRandom`` のように、テスト時に使用される代用品は *テストダブル* と呼ばれる。
テストダブルには *スタブ* や *モック* 等がある（練習問題を参照）。

.. note:: 

   `unittest.mock 標準モジュール`_ は、モックを作るのに便利な
   ``Mock`` クラスや ``MagicMock`` クラスを提供している。

   ``Mock`` クラスを使用すると先程のテストは以下のようにも書ける。

   .. code-block:: python3

      from unittest.mock import Mock, call
      
      from dice import Dice
      
      
      def test_max_in() -> None:
          """max_in() メソッドのテスト。"""

          random = Mock()
          # randint() が呼ばれた順に 83, 98, 56, 81, 28 を返すように設定
          random.randint.side_effect = iter([83, 98, 56, 81, 28])
      
          d = Dice(random, 100)
          assert d.max_in(5) == 98
      
          # randint(1, 100) が５回呼ばれていることを確認
          random.randint.assert_has_calls(
              call(1, 100) for _ in range(5)
          )

.. note:: 

   乱数を用いたコードのテストでは、以下のような方法が取られることもある。

   * 単純に多くの回数試行してテストする
   * シード値を固定してテストする（例えば ``random.seed()`` を利用する）

練習問題
========

1. この章で作成した ``calc_age()`` 関数は、
   2 月 29 日生まれの人に対しても正しく動作するだろうか。テストを書き確かめよ。
2. 以下の ``get_content_type()`` 関数のテストを書け。
   テストしやすいように関数を変更しても構わない。

   .. code-block:: python3

      from urllib.request import urlopen
      
      
      def get_content_type(url: str) -> str:
          """指定された URL にアクセスし、レスポンスの Content-Type ヘッダーの値を取得します。
      
          Args:
              url: URL。
      
          Returns:
              Content-Type ヘッダーの値。設定されていなければ、空文字列。
      
          Raises:
              urllib.error.URLError: エラーが発生した場合に送出されます。
          """
          with urlopen(url) as f:
              content_type: str = f.headers.get("Content-Type", "")
      
          return content_type
      
3. 以下のような「ユーザー取得ユースケース」を作成した。

   TODO: サンプルリポジトリはまだ用意されていない。
   サンプルリポジトリが用意されたら、それに合わせて以下も書き換える予定。

   .. code-block:: python3

      """ユーザー取得ユースケース。"""
      from dataclasses import dataclass
      from datetime import datetime
      from typing import Literal
      
      # ここのインポートパスはパッケージ名やディレクトリ構成に応じて適宜書き換える必要があるだろう。
      # 以下はサンプルリポジトリの場合。
      from sample_project.domain.user import UserNotFound as DomUserNotFound
      from sample_project.domain.user import UserRepository

      
      UserStatus = Literal["normal", "frozen"]
      """ユーザーのステータス。
      
      - `normal`: 通常。
      - `frozen`: 凍結状態。
      """
      
      
      class UserNotFound(Exception):
          """ユーザーが見つかりません。"""
      
      
      @dataclass(frozen=True)
      class Input:
          """ユースケースの入力。
      
          Attributes:
              user_id: ユーザー ID。空でない文字列。
          """
      
          user_id: str
      
      
      @dataclass(frozen=True)
      class Output:
          """ユースケースの出力。
      
          Attributes:
              user_id: ユーザー ID。空でない文字列。
              name: 名前。空でない文字列。
              status: ステータス。
              registered_at: 登録日時。UTC。
          """
      
          user_id: str
          name: str
          status: UserStatus
          registered_at: datetime
      
      
      class Usecase:
          """ユーザー取得ユースケース。
      
          ユーザー情報を取得して返します。
      
          Args:
              user_repository: ユーザーのリポジトリ。
          """
      
          def __init__(self, user_repository: UserRepository):
              self._user_repository = user_repository
      
          def run(self, ipt: Input) -> Output:
              """ユースケースを実行します。
      
              Args:
                  ipt: ユースケースの入力。
      
              Returns:
                  ユースケースの出力。
      
              Raises:
                  UserNotFound: ユーザーが見つかりません。
              """
              try:
                  user = self._user_repository.get(ipt.user_id)
              except DomUserNotFound:
                  raise UserNotFound
      
              return Output(
                  user_id=user.user_id,
                  name=user.name,
                  status=user.status,
                  registered_at=user.registered_at,
              )

   このユースケースのテストを書け。

   また、 ``run`` メソッドが ``User`` オブジェクトを直接返さず
   ``Output`` クラスに「詰め替え」ていたり、
   わざわざ ``sample_project.domain.user.UserNotFound`` 例外を補足して
   ユースケース内で定義した同名の例外を投げ直しているのはなぜだろうか。
   このような設計にすることのメリット・デメリットを考えよ。
4. 以下のユースケースを作成し、テストを書け。
   
   * ユーザー作成ユースケース
   * ユーザー名前変更ユースケース
   * ユーザー凍結ユースケース
   * ユーザー凍結解除ユースケース
   * ユーザー削除ユースケース

   ヒント：ユーザー削除ユースケースは *冪等* にしてもよいだろう。
   つまり、ユーザーが既に削除済み（見つからない）である場合は何もしない。

5. テストダブルの種類について調べよ。スタブとモックはどう使い分けられるだろうか？
6. DI を用いたテストと、モンキーパッチを用いたテストのそれぞれについて
   メリット・デメリットを考察せよ。
7. テスト駆動開発に於ける *ロンドン学派 (Mockist)* と
   *デトロイト学派 (Classicist)* について調べよ。
   この章で作成した ``Dice`` クラスのテストには、モックやスタブを利用すべきだろうか？
8. *依存性逆転の原則 (dependency inversion principle)* について調べよ。