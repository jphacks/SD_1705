# NagaraMeshi

[![Product Name](nagarameshi.jpg)](https://www.youtube.com/watch?v=sktwu80lrEw)

## 製品概要
### 飯 X Tech

### 背景（製品開発のきっかけ、課題等）

~~ 駅にて ~~   
のざ  「大学行くぞ〜！」  
やや  「でもそろそろお腹すいたな〜」  
のざ  「それなwwww」
のざ  「大学に向かい "ながら" お店探すか~~~」  
やや  「web アプリ "NagaraMeshi" 使いますかぁ」

目的地までの道中で美味しいご飯を食べたい!  
多くのアプリは，特定の位置の周辺のお店を検索します．  
しかし，時には目的地までの経路から遠かったり，回り道になって面倒だったり...
webアプリ "NagaraMeshi"　は目的地まで経路上の飲食店を皆様にお届けいたします！

<!-- ここに
- こんかいのプロダクトの開発に至った背景
- 着目した顧客・顧客の課題・現状
を記入してください -->

### 製品説明（具体的な製品の説明）

"NagaraMeshi"は，目的地までの経路上にあるお店を検索できるwebアプリです。
webアプリなので，特定の機種に限定することなくお使いいただけます。

"NagaraMeshi"のページ(http://nozanoza.ddo.jp/)にアクセスし，twitter IDでログインすると，出発地と到着地(目的地)，経由地が入力できます。出発地と到着地の入力は必須ですが，経由地の入力は任意です。検索ボタンを押すと，「到着地までの経路」と「経路上もしくは経路から近い場所に位置する飲食店」を地図によって示し，さらにShopListでそれぞれの飲食店の情報を提供します。ShopList以上に詳細な情報を知りたい方のために，Hotpepperのページへのリンクも掲載しています。

えっ？　検索結果のお店が多くて迷っちゃう？
そんなあなたも大丈夫！　予算，料理のジャンル，経路上からの距離，到着地への移動手段などを使ってよりお好みのお店を探すことができます！

お店選びの時間ももったいない，美味しかったお店にはまた行きたいというあなたには，お気に入り機能もご用意しています。
お気に入り登録は検索結果のページから簡単に行うことができます。お気に入りに登録している飲食店はユーザページからチェックすることができます。

"NagaraMeshi"は忙しい，でも美味しいご飯を食べたい皆様のためのwebアプリです。

### 特長

#### 1. 目的地までの経路上または経路から近い場所のお店を検索できる

特定の場所の周辺のお店を検索するアプリは世の中に数多くあります。
もちろんそういったアプリはとても便利です。しかし，「どこかに向かうついでに」という場合を考えると，検索目的地に向かう経路から遠ざかってしまうお店が検索結果に多く含まれることもあり，少々不便です。
"NagaraMeshi"は，「目的地に向かうついでに美味しいご飯を食べる」という目的に特化したアプリで，日常生活の様々な場面でお使いいただけます。
例えば，彼女と水族館に行く途中，彼女の大好きなイタリアンのお店を探すとき。
例えば，大事な会議に向かう途中，時間とお金を節約しつつも美味しいお店を探したいとき。
皆様はどんな場面で"NagaraMeshi"を使いたいですか？

#### 2. ブラウザで動く

"NagaraMeshi”はブラウザ上で動作しますので，機種を問わず利用できます。経路の表示等をフル活用するためにGoogle Chromeでの利用が推奨されますが，FireFox等他のブラウザでも動作します。もちろん，PCだけではなくスマートフォンからのアクセスも可能です。

#### 3. フィルタリング機能

特定の場所の周辺のお店を検索するとは言っても，場所によってはたくさんのお店が密集していてどのお店を選ぶか迷ってしまうこともあります。
そんなときには，検索結果のフォルタリング機能を使いましょう。
予算，料理のジャンル，経路上からの距離，到着地への移動手段によるフィルタリング機能で，より皆様の好みに合ったお店探しをサポートします。

### 解決出来ること

"NagaraMeshi"が目的地までの経路に沿ったお店を提示します。
美味しいご飯が食べられるのでお腹満足。
目的地への経路から外れたり回り道をしたりすることがなく，時間を有効に活用することができるので心も満足。

<!-- この製品を利用することによって最終的に解決できることについて記載をしてください。 -->

### 今後の展望
* iOS, Android アプリにする．
* google map api, ホットペッパー Webサービスののオプションをフル活用する．
* お店の検索のための，経路上の点を補間するアルゴリズムの改善

<!-- 今回は実現できなかったが、今後改善すること、どのように展開していくことが可能かについて記載をしてください。 -->


## 開発内容・開発技術
### 活用した技術
#### API・データ
<!-- 今回スポンサーから提供されたAPI、製品などの外部技術があれば記述をして下さい。 -->
* [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/?hl=ja)
* [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/?hl=ja)
* [ホットペッパーWebサービス グルメサーチAPI](https://webservice.recruit.co.jp/hotpepper/reference.html)

#### フレームワーク・ライブラリ・モジュール
* [Flask](http://flask.pocoo.org/)
* [Vue.js](https://jp.vuejs.org/index.html)
* [jQuery](https://jquery.com/)
* [SQLite](https://www.sqlite.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
<!-- 
#### デバイス
* 
*  

### 研究内容・事前開発プロダクト（任意）
ご自身やチームの研究内容や、事前に持ち込みをしたプロダクトがある場合は、こちらに実績なども含め記載をして下さい。

* 
* 
-->

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* apiの経路探索の結果から得られる座標（右左折等のポイントの座標）から，不足している座標の線形補完
<!-- * 独自で開発したものの内容をこちらに記載してください
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください（任意） -->
