# Discord Timer Bot

このプロジェクトは、Discord 上でタイマー機能を提供するボットです。

## デプロイ先

このボットは [Render.com](https://render.com) にデプロイされています。

## 使用方法

### コマンド一覧

- `!names <肯定側名> <否定側名> [ランダム化 (オプション)]` - 肯定側と否定側の名前を設定します。オプションの第三引数に 1、true、y、yes を入力するとランダム化が行われます。
- `!t, !times <時間1> <時間2> ... <時間4>` - 各フェーズの時間を設定します。
- `!start` - ディベートを開始します。
- `!stop` - 現在のフェーズを中断します。
- `!n, !next` - 次のフェーズに進みます。
- `!p, !prev` - 前のフェーズに戻ります。
- `!end` - ディベートを終了します。
- `!settings` - 現在の設定を表示します。
- `!f, !flow` - ディベートの全体の流れを表示します。
- `!c, !current` - 現在のフェーズを表示します。
- `!st, !topics, !tp, !suggest` - ランダムに 5 つの論題を提案します。
- `!add, !newtopic, !addtopic <論題>` - 新しい論題を追加します。
- `!remove, !deletetopic, !removetopic <論題>` - 既存の論題を削除します。
- `!alltopics, !listtopics, !showtopics` - 現在の論題リストを表示します。
- `!settopic <論題>` - 現在の論題を設定します。
- `!prepare` - ディベートの準備フェーズを開始します。参加者はこの時間を使って準備を行います。
- `!h, !debate, !hd, !dh, !help_debate` - このヘルプメッセージを表示します。

## 開発

### 環境設定

1. リポジトリをクローンします。
   ```sh
   git clone https://github.com/yourusername/discord-timer-bot.git
   cd discord-timer-bot
   ```
