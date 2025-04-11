import chatgpt
import json
import pyserver
import webbrowser
from flask import render_template
import os
with open("config.json") as cfile:
    config_file = json.load(cfile)
url = "http://127.0.0.1:5000" 


def server(initial_command = r"MEOW = (0,0)"):
    app = pyserver.create_app("meow.ggb")
    @app.route('/')
    def index(initial_command = initial_command):    
        return render_template('test.html', initial_command=initial_command) 
    app.run(debug=True, port=5000, use_reloader=False) 

def main_input():
    print("Введите из чего требуется создать чертеж:")
    input_text = str(input())
    if len(input_text.split()) == 1:
        webbrowser.open(url)
        server(input_text)
        print("Чертеж сгенерирован")
        return
    thread = chatgpt.user_get_thread()
    to_graph_gen = chatgpt.chat_gpt_req(thread, text = input_text, assist_id=config_file["MATH_ASSIST"])
    print(to_graph_gen)
    text_to_gen = chatgpt.chat_gpt_req(thread, text = "Используй твой прошлый ответ в этом треде, сверься с моим прошлым запросом и исполни промпт", assist_id=config_file["GRAPH2D_ASSIST"]).replace("\\n", "\n")
    print("\n", text_to_gen)
    lines = text_to_gen.splitlines()  
    formatted_string = r"\n".join(lines)
    #print(text_to_gen)
    webbrowser.open(url)
    server(formatted_string)
    print("Чертеж сгенерирован")

if __name__ == '__main__':        
    main_input()