# GitHub WebhookでPOSTされてくるjsonデータの必要な値の一覧

* `ref`: `git ref` (`refs/heads/main`など)
* `repository.full_name`: レポジトリの名前 (`himorin/github_wh_deploy`など)
* `repository.updated_at`: commitの更新日時 (ISO8601)
* `repository.pushed_at`: github上へ届いた更新日時 (unixtime)

* 多分使わない
  * `before`, `after`: commit前後のハッシュ
  * `commits.[id].*`: 関連付いているcommitのメタデータの配列
