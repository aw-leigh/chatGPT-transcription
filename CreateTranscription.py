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

TARGET_DURATION_SEC = 45 * 60  # 45 minutes
MAX_FILE_SIZE_MB = 25


class DotPrinter:
    def __init__(self, interval=1):
        self.stop_event = threading.Event()
        self.interval = interval
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            print("Dot printer is already running.")
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


def convert_to_ogg(file_path, file_name, extension, target_sec=TARGET_DURATION_SEC):
    dot_printer = DotPrinter()
    
    try:
        print("音声ファイルを分割して圧縮しています: {file_name}{ext}".format(file_name=file_name,ext=extension))
        dot_printer.start()

        audio = AudioSegment.from_file(file_path, extension[1:])
        chunk_start = 0
        chunk_id = 1
        audio_length_ms = len(audio)

        while chunk_start < audio_length_ms:
            # Estimate the end of the chunk
            chunk_end = chunk_start + target_sec * 1000

            # Limit to file end
            chunk_end = min(chunk_end, audio_length_ms)

            # Try to find a silence near the end
            chunk_segment = audio[chunk_start:chunk_end]
            silence_points = silence.detect_silence(chunk_segment, min_silence_len=700, silence_thresh=-40)
            
            if silence_points:
                # Pick the last silence before the end
                last_silence = silence_points[-1][0]
                split_point = chunk_start + last_silence
            else:
                # No silence found; hard split
                split_point = chunk_end

            chunk = audio[chunk_start:split_point]
            if (len(chunk) == 0):
                break
            filename = "{file_name}-{number}.ogg".format(file_name=file_name,number=(chunk_id))
            chunk.export(filename, format="ogg")

            print(f"Exported: {filename} ({len(chunk) / 1000:.1f} seconds)")
            chunk_start = split_point
            chunk_id += 1
            
        dot_printer.stop()
        print("\n音声ファイルの分割と圧縮が完了しました")
        
    except: 
        dot_printer.stop()
        print('error :(') 
        errors = sys.exc_info() 
        for e in errors: 
            print(str(e)) 
            input('\nPress enter to exit.') 
            exit()

def send_to_chatgpt(ogg_files):
    dot_printer = DotPrinter()
    client = OpenAI()
    prompt = ""
     
    for idx, file in enumerate(ogg_files):
        audio_file = open("./{file}".format(file=file), "rb")
        
        print('\nChatGPTの文字起こしサービスに「{file}」を送信しています'.format(file=file))
        dot_printer.start()
         
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
            # Print the full error message
            dot_printer.stop()
            print(f"APIError: {e}")
            input("Press Enter to exit...")
        except openai.error.APIStatusError as e:
            # For status-related errors, print the status code and other details
            dot_printer.stop()
            print(f"Status Code: {e.http_status}")
            print(f"Error Type: {e.error}")
            print(f"Error Message: {e.error.message}")
            input("Press Enter to exit...")
        except Exception as e:
            # Catch-all for any other exceptions
            dot_printer.stop()
            print(f"An unexpected error occurred: {e}")
            input("Press Enter to exit...")        
        finally:
            dot_printer.stop()  

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    file_name, extension = os.path.splitext(os.path.basename(file_path))
    
    ogg_files = [file for file in os.listdir('.') if file.endswith('.ogg') and file_name in file]
    
    if len(ogg_files) == 0:
        convert_to_ogg(file_path, file_name, extension)
    
    #get all oggs in directory, find ones with file_name as substring, iterate
    ogg_files = [file for file in os.listdir('.') if file.endswith('.ogg') and file_name in file]
    
    send_to_chatgpt(ogg_files)
    
    input('\n完了しました。終了するには任意のキーを押してください。')
