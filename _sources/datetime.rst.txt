==========
日時の扱い
==========

日時とは、日付 (date) と時刻 (time) のことである。

Python の `datetime 標準モジュール`_ では、日時を扱う便利な関数やクラス（型）が提供されている。

.. _`datetime 標準モジュール`: https://docs.python.org/ja/3/library/datetime.html

date 型
========

日付を扱う型。

.. code-block:: python3

   >>> from datetime import date

   >>> d = date(2000, 12, 31)
   >>> d.year  # 年
   2000
   >>> d.month  # 月
   12
   >>> d.day  # 日
   31

   >>> date.today()  # 今日の日付
   datetime.date(2022, 5, 31)

time 型
========

時刻を扱う型。

.. code-block:: python3

   >>> from datetime import time

   >>> t = time(23, 59, 59, 999999)
   >>> t.hour  # 時
   23
   >>> t.minute  # 分
   59
   >>> t.second  # 秒
   59
   >>> t.microsecond  # マイクロ秒
   999999

``time`` 型は、タイムゾーンを含むこともできる。タイムゾーンについては ``datetime`` 型で詳しく見ていく。

datetime 型
============

日付と時刻を扱う型。モジュール名 ( ``datetime`` ) と型名 ( ``datetime`` ) が同じなので注意。

.. code-block:: python3

   >>> from datetime import datetime

   >>> d = datetime(2000, 12, 31, 23, 59, 59, 999999)

   >>> d.isoformat()  # ISO 8601 形式に変換
   '2000-12-31T23:59:59.999999'
   >>> d.strftime("%Y 年 %m 月 %d 日 %H 時 %M 分 %S 秒 %f マイクロ秒")  # 好きな形式に変換
   '2000 年 12 月 31 日 23 時 59 分 59 秒 999999 マイクロ秒'

   >>> datetime.now()  # 現在日時
   datetime.datetime(2022, 6, 2, 11, 47, 38, 892492)

``time`` 型や ``datetime`` 型は、タイムゾーンを含むこともできる。 
タイムゾーンとして UTC ( ``timezone.utc`` ) を指定してみよう。

.. code-block:: python3

   >>> from datetime import datetime, timezone

   >>> d = datetime(2000, 1, 1, tzinfo=timezone.utc)  # 2000 年 1 月 1 日 0 時 0 分 0 秒 (UTC)
   >>> d
   datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
   >>> d.isoformat()  # ISO 8601 形式に変換
   '2000-01-01T00:00:00+00:00'

   >>> datetime.now()  # 現在日時（ローカル）
   datetime.datetime(2022, 6, 2, 11, 58, 58, 289921)
   >>> datetime.now(timezone.utc)  # 現在日時 (UTC)
   datetime.datetime(2022, 6, 2, 2, 58, 58, 290334, tzinfo=datetime.timezone.utc)

協定世界時 (UTC: Coordinated Universal Time) は世界各地の標準時の基準となる時刻で、
イギリスのグリニッジ標準時 (GMT) にほぼ等しい。

日本標準時 (JST: Japan Standard Time) は、UTC から 9 時間進んでいる。
つまり、（サマータイム中でない）イギリスが午前 0 時のとき、日本はだいたい午前 9 時である。

JST は残念ながら ``timezone.jst`` のようには指定できないが、
Python 3.9 以降では `zoneinfo 標準モジュール`_ を用いて
IANA の Time Zone Database から ``Asia/Tokyo`` としてタイムゾーンを取得できる。

.. code-block:: python3

   >>> from datetime import datetime, timezone
   >>> from zoneinfo import ZoneInfo

   >>> d_utc = datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc)
   >>> d_utc.strftime("%H 時 %M 分 (%Z)")
   '00 時 00 分 (UTC)'

   >>> d_jst = d_utc.astimezone(ZoneInfo("Asia/Tokyo"))  # タイムゾーンを変更
   >>> d_jst.strftime("%H 時 %M 分 (%Z)")
   '09 時 00 分 (JST)'

