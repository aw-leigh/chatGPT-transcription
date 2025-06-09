#!C:\Users\Andrew\Documents\@SideProjects\ChatGPTtranscription\venv\Scripts\python
import sys
import os
from openai import OpenAI
import openai
from pydub import AudioSegment, silence
import tkinter as tk
from tkinter import filedialog
import threading
import time

TARGET_DURATION = 45 * 60 * 1000 # 45 minutes
MAX_FILE_SIZE_MB = 25


class DotPrinter:
    def __init__(self, interval=1):
        self.stop_event = threading.Event()
        self.interval = interval
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return 
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._print_dots)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            self.thread = None

    def _print_dots(self):
        while not self.stop_event.is_set():
            print(".", end="", flush=True)
            time.sleep(self.interval)

def get_file_from_user():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"ドラッグ＆ドロップで受け取ったファイル: {file_path}")
    else:
        file_path = filedialog.askopenfilename(
            title="音声ファイルを選択してください",
            filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac *.m4a"), ("All files", "*.*")]
        )
        if not file_path:
            print("キャンセルされました。")
            sys.exit()

    return file_path


def convert_to_ogg(file_path, file_name, extension, target_ms=TARGET_DURATION):
    dot_printer = DotPrinter()
    
    try:
        print("音声ファイルを分割して圧縮しています: {file_name}{ext}".format(file_name=file_name,ext=extension))
        dot_printer.start()

        audio = AudioSegment.from_file(file_path, extension[1:])
        chunk_start = 0
        chunk_id = 1
        audio_length_ms = len(audio)

        while chunk_start < audio_length_ms:
            chunk_end = min(chunk_start + target_ms, audio_length_ms)
            split_point = chunk_end

            # Try to find a silence near the end
            silence_points = silence.detect_silence(audio[chunk_start:chunk_end], min_silence_len=700, silence_thresh=-40)
            
            if silence_points:
                # Pick the last silence before the end
                last_silence = silence_points[-1][0]
                split_point = chunk_start + last_silence

            chunk = audio[chunk_start:split_point]
            if (len(chunk) == 0):
                break
            filename = "{file_name}-{number}.ogg".format(file_name=file_name,number=(chunk_id))
            chunk.export(filename, format="ogg")

            print(f"\n{filename} を出力しました ({len(chunk) / 1000:.1f} 秒)")
            chunk_start = split_point
            chunk_id += 1
            
        dot_printer.stop()
        print("\n音声ファイルの分割と圧縮が完了しました")

    except Exception as e:
        dot_printer.stop()
        print("エラーが発生しました")
        print("エラー", str(e))
        return

def send_to_chatgpt(ogg_files):
    dot_printer = DotPrinter()
    client = OpenAI()
    prompt = ""
     
    for idx, file in enumerate(ogg_files):

        print('\nChatGPTの文字起こしサービスに「{file}」を送信しています'.format(file=file))
        dot_printer.start()

        with open(file, "rb") as audio_file:
            try:
                transcription = client.audio.transcriptions.create(
                model="whisper-1",
                language="ja",
                file=audio_file,
                prompt=prompt
            )
                print('\n「{}」の文字起こしを保存しています…'.format(file))
                with open("{}-文字起こし-{}.txt".format(file.split('.')[0], idx + 1), "w", encoding="utf8") as output_file:
                    output_file.write(transcription.text)
                print('\n{}-文字起こし-{} を保存しました！'.format(file.split('.')[0], idx + 1))

                prompt = transcription.text

            except openai.error.APIError as e:
                dot_printer.stop()
                print("APIエラー", f"APIError: {e}")
                sys.exit()
            except openai.error.APIStatusError as e:
                dot_printer.stop()
                print("ステータスエラー", f"Status: {e.http_status}\nType: {e.error}\nMessage: {e.error.message}")
                sys.exit()
            except Exception as e:
                dot_printer.stop()
                print("予期せぬエラー: ", str(e))
                sys.exit()
            finally:
                dot_printer.stop()
            
    print("一時ファイルを削除中…")
    for file in ogg_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"{file} の削除に失敗: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = get_file_from_user()
    file_name, extension = os.path.splitext(os.path.basename(file_path))
    
    ogg_files = [file for file in os.listdir('.') if file.endswith('.ogg') and file_name in file]
    
    if len(ogg_files) == 0:
        convert_to_ogg(file_path, file_name, extension)
    
    #get all oggs in directory, find ones with file_name as substring, iterate
    ogg_files = [file for file in os.listdir('.') if file.endswith('.ogg') and file_name in file]
    
    send_to_chatgpt(ogg_files)
    
    input('\n処理が完了しました。終了するには任意のキーを押してください。')
