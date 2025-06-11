# 🎧 音声文字起こしツール 使用方法

## ✅ 必須条件

- ご利用のOSに応じて、以下からバイナリをダウンロードしてください：  
  👉 [https://github.com/aw-leigh/chatGPT-transcription/releases/tag/v1.0.0](https://github.com/aw-leigh/chatGPT-transcription/releases/tag/v1.0.0)

  | OS | ダウンロードファイル名 |
  |----|-------------------------|
  | Windows | `CreateTranscriptionWINDOWS.exe` |
  | macOS   | `CreateTranscriptionMAC`         |
- [Whisper API 利用開始ガイド](https://github.com/aw-leigh/chatGPT-transcription/blob/master/WhisperAPISetupGuide.md)にそって、OpenAI APIキーを環境変数 `OPENAI_API_KEY` に設定していること
- 音声の読み込み・変換のため、FFmpegがインストールされていること：

  - 🪟 **Windows**（管理者権限のPowerShellで実行）：

    ① PowerShell を管理者として起動  
    <img src="https://github.com/user-attachments/assets/9cc54baa-77f3-4fca-b75b-3aed856ed536" height="400">

    ② 以下を順番にコピペして実行：

    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    ```

    ```powershell
    choco install ffmpeg
    ```

  - 🍎 **macOS**：  
    ターミナルで以下を順番にコピペして実行：

    <img src="https://github.com/user-attachments/assets/88da4bd6-b372-409a-9edd-7ac12dfa4fdb">

    ```bash
    brew update
    ```

    ```bash
    brew install ffmpeg
    ```

## 🔄 処理の流れ

1. 音声ファイルを選択またはドラッグ＆ドロップで指定します。
2. ChatGPT Whisper APIには **25MBのファイルサイズ制限** があるため、長時間の音声ファイルは自動的に **最大約45分ごとの区間に分けたコピー** に変換されます。（APIのサイズ制限を超えないように分割し、またOGG形式に変換することでファイルサイズを小さく抑えています）
3. 分割の際は音声の無音部分を検出し、なるべく自然に区切るようにしています。無理に途中で切らず、聞きやすさを考慮しています。
4. 分割されたOGGファイルを一つずつChatGPT Whisper APIに送信し、文字起こし結果をテキストファイルに保存します。
5. 文字起こしが完了したら、一時的に作成されたOGGファイルは自動的に削除されます。

## 🧑‍💻 使い方

### 方法①：🚀 ドラッグ＆ドロップ（**Windowsのみ**）
  
音声ファイル（例: `interview.mp3`）を `CreateTranscriptionWINDOWS.exe` ファイルにドラッグ＆ドロップ  
自動で処理が開始され、**分割 → 圧縮 → 文字起こし → 出力** されます

---

### 方法②：🖱️ 手動でファイルを選択

`.exe` ファイルをダブルクリックで起動  
ファイル選択ダイアログが表示されるので、音声ファイルを選択

## 📄 例

例えば、`interview.mp3` という長めの音声ファイルを処理した場合、

- `interview-1.ogg`
- `interview-2.ogg`

といった約45分ごとの区間に分割されたファイルが作成され、

- `interview-文字起こし-1.txt`
- `interview-文字起こし-2.txt`

という形で文字起こし結果が保存されます。

## ⚠️ 注意事項

- 元の音声ファイルは変更されません。あくまでコピーを区間ごとに分割し処理しています。
- APIの制限やネットワーク環境によっては処理が途中で失敗する可能性があります。
- 文字起こし結果は音声内容や発音状況によって変わるため、必ずしも完全な正確さを保証するものではありません。

## 💰 利用料金について

このツールは **ChatGPTのWhisper API** を使用しており、月額制ではなく「使った分だけ課金される」従量課金制です。

📊 2025年6月時点では、**約150分の音声文字起こしで約 $0.90 USD（約140円）** でした（レートにより変動します）。

ご自身の使用量や料金は以下のページから確認できます：  
👉 [https://platform.openai.com/usage](https://platform.openai.com/usage)
