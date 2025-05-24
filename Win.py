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
import shutil
import re
import math

_bgcolor = "#d9d9d9"
_fgcolor = "#000000"

with open("config.json") as cfile:
    config_file = json.load(cfile)


class Toplevel1:
    def __init__(self, top=None):

        self.url = "http://127.0.0.1:"
        self.port = 5000

        try:
            self.thread = chatgpt.user_get_thread()

        except openai.PermissionDeniedError as e:
            self.thread = "error"
            messagebox.showerror(
                "Ошибка",
                "Включите прокси/впн с доступом к чатгпт и перезагрузите приложение!",
            )
        top.geometry("740x920+690+212")
        top.resizable(0, 0)
        top.title(f"AI GeometryGenerator")
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
            command=lambda: (threading.Thread(target=self.reset, daemon=True).start()),
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
            command=lambda: (self.delete_all_file("temp")),
        )
        self.sub_menu.add_command(
            compound="left",
            label="Очистить папку",
            command=lambda: (self.delete_all_file("saved_file")),
        )
        self.Text1 = tk.Text(self.top)
        self.Text1.place(relx=0.027, rely=0.011, relheight=0.196, relwidth=0.946)
        self.Text1.insert(tk.END, f"Это текствое поле поддерживет интерактивный ввод изображений из буфера обмена")
        self.Text1.bind("<<Paste>>", lambda event:(threading.Thread(target=self.paste_text, daemon=True).start()))

        self.Text2 = tk.Text(self.top)
        self.Text2.place(relx=0.027, rely=0.261, relheight=0.734, relwidth=0.946)
        self.Text2.tag_configure("red", foreground="red")
        if self.thread != "error":
            self.logging_on_Text2("Программа работает корректно, введите запрос выше\n")
        else:
            self.Text2.insert(
                tk.END,
                f"[TERMINAL_{self.port-5000}]>> Включите прокси/впн с доступом к чатгпт\n",
                "red",
            )

        self.Button1 = ttk.Button(self.top)
        self.Button1.place(relx=0.027, rely=0.205, height=50, width=350)
        self.Button1.configure(command=lambda: (self.Text1.delete("1.0", tk.END)))
        self.Button1.configure(takefocus=0)
        self.Button1.configure(text="""Сбросить""")

        self.Button2 = ttk.Button(self.top)
        self.Button2.place(relx=0.5, rely=0.205, height=50, width=350)
        self.Button2.configure(
            command=lambda: (
                threading.Thread(target=self.Button2_click, daemon=True).start()
            )
        )
        self.Button2.configure(takefocus=0)
        self.Button2.configure(text="""Отправить""")

    def reset(self):
        self.Button2.config(state=tk.DISABLED)
        self.menubar.entryconfig(2, state=tk.DISABLED)
        try:
            self.thread = chatgpt.user_get_thread()
        except openai.PermissionDeniedError as e:
            self.thread = "error"
            messagebox.showerror("Ошибка", "Включите прокси/впн с доступом к чатгпт!")
            return None
        self.Text1.delete("1.0", tk.END)
        self.Text2.delete("1.0", tk.END)
        self.port = self.port + 1
        self.logging_on_Text2("Успешно перезагружено\n")
        self.Button2.config(state=tk.NORMAL)
        self.menubar.entryconfig(2, state=tk.NORMAL)

    def delete_all_file(self, directory):
        script_dir = None  # Инициализируем script_dir значением None
        # Определяем базовый путь.  Если запущено из EXE, то используем sys.executable.
        if getattr(sys, 'frozen', False):
            script_dir = os.path.dirname(sys.executable) # Путь к исполняемому файлу
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__)) # Путь к скрипту .py

        # Проверяем, что script_dir был успешно определен
        if script_dir is None:
            print("Ошибка: Не удалось определить script_dir.")
            return  # Выходим из функции, если не удалось определить путь

        temp_folder_path = os.path.join(script_dir, directory)
        try:
            if os.path.exists(temp_folder_path):
                shutil.rmtree(temp_folder_path)
            os.makedirs(temp_folder_path, exist_ok=True)
        except OSError as e:
            print(f"Error creating/clearing folder {temp_folder_path}: {e}")
        self.logging_on_Text2("Папка очищена\n")


    


    def style_wrapper(self, object_generation):
        style_generation = ''
        angle_colors = [(0, 100, 0), (204, 0, 102), (83, 172, 248)]
        angle_index = 0
        points = {}
        lines = {} # Добавим словарь для хранения линий (биссектрис)
        for item in object_generation:
            item = item.strip()
            parts = item.split("=")
            name = parts[0].strip()  # Имя объекта

            if len(parts) > 1:
                definition = parts[1].strip()  # Определение объекта (например, "(0,0)" или "Segment(A, B)")
            else:
                definition = ""

            # Точка
            if re.match(r"^\(\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*\)$", definition):
                x, y = map(float, definition.replace("(", "").replace(")", "").split(","))
                points[name] = [x, y]
                print(points)
                style_generation = style_generation + f'api.setColor("{name}", 0,0,0);\n'
                style_generation = style_generation + f'api.setLabelVisible("{name}", true);\n'
                style_generation = style_generation + f'api.setPointSize("{name}", 4);\n'
                style_generation = style_generation + f'api.setCaption("{name}",' + r'"$\\LARGE{%n}$");' + '\n'
                style_generation = style_generation + f'api.setLabelStyle("{name}", 3);\n'

            # Midpoint
            elif re.match(r"^Midpoint\([A-Z_]+, [A-Z_]+\)$", definition):
                A, B = list(definition.replace("Midpoint(", "").replace(")", "").split(","))
                A = A.strip()
                B = B.strip()
                x = (points[A][0] + points[B][0]) / 2
                y = (points[A][1] + points[B][1]) / 2
                points[name] = [x, y]
                print(points)
                style_generation = style_generation + f'api.setColor("{name}", 0,0,0);\n'
                style_generation = style_generation + f'api.setLabelVisible("{name}", true);\n'
                style_generation = style_generation + f'api.setPointSize("{name}", 4);\n'
                style_generation = style_generation + f'api.setCaption("{name}",' + r'"$\\LARGE{%n}$");' + '\n'
                style_generation = style_generation + f'api.setLabelStyle("{name}", 3);\n'
                    
            # Отрезок
            elif re.match(r"^Segment\([A-Z_]+, [A-Z_]+\)$", definition):
                style_generation = style_generation + f'api.setColor("{name}", 0,0,0);\n'
                style_generation = style_generation + f'api.setLabelVisible("{name}", false);\n'
                style_generation = style_generation + f'api.setLineThickness("{name}", 5);\n'

            # Угол
            elif re.match(r"^Angle\([A-Z_]+, ?[A-Z_]+, ?[A-Z_]+\)$", definition):
                print(points)
                A, B, C = list(definition.replace("Angle(", "").replace(")", "").split(","))
                A = A.strip()
                B = B.strip()
                C = C.strip()
                
                AB_x, AB_y = points[A][0] - points[B][0], points[A][1] - points[B][1]
                BC_x, BC_y = points[C][0] - points[B][0], points[C][1] - points[B][1]

                dot_product = AB_x * BC_x + AB_y * BC_y
                AB_magnitude = math.sqrt(AB_x**2 + AB_y**2)
                BC_magnitude = math.sqrt(BC_x**2 + BC_y**2)

                cosine_angle = dot_product / (AB_magnitude * BC_magnitude)
                angle = math.degrees(math.acos(cosine_angle))
                print(f"Angle {name}: {angle}")

                if abs(angle - 90) <= 5:
                    r, g, b = 0, 100, 0
                else:
                    r, g, b = angle_colors[angle_index % len(angle_colors)]
                    angle_index += 1
                style_generation = style_generation + f'api.setColor("{name}", {r},{g},{b});\n'
                style_generation = style_generation + f'api.setLabelVisible("{name}", false);\n'
                style_generation = style_generation + f'api.setLineThickness("{name}", 5);\n'

            # AngleBisector
            elif re.match(r"^AngleBisector\([A-Z_]+, ?[A-Z_]+, ?[A-Z_]+\)$", definition):
                lines[name] = definition  # Сохраняем определение биссектрисы для дальнейшего использования
                style_generation = style_generation + f'api.setColor("{name}", 128, 128, 128);\n'  # Серый цвет
                style_generation = style_generation + f'api.setLabelVisible("{name}", false);\n'
                style_generation = style_generation + f'api.setLineThickness("{name}", 3);\n'
                style_generation = style_generation + f'api.setLineStyle("{name}", "dashed");\n' # Пунктирная линия
                #  Обратите внимание: здесь ничего не вычисляется!  Только стилизация.


            else:
                style_generation = style_generation + f'api.setLabelVisible("{name}", false);\n'

            return style_generation
    
    
    def Button2_click(self):
        self.menubar.entryconfig(2, state=tk.DISABLED)
        self.Button2.config(state=tk.DISABLED)
        self.logging_on_Text2(
            "Ваш запрос зарегистрирован, это может занять около 10 секунд\n"
        )
        if self.thread == "error":
            messagebox.showerror(
                "Ошибка",
                "Приложение было запушено без VPN, перезапустите приложение",
            )
            return None
        if self.port == 5050:
            messagebox.showerror(
                "Предупреждение",
                "Возможно потребуется полный перезапуск приложения для дальнейшей корректной работы",
            )
        a = chatgpt.chat_gpt_req(
            self.thread, text=self.Text1.get("1.0", tk.END), assist_id=config_file["MATH_ASSIST"]
        )
        uncleaned_output = chatgpt.chat_gpt_req(
            self.thread,
            text="Используй твой прошлый ответ в этом треде, сверься с моим прошлым запросом и исполни промпт",
            assist_id=config_file["GRAPH2D_ASSIST"],
        )
        line_by_line_output = uncleaned_output.replace("\\n", "\n").splitlines()
        object_generation = r"\n".join(line_by_line_output).replace(" ", "")
        self.logging_on_Text2("Идет создание стилей\n")
        style_generation = self.style_wrapper(line_by_line_output)

        command_to_server = f'''api.evalCommand("{object_generation}");\n''' + style_generation
        current_time = self.get_current_time()
        app = pyserver.create_app(f"saved_file/GeoGebra_file_{current_time}.ggb")

        @app.route("/")
        def index(initial_command=command_to_server):
            return render_template("main.html", initial_command=initial_command)

        webbrowser.open(self.url + str(self.port))

        def run_app():
            app.run(debug=False, use_reloader=False, port=self.port)

        threading.Thread(target=run_app, daemon=True).start()
        self.logging_on_Text2("Файл сгенерирован!\n")
        self.port = self.port + 1
        self.Button2.config(state=tk.NORMAL)
        self.menubar.entryconfig(2, state=tk.NORMAL)
    def logging_on_Text2(self, text):
        self.Text2.insert(tk.END, f"[TERMINAL_{self.port-5000}]>> {text}")

    def paste_text(self, event=None):
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
                self.logging_on_Text2("Обработка вставленного изображения, это может занять несколько секунд\n")
                try:
                    img = ImageGrab.grabclipboard()
                    if img:
                        buffered = io.BytesIO()
                        format = "PNG"
                        img.save(buffered, format=format)
                        img_str = base64.b64encode(buffered.getvalue()).decode()
                        self.Text1.insert(tk.END, f"{chatgpt.image_to_text(img_str)}\n")
                        self.logging_on_Text2("Текст рассшифрован\n")
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
