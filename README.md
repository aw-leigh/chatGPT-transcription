# 🎓 Whisper API 利用開始ガイド（日本語・初心者向け）

OpenAI の Whisper（音声文字起こし）APIを使うには、以下の手順だけでOKです！

---

## 📌 1. OpenAI アカウントを作成する

1. 下記URLにアクセス：  
   👉 https://platform.openai.com/signup

2. **メールアドレス、Google、または Microsoft アカウント**でサインアップ  
   ![signup](screenshot-signup.png)

3. ログイン後、自動的に**APIダッシュボード**が表示されます。  
   ![dashboard](screenshot-dashboard.png)

---

## 📌 2. 支払い情報を追加する（Whisper APIは有料）

1. 左下の⚙ **Settings（設定）** → **Billing（請求）** をクリック  
   ![billing](screenshot-billing-menu.png)

2. 「**Payment methods（支払い方法）**」を選択し、クレジットカードを登録  
   ![card](screenshot-card-input.png)

⚠️ Whisper API は無料枠対象外のため、**支払い登録は必須**です。

---

## 📌 3. APIキーを作成する

1. 左側のメニューから「**API keys**」を選びます  
   ![keys](screenshot-api-keys.png)

2. 「**+ Create new secret key**」をクリック  
   ![create](screenshot-create-key.png)

3. 任意のキー名を入力し、キーを作成 → 表示されたキー（例：`sk-...`）を**必ずコピー！**  
   ![copy](screenshot-copy-key.png)

4. 「Done」で終了。もう一度表示はできないので注意！

---

## 📌 4. APIキーを環境変数に設定する（セキュアな保存方法）

スクリプトやアプリから安全にAPIキーを使うには、`OPENAI_API_KEY` という環境変数として保存します。

---

### 🪟 Windows の場合

1. スタートメニューで「**環境変数**」と検索し、「**システム環境変数の編集**」を選択  
   ![win-search](screenshot-env-search.png)

2. 「ユーザー環境変数」セクションで「新規(N)...」をクリック

3. 以下のように入力：

   - 変数名（Variable name）：`OPENAI_API_KEY`  
   - 変数値（Variable value）：（あなたのAPIキー）

   ![win-env](screenshot-win-env.png)

4. OKを押してすべて閉じたら、**コマンドプロンプトを再起動**してください。

5. 動作確認：

   ```cmd
   echo %OPENAI_API_KEY%

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

#### ✅ 動作確認（どちらのシェルでも共通）

```
echo $OPENAI_API_KEY
```

→ `sk-...` のようなキーが表示されれば設定完了！

---

## ✅ まとめ：最低限これだけ！

| ステップ         | 必須 | 内容                                     |
|------------------|------|------------------------------------------|
| アカウント作成     | ✅   | OpenAI にサインアップ                     |
| 支払い登録         | ✅   | Whisper API は無料枠対象外               |
| APIキー作成        | ✅   | `sk-...` 形式のキーを取得                 |
| 環境変数に保存     | ✅   | セキュリティのために環境変数として保存     |

---

## 🚀 これで Whisper API の準備は完了！

これで Python やその他のツールから Whisper API を使って文字起こしができます。

---
