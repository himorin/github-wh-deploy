# GitHub Webhookをトリガーとしたコンテンツデプロイ

## 機能要件

* GitHubのwebhookからの通知で、更新があったレポジトリ名とブランチ名のペアが正しい場合に、該当ディレクトリで`git update`を行う
* レポジトリ名、ブランチ名、展開先ディレクトリ名、のデータを設定できるようにする (対外URLなどの関連データもメモとして付けられるようにする？)
* 管理用データはいったんはファイルのみで手編集とする
* ログは管理系のディレクトリにファイルで溜めていく
* 将来拡張？
  * 管理系・ログ系のデータのデータベース化

## 導入・設定

* 適当なディレクトリにレポジトリをクローンする
* ディレクトリに対しての設定
  * `httpd`ディレクトリをサーバで公開してCGIを有効にする
* `common/siteconfig.json`を作成する
* github webhookに`githook.cgi`の公開URLを設定する
  * URLの設定
  * `content-type`は`application/json`に設定する
  * `push event`をターゲットで選択する
  * `secret`は不要
* `common/ghwh`ディレクトリをhttpdから書き込めるように用意、一時的デバッグ用のjson保存領域

### siteconfig.json

必要な設定はこのファイルに全部まとまっている。
詳細は`common/siteconfig.json.skel`を参照。


## 参考メモ

* [webhookのjsonデータ](webhook_json.md)
