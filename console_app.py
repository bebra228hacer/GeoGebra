import chatgpt
import json
import pyserver
import webbrowser
from flask import render_template
import datetime
with open("config.json") as cfile:
    config_file = json.load(cfile)
url = "http://127.0.0.1:5000" 


def server(initial_command = r"MEOW = (0,0)"):
    now = datetime.datetime.now()
    app = pyserver.create_app(f"saved_file/GeoGebra_file_{now.strftime("%Y%m%d_%H%M%S")}.ggb")
    @app.route('/')
    def index(initial_command = initial_command):    
        return render_template('main.html', initial_command=initial_command) 
    app.run(debug=False, use_reloader=False, port=5000)

def main_input():
    print("Введите из чего требуется создать чертеж:")
    input_text = str(input())

    try:
        input_text = input_text.encode('utf-8').decode('utf-8')  
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования: {e}")
        return
        
    thread = chatgpt.user_get_thread()
    to_graph_gen = chatgpt.chat_gpt_req(thread, text = input_text, assist_id=config_file["MATH_ASSIST"])
    print(to_graph_gen)
    text_to_gen = chatgpt.chat_gpt_req(thread, text = "Используй твой прошлый ответ в этом треде, сверься с моим прошлым запросом и исполни промпт. Учитывай что инструкция может быть неверна, ты не можешь выполнять команды которые не указаны", assist_id=config_file["GRAPH2D_ASSIST"]).replace("\\n", "\n")
    print("\n", text_to_gen)
    lines = text_to_gen.splitlines()  
    formatted_string = r"\n".join(lines)
    webbrowser.open(url)
    server(formatted_string)
    print("Чертеж сгенерирован")

if __name__ == '__main__':        
    main_input()