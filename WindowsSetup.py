import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import ctypes
import subprocess
import time
import sys
import threading


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def set_openai_api_key(api_key):
    subprocess.run(['setx', 'OPENAI_API_KEY', api_key], shell=True)


def install_chocolatey():
    try:
        # Run Chocolatey install script
        subprocess.run(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command',
             "Set-ExecutionPolicy Bypass -Scope Process -Force;"
             "[System.Net.ServicePointManager]::SecurityProtocol = "
             "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072;"
             "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"],
            check=True
        )
    except subprocess.CalledProcessError:
        messagebox.showerror("エラー", "Chocolateyのインストールに失敗しました。インターネット接続を確認してください。")
        return False
    return True

def install_ffmpeg():
    # Wait a bit to ensure Chocolatey is ready
    time.sleep(5)

    result = subprocess.run(['choco', 'install', 'ffmpeg', '-y'], shell=True)
    if result.returncode != 0:
        messagebox.showerror(
            "エラー",
            "ffmpegのインストールに失敗しました。\n\n"
            "管理者としてPowerShellを開き、以下のコマンドを手動で実行してください：\n"
            "choco install ffmpeg -y"
        )
        return False
    return True


def update_progress(progress_bar, value):
    progress_bar['value'] = value
    root.update_idletasks()


def setup_environment(api_key, progress_bar):
    try:
        update_progress(progress_bar, 10)
        set_openai_api_key(api_key)

        update_progress(progress_bar, 40)
        if not install_chocolatey():
            messagebox.showerror("エラー", "環境変数の設定に失敗しました。")
            return

        update_progress(progress_bar, 70)
        if not install_ffmpeg():
            messagebox.showerror("エラー", "ffmpegのインストールに失敗しました。")
            return

        update_progress(progress_bar, 100)
        messagebox.showinfo("完了", "セットアップが完了しました！\nPCを再起動すると設定が反映されます。")

    except Exception as e:
        messagebox.showerror("エラー", f"エラーが発生しました: {str(e)}")


def on_start_setup():
    api_key = simpledialog.askstring("APIキーの入力", "OpenAIのAPIキーを入力してください:")
    if not api_key:
        messagebox.showwarning("キャンセル", "APIキーの入力がキャンセルされました。")
        return

    threading.Thread(target=setup_environment, args=(api_key, progress_bar)).start()

def quit_setup():
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("OpenAI + ffmpeg セットアップ")

if not is_admin():
    messagebox.showerror("管理者権限が必要", "このスクリプトを実行するには、管理者として起動してください。")
    root.destroy()
    sys.exit()

frame = ttk.Frame(root, padding=20)
frame.grid()

label = ttk.Label(frame, text="OpenAI APIキーとffmpegのセットアップを開始します。\n OpenAIのAPIキーを用意してください")
label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
progress_bar.grid(row=1, column=0, columnspan=2, pady=(0, 10))

start_button = ttk.Button(frame, text="セットアップ開始", command=on_start_setup)
start_button.grid(row=2, column=0, columnspan=2)

finish_button = ttk.Button(frame, text="終了", command=quit_setup)
finish_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