.. note::

   Python 3.8 以前では `zoneinfo 標準モジュール`_ が使用できないが、
   ``timezone(timedelta(hours=9), "JST")`` のように ``timezone`` オブジェクトを作成して
   使用することができる。

   .. code-block:: python3

      >>> from datetime import datetime, timedelta, timezone

      >>> d_utc = datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc)
      >>> d_utc.strftime("%H 時 %M 分 (%Z)")
      '00 時 00 分 (UTC)'

      >>> jst = timezone(timedelta(hours=9), "JST")
      >>> d_jst = d_utc.astimezone(jst)
      >>> d_jst.strftime("%H 時 %M 分 (%Z)")
      '09 時 00 分 (JST)'

   また、 pytz_ や dateutil_ などタイムゾーンが扱えるサードパーティライブラリも存在する。

.. _`zoneinfo 標準モジュール`: https://docs.python.org/ja/3/library/zoneinfo.html

.. _pytz: https://pypi.org/project/pytz

.. _dateutil: https://github.com/dateutil/dateutil

.. note:: 

   日時を表すオブジェクトがタイムゾーンを含むとき *aware* であるといい、
   タイムゾーンを含まないとき *naive* であるという。

   扱うタイムゾーンが明らかなときは naive な日時でも十分だが、
   常にタイムゾーンを指定しておくようにすると無用な混乱が防げるかもしれない。

timedelta 型
==============

日付や時間の差を表す型。

.. code-block:: python3

   >>> from datetime import datetime, timedelta

   >>> datetime(2000, 1, 1) + timedelta(days=30)
   datetime.datetime(2000, 1, 31, 0, 0)

   >>> datetime(2000, 1, 1) - timedelta(weeks=6)
   datetime.datetime(1999, 11, 20, 0, 0)

   >>> d = datetime(2000, 12, 31) - datetime(2000, 1, 1)
   >>> d
   datetime.timedelta(days=365)
   >>> d.total_seconds()
   31536000.0

ISO 8601
========

`ISO 8601`_ は、日時の表記に関する
ISO（International Organization for Standardization; 国際標準化機構）の規格である。

.. _`ISO 8601`: https://www.iso.org/iso-8601-date-and-time-format.html

ISO 8601 で定められている日時の表記に関する形式（以下 ISO 8601 形式と呼ぶ）は、
日時を文字列で表現する場合によく用いられる。
例えば JSON 文字列に日時を格納したり、
日時を格納するような型を持たないデータベースに日時を格納する場合などである。

``date`` 型、 ``time`` 型、 ``datetime`` 型は、ISO 8601 形式の文字列に変換できる。

.. code-block:: python3

   >>> from datetime import date, datetime, time, timezone

   >>> date(2000, 12, 31).isoformat()
   '2000-12-31'

   >>> time(23, 59, 59).isoformat()
   '23:59:59'

   >>> time(23, 59, 59, 999999, timezone.utc).isoformat()
   '23:59:59.999999+00:00'

   >>> datetime(2000, 12, 31, 23, 59, 59).isoformat()
   '2000-12-31T23:59:59'

   >>> datetime(2000, 12, 31, 23, 59, 59, 999999, timezone.utc).isoformat()
   '2000-12-31T23:59:59.999999+00:00'

ISO 8601 形式の文字列から ``date`` 型、 ``time`` 型、 ``datetime`` 型への変換については、
**一部の形式のみ** サポートされている。

例えば、ISO 8601 形式では ``2000-12-31T23:59:59Z`` のように
UTC を ``Z`` で表すことができるが、
``time.fromisoformat()`` メソッドや ``datetime.fromisoformat()`` メソッド等では
この形式はサポートされていない。

.. code-block:: python3

   >>> from datetime import datetime

   >>> datetime.fromisoformat("2000-12-31T23:59:59+00:00")
   datetime.datetime(2000, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc)

   >>> datetime.fromisoformat("2000-12-31T23:59:59Z")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: Invalid isoformat string: '2000-12-31T23:59:59Z'

