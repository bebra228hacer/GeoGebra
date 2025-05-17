import json
import openai
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox, TclError
import os.path
import subprocess
import datetime
import chatgpt
import Win_support
import pyserver
import webbrowser
from flask import render_template
import threading
from PIL import ImageGrab
import base64
import io
import time
import shutil

_location = os.path.dirname(__file__)
_bgcolor = "#d9d9d9"
_fgcolor = "#000000"
_tabfg1 = "black"
_tabfg2 = "white"
_bgmode = "light"
_tabbg1 = "#d9d9d9"
_tabbg2 = "gray40"
_style_code_ran = 0

with open("config.json") as cfile:
    config_file = json.load(cfile)


def _style_code():
    global _style_code_ran
    if _style_code_ran:
        return
    try:
        Win_support.root.tk.call(
            "source", os.path.join(_location, "themes", "default.tcl")
        )
    except:
        pass
    style = ttk.Style()
    style.theme_use("default")
    style.configure(".", font="TkDefaultFont")
    if sys.platform == "win32":
        style.theme_use("winnative")
    _style_code_ran = 1


class Toplevel1:
    def __init__(self, top=None):

        self.url = "http://127.0.0.1:"
        self.port = 5000

        _style_code()
        try:
            self.thread = chatgpt.user_get_thread()

        except openai.PermissionDeniedError as e:
            self.thread = "error"
            messagebox.showerror("Ошибка", "Включите прокси/впн с доступом к чатгпт!")
        top.geometry("740x920+690+212")
        top.resizable(0, 0)
        top.title(f"GeoGebra generator")
        self.top = top
        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)
        self.menubar.add_command(
            compound="left",
            label="Справка",
            command=lambda: (subprocess.Popen(["notepad.exe", "readme.md"])),
        )
        self.menubar.add_command(
            compound="left",
            label="Перезагрузить",
            command= lambda:(self.reset()),
        )
        self.sub_menu = tk.Menu(
            self.menubar, borderwidth=1, foreground="#000000", tearoff=0
        )
        self.menubar.add_cascade(
            compound="left",
            label="Файлы",
            menu=self.sub_menu,
        )
        self.sub_menu.add_command(
            compound="left",
            label="Текущий файл",
            command=lambda: (self.open_current_file()),
        )
        self.sub_menu.add_command(
            compound="left",
            label="Папка с файлами",
            command=lambda: subprocess.Popen(["explorer", "saved_file"]),
        )
        self.sub_menu.add_command(
            compound="left", 
            label="Очистить кеш", 
            command=lambda:(self.delete_all_file("temp"))
        )
        self.sub_menu.add_command(
            compound="left", 
            label="Очистить папку", 
            command=lambda:(self.delete_all_file("saved_file"))
        )
        self.Text1 = tk.Text(self.top)
        self.Text1.place(relx=0.027, rely=0.011, relheight=0.196, relwidth=0.946)
        self.Text1.bind("<<Paste>>", self.paste_text)
        self.Text1.insert(
            tk.END,
            "Поле для вставки текста. Поддерживает рассшифровку текста с картинки\n",
        )

        self.Text2 = tk.Text(self.top)
        self.Text2.place(relx=0.027, rely=0.261, relheight=0.734, relwidth=0.946)
        self.Text2.tag_configure("red", foreground="red")

        if self.thread != "error":
            self.Text2.insert(
                tk.END, "Программа работает корректно, введите запрос выше\n"
            )
        else:
            self.Text2.insert(
                tk.END, "Включите прокси/впн с доступом к чатгпт\n", "red"
            )

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.027, rely=0.21, height=40, width=350)
        self.Button1.configure(command=lambda: (self.Text1.delete("1.0", tk.END)))
        self.Button1.configure(takefocus=0)
        self.Button1.configure(text="""Сбросить""")

        self.Button2 = ttk.Button(self.top)
        self.Button2.place(relx=0.5, rely=0.21, height=40, width=350)
        self.Button2.configure(command=self.Button2_click)
        self.Button2.configure(takefocus=0)
        self.Button2.configure(text="""Отправить""")

    
    def reset(self):
        try:
            self.thread = chatgpt.user_get_thread()
        except openai.PermissionDeniedError as e:
            self.thread = "error"
            messagebox.showerror("Ошибка", "Включите прокси/впн с доступом к чатгпт!")
        self.Text1.delete("1.0", tk.END)
        self.Text2.delete("1.0", tk.END)
        self.Text2.insert(
                tk.END,
                "Успешно перезагружено",
            )
    
    def delete_all_file(self, directory):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        temp_folder_path = os.path.join(script_dir, directory)
        try:
            if os.path.exists(temp_folder_path):
                shutil.rmtree(temp_folder_path)
            os.makedirs(temp_folder_path, exist_ok=True)
        except OSError as e:
            print(f"Error creating/clearing folder {temp_folder_path}: {e}")

    def message_to_chat_gpt(self, input_text, thread):
        if thread == "error":
            return "GET__VPN=(0,0)"
        to_graph_gen = chatgpt.chat_gpt_req(
            thread, text=input_text, assist_id=config_file["MATH_ASSIST"]
        )
        text_to_gen = chatgpt.chat_gpt_req(
            thread,
            text="Используй твой прошлый ответ в этом треде, сверься с моим прошлым запросом и исполни промпт",
            assist_id=config_file["GRAPH2D_ASSIST"],
        ).replace("\\n", "\n")
        lines = text_to_gen.splitlines()
        formatted_string = r"\n".join(lines)
        return formatted_string

    def Button2_click(self):
        self.Text2.insert(
            tk.END, "Ваш запрос зарегистрирован, это может занять около 10 секунд\n"
        )
        time.sleep(10)
        command_to_server = self.message_to_chat_gpt(
            self.Text1.get("1.0", tk.END), self.thread
        )
        self.Text2.insert(tk.END, "Запрос к ChatGPT успешно отправлен\n")
        print(command_to_server)
        webbrowser.open(self.url + str(self.port))
        if self.port == 5050:
            messagebox.showerror(
                "Предупреждение",
                "Возможно потребуется полный перезапуск приложения для дальнейшей корректной работы",
            )
        current_time = self.get_current_time()
        app = pyserver.create_app(f"saved_file/GeoGebra_file_{current_time}.ggb")

        @app.route("/")
        def index(initial_command=command_to_server):
            return render_template("main.html", initial_command=initial_command)

        def run_app():
            app.run(debug=False, use_reloader=False, port=self.port)

        threading.Thread(target=run_app, daemon=True).start()
        self.port = self.port + 1
        self.Text2.insert(tk.END, "Файл сгенерирован!\n")

    def paste_text(self, event=None):
        print(1)
        try:
            try:
                text = self.top.clipboard_get()
                try:
                    text = text.encode("utf-8").decode("utf-8")
                except UnicodeEncodeError:
                    try:
                        text = text.encode("latin-1").decode("utf-8")
                    except UnicodeEncodeError:
                        try:
                            text = text.encode("cp1251").decode("utf-8")
                        except:
                            print("Не удалось декодировать текст из буфера обмена.")
                            messagebox.showerror(
                                "Ошибка", "Не удалось декодировать текст."
                            )
                            return "break"

                self.Text1.insert(tk.INSERT, text)
                return "break"

            except TclError:
                self.Text2.insert(
                    tk.END,
                    "Обработка вставленного изображения, это может занять несколько секунд\n",
                )
                try:
                    img = ImageGrab.grabclipboard()
                    if img:
                        buffered = io.BytesIO()
                        format = "PNG"
                        img.save(buffered, format=format)
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        self.Text1.insert(tk.END, f"{chatgpt.image_to_text(img_str)}\n")
                        self.Text2.insert(tk.END, "Текст рассшифрован\n")
                        return "break"
                    else:
                        print("В буфере обмена нет ни текста, ни изображения.")
                        messagebox.showinfo(
                            "Информация",
                            "В буфере обмена нет ни текста, ни изображения.",
                        )
                        return "break"

                except Exception as e:
                    print(f"Ошибка при работе с изображением: {e}")
                    messagebox.showerror(
                        "Ошибка", f"Ошибка при работе с изображением: {e}"
                    )
                    return "break"

        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")
            return "break"

    def get_current_time(self):
        now = datetime.datetime.now()
        self.current_time = now.strftime("%Y%m%d_%H%M%S")
        return self.current_time

    def open_current_file(self):
        if not hasattr(self, "current_time"):
            messagebox.showerror("Ошибка", "Сначала нужно создать файл!")
            return
        filepath = os.path.join("saved_file", f"GeoGebra_file_{self.current_time}.ggb")
        print(filepath)
        if os.path.exists(filepath):
            try:
                subprocess.Popen(["explorer", "/select,", filepath])
            except Exception as e:
                print(f"Произошла ошибка при открытии файла: {e}")
        else:
            messagebox.showerror("Ошибка", "Файл еще не создан!")


def start_up():
    Win_support.main()


if __name__ == "__main__":
    start_up()
