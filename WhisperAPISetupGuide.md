# 🎓 Whisper API 利用開始ガイド（日本語・初心者向け）

OpenAI の Whisper（音声文字起こし）APIを使うには、以下の手順だけでOKです！

---

## 📌 1. OpenAI アカウントを作成する

1. 下記URLにアクセス：  
   👉 https://platform.openai.com/signup

2. **メールアドレス、Google、または Microsoft アカウント**でサインアップ

   <img src="https://github.com/user-attachments/assets/6131e74f-3003-42c2-be5b-9ba47aa61897" height="600">


4. アカウント作成直後に、以下のような画面が表示されます：

   ### ✅ オーガナイゼーション設定
   - 組織名（任意）を入力
   - 自分の技術レベルを選択：  
     **→「Not technical（非技術者）」を選んでください。**  
     これは設定に影響しませんので安心してください。

   <img src="https://github.com/user-attachments/assets/68adc60c-6f42-40cf-b07e-3e150c9969ed" height="600">

   ### ✅ チーム招待（スキップ可）
   - 他のメンバーのメールを入力する画面が出ますが、何もせず「I'll invite my team later」を押してOKです。

   <img src="https://github.com/user-attachments/assets/8fc67725-3436-44a5-9749-f3b8d1b56281" height="600">

---

## 📌 2. APIキーとプロジェクトを作成する

1. 続いて自動的に「プロジェクト作成 & APIキーの生成」画面になります。適当にプロジェクト名とキー名を入力してください。

   <img src="https://github.com/user-attachments/assets/04edd88e-bfe8-4e8c-a658-643774087d7a" height="600">

2. 「Generate API key」ボタンをクリックすると、APIキー（例：`sk-...`）が表示されます！

   **🚨🚨🚨 この画面で必ずAPIキーをコピーしてください。二度と表示されません！🚨🚨🚨**

   <img src="https://github.com/user-attachments/assets/ec9908f0-6282-4725-ae93-1f2788797c38" height="600">

4. 「Continue」で進んでください。

---

## 📌 3. クレジット購入と支払い登録

1. 次に「Purchase credits（クレジット購入）」画面が表示されます。

2. 最低 $5（¥700程度）を入力して、**Add a payment method（支払い情報追加）**へ進みます。

   <img src="https://github.com/user-attachments/assets/75ed8612-7943-40ac-b083-48fcb8de2335" height="600">

3. クレジットカード情報を入力して、支払い登録を完了してください。
⚠️ Whisper API は無料枠対象外のため、**支払い登録と残高の追加が必須**です。

   <img src="https://github.com/user-attachments/assets/092bc4d5-a51a-40f0-8d1f-4e08e1b8a929" height="600">

---

## 📌 4. APIダッシュボードにアクセスできるようになります

支払い完了後、自動的に APIダッシュボードへリダイレクトされます。  
左メニューから「API keys」などを確認できます。

✅ **これで初期設定は完了です！このページは閉じても大丈夫です。**

あとで以下のことを確認・変更したい場合は、いつでも https://platform.openai.com にアクセスできます：

- クレジット残高を確認する  
- API の使用量（Usage）を確認する  
- 支払い情報や請求先を更新する

---

## 📌 5. APIキーを環境変数に設定する（セキュアな保存方法）

アプリから安全にAPIキーを使うには、`OPENAI_API_KEY` という環境変数として保存します。

---

### 🪟 Windows の場合

1. スタートメニューで「**環境変数**」と検索し、「**システム環境変数の編集**」を選択  
   <img src="https://github.com/user-attachments/assets/4c7e53b0-1811-4a2b-b320-9312e81acbb7" height="700">


2. 「ユーザー環境変数」セクションで「新規(N)...」をクリック
   <img src="https://github.com/user-attachments/assets/0d1a4b46-87b0-4e38-881d-b1b63597f281" height="700">

3. 以下のように入力：

   - 変数名（Variable name）：`OPENAI_API_KEY`  
   - 変数値（Variable value）：（あなたのAPIキー）

   <img src="https://github.com/user-attachments/assets/cbf5b82b-0c48-46f2-833f-d109cff5bce0" width="700">

4. OKを押してすべて閉じてください。

5. 動作確認はコマンドプロンプトを開いて次を実行：

   ```cmd
   echo %OPENAI_API_KEY%
   ```
   → `sk-...` のようなキーが表示されれば設定完了！

---

### 🍎 Mac（または Linux）の場合：環境変数を設定する

Whisper API キーを安全に使うため、環境変数 `OPENAI_API_KEY` を設定しましょう。

#### 🧭 自分のシェル（bash または zsh）を確認する

1. ターミナルを開いて次を実行：

   ```
   echo $SHELL
   ```

   結果の例：

   | 結果         | 使用中のシェル     |
   |--------------|------------------|
   | `/bin/zsh`   | zsh（標準のmacOS） |
   | `/bin/bash`  | bash（古いMacなど） |

---

#### 🛠 zsh の場合（多くのMacはこれ）

```
echo 'export OPENAI_API_KEY="sk-ここにあなたのキー"' >> ~/.zshrc
source ~/.zshrc
```

---

#### 🛠 bash の場合（古いMacやLinux）

```
echo 'export OPENAI_API_KEY="sk-ここにあなたのキー"' >> ~/.bashrc
source ~/.bashrc
```

---

2. 動作確認は次を実行：

   ```cmd
   echo $OPENAI_API_KEY
   ```
   → `sk-...` のようなキーが表示されれば設定完了！

---

## ✅ まとめ：最低限これだけ！

| ステップ         | 必須 | 内容                                     |
|------------------|------|------------------------------------------|
| アカウント作成     | ✅   | OpenAI にサインアップ                     |
| 技術レベル選択     | ✅   | 「Not technical」を選択（推奨）           |
| APIキー作成        | ✅   | `sk-...` 形式のキーを取得                 |
| クレジット購入     | ✅   | $5以上の残高が必要（Whisperは有料）       |
| 支払い登録         | ✅   | クレジットカードを入力                   |
| 環境変数に保存     | ✅   | セキュリティのために環境変数として保存     |

---

## 🚀 これで Whisper API の準備は完了！

これで Python やその他のツールから Whisper API を使って文字起こしができます。

---