詳細については、 `datetime 標準モジュール`_ のドキュメントを参照されたい。

.. note::

   dateutil_ などサードパーティのライブラリを用いると、
   より多くの ISO 8601 形式の文字列を読み取ることができる。

UNIX 時間
=========

UNIX 時間 (UNIX time, Unix time) は、UTC での 1970 年 1 月 1 日 午前 0 時 0 分 0 秒からの
経過秒数（但し閏秒を無視する）で日時を表したものである。

UNIX 時間は POSIX 時間 (POSIX time, Posix time) やエポック秒 (Epoch time, UNIX Epoch time)
などと呼ばれることもある。

.. note::

   UNIX 時間の正確な定義や歴史についてはここでは触れない。
   多くの場合、上記のような定義で問題ない。

   また、UNIX 時間は通常秒単位だが、
   ミリ秒、マイクロ秒などより細かい単位まで拡張して使用されることも多い。

UNIX 時間も、ISO 8601 形式と同様に日時を表すためによく用いられる。

``datetime`` 型は、UNIX 時間と相互変換が行えるメソッドを提供する。

.. code-block:: python3

   >>> from datetime import datetime, timezone

   >>> d = datetime.fromtimestamp(978274799)
   >>> d
   datetime.datetime(2000, 12, 31, 23, 59, 59)
   >>> d.timestamp()
   978274799.0

   >>> d = datetime.fromtimestamp(978274799.999999, timezone.utc)
   >>> d
   datetime.datetime(2000, 12, 31, 14, 59, 59, 999999, tzinfo=datetime.timezone.utc)
   >>> d.timestamp()
   978274799.999999

.. note::

   ``timestamp()`` や ``fromtimestamp()`` メソッドの動作はプラットフォーム依存であるが、
   通常は殆ど問題にならない。
   詳細については、 `datetime 標準モジュール`_ のドキュメントを参照されたい。

日時や時間に関するその他の標準モジュール
========================================

* `calendar 標準モジュール`_: カレンダーに関する様々な関数群を提供するモジュール
* `time 標準モジュール`_: 時刻に関する様々な関数群を提供するモジュール
* `timeit 標準モジュール`_: 時間を計測するためのシンプルな手段を提供するモジュール

.. _`calendar 標準モジュール`: https://docs.python.org/ja/3/library/calendar.html
.. _`time 標準モジュール`: https://docs.python.org/ja/3/library/time.html
.. _`timeit 標準モジュール`: https://docs.python.org/ja/3/library/timeit.html

``time`` モジュールは ``datetime`` モジュールに比べてより低レベルであり、
プラットフォーム提供の C ライブラリ関数を呼び出す関数などを提供する。

練習問題
========

1. ``User`` クラスに ``registered_at`` 属性（ ``datetime`` 型）を追加せよ。
   ``registered_at`` 属性は、コンストラクタ内で現在日時で初期化せよ。タイムゾーンは UTC とせよ。
2. ``User`` クラスのインスタンスを作成するたびに、 ``registered_at`` 属性が設定されることを確認せよ。
   この日時は、インスタンスを作成した日時に正しく設定されているか。
3. ``regist`` という英単語について調べよ。
4. アプリケーションコード内で日時を扱う場合、以下のように様々な選択肢がある。

   * naive オブジェクトとして扱う
   * aware オブジェクト (UTC) として扱う
   * aware オブジェクト (JST) として扱う

   それぞれのメリット・デメリットを考察せよ。
5. アプリケーションコード外と日時をやりとりする場合、以下のように様々な選択肢がある。

   * ISO 8601 形式の文字列として扱う
   * UNIX 時間の数値として扱う
   * データベースの日付型や時刻型など、固有のデータ型を用いる

   それぞれのメリット・デメリットを考察せよ。
6. 2038 年問題について調べよ。
7. 閏秒について調べよ。
8. Coordinated Universal Time の略がなぜ CUT ではなく UTC なのか調べよ。
