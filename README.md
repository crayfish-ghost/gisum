# gisum

## 概要
gisumは、GitHubのIssueを読み込み、OpenAIのChatGPTを使って要約するスクリプトです。  
ChatGPTの入力上限を超えた長いIssueでも、テキストを再帰的に要約することで入力上限を回避しています。

## 実行方法
環境変数にOPENAIとgithubのAPIキーを設定した上で、下記のコマンドでgisumを実行できます。  

### bashrc
```bash
export OPENAI_API_KEY="{OPENAIのAPIkey}"
export GITHUB_API_KEY="{githubのAPIkey}"
```

### コマンド
```bash
python3 gisum.py {githubのIssueのURL}
```

## 実行例
```bash
$ python3 gisum.py https://github.com/ztjhz/BetterChatGPT/issues/83
Sorry this comment is too long, eliminated:
https://github.com/ztjhz/BetterChatGPT/issues/83#issuecomment-1492919219
all comments:18
Now summarizing 18 comments ... ( last 0 )

議論のテーマ: CentOS8サーバーのデプロイに関する問題
ステータス: 解決済み
内容:
このGitHubの問題は、CentOS8サーバーのデプロイに関する問題が話題となっています。
最初の問題は、パブリックIPアドレスが有効にならず、ポート5173がnpm run devを実行した後に実行されないことでした。
解決策として、vite.config.tsファイルに「host：'0.0.0.0'」フィールドを追加することが提案されました。
また、npm buildを使用して静的ファイルをコンパイルし、nginxをリバースプロキシとして使用することも提案されました。
問題は、npmをバージョン9.6.3に更新し、「npm run build」を再実行することで解決されました。
最後に、NginxのHTTP Basic Authenticationを使用して、ページにアカウントパスワード認証を設定する方法について説明されました。
この方法で問題は解決され、CentOS8サーバーのデプロイに関する問題が解決されました。
```

## 注意点
- gisumは再帰的にChatGPTのAPIを繰り返し呼び出すため、Issueのcomment量によっては課金額が高額になる可能性があります
- 画像で説明されているissueのコメントは要約に反映されません
- 長過ぎるcomment(デフォルトで2000token以上)はpromptが作れなくなる恐れがあるため要約対象外としています
- issueが長くなればなるほど要約の精度は低くなると思います

## ライセンス
MIT
