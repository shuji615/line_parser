# line parser
- line のログから特定の語の出現回数を、日付別にカウントするスクリプトです

# 使い方
- conf.yaml の name に、line の log 上の相手と自分の名前を記入
    - conf.yaml の書き方は conf_sample.yaml を参考にしてください
    - 実際の設定ファイル名は "conf.yaml" じゃないと動かないので注意
- conf.yaml の count_words に、数えたい後を記述
- $ python parser.py <lineのlogファイル>

# line の log ファイルの取得方法(2017.11月現在)
- 二人のトークの右上の「∨」を押す
- 「設定」→「トーク履歴を送信」→メールで送信