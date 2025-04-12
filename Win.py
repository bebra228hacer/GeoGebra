import json
import openai
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox
import os.path
import subprocess
import datetime
import chatgpt
import Win_support
import pyserver
import webbrowser
from flask import render_template
import threading

_location = os.path.dirname(__file__)
_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 
_style_code_ran = 0

with open("config.json") as cfile:
    config_file = json.load(cfile)
url = "http://127.0.0.1:5000" 


def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: Win_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "TkDefaultFont")
    if sys.platform == "win32":
        style.theme_use('winnative')    
    _style_code_ran = 1

def message_to_chat_gpt(input_text, thread):
    if thread == "error":
        return "Вам нужен впн/прокси с поддержкой чатгпт!"
    to_graph_gen = chatgpt.chat_gpt_req(thread, text = input_text, assist_id=config_file["MATH_ASSIST"])
    print(to_graph_gen)
    text_to_gen = chatgpt.chat_gpt_req(thread, text = "Используй твой прошлый ответ в этом треде, сверься с моим прошлым запросом и исполни промпт", assist_id=config_file["GRAPH2D_ASSIST"]).replace("\\n", "\n")
    print("\n", text_to_gen)
    lines = text_to_gen.splitlines()  
    formatted_string = r"\n".join(lines)
    return formatted_string

def open_current_file(current_time):
    filepath = os.path.join("saved_file", f"GeoGebra_file_{current_time}.ggb")
    print(filepath)
    if os.path.exists(filepath):
        try:
            subprocess.Popen(['explorer', '/select,', filepath])
        except Exception as e:
            print(f"Произошла ошибка при открытии файла: {e}")  
    else:
        messagebox.showerror("Ошибка", "Файл еще не создан!")

def server(initial_command = r"MEOW = (0,0)"):
    webbrowser.open(url)
    app = pyserver.create_app(f"saved_file/GeoGebra_file_{current_time}.ggb")
    @app.route('/')
    def index(initial_command = initial_command):    
        return render_template('test.html', initial_command=initial_command) 
    app.run(debug=False, use_reloader=False, port=5000)
    




class Toplevel1:
    def __init__(self, top=None):
        
        global current_time 
        global thread
        
        _style_code()
        try:
            thread = chatgpt.user_get_thread()

        except openai.PermissionDeniedError as e:
            thread = "error"
            messagebox.showerror("Ошибка", "Включите прокси/впн с доступом к чатгпт!")
        now = datetime.datetime.now()
        current_time = now.strftime("%Y%m%d_%H%M%S")
        top.geometry("740x920+690+212")
        top.resizable(0,  0)
        top.title(f"GeoGebra generator       {datetime.datetime.now()}")

        self.top = top

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)
        self.menubar.add_command(compound='left', label='Справка', command = lambda:(subprocess.Popen(["notepad.exe", "readme.md"])))
        self.menubar.add_command(compound='left', label='Перезагрузить', command = lambda:(messagebox.showerror("Ошибка", "Декоративная кнопка")))
        self.sub_menu = tk.Menu(self.menubar, borderwidth=1, foreground='#000000',tearoff=0)
        self.menubar.add_cascade(compound='left', label='Файлы',menu=self.sub_menu, )
        self.sub_menu.add_command(compound='left', label='Текущий файл', command = lambda:(open_current_file(current_time)))
        self.sub_menu.add_command(compound='left', label='Папка с файлами', command = lambda:subprocess.Popen(['explorer', "saved_file"]))
        self.sub_menu.add_command(compound='left', label='Очистить кеш')

        
        self.Text1 = tk.Text(self.top)
        self.Text1.place(relx=0.027, rely=0.011, relheight=0.196, relwidth=0.946)

        self.Text2 = tk.Text(self.top)
        self.Text2.place(relx=0.027, rely=0.261, relheight=0.734, relwidth=0.946)
        self.Text2.tag_configure("red", foreground="red") 
        
        if thread != "error":
            self.Text2.insert(tk.END, "Программа работает корректно, введите запрос выше\n")
        else:
            self.Text2.insert(tk.END, "Включите прокси/впн с доступом к чатгпт\n", "red")
        
        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.027, rely=0.21, height=40, width=350)
        self.Button1.configure(command = lambda: (self.Text1.delete("1.0", tk.END)))
        self.Button1.configure(takefocus=0)
        self.Button1.configure(text='''Сбросить''')

        def auxiliary_function():
            self.Text2.insert(tk.END, "Ваш запрос отправлен, это может занять около 10 секунд\n")
            command_to_server = "MEOW = (0, 0)"
            command_to_server = message_to_chat_gpt(self.Text1.get("1.0", tk.END), thread)
            self.Text2.insert(tk.END, "Запрос к ChatGPT успешно отправлен\n")
            print(command_to_server)
            threading.Thread(target=server, args=(command_to_server,), daemon=True).start()
            self.Text2.insert(tk.END, "Файл сгенерирован!\n")

            
            
        self.Button2 = ttk.Button(self.top)
        self.Button2.place(relx=0.5, rely=0.21, height=40, width=350)
        self.Button2.configure(command = lambda:(auxiliary_function()))
        self.Button2.configure(takefocus=0)
        self.Button2.configure(text='''Отправить''')


def start_up():
    Win_support.main()

if __name__ == '__main__':
    Win_support.main()




